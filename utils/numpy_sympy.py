import ast
import os
import subprocess
import sys
import tokenize

import nbformat

import recursively_convert_units as rcu
import nbutils.nb_file_util as fu


def main(argv):

    # no argument
    if not argv:
        root = get_chapter_par_dir()
    else:
        root = argv[0]

    cases = {}

    # Chapter folder
    for root_dir, _, filename_list in rcu.os_walk_if_not_ignore(root):

        chapter_folder = os.path.split(root_dir)[-1]

        # Notebook file loop
        for ipynb_filename in filter(rcu.is_ipynb, filename_list):
            # print('processing', chapter_folder, ipynb_filename)

            marker = process_one_ipynb_file(root_dir, ipynb_filename,)
            this_list = cases.get(marker, [])
            this_list.append((chapter_folder, ipynb_filename))
            cases[marker] = this_list


def get_new_filename_with_usage_marker(usage_marker, filename, b_verbose=False):
    """
    ('numpy', 'ch08.005.2D.Stress.Transform.ipynb') -> 'ch08.005.numpy.2D.Stress.Transform.ipynb'
    ('numpy', 'ch08.005.a.2D.Stress.Transform.ipynb') -> 'ch08.005.numpy.2D.Stress.Transform.ipynb'    
    ('numpy', 'ch08.005.2D.numpy.Stress.Transform.ipynb') -> 'ch08.005.2D.numpy.Stress.Transform.ipynb'    
    ('numpy', 'ch08.005.2D.numpyStress.Transform.ipynb') -> 'ch08.005.numpy.2D.numpyStress.Transform.ipynb'    
    """

    split = filename.split('.')

    if (usage_marker not in split) and usage_marker:
        # put usage marker into the filename
        split.insert(2, usage_marker)
        new_filename = '.'.join(split)
    else:
        new_filename = filename

    if b_verbose : print('(%r, %r, %r),' % (usage_marker, filename, new_filename))

    return new_filename


def process_one_ipynb_file(root_dir, ipynb_filename, b_verbose=False):
    used_dict = get_module_usage(root_dir, ipynb_filename,)

    usage_marker = get_usage_marker(used_dict)

    new_filename = get_new_filename_with_usage_marker(usage_marker, ipynb_filename)

    # present result
    if b_verbose:
        old_full_path = os.path.join(root_dir, ipynb_filename)
        new_full_path = os.path.join(root_dir, new_filename)
        if not os.path.exists(old_full_path):
            raise SystemError('unable to find %r' % old_full_path)
        else:
            mv_cmd = ('mv', old_full_path, new_full_path,)
            print(mv_cmd)

    return usage_marker


def get_usage_marker(used_dict):
    """
    {'a':True, 'b':False} -> 'a'
    {'a':True, 'b':True} -> 'a_b'
    """
    modules = []

    # module name loop
    for key in used_dict:
        # skip if not used or degrees module
        if used_dict[key] and 'degrees' != key:
            # representative 'numpy' or 'sympy' only
            if (('.' not in key) or (key.split('.')[0] not in modules)):
                modules.append(key)

    # build marker
    result = '_'.join(modules)
    return result


