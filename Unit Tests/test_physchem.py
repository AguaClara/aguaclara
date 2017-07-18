# -*- coding: utf-8 -*-
"""
Created on Fri Jul  7 11:51:51 2017

@author: Sage Weber-Shirk

Last modified: Tue Jul 11 2017
By: Sage Weber-Shirk
"""

import unittest

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
        checks = (((12, 6, 0.2), 12.732395447351628),
                  ((12, 12, 0.9), 1.4147106052612919),
                  ((12, 12, .45), 2.8294212105225838))
        for i in checks:
            with self.subTest(i=i):
                self.assertEqual(pc.re_pipe(*i[0]), i[1])

    


if __name__ == "__main__":
    unittest.main()