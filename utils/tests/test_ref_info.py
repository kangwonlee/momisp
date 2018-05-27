import os
import pytest
import sys

import nbformat


sys.path.append(os.path.split(os.path.split(__file__)[0])[0])


import ref_info as ri


def test_gen_cells_in_ipynb():

    ch_par_dir = ri.get_chapter_par_dir()
    ipynb_full_path = os.path.join(ch_par_dir, 'Ch04_SFD.BMD', 'ex04.003.numpy.simply.supported_v.w.ipynb')

    nb = ri.NotebookFile(ipynb_full_path)

    for cell in nb.gen_cells():
        assert isinstance(cell, dict)
        assert 'cell_type' in cell
        if 'code' == cell['cell_type']:
            assert 'execution_count' in cell
            assert 'metadata' in cell
            assert 'outputs' in cell
            assert 'source' in cell
        elif 'markdown' == cell['cell_type']:
            assert 'metadata' in cell
            assert 'source' in cell
        else:
            raise ValueError('Unknown cell type:', cell['cell_type'])
