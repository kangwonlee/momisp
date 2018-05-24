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
