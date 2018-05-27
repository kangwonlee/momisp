import os

import nbformat

import recursively_convert_units as rcu


def main():

    help(nbformat)

    # Chapter loop
    for chapter_path, ipynb_filename in rcu.gen_ipynb(get_chapter_par_dir()):
        process_one_ipynb(chapter_path, ipynb_filename)


def process_one_ipynb(chapter_path, ipynb_filename):
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
    main()
