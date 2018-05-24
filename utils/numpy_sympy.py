import ast
import os
import subprocess
import sys

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

            ipynb_filename_name = os.path.splitext(ipynb_filename)[0]

            py_filename_full_path = os.path.join(root_dir, ipynb_filename_name + '.py')

            if os.path.exists(py_filename_full_path):
                raise IOError('file %s already exists.' % py_filename_full_path)

            # convert a .ipynb file into a .py file
            conversion_cmd = get_conversion_cmd_list(root_dir, ipynb_filename)

            print(conversion_cmd)


def get_conversion_cmd_list(root_dir, ipynb_filename):
    # convert a .ipynb file into a .py file
    conversion_cmd = ['jupyter', 'nbconvert', 
                      '--to', 'python', 
                      '--output-dir='+root_dir,
                      os.path.join(root_dir, ipynb_filename)]

    return conversion_cmd


if "__main__" == __name__:
    main(sys.argv[1:])
