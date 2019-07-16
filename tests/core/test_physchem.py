# -*- coding: utf-8 -*-
"""
Created on Fri Jul 7 11:51:51 2017

@author: Sage Weber-Shirk

Last modified: Tue Jun 4 2019
By: Hannah Si
"""

#Note: All answer values in this file should be checked against MathCad
#before this file is released to the Master branch!

from aguaclara.core.units import u
import unittest

developing = False
if developing:
    import sys
    sys.path.append("../../aguaclara/core")
    import physchem as pc
else:
    from aguaclara.core import physchem as pc

class AirTest(unittest.TestCase):
    """Test the air density function"""
    def assertAlmostEqualQuantity(self, first, second, places=7):
        self.assertAlmostEqual(first.magnitude, second.magnitude, places)
        self.assertEqual(first.units, second.units, places)

    def test_air_density(self):
        answer = 1.29320776*u.kg/u.m**3
        self.assertAlmostEqualQuantity(pc.density_air(1*u.atm, 28.97*u.g/u.mol, 273*u.K), answer)
        answer = 2.06552493*u.kg/u.m**3
        self.assertAlmostEqualQuantity(pc.density_air(5*u.atm, 10*u.g/u.mol, 295*u.K), answer)
        answer = 1.62487961*u.kg/u.m**3
        self.assertAlmostEqualQuantity(pc.density_air(101325*u.Pa, 40*u.g/u.mol, 300*u.K), answer)
        answer = 0.20786109*u.kg/u.m**3
        self.assertAlmostEqualQuantity(pc.density_air(700*u.mmHg, 5*u.g/u.mol, 270*u.K), answer)
        answer = 0*u.kg/u.m**3
        self.assertAlmostEqualQuantity(pc.density_air(0*u.atm, 28.97*u.g/u.mol, 273*u.K), answer)

