# floc.d_exp_max, 0.375*u.m
# floc.baffles_s, 0.063*u.m

import unittest

from aguaclara.design.floc import Flocculator
from aguaclara.core.units import unit_registry as u


class FlocTest(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.floc = Flocculator()

    def test_vel_gradient_avg(self):
        self.assertAlmostEqual(self.floc.vel_grad_avg,
                               118.71480891150065 * (u.s ** -1))

    def test_retention_time(self):
        self.assertAlmostEqual(self.floc.retention_time,
                               311.6713099170526 * u.s)

    def test_vol(self):
        self.assertAlmostEqual(self.floc.vol, 6.233426198341053 * u.m**3)

    def test_l_max_vol(self):
        self.assertAlmostEqual(self.floc.l_max_vol, 3.463014554633918 * u.m)

    def test_channel_l(self):
        self.assertAlmostEqual(self.floc.channel_l, 3.463014554633918 * u.m)

    def test_w_min_hs_ratio(self):
        self.assertAlmostEqual(self.floc.w_min_hs_ratio,
                               11.114415605933008 * u.cm)

    def test_w_min(self):
        self.assertAlmostEqual(self.floc.w_min, 45 * u.cm)
