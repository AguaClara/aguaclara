# -*- coding: utf-8 -*-
"""
Created on Fri Jul  7 11:51:51 2017

@author: Sage Weber-Shirk

Last modified: Wed Aug 2 2017
By: Sage Weber-Shirk
"""

#Note: All answer values in this file should be checked against MathCad
#before this file is released to the Master branch!

import unittest
import numpy as np

import sys, os
myGitHubdir = os.path.expanduser('~\\Documents\\GitHub')
if myGitHubdir not in sys.path:
    sys.path.append(myGitHubdir)

from AguaClara_design.units import unit_registry as u
from AguaClara_design import physchem as pc

class GeometryTest(unittest.TestCase):
    """Test the circular area and diameter functions."""
    def test_area_circle_true(self):
        """area_circle should  should give known result with known input."""
        checks = ((1, 0.7853981633974483), 
                  (495.6, 192908.99423885669))
        for i in checks:
            with self.subTest(i=i):
                self.assertEqual(pc.area_circle(i[0]), i[1])

    def test_area_circle_error(self):
        """area_circle should return errors with inputs <= 0."""
        checks = ((0, ValueError), 
                  (-3, ValueError))
        for i in checks:
            with self.subTest(i=i):
                self.assertRaises(i[1], pc.area_circle, i[0])

    def test_diam_circle_true(self):
        """diam_circle should should give known result with known input."""
        checks = ((1, 1.1283791670955126), 
                  (0.1, 0.3568248232305542), 
                  (347, 21.019374919894773), 
                  (10000 * u.cm**2, 1.1283791670955126))
        for i in checks:
            with self.subTest(i=i):
                self.assertEqual(pc.diam_circle(i[0]).magnitude, i[1])

    def test_diam_circle_error(self):
        """diam_circle should return errors with inputs <= 0."""
        checks = ((0, ValueError), 
                  (-3, ValueError))
        for i in checks:
            with self.subTest(i=i):
                self.assertRaises(i[1], pc.diam_circle, i[0])


class WaterPropertiesTest(unittest.TestCase):
    """Test the density and dynamic/kinematic viscosity functions."""
    def test_water_table(self):
        """The table density_water relies upon shouldn't need to be changed."""
        table = pc.WATER_DENSITY_TABLE
        checks = ((0, 273.15, 999.9),
                  (4, 303.15, 995.7),
                  (11, 373.15, 958.4))
        for i in checks:
            with self.subTest(i=i):
                self.assertEqual(table[0][i[0]], i[1])
                self.assertEqual(table[1][i[0]], i[2])

    def test_water_table_units(self):
        """The water density table should handle units properly."""
        table = pc.WATER_DENSITY_TABLE
        self.assertEqual(table[0][0], (0 * u.degC).to_base_units().magnitude)
        self.assertEqual(table[0][4], (30 * u.degC).to_base_units().magnitude)

    def test_density_water_true(self):
        """density_water should give known result with known input."""
        checks = ((273.15, 999.9),
                  (300, 996.601907542082),
                  (343.15, 977.8))
        for i in checks:
            with self.subTest(i=i):
                self.assertEqual(pc.density_water(i[0]).magnitude, i[1])

    def test_viscosity_dynamic(self):
        """viscosity_dynamic should give known result with known input."""
        checks = ((300, 0.0008540578046518858),
                  (372, 0.00028238440851243975),
                  (274, 0.0017060470223965783))
        for i in checks:
            with self.subTest(i=i):
                self.assertEqual(pc.viscosity_dynamic(i[0]).magnitude, i[1])

    def test_viscosity_dynamic_units(self):
        """viscosity_dynamic should give known result with known input."""
        checks = ((300 * u.degK, 0.0008540578046518858),
                  (26.85 * u.degC, 0.0008540578046518858))
        for i in checks:
            with self.subTest(i=i):
                self.assertEqual(pc.viscosity_dynamic(i[0]).magnitude, i[1])

    def test_viscosity_kinematic(self):
        """viscosity_kinematic should give known results with known input."""
        checks = ((342, 4.1584506710898959e-07),
                  (297, 9.1670473903811879e-07),
                  (273.15, 1.7532330683680798e-06),
                  (373.15, 2.9108883329847625e-07))
        for i in checks:
            with self.subTest(i=i):
                self.assertEqual(pc.viscosity_kinematic(i[0]).magnitude, i[1])

    def test_viscosity_kinematic_units(self):
        """viscosity_kinematic should handle units correctly."""
        checks = ((342, 4.1584506710898959e-07),
                  (297 * u.degK, 9.1670473903811879e-07),
                  (0 * u.degC, 1.7532330683680798e-06),
                  (100 * u.degC, 2.9108883329847625e-07))
        for i in checks:
            with self.subTest(i=i):
                self.assertEqual(pc.viscosity_kinematic(i[0]).magnitude, i[1])
                self.assertEqual(pc.viscosity_kinematic(i[0]),
                                 (pc.viscosity_dynamic(i[0]) / pc.density_water(i[0])))


