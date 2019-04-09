import unittest

from aguaclara.design.sed_tank_bay import SedimentationTankBay
from aguaclara.core.units import unit_registry as u


class SedimentationTankBayTest(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.sed_tank_bay = SedimentationTankBay()

    def test_q(self):
        self.assertAlmostEqual(self.sed_tank_bay.q, 6.18744* u.L / u.s)

    def test_n(self):
        self.assertAlmostEqual(self.sed_tank_bay.n, 4)

    def test_w_diffuser_inner_min(self):
        self.assertAlmostEqual(self.sed_tank_bay.w_diffuser_inner_min, 0.09482953262587492* u.inch)

    def test_vel_inlet_man_max(self):
        self.assertAlmostEqual(self.sed_tank_bay.vel_inlet_man_max, 0.29346073739129713*(u.m/u.s))

    # def test_ID_exit_man(self):
    #     self.assertAlmostEqual(self.sed_tank_bay.ID_exit_man, 0.06184467012869722)
    #
    # def test_D_exit_man_orifice(self):
    #     self.assertAlmostEqual(self.sed_tank_bay.D_exit_man_orifice, 0.001373119658119658*u.mm)

    def test_L_sed_plate(self):
        self.assertAlmostEqual(self.sed_tank_bay.L_sed_plate, 0.4618802153517006*u.m)

    def test_diffuser_a(self):
        self.assertAlmostEqual(self.sed_tank_bay.diffuser_a, 0.00012935450691151752*u.L/u.mm)
