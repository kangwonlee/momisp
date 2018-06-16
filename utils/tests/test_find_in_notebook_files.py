import os
import pytest
import sys

import nbformat


sys.path.append(os.path.split(os.path.split(__file__)[0])[0])


import find_in_notebook_files as ri


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


def test_find_or_replace_notebook_file_regex():
    ch_par_dir = ri.get_chapter_par_dir()
    ipynb_full_path = os.path.join(ch_par_dir, 'Ch04_SFD.BMD', 'ex04.003.numpy.simply.supported_v.w.ipynb')
    
    assert os.path.exists(ipynb_full_path)

    # Class object under test
    nb = ri.FindOrReplaceNotebookFileRegex(ipynb_full_path, r'^####\s+B-C\s+구간$', '#### B-C 구간<br>B-C span', b_replace=True, b_verbose=True, b_arm=False)

    sample_dict = {'cell_type': 'markdown', 'metadata': {}, 'source': '#### B-C 구간'}
    expected_dict = {'cell_type': 'markdown', 'metadata': {}, 'source': '#### B-C 구간<br>B-C span'}

    # Method under test 01
    assert nb.found(sample_dict)

    # Method under test 02
    nb.find_or_replace_in_one_cell(sample_dict)

    assert expected_dict == sample_dict
