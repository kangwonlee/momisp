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


class FindOrReplaceNotebookFile(NotebookFile):
    def __init__(self, ipynb_full_path, replace_this, to_this, b_verbose=False, b_replace=False, b_arm=False):
        """
        If not b_verbose : does not present results
        If not b_replace : search only
        If not b_arm : display only
        If b_arm : rewrite the file
        """
        super().__init__(ipynb_full_path)

        # Find or replace        
        self.replace_this = replace_this
        self.to_this = to_this

        # Operation switches
        self.b_verbose = b_verbose
        self.b_replace = b_replace
        self.b_arm = b_arm
        # To indicate search result
        self.count = 0

    def for_all_cells_in_file_find_or_replace(self):
        """
        For all cells in the notebook file, replace_this -> to_this
        """
        # To initialize the counter everytime a search starts
        self.count = 0

        # Cell loop
        for cell in self.gen_cells():
            self.count = self.find_or_replace_in_one_cell(cell)

        return self.count

    def found(self, cell_dict):
        """
        See if this cell is of interest
        cell_dict : one of the dicts in nb_node.cells
        """
        return self.replace_this in cell_dict.get('source')

    def find_or_replace_in_one_cell(self, cell):
        """
        Within one cell of the notebook file, replace_this -> to_this
        If not b_verbose : does not present results
        If not b_replace : search only
        """

        # Found
        if self.found(cell):
            # to indicate search result
            self.count += 1

            if self.b_verbose:
                print(self.ipynb_full_path)

                if self.b_replace:
                    marker = 'before'
                else:
                    marker = 'found'

                # Separate found case
                print(('%s ' % marker).ljust(60, '-'))
                print(cell)
                if self.b_replace:
                    # Replacing here
                    self.update_found_cell_dict(cell)
                    print('after '.ljust(60, '-'))
                    print(cell)

                # Separate file
                print('=' * 80)

        return self.count

    def update_found_cell_dict(self, cell_dict):
        """
        Update the cell of interest
        """
        cell_dict['source'] = cell_dict.get('source').replace(self.replace_this, self.to_this)

    def write(self, ipynb_full_path):
        """
        Write if (b_replace and b_verbose and b_arm)
        If same filename but no replacement count, do not overwrite
        """
        if self.b_replace and self.b_verbose and self.b_arm:
            if (
                (ipynb_full_path != self.ipynb_full_path) 
                or (0 < self.count)
               ):
               # If same filename but no replacement count, do not overwrite
                super().write(ipynb_full_path)


def main(argv):

    replace_this, to_this, b_replace, b_verbose, b_arm = get_param(argv)

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


def get_param(argv, default_filename='finf.cfg'):
    """
    Get parameters from commandline argument or default file
    """

    # If commandline argument
    if 5 <= len(argv):
        replace_this, to_this, b_replace, b_verbose, b_arm = argv[0], argv[1], argv[2], argv[3], argv[4]
    # If commandline argument missing
    else:
        config = configparser.ConfigParser()

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

    return replace_this, to_this, b_replace, b_verbose, b_arm


# Please commit as `b_verbose=False, b_arm=False` for safety
def process_one_ipynb(chapter_path, ipynb_filename, replace_this, to_this, b_replace, b_verbose=False, b_arm=False):
    """
    When ready to use, first set b_verbose to True and evaluate the result even if you are confident
    After a sufficient review, if you still feel confident, if possible commit your files before applying changes
    As you now have a measure to undo the changes, set b_arm to True and run. I hope you best of luck.
    """
    # Full path to the ipynb file to reuse later
    ipynb_full_path = os.path.join(chapter_path, ipynb_filename)

    nb = FindOrReplaceNotebookFile(ipynb_full_path, replace_this, to_this, b_verbose=b_verbose, b_replace=b_replace, b_arm=b_arm)

    # Count number of found items to indicate search result
    count = nb.for_all_cells_in_file_find_or_replace()

    # overwrite
    nb.write(ipynb_full_path)

    return count


def get_chapter_par_dir():
    """
    Absolute path to the parent directory of chapter folders
    """
    return os.path.abspath(os.path.join(os.path.split(__file__)[0], os.pardir))


if __name__ == '__main__':
    main(sys.argv[1:])
