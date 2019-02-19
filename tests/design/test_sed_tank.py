import unittest

from aguaclara.design.sed_tank import SedimentationTank
from aguaclara.core.units import unit_registry as u


class SedimentationTankTest(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.sedtank = SedimentationTank()