class ReynoldsNumsTest(unittest.TestCase):
    """Test the various Reynolds Number functions."""
    def test_re_pipe(self):
        """re_pipe should return known results with known input."""
        checks = (((12, 6, 0.01), 254.64790894703253),
                  ((60, 1, 1), 76.39437268410977),
                  ((1, 12, .45), 0.23578510087688198))
        for i in checks:
            with self.subTest(i=i):
                self.assertEqual(pc.re_pipe(*i[0]), i[1])

    def test_re_pipe_range(self):
        """re_pipe should raise errors when inputs are out of bounds."""
        checks = ((0, 4, .5), (1, 0, .4), (1, 1, -0.1), (1, 1, 0))
        for i in checks:
            with self.subTest(i=i):
                self.assertRaises(ValueError, pc.re_pipe, *i)

    def test_re_pipe_units(self):
        """re_pipe should handle units correctly."""
        base = pc.re_pipe(12, 6, 0.01)
        checks = ([12 * u.m**3/u.s, 6 * u.m, 0.01 * u.m**2/u.s],
                  [12000 * u.L/u.s, 600 * u.cm, 0.000001 * u.ha/u.s],
                  [12, 0.006 * u.km, 100 * u.cm**2/u.s])
        for i in checks:
            with self.subTest(i=i):
                self.assertEqual(pc.re_pipe(*i), base)
    
    def test_re_rect(self):
        """re_rect should return known result with known input."""
        self.assertEqual(pc.re_rect(10, 4, 6, 1, True), 2.5)
    
    def test_re_rect_range(self):
        """re_rect should raise errors when inputs are out of bounds."""
        checks = ((0, 1, 1, 1, False), (1, 1, 1, 0, False))
        for i in checks:
            with self.subTest(i=i):
                self.assertRaises(ValueError, pc.re_rect, *i)
    
    def test_re_rect_units(self):
        """re_rect should handle units correctly."""
        base = pc.re_rect(10, 4, 6, 1, True)
        checks = ([10 * u.m**3/u.s, 4 * u.m, 6 * u.m, 1 * u.m**2/u.s, True],
                  [10000 * u.L/u.s, 4, 6, 1, True],
                  [10, 400 * u.cm, 6, 1, True],
                  [10, 4, 0.006 * u.km, 1, True],
                  [10, 4, 6, 0.0001 * u.ha/u.s, True])
        for i in checks:
            with self.subTest(i=i):
                self.assertEqual(pc.re_rect(*i), base)
    
    def test_re_general(self):
        """re_general should return known values with known input."""
        checks = (([1, 2, 3, 0.4], 6.666666666666666),
                  ([17, 6, 42, 1], 9.714285714285714),
                  ([0, 1, 2, 0.3], 0))
        for i in checks:
            with self.subTest(i=i):
                self.assertEqual(pc.re_general(*i[0]), i[1])
    
    def test_re_general_range(self):
        """re_general should raise errors with invalid inputs."""
        checks = ((-1, 2, 3, 0.4), (1, 2, 3, 0))
        for i in checks:
            with self.subTest(i=i):
                self.assertRaises(ValueError, pc.re_general, *i)
    
    def test_re_general_units(self):
        """re_general should handle units correctly."""
        base = pc.re_general(1, 2, 3, 0.4)
        checks = ([1 * u.m/u.s, 2 * u.m**2, 3 * u.m, 0.4 * u.m**2/u.s],
                  [100 * u.cm/u.s, 2, 3, 0.4],
                  [1, 20000 * u.cm**2, 3, 0.4],
                  [1, 2, 0.003 * u.km, 0.4],
                  [1, 2, 3, 4000 * u.cm**2/u.s])
        for i in checks:
            with self.subTest(i=i):
                self.assertEqual(pc.re_general(*i), base)