class GeometryTest(unittest.TestCase):
    """Test the circular area and diameter functions."""
    def test_area_circle(self):
        """area_circle should  should give known result with known input."""
        checks = ((1, 0.7853981633974483*u.m**2),
                  (495.6, 192908.99423885669*u.m**2))
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqual(pc.area_circle(i[0]), i[1])

    def test_area_circle_units(self):
        """area_circle should  should give known result with known input and correct units"""
        checks = ((1*u.m, 7853.981633974483*u.cm**2),
                  (495.6*u.cm, 19.290899423885669*u.m**2))
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqual(pc.area_circle(i[0]), i[1])

    def test_area_circle_range(self):
        """area_circle should return errors with inputs <= 0."""
        checks = (0, -3)
        for i in checks:
            with self.subTest(i=i):
                self.assertRaises(ValueError, pc.area_circle, i)

    def test_diam_circle(self):
        """diam_circle should should give known result with known input."""
        checks = ((1, 1.1283791670955126),
                  (0.1, 0.3568248232305542),
                  (347, 21.019374919894773),
                  (10000 * u.cm**2, 1.1283791670955126))
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqual(pc.diam_circle(i[0]).magnitude, i[1])

    def test_diam_circle_range(self):
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
                self.assertAlmostEqual(table[0][i[0]], i[1])
                self.assertAlmostEqual(table[1][i[0]], i[2])

    def test_water_table_units(self):
        """The water density table should handle units properly."""
        table = pc.WATER_DENSITY_TABLE
        self.assertAlmostEqual(table[0][0], (0 * u.degC).to_base_units().magnitude)
        self.assertAlmostEqual(table[0][4], (30 * u.degC).to_base_units().magnitude)

    def test_density_water_true(self):
        """density_water should give known result with known input."""
        checks = ((273.15, 999.9),
                  (300, 996.601907542082),
                  (343.15, 977.8))
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqual(pc.density_water(i[0]).magnitude, i[1])

    def test_viscosity_dynamic(self):
        """viscosity_dynamic should give known result with known input."""
        checks = ((300, 0.0008540578046518858),
                  (372, 0.00028238440851243975),
                  (274, 0.0017060470223965783))
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqual(pc.viscosity_dynamic(i[0]).magnitude, i[1])

    def test_viscosity_dynamic_units(self):
        """viscosity_dynamic should give known result with known input."""
        checks = ((300 * u.degK, 0.0008540578046518858),
                  (26.85 * u.degC, 0.0008540578046518858))
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqual(pc.viscosity_dynamic(i[0]).magnitude, i[1])

    def test_viscosity_kinematic(self):
        """nu should give known results with known input."""
        checks = ((342, 4.1584506710898959e-07),
                  (297, 9.1670473903811879e-07),
                  (273.15, 1.7532330683680798e-06),
                  (373.15, 2.9108883329847625e-07))
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqual(pc.viscosity_kinematic(i[0]).magnitude, i[1])

    def test_viscosity_kinematic_units(self):
        """nu should handle units correctly."""
        checks = ((342, 4.1584506710898959e-07),
                  (297 * u.degK, 9.1670473903811879e-07),
                  (0 * u.degC, 1.7532330683680798e-06),
                  (100 * u.degC, 2.9108883329847625e-07))
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqual(pc.viscosity_kinematic(i[0]).magnitude, i[1])
                self.assertAlmostEqual(pc.viscosity_kinematic(i[0]),
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
                self.assertAlmostEqual(pc.re_pipe(*i[0]), i[1])

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
                self.assertAlmostEqual(pc.re_pipe(*i), base)

    def test_re_rect(self):
        """re_rect should return known result with known input."""
        self.assertAlmostEqual(pc.re_rect(10, 4, 6, 1, True), 2.5)

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
                self.assertAlmostEqual(pc.re_rect(*i), base)

    def test_re_general(self):
        """re_general should return known values with known input."""
        checks = (([1, 2, 3, 0.4], 6.666666666666666),
                  ([17, 6, 42, 1], 9.714285714285714),
                  ([0, 1, 2, 0.3], 0))
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqual(pc.re_general(*i[0]), i[1])

    def test_re_general_range(self):
        """re_general should raise errors when inputs are out of bounds."""
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
                self.assertAlmostEqual(pc.re_general(*i), base)


class RadiusFuncsTest(unittest.TestCase):
    """Test the various radius-acquisition functions."""
    def test_radius_hydraulic(self):
        """radius_hydraulic should return known results with known input."""
        checks = (([10, 4, False], 1.4285714285714286),
                  ([10, 4, True], 2.2222222222222223))
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqual(pc.radius_hydraulic(*i[0]).magnitude, i[1])

    def test_radius_hydraulic_range(self):
        """radius_hydraulic should raise errors when inputs are out of bounds."""
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
                self.assertAlmostEqual(pc.radius_hydraulic(*i), base)

    def test_radius_hydraulic_general(self):
        """radius_hydraulic_general should return known results with known input."""
        checks = (([6, 12], 0.5), ([70, 0.4], 175))
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqual(pc.radius_hydraulic_general(*i[0]).magnitude, i[1])

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
                self.assertAlmostEqual(pc.radius_hydraulic_general(*i), base)


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
                self.assertAlmostEqual(pc.fric(*i[0]), i[1])

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
                self.assertAlmostEqual(pc.fric(*i), base)

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
                self.assertAlmostEqual(pc.fric_rect(*i[0]), i[1])

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
                self.assertAlmostEqual(pc.fric_rect(*i), base)

    def test_fric_general(self):
        """fric_general should return known results with known inputs."""
        checks = (([9, 0.67, 3, 0.987, 0.86], 0.3918755555555556),
                  ([1, 1, 1, 1, 1], 16),
                  ([120, 0.6, 12, 0.3, 0.002], 0.023024557179148988))
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqual(pc.fric_general(*i[0]), i[1])

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
                self.assertAlmostEqual(pc.fric_general(*i), base)


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
                self.assertAlmostEqual(pc.headloss_fric(*i[0]).magnitude, i[1])

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
                self.assertAlmostEqual(pc.headloss_fric(*i), base)

    def test_headloss_exp(self):
        """headloss_exp should return known results with known input."""
        self.assertAlmostEqual(pc.headloss_exp(60, 0.9, 0.067).magnitude,
                         30.386230766265214)

    def test_headloss_exp_range(self):
        """headloss_exp should raise errors when inputs are out of bounds."""
        checks = ([0, 1, 1], [1, 0, 1], [1, 1, -1])
        for i in checks:
            with self.subTest(i=i):
                self.assertRaises(ValueError, pc.headloss_exp, *i)
        pc.headloss_exp(1, 1, 0)

    def test_headloss_exp_units(self):
        """headloss_exp should handle units correctly."""
        base = pc.headloss_exp(60, 0.9, 0.067).magnitude
        checks = ([60 * u.m**3/u.s, 0.9 * u.m, 0.067 * u.dimensionless],
                  [60000 * u.L/u.s, 0.9, 0.067],
                  [60, 900 * u.mm, 0.067])
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqual(pc.headloss_exp(*i).magnitude, base)

    def test_headloss(self):
        """headloss should return known results with known inputs."""
        checks = (([100, 2, 4, 0.001, 1, 2], 137.57379509731857),
                  ([100, 2, 4, 0.1, 1, 0.4], 31.05051478980984),
                  ([100, 2, 4, 0.001, 0, 1.2], 64.024150356751633),
                  ([46, 9, 12, 0.001, 0.03, 4], 0.10802874052554703),
                  ([55, 0.4, 2, 0.5, 0.0001, 0.12], 10098.131417963332))
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqual(pc.headloss(*i[0]).magnitude, i[1])

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
                self.assertAlmostEqual(pc.headloss(*i), base)

    def test_headloss_fric_rect(self):
        """headloss_fric_rect should return known result with known inputs."""
        checks = (([0.06, 3, 0.2, 4, 0.5, 0.006, True], 1.3097688246694272),
                  ([0.06, 3, 0.2, 4, 0.5, 0.006, False], 4.640841787063992))
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqual(pc.headloss_fric_rect(*i[0]).magnitude, i[1])

    def test_headloss_fric_rect_range(self):
        """headloss_fric_rect should raise an error when Length <=0."""
        checks = ((1, 1, 1, 0, 1, 1, 1), (1, 1, 1, -1, 1, 1, 1))
        for i in checks:
            with self.subTest(i=i):
                self.assertRaises(ValueError, pc.headloss_fric_rect, *i)

    def test_headloss_fric_rect_units(self):
        """headloss_fric_rect should handle units correctly."""
        base = pc.headloss_fric_rect(0.06, 2, 0.004, 3, 0.89, 0.07, True)
        checks = ([0.06 * u.m**3/u.s, 2 * u.m, 0.004 * u.m, 3 * u.m,
                   0.89 * u.m**2/u.s, 0.07 * u.m, True],
                  [60 * u.L/u.s, 2, 0.004, 3, 0.89, 0.07, True],
                  [0.06, 200 * u.cm, 0.004, 3, 0.89, 0.07, True],
                  [0.06, 2, 4 * u.mm, 3, 0.89, 0.07, True],
                  [0.06, 2, 0.004, 300 * u.cm, 0.89, 0.07, True],
                  [0.06, 2, 0.004, 3, 8900 * u.cm**2/u.s, 0.07, True],
                  [0.06, 2, 0.004, 3, 0.89, 7 * u.cm, True])
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqual(pc.headloss_fric_rect(*i), base)

    def test_headloss_exp_rect(self):
        """headloss_exp_rect should return known result for known input."""
        checks = ([0.06, 2, 0.004, 1], 2.8679518490004234)
        self.assertAlmostEqual(pc.headloss_exp_rect(*checks[0]).magnitude, checks[1])

    def test_headloss_exp_rect_range(self):
        """headloss_exp_rect should raise errors when inputs are out of bounds."""
        checks = ((0, 1, 1, 1), (1, 0, 1, 1), (1, 1, 0, 1), (1, 1, 1, -1))
        for i in checks:
            with self.subTest(i=i):
                self.assertRaises(ValueError, pc.headloss_exp_rect, *i)
        pc.headloss_exp_rect(1, 1, 1, 0)

    def test_headloss_exp_rect_units(self):
        """headloss_exp_rect should handle units correctly."""
        base = pc.headloss_exp_rect(0.06, 2, 0.9, 1)
        checks = ([0.06 * u.m**3/u.s, 2 * u.m, 0.9 * u.m, 1 * u.dimensionless],
                  [60 * u.L/u.s, 2, 0.9, 1],
                  [0.06, 200 * u.cm, 0.9, 1],
                  [0.06, 2, 900 * u.mm, 1])
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqual(pc.headloss_exp_rect(*i), base)

    def test_headloss_rect(self):
        """headloss_rect should return known result for known inputs."""
        checks = (([0.06, 3, 0.2, 4, 1, 0.5, 0.006, True], 1.3102786827759163),
                  ([0.06, 3, 0.2, 4, 1, 0.5, 0.006, False], 4.641351645170481))
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqual(pc.headloss_rect(*i[0]).magnitude, i[1])

    def test_headloss_rect_units(self):
        """headloss_rect should handle units properly."""
        base = pc.headloss_rect(0.06, 3, 0.2, 4, 1, 0.5, 0.006, True)
        checks = ([0.06 * u.m**3/u.s, 3 * u.m, 0.2 * u.m, 4 * u.m,
                   1, 0.5 * u.m**2/u.s, 0.006 * u.m, True],
                  [60 * u.L/u.s, 3, 0.2, 4, 1, 0.5, 0.006, True],
                  [0.06, 300 * u.cm, 0.2, 4, 1, 0.5, 0.006, True],
                  [0.06, 3, 200 * u.mm, 4, 1, 0.5, 0.006, True],
                  [0.06, 3, 0.2, 0.004 * u.km, 1, 0.5, 0.006, True],
                  [0.06, 3, 0.2, 4, 1, 5000 * u.cm**2/u.s, 0.006, True],
                  [0.06, 3, 0.2, 4, 1, 0.5, 6 * u.mm, True])
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqual(pc.headloss_rect(*i), base)
        self.assertRaises(ValueError, pc.headloss_rect,
                          *[1, 1, 1, 1, 1 * u.m, 1, 1, True])

    def test_headloss_fric_general(self):
        """headloss_fric_general should return known result for known inputs."""
        checks = (([1, 1, 1, 1, 1, 1], 0.20394324259558566),
                  ([25, 4, 0.6, 2, 1, 1], 0.006265136412536391))
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqual(pc.headloss_fric_general(*i[0]).magnitude, i[1])

    def test_headloss_fric_general_range(self):
        """headloss_fric_general should raise an error when Length <= 0."""
        checks = ([1, 1, 1, 0, 1, 1], [1, 1, 1, -1, 1, 1])
        for i in checks:
            with self.subTest(i=i):
                self.assertRaises(ValueError, pc.headloss_fric_general, *i)

    def test_headloss_fric_general_units(self):
        """headloss_fric_general should handle units correctly."""
        base = pc.headloss_fric_general(36, 5, 0.2, 6, 0.4, 0.002)
        checks = ([36 * u.m**2, 5 * u.m, 0.2 * u.m/u.s,
                   6 * u.m, 0.4 * u.m**2/u.s, 0.002 * u.m],
                  [0.000036 * u.km**2, 5, 0.2, 6, 0.4, 0.002],
                  [36, 500 * u.cm, 0.2, 6, 0.4, 0.002],
                  [36, 5, 20 * u.cm/u.s, 6, 0.4, 0.002],
                  [36, 5, 0.2, 0.006 * u.km, 0.4, 0.002],
                  [36, 5, 0.2, 6, 4000 * u.cm**2/u.s, 0.002],
                  [36, 5, 0.2, 6, 0.4, 2 * u.mm])
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqual(pc.headloss_fric_general(*i), base)

    def test_headloss_exp_general(self):
        """headloss_exp_general should return known result for known input."""
        self.assertAlmostEqual(pc.headloss_exp_general(0.06, 0.02).magnitude,
                         3.670978366720542e-06)

    def test_headloss_exp_general_range(self):
        """headloss_exp_general should raise errors if inputs are out of bounds."""
        checks = ((0,1), (1, -1))
        for i in checks:
            with self.subTest(i=i):
                self.assertRaises(ValueError, pc.headloss_exp_general, *i)
        pc.headloss_exp_general(1, 0)

    def test_headloss_exp_general_units(self):
        """headloss_exp_general should handle units correctly."""
        base = pc.headloss_exp_general(0.06, 0.02).magnitude
        checks = ([0.06 * u.m/u.s, 0.02 * u.dimensionless],
                  [6 * u.cm/u.s, 0.02])
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqual(pc.headloss_exp_general(*i).magnitude, base)

    def test_headloss_gen(self):
        """headloss_gen should return known value for known inputs."""
        checks = (([36, 0.1, 4, 6, 0.02, 0.86, 0.0045], 0.0013093911519979546),
                  ([49, 2.4, 12, 3, 2, 4, 0.6], 0.9396236839032805))
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqual(pc.headloss_gen(*i[0]).magnitude, i[1])

    def test_headloss_gen_units(self):
        """headloss_gen should handle units correctly."""
        base = pc.headloss_gen(49, 2.4, 12, 3, 2, 4, 0.6).magnitude
        checks = ([49 * u.m**2, 2.4 * u.m/u.s, 12 * u.m, 3 * u.m,
                   2 * u.dimensionless, 4 * u.m**2/u.s, 0.6 * u.m],
                  [490000 * u.cm**2, 2.4, 12, 3, 2, 4, 0.6],
                  [49, 240 * u.cm/u.s, 12, 3, 2, 4, 0.6],
                  [49, 2.4, 0.012 * u.km, 3, 2, 4, 0.6],
                  [49, 2.4, 12, 3000 * u.mm, 2, 4, 0.6],
                  [49, 2.4, 12, 3, 2, 40000 * u.cm**2/u.s, 0.6],
                  [49, 2.4, 12, 3, 2, 4, 60 * u.cm])
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqual(pc.headloss_gen(*i).magnitude, base)

    def test_headloss_manifold(self):
        """headloss_manifold should return known value for known input."""
        checks = (([0.12, 0.4, 6, 0.8, 0.75, 0.0003, 5], 38.57715300752375),
                  ([2, 6, 40, 5, 1.1, 0.04, 6], 0.11938889890999548))
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqual(pc.headloss_manifold(*i[0]).magnitude, i[1])

    def test_headloss_manifold_range(self):
        """headloss_manifold should object if NumOutlets is not a positive int."""
        failChecks = ((1, 1, 1, 1, 1, 1, -1), (1, 1, 1, 1, 1, 1, 0),
                      (1, 1, 1, 1, 1, 1, 0.1))
        passchecks = ((1, 1, 1, 1, 1, 1, 1.0), (1, 1, 1, 1, 1, 1, 47))
        for i in failChecks:
            with self.subTest(i=i):
                self.assertRaises((ValueError, TypeError), pc.headloss_manifold, *i)
        for i in passchecks:
            with self.subTest(i=i):
                pc.headloss_manifold(*i)

    def test_headloss_manifold_units(self):
        """headloss_manifold should handle units correctly."""
        base = pc.headloss_manifold(2, 6, 40, 5, 1.1, 0.04, 6).magnitude
        unitchecks = ([2 * u.m**3/u.s, 6 * u.m, 40 * u.m, 5* u.dimensionless,
                       1.1 * u.m**2/u.s, 0.04 * u.m, 6* u.dimensionless],
                      [2 * u.m**3/u.s, 6, 40, 5, 1.1, 0.04, 6],
                      [2, 6000 * u.mm, 40, 5, 1.1, 0.04, 6],
                      [2, 6, 0.04 * u.km, 5, 1.1, 0.04, 6],
                      [2, 6, 40, 5, 11000 * u.cm**2/u.s, 0.04, 6],
                      [2, 6, 40, 5, 1.1, 4 * u.cm, 6])
        for i in unitchecks:
            with self.subTest(i=i):
                self.assertAlmostEqual(pc.headloss_manifold(*i).magnitude, base)


class OrificeFuncsTest(unittest.TestCase):
    """Test the orifice functions."""
    def test_flow_orifice(self):
        """flow_orifice should return known result for known input."""
        checks = (([0.4, 2, 0.46], 0.36204122788069698),
                  ([2, 0.04, 0.2], 0.55652566805118475),
                  ([7, 0, 1], 0),
                  ([1.4, 0.1, 0], 0))
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqual(pc.flow_orifice(*i[0]).magnitude, i[1])

    def test_flow_orifice_range(self):
        """flow_orifice should raise errors when inputs are out of bounds."""
        checks = ((0,1,1), (1, 1, 1.1), (1, 1, -1))
        for i in checks:
            with self.subTest(i=i):
                self.assertRaises(ValueError, pc.flow_orifice, *i)
        pc.flow_orifice(1, 1, 0)

    def test_flow_orifice_units(self):
        """flow_orifice should handle units correctly."""
        base = pc.flow_orifice(2, 3, 0.5).magnitude
        checks = ((2 * u.m, 3 * u.m, 0.5 * u.dimensionless),
                  (200 * u.cm, 3, 0.5),
                  (2, 0.003 * u.km, 0.5))
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqual(pc.flow_orifice(*i).magnitude, base)

    def test_flow_orifice_vert(self):
        """flow_orifice_vert should return known values for known inputs."""
        checks = (([1, 3, 0.4], 2.4077258053173911),
                  ([0.3, 4, 0.67], 0.41946278400781861), ([2, -4, 0.2], 0))
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqual(pc.flow_orifice_vert(*i[0]).magnitude, i[1])

    def test_flow_orifice_vert_range(self):
        """flow_orifice_vert should raise errors when inputs are out of bounds."""
        errorChecks = ((1, 1, -1), (1, 1, 2))
        errorlessChecks = ((1, 1, 1), (1, 1, 0), (1, 1, 0.5))
        for i in errorChecks:
            with self.subTest(i=i):
                self.assertRaises(ValueError, pc.flow_orifice_vert, *i)
        for i in errorlessChecks:
            with self.subTest(i=i):
                pc.flow_orifice_vert(*i)

    def test_flow_orifice_vert_units(self):
        """flow_orifice_vert should handle units correctly."""
        base = pc.flow_orifice_vert(1, 3, 0.4).magnitude
        checks = ([1 * u.m, 3 * u.m, 0.4 * u.dimensionless],
                  [100 * u.cm, 3, 0.4],
                  [1, 0.003 * u.km, 0.4])
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqual(pc.flow_orifice_vert(*i).magnitude, base)

    def test_head_orifice(self):
        """head_orifice should return known value for known inputs."""
        checks = (([1, 1, 1], 0.08265508294256473),
                  ([1.2, 0.1, 0.12], 0.05739936315455882),
                  ([2, 0.5, 0.04], 3.3062033177025895e-05))
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqual(pc.head_orifice(*i[0]).magnitude, i[1])

    def test_head_orifice_range(self):
        """head_orifice should raise errors when passed invalid inputs."""
        failChecks = ((0,1,1), (1, 1, 0), (1, -1, 1), (1, 2, 1))
        for i in failChecks:
            with self.subTest(i=i):
                self.assertRaises(ValueError, pc.head_orifice, *i)
        pc.head_orifice(1, 1, 1)
        self.assertRaises(ZeroDivisionError, pc.head_orifice, *(1, 0, 1))

    def test_head_orifice_units(self):
        """head_orifice should handle units correctly."""
        base = pc.head_orifice(2, 0.5, 0.04).magnitude
        checks = ([2 * u.m, 0.5 * u.dimensionless, 0.04 * u.m**3/u.s],
                  [200 * u.cm, 0.5, 0.04],
                  [2, 0.5, 40 * u.L/u.s])
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqual(pc.head_orifice(*i).magnitude, base)

    def test_area_orifice(self):
        """area_orifice should return known value for known inputs."""
        checks = (([3, 0.4, 0.06], 0.019554886342464974),
                  ([2, 0.1, 0.1], 0.15966497839052934),
                  ([0.5, 0.02, 3], 47.899493517158803))
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqual(pc.area_orifice(*i[0]).magnitude, i[1])

    def test_area_orifice_range(self):
        """area_orifice should raise errors when inputs are out of bounds."""
        failChecks = ((0, 1, 1), (1, 1, 0), (1, -1, 1), (1, 2, 1), (1, 0, 1))
        for i in failChecks:
            with self.subTest(i=i):
                self.assertRaises(ValueError, pc.area_orifice, *i)
        pc.area_orifice(1, 1, 1)

    def test_area_orifice_units(self):
        """area_orifice should handle units correctly."""
        base = pc.area_orifice(3, 0.4, 0.06).magnitude
        checks = ([3 * u.m, 0.4 * u.dimensionless, 0.06 * u.m**3/u.s],
                  [300 * u.cm, 0.4, 0.06],
                  [3, 0.4, 60 * u.L/u.s])
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqual(pc.area_orifice(*i).magnitude, base)

    def test_num_orifices(self):
        """num_orifices should return known value for known inputs."""
        checks = (([0.12, 0.04, 0.05, 2], 1),
                  ([6, 0.8, 0.08, 1.2], 6))
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqual(pc.num_orifices(*i[0]), i[1])

    def test_num_orifices_units(self):
        """num_orifices should handle units correctly."""
        base = pc.num_orifices(6, 0.8, 0.08, 1.2)
        checks = ([6 * u.m**3/u.s, 0.8 * u.dimensionless, 0.08 * u.m, 1.2 * u.m],
                  [6000 * u.L/u.s, 0.8, 0.08, 1.2],
                  [6, 0.8, 8 * u.cm, 1.2],
                  [6, 0.8, 0.08, 0.0012 * u.km])
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqual(pc.num_orifices(*i), base)

class FlowFuncsTest(unittest.TestCase):
    """Test the flow functions."""
    def test_flow_transition(self):
        """flow_transition should return known value for known inputs."""
        checks = (([2, 0.4], 1319.4689145077132),
                  ([0.8, 1.1], 1451.4158059584847))
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqual(pc.flow_transition(*i[0]).magnitude, i[1])

    def test_flow_transition_range(self):
        """flow_transition should not accept inputs <= 0."""
        checks = ((1, 0), (0, 1))
        for i in checks:
            with self.subTest(i=i):
                self.assertRaises(ValueError, pc.flow_transition, *i)

    def test_flow_transition_units(self):
        """flow_transition should handle units correctly."""
        base = pc.flow_transition(2, 0.4).magnitude
        checks = ([2 * u.m, 0.4 * u.m**2/u.s],
                  [200 * u.cm, 0.4],
                  [2, 4000 * u.cm**2/u.s])
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqual(pc.flow_transition(*i).magnitude, base)

    def test_flow_hagen(self):
        """flow_hagen should return known value for known inputs."""
        checks = (([1, 0.4, 5.21, 0.6], 0.03079864403023667),
                  ([0.05, 0.0006, 0.3, 1.1], 2.7351295806397676e-09))
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqual(pc.flow_hagen(*i[0]).magnitude, i[1])

    def test_flow_hagen_range(self):
        """flow_hagen should raise errors when inputs are out of bounds."""
        failChecks = ((0, 1, 1, 1), (1, -1, 1, 1), (1, 1, 0, 1), (1, 1, 1, 0))
        for i in failChecks:
            with self.subTest(i=i):
                self.assertRaises(ValueError, pc.flow_hagen, *i)
        passChecks = ((1, 1, 1, 1), (1, 0, 1, 1))
        for i in passChecks:
            with self.subTest(i=i):
                pc.flow_hagen(*i)

    def test_flow_hagen_units(self):
        """flow_hagen should handle units properly."""
        base = pc.flow_hagen(0.05, 0.0006, 0.3, 1.1).magnitude
        checks = ([0.05 * u.m, 0.0006 * u.m, 0.3 * u.m, 1.1 * u.m**2/u.s],
                  [5 * u.cm, 0.0006, 0.3, 1.1],
                  [0.05, 0.6 * u.mm, 0.3, 1.1],
                  [0.05, 0.0006, 0.0003 * u.km, 1.1],
                  [0.05, 0.0006, 0.3, 11000 * u.cm**2/u.s])
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqual(pc.flow_hagen(*i).magnitude, base)

    def test_flow_swamee(self):
        """flow_swamee should return known value for known inputs."""
        checks = (([2, 0.04, 3, 0.1, 0.37], 2.9565931732010045),)
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqual(pc.flow_swamee(*i[0]).magnitude, i[1])

    def test_flow_swamee_range(self):
        """flow_swamee should raise errors when inputs are out of bounds."""
        failChecks = ((0, 1, 1, 1, 1), (1, 0, 1, 1, 1), (1, 1, 0, 1, 1),
                      (1, 1, 1, 0, 1), (1, 1, 1, 1, -0.1), (1, 1, 1, 1, 2))
        for i in failChecks:
            with self.subTest(i=i):
                self.assertRaises(ValueError, pc.flow_swamee, *i)
        passChecks = ((1, 1, 1, 1, 1), (1, 1, 1, 1, 0))
        for i in passChecks:
            with self.subTest(i=i):
                pc.flow_swamee(*i)

    def test_flow_swamee_units(self):
        """flow_swamee should handle units correctly."""
        base = pc.flow_swamee(2, 0.04, 3, 0.1, 0.37).magnitude
        checks = ([2 * u.m, 0.04 * u.m, 3 * u.m, 0.1 * u.m**2/u.s, 0.37 * u.m],
                  [200 * u.cm, 0.04, 3, 0.1, 0.37],
                  [2, 40 * u.mm, 3, 0.1, 0.37],
                  [2, 0.04, 0.003 * u.km, 0.1, 0.37],
                  [2, 0.04, 3, 1000 * u.cm**2/u.s, 0.37],
                  [2, 0.04, 3, 0.1, 37 * u.cm])
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqual(pc.flow_swamee(*i).magnitude, base)

    def test_flow_pipemajor(self):
        """flow_pipemajor should return known result for known inputs."""
        checks = (([1, 0.97, 0.5, 0.025, 0.06], 18.677652880272845),
                  ([2, 0.62, 0.5, 0.036, 0.23], 62.457206502701297))
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqual(pc.flow_pipemajor(*i[0]).magnitude, i[1])

    def test_flow_pipemajor_units(self):
        """flow_pipemajor should handle units correctly."""
        base = pc.flow_pipemajor(2, 0.62, 0.5, 0.036, 0.23).magnitude
        checks = ([2 * u.m, 0.62 * u.m, 0.5 * u.m,
                   0.036 * u.m**2/u.s, 0.23 * u.m],
                  [200 * u.cm, 0.62, 0.5, 0.036, 0.23],
                  [2, 620 * u.mm, 0.5, 0.036, 0.23],
                  [2, 0.62, 0.0005 * u.km, 0.036, 0.23],
                  [2, 0.62, 0.5, 360 * u.cm**2/u.s, 0.23],
                  [2, 0.62, 0.5, 0.036, 23 * u.cm])
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqual(pc.flow_pipemajor(*i).magnitude, base)

    def test_flow_pipeminor(self):
        """flow_pipeminor should return known results for known input."""
        self.assertAlmostEqual(pc.flow_pipeminor(1, 0.125, 3).magnitude,
                         0.71000203931611083)

    def test_flow_pipeminor_range(self):
        """flow_pipeminor should raise errors when inputs are out of bounds."""
        failChecks = ((1, -1, 1), (1, 1, 0))
        for i in failChecks:
            with self.subTest(i=i):
                self.assertRaises(ValueError, pc.flow_pipeminor, *i)
        passChecks = ((1, 1, 1), (1, 0, 1))
        for i in passChecks:
            with self.subTest(i=i):
                pc.flow_pipeminor(*i)

    def test_flow_pipeminor_units(self):
        """flow_pipeminor should handle units correctly."""
        base = pc.flow_pipeminor(1, 0.125, 3).magnitude
        checks = ((1 * u.m, 0.125 * u.m, 3 * u.dimensionless),
                  (0.001 * u.km, 0.125, 3),
                  (1, 125 * u.mm, 3))
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqual(pc.flow_pipeminor(*i).magnitude, base)

    def test_flow_pipe(self):
        """flow_pipe should return known value for known inputs."""
        checks = (([0.25, 0.4, 2, 0.58, 0.029, 0], 0.000324207170118938),
                  ([0.25, 0.4, 2, 0.58, 0.029, 0.35], 0.000324206539183988))
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqual(pc.flow_pipe(*i[0]).magnitude, i[1])

    def test_flow_pipe_units(self):
        """flow_pipe should handle units correctly."""
        base = pc.flow_pipe(0.25, 0.4, 2, 0.58, 0.029, 0.35).magnitude
        checks = ([0.25 * u.m, 0.4 * u.m, 2 * u.m,
                   0.58 * u.m**2/u.s, 0.029 * u.m, 0.35],
                  [25 * u.cm, 0.4, 2, 0.58, 0.029, 0.35],
                  [0.25, 400 * u.mm, 2, 0.58, 0.029, 0.35],
                  [0.25, 0.4, 0.002 * u.km, 0.58, 0.029, 0.35],
                  [0.25, 0.4, 2, 580000 * u.mm**2/u.s, 0.029, 0.35],
                  [0.25, 0.4, 2, 0.58, 29 * u.mm, 0.35])
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqual(pc.flow_pipe(*i).magnitude, base)


class DiamFuncsTest(unittest.TestCase):
    """Test the diameter functions."""
    def test_diam_hagen(self):
        """diam_hagen should return known value for known inputs."""
        self.assertAlmostEqual(pc.diam_hagen(0.006, 0.00025, 0.75, 0.0004).magnitude,
                         0.4158799465199102)

    def test_diam_hagen_range(self):
        """diam_hagen should raise errors when inputs are out of bounds."""
        failChecks = ((0, 1, 1, 1), (1, 0, 1, 1), (1, 1, 0, 1), (1, 1, 1, 0))
        for i in failChecks:
            with self.subTest(i=i):
                self.assertRaises(ValueError, pc.diam_hagen, *i)
        pc.diam_hagen(1, 1, 1, 1)

    def test_diam_hagen_units(self):
        """diam_hagen should handle units correctly."""
        base = pc.diam_hagen(0.006, 0.00025, 0.75, 0.0004).magnitude
        checks = ([0.006 * u.m**3/u.s, 0.00025 * u.m,
                   0.75 * u.m, 0.0004 * u.m**2/u.s],
                  [6 * u.L/u.s, 0.00025, 0.75, 0.0004],
                  [0.006, 0.25 * u.mm, 0.75, 0.0004],
                  [0.006, 0.00025, 75 * u.cm, 0.0004],
                  [0.006, 0.00025, 0.75, 4 * u.cm**2/u.s])
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqual(pc.diam_hagen(*i).magnitude, base)

    def test_diam_swamee(self):
        """diam_swamee should return known value for known input."""
        self.assertAlmostEqual(pc.diam_swamee(0.06, 1.2, 7, 0.2, 0.0004).magnitude,
                         0.19286307314945772)

    def test_diam_swamee_range(self):
        """diam_swamee should raise errors if inputs are out of bounds."""
        failChecks = ((0, 1, 1, 1, 1), (1, 0, 1, 1, 1), (1, 1, 0, 1, 1),
                      (1, 1, 1, 0, 1), (1, 1, 1, 1, 2), (1, 1, 1, 1, -1))
        for i in failChecks:
            with self.subTest(i=i):
                self.assertRaises(ValueError, pc.diam_swamee, *i)
        passChecks = ((1, 1, 1, 1, 1), (1, 1, 1, 1, 0))
        for i in passChecks:
            with self.subTest(i=i):
                pc.diam_swamee(*i)

    def test_diam_swamee_units(self):
        """diam_swamee should handle units correctly."""
        base = pc.diam_swamee(0.06, 1.2, 7, 0.2, 0.0004).magnitude
        checks = ([0.06 * u.m**3/u.s, 1.2 * u.m, 7 * u.m,
                   0.2 * u.m**2/u.s, 0.0004 * u.m],
                  [60 * u.L/u.s, 1.2, 7, 0.2, 0.0004],
                  [0.06, 0.0012 * u.km, 7, 0.2, 0.0004],
                  [0.06, 1.2, 700 * u.cm, 0.2, 0.0004],
                  [0.06, 1.2, 7, 2000 * u.cm**2/u.s, 0.0004],
                  [0.06, 1.2, 7, 0.2, 0.4 * u.mm])
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqual(pc.diam_swamee(*i).magnitude, base)

    def test_diam_pipemajor(self):
        """diam_pipemajor should return known value for known inputs."""
        checks = (([0.005, 0.03, 1.6, 0.53, 0.002], 0.8753787620849313),
                  ([1, 2, 0.03, 0.004, 0.005], 0.14865504303291951))
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqual(pc.diam_pipemajor(*i[0]).magnitude, i[1])

    def test_diam_pipemajor_units(self):
        """diam_pipemajor should handle units correctly."""
        base = pc.diam_pipemajor(1, 2, 0.03, 0.004, 0.005).magnitude
        checks = ([1 * u.m**3/u.s, 2 * u.m, 0.03 * u.m,
                   0.004 * u.m**2/u.s, 0.005 * u.m],
                  [1000 * u.L/u.s, 2, 0.03, 0.004, 0.005],
                  [1, 0.002 * u.km, 0.03, 0.004, 0.005],
                  [1, 2, 3 * u.cm, 0.004, 0.005],
                  [1, 2, 0.03, 40 * u.cm**2/u.s, 0.005],
                  [1, 2, 0.03, 0.004, 5 * u.mm])
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqual(pc.diam_pipemajor(*i).magnitude, base)

    def test_diam_pipeminor(self):
        """diam_pipeminor should return known value for known inputs."""
        checks = (([0.008, 0.012, 0.93], 0.14229440061589257),
                  ([0.015, 0.3, 0.472], 0.073547549463488848))
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqual(pc.diam_pipeminor(*i[0]).magnitude, i[1])

    def test_diam_pipeminor_range(self):
        """diam_pipeminor should raise errors when inputs are out of bounds."""
        failChecks = ((0, 1, 1), (1, 0, 1), (1, 1, -1))
        for i in failChecks:
            with self.subTest(i=i):
                self.assertRaises(ValueError, pc.diam_pipeminor, *i)
        passChecks = ((1, 1, 1), (1, 1, 0))
        for i in passChecks:
            with self.subTest(i=i):
                pc.diam_pipeminor(*i)

    def test_diam_pipeminor_units(self):
        """diam_pipeminor should handle units correctly."""
        base = pc.diam_pipeminor(0.008, 0.012, 0.93).magnitude
        checks = ([0.008 * u.m**3/u.s, 0.012 * u.m, 0.93 * u.dimensionless],
                  [8 * u.L/u.s, 0.012, 0.93],
                  [0.008, 1.2 * u.cm, 0.93])
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqual(pc.diam_pipeminor(*i).magnitude, base)

    def test_diam_pipe(self):
        """diam_pipe should return known value for known inputs."""
        checks = (([0.007, 0.04, 0.75, 0.16, 0.0079, 0], 0.5434876490369928),
                  ([0.007, 0.04, 0.75, 0.16, 0.0079, 0.8], 0.5436137491479152))
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqual(pc.diam_pipe(*i[0]).magnitude, i[1])

    def test_diam_pipe_units(self):
        """diam_pipe should handle units correctly."""
        base = pc.diam_pipe(0.007, 0.04, 0.75, 0.16, 0.0079, 0.8).magnitude
        checks = ([0.007 * u.m**3/u.s, 0.04 * u.m, 0.75 * u.m,
                   0.16 * u.m**2/u.s, 0.0079 * u.m, 0.8],
                  [7 * u.L/u.s, 0.04, 0.75, 0.16, 0.0079, 0.8],
                  [0.007, 4 * u.cm, 0.75, 0.16, 0.0079, 0.8],
                  [0.007, 0.04, 75 * u.cm, 0.16, 0.0079, 0.8],
                  [0.007, 0.04, 0.75, 1600 * u.cm**2/u.s, 0.0079, 0.8],
                  [0.007, 0.04, 0.75, 0.16, 7.9 * u.mm, 0.8])
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqual(pc.diam_pipe(*i).magnitude, base)

class WeirFuncsTest(unittest.TestCase):
    """Test the weir functions."""
    def test_width_rect_weir(self):
        """width_rect_weir should return known value for known inputs."""
        self.assertAlmostEqual(pc.width_rect_weir(0.005, 0.2).magnitude,
                         0.030, places=3)

    def test_width_rect_weir_range(self):
        """width_rect_weird should raise errors when inputs are out of bounds."""
        checks = ((0, 1), (1, 0))
        for i in checks:
            with self.subTest(i=i):
                self.assertRaises(ValueError, pc.width_rect_weir, *i)
        pc.width_rect_weir(1, 1)

    def test_width_rect_weir_units(self):
        """width_rect_weir should handle units correctly."""
        base = pc.width_rect_weir(0.005, 0.2).magnitude
        checks = ([0.005 * u.m**3/u.s, 0.2 * u.m],
                  [5 * u.L/u.s, 0.2],
                  [0.005, 20 * u.cm])
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqual(pc.width_rect_weir(*i).magnitude, base)

    def test_headloss_weir(self):
        """headloss_weir should return known value for known inputs."""
        self.assertAlmostEqual(pc.headloss_weir(0.005, 1).magnitude,
                         0.019, places=3)

    def test_headloss_weir_range(self):
        """headloss_weir should raise errors when inputs are out of bounds."""
        checks = ((0, 1), (1, 0))
        for i in checks:
            with self.subTest(i=i):
                self.assertRaises(ValueError, pc.headloss_weir, *i)
        pc.headloss_weir(1,1)

    def test_headloss_weir_units(self):
        """headloss_weir should handle units correctly."""
        base = pc.headloss_weir(0.005, 1).magnitude
        checks = ([0.005 * u.m**3/u.s, 1 * u.m],
                  [5 * u.L/u.s, 1],
                  [0.005, 100 * u.cm])
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqual(pc.headloss_weir(*i).magnitude, base)

    def test_flow_rect_weir(self):
        """flow_rect_weir should return known value for known inputs."""
        self.assertAlmostEqual(pc.flow_rect_weir(2, 1).magnitude, 5.261, places=3)

    def test_flow_rect_weir_range(self):
        """flow_rect_weir should raise errors when inputs are out of bounds."""
        checks = ((0, 1), (1, 0))
        for i in checks:
            with self.subTest(i=i):
                self.assertRaises(ValueError, pc.flow_rect_weir, *i)
        pc.flow_rect_weir(1, 1)

    def test_flow_rect_weir_units(self):
        """flow_rect_weir should handle units correctly."""
        base = pc.flow_rect_weir(2, 1).magnitude
        checks = ([2 * u.m, 1 * u.m],
                  [200 * u.cm, 1],
                  [2, 100 * u.cm])
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqual(pc.flow_rect_weir(*i).magnitude, base)


class MiscPhysFuncsTest(unittest.TestCase):
    """Test the miscellaneous physchem functions."""
    def test_height_water_critical(self):
        """height_water_critical should return known value for known inputs."""
        self.assertAlmostEqual(pc.height_water_critical(0.006, 1.2).magnitude,
                         0.013660704939951886)

    def test_height_water_critical_range(self):
        """height_water_critical should raise errors when inputs are out of bounds."""
        checks = ((0, 1), (1, 0))
        for i in checks:
            with self.subTest(i=i):
                self.assertRaises(ValueError, pc.height_water_critical, *i)
        pc.height_water_critical(1, 1)

    def test_height_water_critical_units(self):
        """height_water_critical should handle units correctly."""
        base = pc.height_water_critical(0.006, 1.2).magnitude
        checks = ([0.006 * u.m**3/u.s, 1.2 * u.m],
                  [6 * u.L/u.s, 1.2],
                  [0.006, 120 * u.cm])
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqual(pc.height_water_critical(*i).magnitude, base)

    def test_vel_horizontal(self):
        """vel_horizontal should return known value for known inputs."""
        self.assertAlmostEqual(pc.vel_horizontal(0.03).magnitude, 0.5424016039799292)

    def test_vel_horizontal_range(self):
        """vel_horizontzal should raise an errors when input is <= 0."""
        self.assertRaises(ValueError, pc.vel_horizontal, 0)

    def test_vel_horizontal_units(self):
        """vel_horizontal should handle units correctly."""
        base = pc.vel_horizontal(0.03).magnitude
        checks = (0.03 * u.m, 3 * u.cm)
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqual(pc.vel_horizontal(i).magnitude, base)

    def test_headloss_kozeny(self):
        """headloss_kozeny should return known value for known input."""
        self.assertAlmostEqual(pc.headloss_kozeny(1, 1.4, 0.5, 0.625, 0.8).magnitude,
                         2.1576362645214617)

    def test_headloss_kozeny_range(self):
        """headloss_kozeny should raise errors when inputs are out of bounds."""
        checks = ((0, 1, 1, 1, 1), (1, 0, 1, 1, 1), (1, 1, 0, 1, 1),
                  (1, 1, 1, 1, 0), (1, 1, 1, -1, 1), (1, 1, 1, 2, 1))
        for i in checks:
            with self.subTest(i=i):
                self.assertRaises(ValueError, pc.headloss_kozeny, *i)
        pc.headloss_kozeny(1, 1, 1, 1, 1)

    def test_headloss_kozeny_units(self):
        """headloss_kozeny should handle units correctly."""
        base = pc.headloss_kozeny(1, 1.4, 0.5, 0.625, 0.8).magnitude
        checks = ([1 * u.m, 1.4 * u.m, 0.5 * u.m/u.s,
                   0.625 * u.m, 0.8 * u.m**2/u.s],
                  [100 * u.cm, 1.4, 0.5, 0.625, 0.8],
                  [1, 0.0014 * u.km, 0.5, 0.625, 0.8],
                  [1, 1.4, 30 * u.m/u.min, 0.625, 0.8],
                  [1, 1.4, 0.5, 625 * u.mm, 0.8],
                  [1, 1.4, 0.5, 0.625, 8000 * u.cm**2/u.s])
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqual(pc.headloss_kozeny(*i).magnitude, base)

    def test_pipe_ID(self):
        """pipe_ID should return known value for known input"""
        self.assertAlmostEquals(pc.pipe_ID(0.006, 1.2).magnitude, 0.039682379412712764)


if __name__ == "__main__":
    unittest.main()
