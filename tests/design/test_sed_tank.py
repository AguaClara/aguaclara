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
        self.assertAlmostEqual(self.sed_tank.L_diffuser_inner, -0.05806288034188034*u.m)

    def test_q_diffuser(self):
        self.assertAlmostEqual(self.sed_tank.q_diffuser, 1.4648440512820511e-06*u.m)

    def test_vel_sed_diffuser(self):
        self.assertAlmostEqual(self.sed_tank.vel_sed_diffuser, -0.0002018286440709652)

    def test_q_tank(self):
        self.assertAlmostEqual(self.sed_tank.q_tank, 6.18744*(u.L / u.s))

    def test_vel_inlet_man_max(self):
        self.assertAlmostEqual(self.sed_tank.vel_inlet_man_max, 0.29346073739129713)

    def test_n_tanks(self):
        self.assertAlmostEqual(self.sed_tank.n_tanks, 4)

    def test_L_channel(self):
        self.assertAlmostEqual(self.sed_tank.L_channel, 191.6220472440945*u.inch)

    #def test_ID_exit_man(self):
    #    self.assertAlmostEqual(self.sed_tank.ID_exit_man, 4*u.m)




