import nbutils.symbol_converter as sc
import os

ignore_path_list = {'__pycache__', '.ipynb_checkpoints', '.git', '.cache', '.idea', 
                    'nbutils', 'tests'}


def is_ignore(path):
    result = False
    path_split_set = set(os.path.split(path))
    for ignore in ignore_path_list:
        if ignore in path_split_set:
            result= True
            break

    return result


def os_walk_if_not_ignore(root):
    """
    Run an os.walk() loop and yield if not is_ignore()

    root : a path string to a folder
    """
    for root_name, dir_list, filename_list in os.walk(root):
        if not is_ignore(root_name):
            yield root_name, dir_list, filename_list


def is_ipynb(path):
    return '.ipynb' == os.path.splitext(path)[-1]


def main():

    # file processor
    fp = sc.IpynbUnitConverter(None)

    # Chapter loop
    for root_name, _, filename_list in os_walk_if_not_ignore(os.pardir):
        # ipynb file loop
        for filename in filename_list:
            if is_ipynb(filename):
                full_path = os.path.join(root_name, filename)
                fp.process_nb_file(full_path, b_write_file=True)


if __name__ == '__main__':
    main()
