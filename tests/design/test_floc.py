# from pytest import approx
#
# from aguaclara.design.floc import Flocculator
# from aguaclara.core.units import unit_registry as u
#
#
# def test_all_functions(utils):
#     floc = Flocculator(q=(20 * (u.L/u.s)), temp=(25 * u.degC))
#
#     tests = zip(
#         (floc.vel_gradient_avg, 118.715*(u.s**-1), 0.001),
#         (floc.vol, 6.233*(u.m**3), 0.001),
#         (floc.w_min_h_s_ratio, 0.1074*u.cm, 0.0001),
#         (floc.d_exp_max, 0.375*u.m, 0.001),
#         (floc.baffles_s, 0.063*u.m, 0.001)
#     )
#
#     assert floc.num_channel == 2
#     assert floc.baffles_n == approx(31, 1)
#     utils.vaue(tests)

import unittest

from aguaclara.design.floc import Flocculator
from aguaclara.core.units import unit_registry as u


class FlocTest(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.floc = Flocculator()

    def test_vel_gradient_avg(self):
        self.assertAlmostEqual(self.floc.vel_grad_avg, 118.71480891150065 * (u.s ** -1))

    def test_retention_time(self):
        self.assertAlmostEqual(self.floc.retention_time, 311.6713099170526 * u.s)

    def test_vol(self):
        self.assertAlmostEqual(self.floc.vol, 6.233426198341053 * (u.m**3))
