"""
Tests for the research package's floc_model functions
"""

import unittest
from aguaclara.core.units import unit_registry as u

developing = False
if developing:
    import sys
    sys.path.append("../../aguaclara/research")
    import floc_model as fm
else:
    import aguaclara.research.floc_model as fm


class TestFlocModel(unittest.TestCase):

    def test_Material(self):
        self.assertEqual(fm.Clay.name, 'Clay')
        self.assertEqual(fm.Clay.Diameter, 7 * 10**-6 * u.m)
        self.assertEqual(fm.Clay.Density, 2650 * u.kg/u.m**3)
        self.assertEqual(fm.Clay.MolecWeight, None)

    def test_Chemical(self):
        PaCl = fm.Chemical('PACl', 9 * 10 **-8 * u.m, 1138 * u.kg/u.m**3, 1.039 * u.kg/u.mol, 'PACl', AluminumMPM=13)
        self.assertEqual(fm.PACl.name, 'PACl')
        self.assertEqual(fm.PACl.Diameter, 9 * 10 **-8 * u.m)
        self.assertEqual(fm.PACl.Density, 1138 * u.kg/u.m**3)
        self.assertEqual(fm.PACl.MolecWeight, 1.039 * u.kg/u.mol)
        self.assertEqual(fm.PACl.Precip, 'PACl')
        self.assertEqual(fm.PACl.AluminumMPM, 13)

        self.assertEqual(fm.Alum.name, 'Alum')
        self.assertEqual(fm.Alum.Diameter, 7 * 10 **-8 * u.m)
        self.assertEqual(fm.Alum.Density, 2420 * u.kg/u.m**3)
        self.assertEqual(fm.Alum.MolecWeight, 0.59921 * u.kg/u.mol)
        self.assertEqual(fm.Alum.Precip, 'AlOH3')
        self.assertEqual(fm.Alum.AluminumMPM, 2)

        self.assertEqual(fm.HumicAcid.name, 'Humic Acid')
        self.assertEqual(fm.HumicAcid.Diameter, 72 * 10**-9 * u.m)
        self.assertEqual(fm.HumicAcid.Density, 1780 * u.kg/u.m**3)
        self.assertEqual(fm.HumicAcid.MolecWeight, None)
        self.assertEqual(fm.HumicAcid.Precip, 'Humic Acid')
