import nbutils.symbol_converter as sc
import nbutils.nb_file_util as nf
import os


def gen_filename_ipynb(filename_list):
    """
    Generator for ipynb filenames in the filename_list

    filename_list : list of filenames within a folder
    """
    for filename in filename_list:
        if nf.is_ipynb(filename):
            yield filename    


def gen_ipynb(root):
    """
    Generate ipynb files within each chapter
    root(==parent folder of chapter folders) -> chapter_path, ipynb_filename
    """
    # Chapter folder
    for chapter_path, _, filename_list in nf.os_walk_if_not_ignore(root):

        # Notebook file loop
        for ipynb_filename in filter(nf.is_ipynb, filename_list):
            yield chapter_path, ipynb_filename


def main():

    # file processor
    fp = sc.IpynbUnitConverter(None)

    # Chapter loop
    for root_name, _, filename_list in nf.os_walk_if_not_ignore(os.pardir):
        # ipynb file loop
        for ipynb_filename in filter(nf.is_ipynb, filename_list):
            full_path = os.path.join(root_name, ipynb_filename)
            fp.process_nb_file(full_path, b_write_file=True)


if __name__ == '__main__':
    main()
