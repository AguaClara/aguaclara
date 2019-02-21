import unittest

from aguaclara.design.plant import Plant
from aguaclara.core.units import unit_registry as u


class PlantTest(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.plant = Plant()

    def test_vel_grad_avg(self):
        self.assertAlmostEqual(self.plant.ent_tank_a, 2.819052298257505 * (u.m ** 2), 3)
