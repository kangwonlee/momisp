import os
import sys

import nbformat

import recursively_convert_units as rcu


def main(argv):

    if 2 <= len(argv):
        replace_this, to_this = argv[0], argv[1]
    else:
        with open('ref_info.txt', 'r') as in_file:
            replace_this = in_file.readline().strip()
            to_this = in_file.readline().strip()

    # Chapter loop + file loop
    for chapter_path, ipynb_filename in rcu.gen_ipynb(get_chapter_par_dir()):
        process_one_ipynb(chapter_path, ipynb_filename, replace_this, to_this)


def process_one_ipynb(chapter_path, ipynb_filename, replace_this, to_this):
    pass


def gen_cells_in_ipynb(ipynb_filename):
    with open(ipynb_filename, 'rb') as nb_file:
        txt = nb_file.read()
    
    nb_node = nbformat.reads(txt.decode(), nbformat.NO_CONVERT)

    for cell in nb_node.cells:
        yield cell


def get_chapter_par_dir():
    """
    Absolute path to the parent directory of chapter folders
    """
    return os.path.abspath(os.path.join(os.path.split(__file__)[0], os.pardir))


if __name__ == '__main__':
    main(sys.argv[1:])
