import unittest

from aguaclara.design.sed_tank import SedimentationTank
from aguaclara.core.units import unit_registry as u


class SedimentationTankTest(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.sed_tank = SedimentationTank()

    def test_n_sed_plates_max(self):
        self.assertAlmostEqual(self.sed_tank.n_sed_plates_max, 13)

    def test_w_diffuser_inner_min(self):
        self.assertAlmostEqual(self.sed_tank.w_diffuser_inner_min, 0.09482953262587492 * u.inch)

    def test_w_diffuser_inner(self):
        self.assertAlmostEqual(self.sed_tank.w_diffuser_inner, 0.125* u.inch)

    def test_w_diffuser_outer(self):
        self.assertAlmostEqual(self.sed_tank.w_diffuser_outer, 0.06184467012869722)

    def test_L_diffuser_outer(self):
        self.assertAlmostEqual(self.sed_tank.L_diffuser_outer, 0.001373119658119658)

    def test_L_diffuser_inner(self):
        self.assertAlmostEqual(self.sed_tank.L_diffuser_inner, -0.05806288034188034)

    def test_q_diffuser(self):
        self.assertAlmostEqual(self.sed_tank.q_diffuser, 1.4648440512820511e-06)


