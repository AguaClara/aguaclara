from aguaclara.design.ent import EntranceTank
from aguaclara.core.units import unit_registry as u

import unittest

class EntranceTankTest(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)

        self.ent_12 = EntranceTank(12 * u.L / u.s)
        self.ent_20 = EntranceTank(20 * u.L / u.s)
        self.ent_40 = EntranceTank(40 * u.L / u.s)
        self.ent_60 = EntranceTank(60 * u.L / u.s)

    def test_drain_od(self):
        self.assertAlmostEqual(self.ent_12.drain_od, 0 * u.m)
        self.assertAlmostEqual(self.ent_20.drain_od, 0 * u.m)
        self.assertAlmostEqual(self.ent_40.drain_od, 0 * u.m)
        self.assertAlmostEqual(self.ent_60.drain_od, 0 * u.m)

    def test_plate_n(self):
        self.assertAlmostEqual(self.ent_12.plate_n, 9)
        self.assertAlmostEqual(self.ent_20.plate_n, 11)
        self.assertAlmostEqual(self.ent_40.plate_n, 15)
        self.assertAlmostEqual(self.ent_60.plate_n, 19)

    def test_l(self):
        self.assertAlmostEqual(self.ent_12.l, 0 * u.m)
        self.assertAlmostEqual(self.ent_20.l, 0 * u.m)
        self.assertAlmostEqual(self.ent_40.l, 0 * u.m)
        self.assertAlmostEqual(self.ent_60.l, 0 * u.m)
