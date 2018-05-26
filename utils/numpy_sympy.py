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
        root = os.pardir
    else:
        root = argv[0]

    # Chapter folder
    for root_dir, _, filename_list in rcu.os_walk_if_not_ignore(root):

        # Notebook file loop
        for ipynb_filename in filter(rcu.is_ipynb, filename_list):

            process_one_ipynb_file(root_dir, ipynb_filename,)


def process_one_ipynb_file(root_dir, ipynb_filename,):
    ipynb_filename_name = os.path.splitext(ipynb_filename)[0]

    py_filename_full_path = os.path.join(root_dir, ipynb_filename_name + '.py')

    if os.path.exists(py_filename_full_path):
        raise IOError('file %s already exists.' % py_filename_full_path)

    # convert a .ipynb file into a .py file
    conversion_cmd = get_conversion_cmd_list(root_dir, ipynb_filename)

    print(conversion_cmd)

    stdout, stderr = run_cmd(conversion_cmd)

    if stdout:
        print('stdout:\n%s' % stdout)
    if stderr:
        print('stderr:\n%s' % stderr)

    # end of conversion

    # using tokenize module to understand converted file
    results_list = []

    try:
        with open(py_filename_full_path, encoding='utf-8') as f:
            for toktype, tok, start, end, line in gen_python_lines(f.readline):
                if 'import' in tok:
                    if ('numpy' in line) or ('sympy' in line):
                        # remove comment
                        if '#' in line:
                            line = line[0:line.find('#')].strip()
                        results_list.append({'toktype':toktype, 'tok':tok, 'start':start, 'end':end, 'line':line})
    except BaseException as e:
        tear_down(py_filename_full_path)
        raise e
    # end obtaining import lines

    # import line loop
    for import_dict in results_list:
        import_as_dict = get_module_and_import_names(import_dict['line'])

        import_dict.update(import_as_dict)
        print(import_dict['line'], import_as_dict)
    # end import line loop

    tear_down(py_filename_full_path)


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
