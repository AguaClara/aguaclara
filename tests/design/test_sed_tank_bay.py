import unittest

from aguaclara.design.sed_tank_bay import SedimentationTankBay
from aguaclara.core.units import unit_registry as u


class SedimentationTankBayTest(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.sed_tank_bay = SedimentationTankBay()