class RadiusFuncsTest(unittest.TestCase):
    """Test the various radius-acquisition functions."""
    def test_radius_hydraulic(self):
        """radius_hydraulic should return known results with known input."""
        checks = (([10, 4, False], 1.4285714285714286),
                  ([10, 4, True], 2.2222222222222223))
        for i in checks:
            with self.subTest(i=i):
                self.assertEqual(pc.radius_hydraulic(*i[0]).magnitude, i[1])

    def test_radius_hydraulic_range(self):
        """radius_hydraulic should return errors with invalid inputs."""
        checks = (([0, 4, True], ValueError), ([-1, 4, True], ValueError),
                  ([1, 0, True], ValueError), ([10, -1, True], ValueError),
                  ([10, 4, 0], TypeError), ([10, 4, 6], TypeError))
        for i in checks:
            with self.subTest(i=i):
                self.assertRaises(i[1], pc.radius_hydraulic, *i[0])

    def test_radius_hydraulic_units(self):
        """radius_hydraulic should handle units correctly."""
        base = pc.radius_hydraulic(10, 4, False)
        checks = ([1000 * u.cm, 4, False], 
                  [0.01 * u.km, 40 * u.dm, False])
        for i in checks:
            with self.subTest(i=i):
                self.assertEqual(pc.radius_hydraulic(*i), base)
    
    def test_radius_hydraulic_lists(self):
        """radius_hydraulic should handle list inputs."""
        checks = ([(10, 4, [False, True]), [1.4285714285714286, 2.2222222222222223]])
        self.assertTrue(np.array_equal(pc.radius_hydraulic(*checks[0]).magnitude, checks[1]))

    def test_radius_hydraulic_general(self):
        """radius_hydraulic_general should return known results with known input."""
        checks = (([6, 12], 0.5), ([70, 0.4], 175))
        for i in checks:
            with self.subTest(i=i):
                self.assertEqual(pc.radius_hydraulic_general(*i[0]).magnitude, i[1])
    
    def test_radius_hydraulic_general_range(self):
        """radius_hydraulic_general should not accept inputs of 0 or less."""
        checks = ([0, 6], [6, 0])
        for i in checks:
            with self.subTest(i=i):
                self.assertRaises(ValueError, pc.radius_hydraulic_general, *i)
    
    def test_radius_hydraulic_general_units(self):
        """radius_hydraulic_general should handle units correctly."""
        base = pc.radius_hydraulic_general(4, 7)
        checks = ([4 * u.m**2, 7 * u.m], [40000 * u.cm**2, 7],
                  [4, 0.007 * u.km])
        for i in checks:
            with self.subTest(i=i):
                self.assertEqual(pc.radius_hydraulic_general(*i), base)


