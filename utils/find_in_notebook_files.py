import ast
import configparser as configparser
import os
import sys

import nbformat

import recursively_convert_units as rcu


class NotebookFile(object):
    def __init__(self, ipynb_full_path):
        # constructor
        self.ipynb_full_path = ipynb_full_path
        self.nb_node = nbformat.read(ipynb_full_path, nbformat.NO_CONVERT)

    def __del__(self):
        del self.nb_node

    def gen_cells(self):
        for cell in self.nb_node.cells:
            yield cell

    def write(self, new_file_full_path):
        nbformat.write(self.nb_node, new_file_full_path)
        

def main(argv):

    if 5 <= len(argv):
        replace_this, to_this, b_replace, b_verbose, b_arm = argv[0], argv[1], argv[2], argv[3], argv[4]
    # If commandline argument missing
    else:
        config = configparser.ConfigParser()

        default_filename = 'finf.cfg'

        if not os.path.exists(default_filename):
            raise IOError('Unable to find {filename} from {cwd}'.format(filename=default_filename, cwd=os.getcwd()))

        config.read(default_filename)

        # to enable more precise control, adopts ast.litearl_eval
        try:
            replace_this = ast.literal_eval(config['string']['replace this'])
            to_this = ast.literal_eval(config['string']['to this'])
        except KeyError as e:
            print("%r\nconfig has sections : %r" % ('string', config.sections()))
            print('config = %r' % config)
            raise e

        # control parameters
        b_verbose = ('True' == config['control']['verbose'])
        b_arm = ('True' == config['control']['arm'])
        b_replace = ('True' == config['control']['replace'])

    if b_verbose:
        if b_replace:
            print('Will try to replace %r to %r' % (replace_this, to_this))
        else:
            print('Will try to find %r' % replace_this)

    count_files = 0
    count_found = 0
    # Chapter loop + file loop
    for chapter_path, ipynb_filename in rcu.gen_ipynb(get_chapter_par_dir()):
        count_files += 1
        count_found += process_one_ipynb(chapter_path, ipynb_filename, replace_this, to_this, b_replace, b_verbose=b_verbose, b_arm=b_arm)

    print('Found %d/%d cases' % (count_found, count_files))


# Please commit as `b_verbose=False, b_arm=False` for safety
def process_one_ipynb(chapter_path, ipynb_filename, replace_this, to_this, b_replace, b_verbose=False, b_arm=False):
    """
    When ready to use, first set b_verbose to True and evaluate the result even if you are confident
    After a sufficient review, if you still feel confident, if possible commit your files before applying changes
    As you now have a measure to undo the changes, set b_arm to True and run. I hope you best of luck.
    """
    # Full path to the ipynb file to reuse later
    ipynb_full_path = os.path.join(chapter_path, ipynb_filename)

    nb = NotebookFile(ipynb_full_path)

    # to indicate search result
    count = 0

    for cell in nb.gen_cells():
        source = cell.get('source')
        if replace_this in source:
            # to indicate search result
            count += 1

            if b_verbose:
                print(chapter_path, ipynb_filename)

                if b_replace:
                    marker = 'before'
                else:
                    marker = 'found'

                print(('%s ' % marker).ljust(60, '-'))
                print(cell)
                if b_replace:
                    # Replacing here
                    cell['source'] = source.replace(replace_this, to_this)
                    print('after '.ljust(60, '-'))
                    print(cell)
                print('=' * 80)

    # write
    if b_replace and b_verbose and b_arm:
        nb.write(ipynb_full_path)

    return count


def get_chapter_par_dir():
    """
    Absolute path to the parent directory of chapter folders
    """
    return os.path.abspath(os.path.join(os.path.split(__file__)[0], os.pardir))


if __name__ == '__main__':
    main(sys.argv[1:])
