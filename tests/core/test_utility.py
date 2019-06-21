import unittest

from aguaclara.play import *


class UtilityTest(unittest.TestCase):

    def test_round_sig_figs(self):
        self.assertAlmostEqual(ut.round_sig_figs(123456.789, 8), 123456.79)
        self.assertAlmostEqual(ut.round_sig_figs(20.01 * u.L/u.s, 2), 20 * u.L/u.s)
        self.assertAlmostEqual(ut.round_sig_figs(-456.789 * u.L/u.s, 4), -456.8 * u.L/u.s)
        self.assertAlmostEqual(ut.round_sig_figs(0, 4), 0)
        self.assertAlmostEqual(ut.round_sig_figs(0 * u.m, 4), 0 * u.m)
    def test_max(self):
        self.assertEqual(ut.max(2 * u.m, 4 * u.m),4 * u.m)
        self.assertEqual(ut.max(3 * u.m, 1 * u.m, 6 * u.m, 10 * u.m, 1.5 * u.m), 10 * u.m)
        self.assertEqual(ut.max(2 * u.m),2 * u.m)

    def test_min(self):
        self.assertEqual(ut.min(2 * u.m, 4 * u.m), 2 * u.m)
        self.assertEqual(ut.min(3 * u.m, 1 * u.m, 6 * u.m, 10 * u.m, 1.5 * u.m), 1 * u.m)
        self.assertEqual(ut.min(2 * u.m), 2 * u.m)