class FrictionFuncsTest(unittest.TestCase):
    """Test the friction functions."""
    def test_fric(self):
        """fric should return known results with known input."""
        checks = (([100, 2, 0.001, 1], 0.33154589118654193),
                  ([100, 2, 0.1, 1], 0.10053096491487337),
                  ([100, 2, 0.001, 0], 0.019675384283293733),
                  ([46, 9, 0.001, 0.03], 0.039382681891291252),
                  ([55, 0.4, 0.5, 0.0001], 0.18278357257249706))
        for i in checks:
            with self.subTest(i=i):
                self.assertEqual(pc.fric(*i[0]), i[1])
    
    def test_fric_range(self):
        """fric should raise an error if 0 <= PipeRough <= 1 is not true."""
        checks = ([1, 2, 0.1, -0.1],
                  [1, 2, 0.1, 1.1])
        for i in checks:
            with self.subTest(i=i):
                self.assertRaises(ValueError, pc.fric, *i)
    
    def test_fric_units(self):
        """fric should handle units correctly."""
        base = pc.fric(100, 2, 0.001, 1)
        checks = ([100 * u.m**3/u.s, 2 * u.m, 0.001 * u.m**2/u.s, 1 * u.m],
                  [100000 * u.L/u.s, 2, 0.001, 1],
                  [100, 20 * u.dm, 0.001, 1],
                  [100, 2, 10 * u.cm**2/u.s, 1],
                  [100, 2, 0.001, 1000 * u.mm])
        for i in checks:
            with self.subTest(i=i):
                self.assertEqual(pc.fric(*i), base)
    
    def test_fric_rect(self):
        """fric_rect should return known results with known inputs."""
        checks = (([60, 0.7, 1, 0.6, 0.001, True], 0.432),
                  ([60, 0.7, 1, 0.6, 0.001, False], 0.544),
                  ([120, 1, 0.04, 0.125, 0.6, True], 150.90859874356411),
                  ([120, 1, 0.04, 0.125, 0.6, False], 0.034666666666666665),
                  ([120, 1, 0.04, 0.125, 0, False], 0.034666666666666665),
                  ([120, 1, 0.04, 0.125, 0, True], 0.042098136441473824))
        for i in checks:
            with self.subTest(i=i):
                self.assertEqual(pc.fric_rect(*i[0]), i[1])
    
    def test_fric_rect_range(self):
        """fric_rect should raise an error if 0 <= PipeRough <= 1 is not true."""
        checks = ([1, 1, 1, 1, 1.1, True],)
        for i in checks:
            with self.subTest(i=i):
                self.assertRaises(ValueError, pc.fric_rect, *i)
        
    def test_fric_rect_units(self):
        """fric_rect should handle units correctly."""
        base = pc.fric_rect(0.06, 0.1, 0.0625, 0.347, 0.06, True)
        checks = ([0.06 * u.m**3/u.s, 0.1 * u.m, 0.0625 * u.m, 
                   0.347 * u.m**2/u.s, 0.06 * u.m, True],
                  [60 * u.L/u.s, 0.1, 0.0625, 0.347, 0.06, True],
                  [0.06, 10 * u.cm, 0.0625, 0.347, 0.06, True],
                  [0.06, 0.1, 6.25 * u.cm, 0.347, 0.06, True],
                  [0.06, 0.1, 0.0625, 3470 * u.cm**2/u.s, 0.06, True],
                  [0.06, 0.1, 0.0625, 0.347, 6 * u.cm, True])
        for i in checks:
            with self.subTest(i=i):
                self.assertEqual(pc.fric_rect(*i), base)
    
    def test_fric_general(self):
        """fric_general should return known results with known inputs."""
        checks = (([9, 0.67, 3, 0.987, 0.86], 0.3918755555555556),
                  ([1, 1, 1, 1, 1], 16),
                  ([120, 0.6, 12, 0.3, 0.002], 0.023024557179148988))
        for i in checks:
            with self.subTest(i=i):
                self.assertEqual(pc.fric_general(*i[0]), i[1])
    
    def test_fric_general_range(self):
        """fric_general should raise an error if 0 <= PipeRough <= 1 is not true."""
        checks = ((1, 1, 1, 1, -0.0001), (1, 1, 1, 1, 1.1))
        for i in checks:
            with self.subTest(i=i):
                self.assertRaises(ValueError, pc.fric_general, *i)
    
    def test_fric_general_units(self):
        """fric_general should handle units correctly."""
        base = pc.fric_general(46.2, 0.75, 1.23, 0.46, 0.002)
        checks = ([46.2 * u.m**2, 0.75 * u.m, 1.23 * u.m/u.s, 
                   0.46 * u.m**2/u.s, 0.002 * u.m],
                  [462000 * u.cm**2, 0.75, 1.23, 0.46, 0.002],
                  [46.2, 750 * u.mm, 1.23, 0.46, 0.002],
                  [46.2, 0.75, 0.00123 * u.km/u.s, 0.46, 0.002],
                  [46.2, 0.75, 1.23, 4600 * u.cm**2/u.s, 0.002],
                  [46.2, 0.75, 1.23, 0.46, 2 * u.mm])
        for i in checks:
            with self.subTest(i=i):
                self.assertEqual(pc.fric_general(*i), base)


