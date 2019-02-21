import unittest

from aguaclara.design.floc import Flocculator
from aguaclara.core.units import unit_registry as u


class FlocTest(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.floc = Flocculator()

    def test_vel_grad_avg(self):
        self.assertAlmostEqual(self.floc.vel_grad_avg, 118.71480891150067 * (u.s ** -1))

    def test_retention_time(self):
        self.assertAlmostEqual(self.floc.retention_time,
                               311.67130991705255 * u.s)

    def test_vol(self):
        self.assertAlmostEqual(self.floc.vol, 6.233426198341051 * u.m**3)

    def test_channel_l(self):
        self.assertAlmostEqual(self.floc.channel_L, 4.213014554633917 * u.m)

    def test_w_min_hs_ratio(self):
        self.assertAlmostEqual(self.floc.W_min_HS_ratio,
                               11.026896890543643 * u.cm)

    def test_channel_n(self):
        self.assertEqual(self.floc.channel_n, 2)

    def channel_w(self):
        self.assertAlmostEqual(self.floc.channel_W, 0.45 * u.m)

    def test_expansion_h_max(self):
        self.assertAlmostEqual(self.floc.expansion_max_H,
                               1.1714751817536837 * u.m)

    def test_expansion_n(self):
        self.assertAlmostEqual(self.floc.expansion_n, 2)

    def test_expansion_h(self):
        self.assertAlmostEqual(self.floc.expansion_H, 100.0 * u.cm)

    def test_baffle_s(self):
        self.assertAlmostEqual(self.floc.baffle_S, 20.58225112209816 * u.cm)

    def test_obstacle_n(self):
        self.assertAlmostEqual(self.floc.obstacle_n, 1)
