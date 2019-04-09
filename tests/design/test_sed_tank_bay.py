import unittest

from aguaclara.design.sed_tank_bay import SedimentationTankBay
from aguaclara.core.units import unit_registry as u


class SedimentationTankBayTest(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.sed_tank_bay = SedimentationTankBay()

    def test_q_bay(self):
        self.assertAlmostEqual(self.sed_tank_bay.q, 13)

#    def test_n(self):
#        self.assertAlmostEqual(self.sed_tank_bay.n, 4)

#    def test_w_diffuser_inner_min(self):
#        self.assertAlmostEqual(self.sed_tank_bay.w_diffuser_inner_min, 0.125* u.inch)

#    def test_vel_inlet_man_max(self):
#        self.assertAlmostEqual(self.sed_tank_bay.vel_inlet_man_max, 0.29346073739129713*(u.m/u.s))

#    def test_ID_exit_man(self):
#        self.assertAlmostEqual(self.sed_tank_bay.ID_exit_man, 0.06184467012869722*u.m)

#    def test_D_exit_man_orifice(self):
#        self.assertAlmostEqual(self.sed_tank_bay.D_exit_man_orifice, 0.001373119658119658*u.m)

#    def test_L_sed_plate(self):
#        self.assertAlmostEqual(self.sed_tank_bay.L_sed_plate, -0.05806288034188034*u.m)

#    def test_diffuser_a(self):
#        self.assertAlmostEqual(self.sed_tank_bay.diffuser_a, 1.4648440512820511e-06*((u.m**3)/u.s))
