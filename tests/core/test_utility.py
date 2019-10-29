import unittest
import aguaclara.core.utility as ut
from aguaclara.core.units import u
import numpy as np


class QuantityTest(unittest.TestCase):
    def assertAlmostEqualQuantity(self, first, second, places=7):
        self.assertAlmostEqual(first.magnitude, second.magnitude, places)
        self.assertEqual(first.units, second.units, places)

    def assertAlmostEqualArray(self, first, second, places=7):
        self.assertEqual(type(first), type(second))
        for i in range(len(first)):
            self.assertAlmostEqual(first[i], second[i], places)

    def assertAlmostEqualArrayQuantity(self, first, second, places=7):
        second = second.to(first.units)
        self.assertEqual(first.units, second.units, places)
        self.assertAlmostEqualArray(first.magnitude, second.magnitude)


class UtilityTest(QuantityTest):

    def test_round_sig_figs(self):
        self.assertAlmostEqual(ut.round_sig_figs(123456.789, 8), 123456.79)
        self.assertAlmostEqual(ut.round_sig_figs(20.01 * u.L/u.s, 2), 20 * u.L/u.s)
        self.assertAlmostEqual(ut.round_sig_figs(-456.789 * u.L/u.s, 4), -456.8 * u.L/u.s)
        self.assertAlmostEqual(ut.round_sig_figs(0, 4), 0)
        self.assertAlmostEqual(ut.round_sig_figs(0 * u.m, 4), 0 * u.m)

    def test_max(self):
        self.assertEqual(ut.max(2 * u.m, 4 * u.m),4 * u.m)
        self.assertEqual(ut.max(3 * u.m, 1 * u.m, 6 * u.m, 10 * u.m, 1.5 * u.m), 10 * u.m)
        self.assertEqual(ut.max(2 * u.m), 2 * u.m)

    def test_min(self):
        self.assertEqual(ut.min(2 * u.m, 4 * u.m), 2 * u.m)
        self.assertEqual(ut.min(3 * u.m, 1 * u.m, 6 * u.m, 10 * u.m, 1.5 * u.m), 1 * u.m)
        self.assertEqual(ut.min(2 * u.m), 2 * u.m)

    def test_list_handler_with_units(self):
        @ut.list_handler()
        def density_air(Pressure, MolarMass, Temperature):
            """Return the density of air at the given pressure, molar mass, and
            temperature.

            :param Pressure: pressure of air in the system
            :type Pressure: u.pascal
            :param MolarMass: molar mass of air in the system
            :type MolarMass: u.gram/u.mol
            :param Temperature: Temperature of air in the system
            :type Temperature: u.degK

            :return: density of air in the system
            :rtype: u.kg/u.m**3
            """
            return (Pressure * MolarMass / (u.R * Temperature)).to(u.kg/u.m**3)

        answer = 1.29320776*u.kg/u.m**3
        self.assertAlmostEqualQuantity(density_air(1*u.atm, 28.97*u.g/u.mol, 273*u.K), answer)

        answer = 1.29320776*u.kg/u.m**3
        self.assertAlmostEqualQuantity(density_air(MolarMass=28.97*u.g/u.mol, Temperature=273*u.K, Pressure=1*u.atm), answer)

        answer = np.array([1.29320776, 2.58641552, 3.87962328, 12.93207761])*u.kg/u.m**3
        self.assertAlmostEqualArrayQuantity(density_air([1, 2, 3, 10]*u.atm, 28.97*u.g/u.mol, 273*u.K), answer)

        answer = np.array([1.29320776, 2.58641552, 3.87962328, 12.93207761])*u.kg/u.m**3
        self.assertAlmostEqualArrayQuantity(density_air(MolarMass=28.97*u.g/u.mol, Temperature=273*u.K, Pressure=[1, 2, 3, 10]*u.atm), answer)

        answer = np.array([[1.29320776, 1.20526784, 1.07134919, 0.89279099],
                           [2.58641552, 2.41053569, 2.14269839, 1.78558199],
                           [3.87962328, 3.61580354, 3.21404759, 2.67837299],
                           [12.93207761, 12.05267848, 10.71349198, 8.92790998]])*u.kg/u.m**3
        output = density_air([1, 2, 3, 10]*u.atm, [28.97, 27, 24, 20]*u.g/u.mol, 273*u.K)
        self.assertEqual(output.units, answer.units)
        for i in range(len(output.magnitude)):
            self.assertAlmostEqualArray(output.magnitude[i], answer.magnitude[i])

    def test_list_handler_dimensionless(self):
        @ut.list_handler()
        def re_pipe(FlowRate, Diam, Nu):
            """Return the Reynolds number of flow through a pipe.

            :param FlowRate: flow rate through pipe
            :type FlowRate: u.m**3/u.s
            :param Diam: diameter of pipe
            :type Diam: u.m
            :param Nu: kinematic viscosity of fluid
            :type Nu: u.m**2/u.s

            :return: Reynolds number of flow through pipe
            :rtype: u.dimensionless
            """
            return ((4 * FlowRate) / (np.pi * Diam * Nu))

        answer = 254.64790894703253 * u.dimensionless
        self.assertAlmostEqualQuantity(re_pipe(12 * u.m**3/u.s, 6 * u.m, 0.01 * u.m**2/u.s), answer)

        answer = np.array([254.647908947, 218.26963624, 190.98593171]) * u.dimensionless
        self.assertAlmostEqualArrayQuantity(re_pipe(12 * u.m**3/u.s, [6, 7, 8] * u.m, 0.01 * u.m**2/u.s), answer)