class HeadlossFuncsTest(unittest.TestCase):
    """Test the headloss functions."""
    def test_headloss_fric(self):
        """headloss_fric should return known results with known inputs."""
        checks = (([100, 2, 4, 0.001, 1], 34.2549414191127),
                  ([100, 2, 4, 0.1, 1], 10.386744054168654),
                  ([100, 2, 4, 0.001, 0], 2.032838149828097),
                  ([46, 9, 12, 0.001, 0.03], 0.001399778168304583),
                  ([55, 0.4, 2, 0.5, 0.0001], 8926.108171551185))
        for i in checks:
            with self.subTest(i=i):
                self.assertEqual(pc.headloss_fric(*i[0]).magnitude, i[1])
    
    def test_headloss_fric_range(self):
        """headloss_fric should raise an error if Length <= 0."""
        checks = ([1, 1, 0, 1, 1], [1, 1, -1, 1, 1])
        for i in checks:
            with self.subTest(i=i):
                self.assertRaises(ValueError, pc.headloss_fric, *i)
    
    def test_headloss_fric_units(self):
        """headloss_fric should handle units correctly."""
        base = pc.headloss_fric(100, 2, 4, 0.001, 0.03)
        checks = ([100 * u.m**3/u.s, 2 * u.m, 4 * u.m, 
                   0.001 * u.m**2/u.s, 0.03 * u.m], 
                  [10**5 * u.L/u.s, 2, 4, 0.001, 0.03],
                  [100, 200 * u.cm, 4, 0.001, 0.03],
                  [100, 2, 4000 * u.mm, 0.001, 0.03],
                  [100, 2, 4, 10 * u.cm**2/u.s, 0.03],
                  [100, 2, 4, 0.001, 3 * u.cm])
        for i in checks:
            with self.subTest(i=i):
                self.assertEqual(pc.headloss_fric(*i), base)
    
    def test_headloss_exp(self):
        """headloss_exp should return known results with known input."""
        self.assertEqual(pc.headloss_exp(60, 0.9, 0.067).magnitude, 
                         30.386230766265214)
    
    def test_headloss_exp_range(self):
        """headloss_exp should raise errors when inputs are out of bounds."""
        checks = ([0, 1, 1], [1, 0, 1], [1, 1, -1])
        for i in checks:
            with self.subTest(i=i):
                self.assertRaises(ValueError, pc.headloss_exp, *i)
        self.assertRaises(AssertionError, self.assertRaises, 
                          *(ValueError, pc.headloss_exp, *[1, 1, 0]))
    
    def test_headloss_exp_units(self):
        """headloss_exp should handle units correctly."""
        base = pc.headloss_exp(60, 0.9, 0.067)
        checks = ([60 * u.m**3/u.s, 0.9 * u.m, 0.067],
                  [60000 * u.L/u.s, 0.9, 0.067],
                  [60, 900 * u.mm, 0.067])
        for i in checks:
            with self.subTest(i=i):
                self.assertEqual(pc.headloss_exp(*i), base)
        self.assertRaises(ValueError, pc.headloss_exp, *[60, 0.9, 0.067 * u.m])
    
    def test_headloss(self):
        """headloss should return known results with known inputs."""
        checks = (([100, 2, 4, 0.001, 1, 2], 137.57379509731857),
                  ([100, 2, 4, 0.1, 1, 0.4], 31.05051478980984),
                  ([100, 2, 4, 0.001, 0, 1.2], 64.024150356751633),
                  ([46, 9, 12, 0.001, 0.03, 4], 0.10802874052554703),
                  ([55, 0.4, 2, 0.5, 0.0001, 0.12], 10098.131417963332))
        for i in checks:
            with self.subTest(i=i):
                self.assertEqual(pc.headloss(*i[0]).magnitude, i[1])
    
    def test_headloss_units(self):
        """headloss should handle units correctly."""
        base = pc.headloss(100, 2, 4, 0.001, 1, 2)
        checks = ([100 * u.m**3/u.s, 2 * u.m, 4 * u.m,
                   0.001 * u.m**2/u.s, 1 * u.m, 2],
                  [10**5 * u.L/u.s, 2, 4, 0.001, 1, 2],
                  [100, 200 * u.cm, 4, 0.001, 1, 2],
                  [100, 2, 4000 * u.mm, 0.001, 1, 2],
                  [100, 2, 4, 10 * u.cm**2/u.s, 1, 2],
                  [100, 2, 4, 0.001, 100 * u.cm, 2])
        for i in checks:
            with self.subTest(i=i):
                self.assertEqual(pc.headloss(*i), base)
    
    def test_headloss_fric_rect(self):
        """headloss_fric_rect should return known result with known inputs."""
        checks = (([0.06, 2, 0.004, 3, 0.89, 0.07, True], 4),
                  ([0.06, 2, 0.004, 3, 0.89, 0.07, False], 5))
        for i in checks:
            with self.subTest(i=i):
                self.assertEqual(pc.headloss_fric_rect(*i[0]).magnitude, i[1])


if __name__ == "__main__":
    unittest.main()