def get_module_usage(root_dir, ipynb_filename, b_verbose=False):

    ipynb_filename_name = os.path.splitext(ipynb_filename)[0]

    py_filename_full_path = os.path.join(root_dir, ipynb_filename_name + '.py')

    if os.path.exists(py_filename_full_path):
        raise IOError('file %s already exists.' % py_filename_full_path)

    # prepare conversion command
    conversion_cmd = get_conversion_cmd_list(root_dir, ipynb_filename)

    # convert a .ipynb file into a .py file
    _, stderr = run_cmd(conversion_cmd)

    if ('error' in stderr) or ('fatal' in stderr) or ('fail' in stderr) or not (os.path.exists(py_filename_full_path)):
        raise SystemError('ipynb -> py conversion seemingly failed : %s' % stderr)
    # end of conversion

    # using tokenize module to understand converted file
    results_list = []
    # Checklist of import name usage
    used_dict = {}
    # Conversion table from import name to module name
    as_module_dict ={}

    try:
        with open(py_filename_full_path, encoding='utf-8') as f:
            for toktype, tok, start, end, line in gen_python_lines(f.readline):
                # process import
                if 'import' == tok:
                    if ('numpy' in line) or ('sympy' in line):
                        # remove comment
                        if '#' in line:
                            line = line[0:line.find('#')].strip()

                        results_list.append({'toktype':toktype, 'tok':tok, 'start':start, 'end':end, 'line':line})

                        # Get module name and import name
                        import_as_dict = get_module_and_import_names(line)
                        # Add to the lookup table
                        as_module_dict[import_as_dict['as']] = import_as_dict['module']
                        # Initialize (or update) entry in the checklist
                        used_dict[import_as_dict['module']] = used_dict.get(import_as_dict['module'], False)
                # tokens other than import
                else:
                    # if tok is one of import names
                    if ('import' not in line) and tok in as_module_dict:
                        # ignore
                        if '.init_printing' not in line:
                            if b_verbose: print(toktype, tok, start, end, line)
                            used_dict[as_module_dict[tok]] = True

    except BaseException as e:
        tear_down(py_filename_full_path)
        raise e
    # end obtaining import lines

    tear_down(py_filename_full_path)

    if b_verbose: print('as_module_dict :', as_module_dict)
    return used_dict


def get_module_and_import_names(import_line):
    """
    'import something as sth' -> {'module': 'something', 'as': 'sth'}
    """
    line_split = import_line.split()

    import_as_dict = {}
    # import something as sth
    if 'as' in line_split:
        i = line_split.index('as')

        # something
        if 0 < (i - 1):
            import_as_dict['module'] = line_split[i - 1]
        else:
            raise SystemError("The location of 'as' seems not normal in %r" % (import_line))

        # sth
        if len(line_split[i - 1]) > (i + 1):
            import_as_dict['as'] = line_split[i + 1]
        else:
            raise SystemError("The location of 'as' seems not normal in %r" % (import_line))

    # import something
    elif 'import' in line_split:
        i = line_split.index('import')
        if len(line_split[i - 1]) > (1 + i):
            import_as_dict['as'] = import_as_dict['module'] = line_split[i + 1]
    else:
        raise SystemError('Something seems not right in %r' % (import_line))

    return import_as_dict


def gen_python_lines(readline_obj):
    """
    Generator of python lines not comments
    """
    for toktype, tok, start, end, line in tokenize.generate_tokens(readline_obj):
        # skip comment lines
        if (tokenize.COMMENT != toktype):
            yield toktype, tok, start, end, line


def tear_down(py_filename_full_path):
    if os.path.exists(py_filename_full_path):
        os.remove(py_filename_full_path)

    if os.path.exists(py_filename_full_path):
        raise IOError('unable to remove file %s.' % py_filename_full_path)


def run_cmd(conversion_cmd):
    p = subprocess.Popen(conversion_cmd, 
                         stdout=subprocess.PIPE, 
                         stderr=subprocess.PIPE)
    fo, fe = p.stdout, p.stderr

    stdout = fo.read().decode('utf-8')
    stderr = fe.read().decode('utf-8')

    fo.close()
    fe.close()
    return stdout, stderr


def get_conversion_cmd_list(root_dir, ipynb_filename):
    # convert a .ipynb file into a .py file
    conversion_cmd = ['jupyter', 'nbconvert', 
                      '--to', 'python', 
                      '--output-dir='+root_dir,
                      os.path.join(root_dir, ipynb_filename)]

    return conversion_cmd


def get_chapter_par_dir():
    """
    Absolute path to the parent directory of chapter folders
    """
    return os.path.abspath(os.path.join(os.path.split(__file__)[0], os.pardir))


if "__main__" == __name__:
    main(sys.argv[1:])
