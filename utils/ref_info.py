import os

import nbutils.nb_file_util as fu
from recursively_convert_units import ignore_path_list, is_ignore, is_ipynb


class RefCellCorrector(fu.CellProcessorBase):

    def __init__(self, cell=None):
        super(RefCellCorrector, self).__init__(cell=cell)

    def process_cell(self):
        if not self.is_code():
            print(self)


class ReferenceTypoCorrector(fu.FileProcessor):

    def __init__(self, nb_filename, cell_processor=RefCellCorrector()):
        super(ReferenceTypoCorrector, self).__init__(nb_filename=nb_filename, cell_processor=cell_processor)


def main():
    fp = ReferenceTypoCorrector(None)

    for root_name, dir_list, filename_list in os.walk(os.pardir):
        if not is_ignore(root_name):
            for filename in filename_list:
                if is_ipynb(filename):
                    full_path = os.path.join(root_name, filename)
                    fp.process_nb_file(full_path, b_write_file=True)


if __name__ == '__main__':
    main()
