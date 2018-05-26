import os
import pytest
import sys

sys.path.append(os.path.split(os.path.split(__file__)[0])[0])

import numpy_sympy as ns


def test_get_conversion_cmd_list():
    root_dir = os.getcwd()
    ipynb_filename = 'none.ipynb'

    result = ns.get_conversion_cmd_list(root_dir, ipynb_filename)

    assert isinstance(result, list)
    assert 'jupyter' in result
    assert 'nbconvert' in result
    assert 'python' in result
    assert os.path.join(root_dir, ipynb_filename) in result


def test_process_one_ipynb_file():
    # ../../Ch?? relative to the location of the file instead of the test execution location
    chapter_dir = os.path.abspath(os.path.join(os.path.split(__file__)[0], os.pardir, os.pardir, 'Ch04_SFD.BMD'))
    filename = 'ex04.003.simply.supported_v.w.ipynb'

    # Function under test
    result = ns.process_one_ipynb_file(chapter_dir, filename)

    # TODO : The function under test and this test function are not finished. Verify later.
    assert result is None
