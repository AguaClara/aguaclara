import unittest

from aguaclara.play import *


class UtilityTest(unittest.TestCase):

    def test_round_sf(self):
        self.assertAlmostEqual(ut.round_sf(123456.789, 8), 123456.79)
        self.assertAlmostEqual(ut.round_sf(20.01 * u.L/u.s, 2), 20 * u.L/u.s)
        self.assertAlmostEqual(ut.round_sf(-456.789 * u.L/u.s, 4), -456.8 * u.L/u.s)
        self.assertAlmostEqual(ut.round_sf(0, 4), 0)
        self.assertAlmostEqual(ut.round_sf(0 * u.m, 4), 0 * u.m)
