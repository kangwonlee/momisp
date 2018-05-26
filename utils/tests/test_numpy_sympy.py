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
    chapter_dir = os.path.abspath(os.path.join(ns.get_chapter_par_dir(), 'Ch04_SFD.BMD'))
    filename = 'ex04.003.simply.supported_v.w.ipynb'

    # Function under test
    result = ns.process_one_ipynb_file(chapter_dir, filename)

    # TODO : The function under test and this test function are not finished. Verify later.
    assert 'numpy' == result

# https://docs.pytest.org/en/latest/parametrize.html#parametrize
@pytest.mark.parametrize(
    "chapter_folder, filename, expected",
    [
        ('Ch02_Strain', 'ex02.002.numpy.varying.width.ipynb',                                   {'numpy': True}),
        ('Ch03_Torsion', 'ex03.001.torsional.displacement.ipynb',                               {'numpy': True, 'numpy.linalg': False, 'sympy': True}),
        ('Ch05_Stress.in.Beams', 'ex05.002.BendingStress.T.section_simple.overhang_w.p.ipynb',  {'numpy': True, 'numpy.linalg': False, 'numpy.matlib': True, 'sympy': True}),
    ],
)
def test_get_module_usage(chapter_folder, filename, expected):
    # ../../Ch?? relative to the location of the file instead of the test execution location
    chapter_full_dir = os.path.abspath(os.path.join(ns.get_chapter_par_dir(), chapter_folder))

    # Function under test
    result = ns.get_module_usage(chapter_full_dir, filename)

    assert expected == result


def test_get_module_usage_04_003():
    # ../../Ch?? relative to the location of the file instead of the test execution location
    chapter_full_dir = os.path.abspath(os.path.join(ns.get_chapter_par_dir(), 'Ch04_SFD.BMD'))
    filename = 'ex04.003.simply.supported_v.w.ipynb'
    expected = {'numpy': True, 'numpy.linalg': False, 'sympy': False}

    # Function under test
    result = ns.get_module_usage(chapter_full_dir, filename)

    assert expected == result


def test_get_chapter_par_dir():
    # Function under test
    chapter_par_dir = ns.get_chapter_par_dir()

    # at least some of the     
    assert 4 < len(list(filter(lambda x: x.startswith('Ch'), os.listdir(chapter_par_dir))))


def test_get_module_and_import_names_as():
    expected_dict = {'module': 'something', 'as': 'sth'}

    # Function under test
    result_dict = ns.get_module_and_import_names('import {module} as {as}'.format(**expected_dict))

    assert expected_dict == result_dict


def test_get_module_and_import_names():
    expected_dict = {'module': 'something', 'as': 'something'}

    # Function under test
    result_dict = ns.get_module_and_import_names('import {module}'.format(**expected_dict))

    assert expected_dict == result_dict


# https://docs.pytest.org/en/latest/parametrize.html#parametrize
@pytest.mark.parametrize(
    "usage_dict, expected",
    [
        ({'numpy': True}, 'numpy'),
        ({'numpy': False, 'numpy.linalg': False, 'sympy': True}, 'sympy'),
    ],
)
def test_get_usage_marker(usage_dict, expected):
    result = ns.get_usage_marker(usage_dict)

    assert expected == result
