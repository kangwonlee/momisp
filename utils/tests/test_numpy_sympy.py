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
    assert result is None

# https://docs.pytest.org/en/latest/parametrize.html#parametrize
@pytest.mark.parametrize(
    "chapter_folder, filename, expected",
    [
        ('Ch02_Strain', 'ex02.002.numpy.varying.width.ipynb',                                   {'numpy': True}),
        ('Ch02_Strain', 'ex02.007.numpy.reinforced.concrete.column.ipynb',                      {'numpy': True, 'numpy.linalg': True}),
        ('Ch03_Torsion', 'ex03.001.torsional.displacement.ipynb',                               {'numpy': True, 'numpy.linalg': False, 'sympy': True}),
        ('Ch04_SFD.BMD', 'ch04.004.SFD.BMD.area.ipynb',                                         {'numpy': False, 'numpy.linalg': False, 'sympy': True}),
        ('Ch03_Torsion', 'ex03.000.radian.degree.ipynb',                                        {'numpy': True, 'numpy.linalg': False, 'sympy': False}),
        ('Ch02_Strain', 'ex02.011.eq.thermal.stress.ipynb',                                     {'numpy': False, 'numpy.linalg': False, 'sympy': False}),
        ('Ch05_Stress.in.Beams', 'ex05.002.BendingStress.T.section_simple.overhang_w.p.ipynb',  {'numpy': True, 'numpy.linalg': False, 'numpy.matlib': True, 'sympy': True}),
        ('Ch05_Stress.in.Beams', 'ex05.001.BendingStress.BMD_rect_simple_w.p.ipynb',            {'numpy': True, 'numpy.linalg': False, 'numpy.matlib': True, 'sympy': False}),
        ('Ch05_Stress.in.Beams', 'ex05.004.BendingStress.W200.section_cantilever_m.ipynb',      {'numpy': True, 'numpy.linalg': False, 'sympy': True, 'sympy.plotting': True}),        
        ('Ch05_Stress.in.Beams', 'ex05.007.ShearStress.H.beam.v.ipynb',                         {'numpy': True, 'numpy.linalg': False, 'sympy': True, 'sympy.plotting': False}),
        ('Ch07_Stat.Indet', 'ex07.003.Double.Integral_bracket_fix_simple_v.ipynb',              {'numpy': True, 'numpy.linalg': True, 'sympy': False, 'sympy.plotting': False}),
        ('Ch05_Stress.in.Beams', 'ch05.004.ShearStressBeam.ipynb',                              {'numpy': False, 'numpy.linalg': False, 'sympy': True, 'sympy.plotting': True}),
        ('Ch05_Stress.in.Beams', 'ch05.000.Second.Moment.Of.Inertia.ipynb',                     {'numpy': False, 'numpy.linalg': False, 'sympy': True, 'sympy.plotting': False}),
        ('Ch05_Stress.in.Beams', 'ch05.002.BendingStress.ipynb',                                {'numpy': True, 'numpy.linalg': False, 'sympy': False, 'sympy.plotting': False}),
        ('Ch08_Stress_Due.To_Combined.Loads', 'ch08.009.Strain.Transform.ipynb',                {'numpy': False, 'numpy.linalg': False, 'sympy': False, 'sympy.plotting': False}),
        ('Ch05_Stress.in.Beams', 'ex05.003.BendingStress.rect.two.h_cantilever_v.ipynb',        {'numpy': True, 'numpy.linalg': False, 'numpy.matlib': False, 'sympy': True, 'sympy.plotting': True}),
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
