import os

import nbutils.nb_file_util as fu
import recursively_convert_units as rcu


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

    # Chapter loop
    for root_name, _, filename_list in rcu.os_walk_if_not_ignore(os.pardir):
        # Notebook file loop
        for filename in filter(rcu.is_ipynb, filename_list):
            full_path = os.path.join(root_name, filename)
            fp.process_nb_file(full_path, b_write_file=True)


if __name__ == '__main__':
    main()
