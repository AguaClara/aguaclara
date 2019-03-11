"""
Tests for the research package's floc_model functions
"""

import sys
sys.path.append("../../aguaclara/research")

import unittest
import floc_model as fm
import aguaclara.research.floc_model as fm
from aguaclara.core.units import unit_registry as u

class TestFlocModel(unittest.TestCase):

    def test_Material(self):
        # Clay = fm.Material('Clay', 7 * 10**-6 * u.m, 2650 * u.kg/u.m**3, None)
        # self.assertEqual(Clay.name, 'Clay')
        # self.assertEqual(Clay.Diameter, 7 * 10**-6 * u.m)
        # self.assertEqual(Clay.Density, 2650 * u.kg/u.m**3)
        # self.assertEqual(Clay.MolecWeight, None)
        fm.sep_dist_clay(.5*u.kg/u.m**3, fm.Clay)
