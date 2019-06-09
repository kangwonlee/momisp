import os
import pytest
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

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
    filename = 'ex04.003.numpy.simply.supported_v.w.ipynb'

    # Function under test
    result = ns.process_one_ipynb_file(chapter_dir, filename)

    # TODO : The function under test and this test function are not finished. Verify later.
    assert 'numpy' == result

# https://docs.pytest.org/en/latest/parametrize.html#parametrize
@pytest.mark.parametrize(
    "chapter_folder, filename, expected",
    [
        ('Ch02_Strain', 'ex02.002.numpy.varying.width.ipynb',                                   {'numpy': True}),
        ('Ch03_Torsion', 'ex03.001.numpy_sympy.torsional.displacement.ipynb',                               {'numpy': True, 'numpy.linalg': False, 'sympy': True}),
        ('Ch05_Stress.in.Beams', 'ex05.002.numpy_sympy.BendingStress.T.section_simple.overhang_w.p.ipynb',  {'numpy': True, 'numpy.linalg': False, 'numpy.matlib': True, 'sympy': True}),
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
    filename = 'ex04.003.numpy.simply.supported_v.w.ipynb'
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


# https://docs.pytest.org/en/latest/parametrize.html#parametrize
@pytest.mark.parametrize(
    "usage_marker, ipynb_filename, expected",
    [
        ('numpy', 'ex02.002.numpy.varying.width.ipynb', 'ex02.002.numpy.varying.width.ipynb'),
        ('numpy', 'ex02.007.numpy.reinforced.concrete.column.ipynb', 'ex02.007.numpy.reinforced.concrete.column.ipynb'),
        ('numpy', 'ex03.000.radian.degree.ipynb', 'ex03.000.numpy.radian.degree.ipynb'),
        ('numpy', 'ex04.001.simply.supported_v_numerical.arrows.ipynb', 'ex04.001.numpy.simply.supported_v_numerical.arrows.ipynb'),
        ('numpy', 'ex04.002.simply.supported_m.only.ipynb', 'ex04.002.numpy.simply.supported_m.only.ipynb'),
        ('numpy', 'ex04.003.numpy.simply.supported_v.w.ipynb', 'ex04.003.numpy.simply.supported_v.w.ipynb'),
        ('numpy', 'ex04.005.area_simple_v.m.ipynb', 'ex04.005.numpy.area_simple_v.m.ipynb'),
        ('numpy', 'ex04.006.area_simple_v.w.ipynb', 'ex04.006.numpy.area_simple_v.w.ipynb'),
        ('numpy', 'ch05.002.BendingStress.ipynb', 'ch05.002.numpy.BendingStress.ipynb'),
        ('numpy', 'ex05.001.BendingStress.BMD_rect_simple_w.p.ipynb', 'ex05.001.numpy.BendingStress.BMD_rect_simple_w.p.ipynb'),
        ('numpy', 'ex05.010.Bending.Shear.Stress_box.section_overhang_v.ipynb', 'ex05.010.numpy.Bending.Shear.Stress_box.section_overhang_v.ipynb'),
        ('numpy', 'ch06.004.moment_area.ipynb', 'ch06.004.numpy.moment_area.ipynb'),
        ('numpy', 'ex06.002.Direct.Integration_simple_w.ipynb', 'ex06.002.numpy.Direct.Integration_simple_w.ipynb'),
        ('numpy', 'ex06.005.bracket_EI_simple_v.ipynb', 'ex06.005.numpy.bracket_EI_simple_v.ipynb'),
        ('numpy', 'ex07.003.Double.Integral_bracket_fix_simple_v.ipynb', 'ex07.003.numpy.Double.Integral_bracket_fix_simple_v.ipynb'),
        ('numpy', 'ch08.006.Mohrs.Circle.ipynb', 'ch08.006.numpy.Mohrs.Circle.ipynb'),
        ('numpy', 'ch12.004.Theories.of.Failure_b.Ductile.Material.ipynb', 'ch12.004.numpy.Theories.of.Failure_b.Ductile.Material.ipynb'),
        ('', 'ex02.011.eq.thermal.stress.ipynb', 'ex02.011.eq.thermal.stress.ipynb'),
        ('', 'ch03.003.thin.wall.tube.ipynb', 'ch03.003.thin.wall.tube.ipynb'),
        ('', 'ch08.009.Strain.Transform.ipynb', 'ch08.009.Strain.Transform.ipynb'),
        ('numpy_sympy', 'ex03.001.torsional.displacement.ipynb', 'ex03.001.numpy_sympy.torsional.displacement.ipynb'),
        ('numpy_sympy', 'ex03.002.statically.indeterminate.ipynb', 'ex03.002.numpy_sympy.statically.indeterminate.ipynb'),
        ('numpy_sympy', 'ex03.007.thin.wall.tube.ipynb', 'ex03.007.numpy_sympy.thin.wall.tube.ipynb'),
        ('numpy_sympy', 'ex05.002.BendingStress.T.section_simple.overhang_w.p.ipynb', 'ex05.002.numpy_sympy.BendingStress.T.section_simple.overhang_w.p.ipynb'),
        ('numpy_sympy', 'ex05.003.BendingStress.rect.two.h_cantilever_v.ipynb', 'ex05.003.numpy_sympy.BendingStress.rect.two.h_cantilever_v.ipynb'),
        ('numpy_sympy', 'ex05.004.BendingStress.W200.section_cantilever_m.ipynb', 'ex05.004.numpy_sympy.BendingStress.W200.section_cantilever_m.ipynb'),
        ('numpy_sympy', 'ex05.006.ShearStress.rect.section_simple_w.ipynb', 'ex05.006.numpy_sympy.ShearStress.rect.section_simple_w.ipynb'),
        ('numpy_sympy', 'ex05.007.ShearStress.H.beam.v.ipynb', 'ex05.007.numpy_sympy.ShearStress.H.beam.v.ipynb'),
        ('numpy_sympy', 'pr05.062.ShearStress.H.beam.ipynb', 'pr05.062.numpy_sympy.ShearStress.H.beam.ipynb'),
        ('numpy_sympy', 'ex07.004.Double.Integral_bracket_fix_fix_w.ipynb', 'ex07.004.numpy_sympy.Double.Integral_bracket_fix_fix_w.ipynb'),
        ('numpy_sympy', 'ch08.005.2D.Stress.Transform.ipynb', 'ch08.005.numpy_sympy.2D.Stress.Transform.ipynb'),
        ('numpy_sympy', 'ex08.002.Offset_Tension.ipynb', 'ex08.002.numpy_sympy.Offset_Tension.ipynb'),
        ('numpy_sympy', 'ex08.007.Mohr.Circle.ipynb', 'ex08.007.numpy_sympy.Mohr.Circle.ipynb'),
        ('numpy_sympy', 'ch10.002.Euler.Equation_for_a.Column.ipynb', 'ch10.002.numpy_sympy.Euler.Equation_for_a.Column.ipynb'),
        ('sympy', 'ex03.006.thin.wall.tube.ipynb', 'ex03.006.sympy.thin.wall.tube.ipynb'),
        ('sympy', 'ch04.004.SFD.BMD.area.ipynb', 'ch04.004.sympy.SFD.BMD.area.ipynb'),
        ('sympy', 'ch05.000.Second.Moment.Of.Inertia.ipynb', 'ch05.000.sympy.Second.Moment.Of.Inertia.ipynb'),
        ('sympy', 'ch05.004.ShearStressBeam.ipynb', 'ch05.004.sympy.ShearStressBeam.ipynb'),
        ('sympy', 'ex05.005.BendingStress.lightest.section_W_simple_v.ipynb', 'ex05.005.sympy.BendingStress.lightest.section_W_simple_v.ipynb'),
        ('sympy', 'ex05.009.Bending.Shear.Stress_max.length_rect_simple_w.ipynb', 'ex05.009.sympy.Bending.Shear.Stress_max.length_rect_simple_w.ipynb'),
        ('sympy', 'ex05.011.Shear.Bearing.Stress_girder.section_fastener.ipynb', 'ex05.011.sympy.Shear.Bearing.Stress_girder.section_fastener.ipynb'),
        ('sympy', 'ch06.000.Dirac.delta_Step.ipynb', 'ch06.000.sympy.Dirac.delta_Step.ipynb'),
        ('sympy', 'ex06.001.W200_cantilever_w.ipynb', 'ex06.001.sympy.W200_cantilever_w.ipynb'),
        ('sympy', 'ex06.008.moment_area.cantilever.w.P.ipynb', 'ex06.008.sympy.moment_area.cantilever.w.P.ipynb'),
        ('sympy', 'ex06.011.Method.of.Superposition_simple_p.ipynb', 'ex06.011.sympy.Method.of.Superposition_simple_p.ipynb'),
        ('sympy', 'ex07.001.Double.Integral_fix_simple_w.ipynb', 'ex07.001.sympy.Double.Integral_fix_simple_w.ipynb'),
        ('sympy', 'ex07.003.Superposition_bracket_fix_simple_v.ipynb', 'ex07.003.sympy.Superposition_bracket_fix_simple_v.ipynb'),
        ('sympy', 'ex07.005.Moment.Area_fix_simple_w.ipynb', 'ex07.005.sympy.Moment.Area_fix_simple_w.ipynb'),
        ('sympy', 'ex07.008.Superposition_fix_simple_w.ipynb', 'ex07.008.sympy.Superposition_fix_simple_w.ipynb'),
        ('sympy', 'ch08.010.Strain.Rosette.ipynb', 'ch08.010.sympy.Strain.Rosette.ipynb'),
        ('sympy', 'ex08.001.Pressure_vessle.ipynb', 'ex08.001.sympy.Pressure_vessle.ipynb'),
        ('sympy', 'ex08.004.Stress_Transform.ipynb', 'ex08.004.sympy.Stress_Transform.ipynb'),
        ('sympy', 'ex08.008.Abs.Max.Tau_3D.ipynb', 'ex08.008.sympy.Abs.Max.Tau_3D.ipynb'),
        ('sympy', 'ex10.001.Column.W.Section.ipynb', 'ex10.001.sympy.Column.W.Section.ipynb'),    
    ],
)
def test_get_new_filename_with_usage_marker(usage_marker, ipynb_filename, expected):
    result = ns.get_new_filename_with_usage_marker(usage_marker, ipynb_filename)

    assert expected == result
