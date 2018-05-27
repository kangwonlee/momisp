import os
import sys

import nbformat

import recursively_convert_units as rcu


class NotebookFile(object):
    def __init__(self, ipynb_full_path):
        self.ipynb_full_path = ipynb_full_path
        self.nb_node = nbformat.read(ipynb_full_path, nbformat.NO_CONVERT)

    def gen_cells(self):
        for cell in self.nb_node.cells:
            yield cell

    def write(self, new_file_full_path):
        nbformat.write(self.nb_node, new_file_full_path)
        

def main(argv):

    if 2 <= len(argv):
        replace_this, to_this = argv[0], argv[1]
    # If commandline argument missing
    else:
        if os.path.exists('ref_info.txt'):
            with open('ref_info.txt', 'r') as in_file:
                replace_this = in_file.readline().strip()
                to_this = in_file.readline().strip()
        else:
            with open('ref_info.txt', 'w') as out_file:
                replace_this = 'abc'
                to_this = 'abc'
                out_file.write(replace_this + '\n')
                out_file.write(to_this + '\n')            

    # Chapter loop + file loop
    for chapter_path, ipynb_filename in rcu.gen_ipynb(get_chapter_par_dir()):
        process_one_ipynb(chapter_path, ipynb_filename, replace_this, to_this)


# Please commit as `b_verbose=False, b_arm=False` for safety
def process_one_ipynb(chapter_path, ipynb_filename, replace_this, to_this, b_verbose=False, b_arm=False):
    """
    When ready to use, first set b_verbose to True and evaluate the result even if you are confident
    After a sufficient review, if you still feel confident, if possible commit your files before applying changes
    As you now have a measure to undo the changes, set b_arm to True and run. I hope you best of luck.
    """
    # Full path to the ipynb file to reuse later
    ipynb_full_path = os.path.join(chapter_path, ipynb_filename)

    nb = NotebookFile(ipynb_full_path)

    for cell in nb.gen_cells():
        source = cell.get('source')
        if replace_this in source:
            if b_verbose:
                print(chapter_path, ipynb_filename)
                print('before '.ljust(60, '-'))
                print(cell)
                # Replacing here
                cell['source'] = source.replace(replace_this, to_this)
                print('after '.ljust(60, '-'))
                print(cell)
                print('=' * 80)

    # write
    if b_verbose and b_arm:
        nb.write(ipynb_full_path)


def get_chapter_par_dir():
    """
    Absolute path to the parent directory of chapter folders
    """
    return os.path.abspath(os.path.join(os.path.split(__file__)[0], os.pardir))


if __name__ == '__main__':
    main(sys.argv[1:])
