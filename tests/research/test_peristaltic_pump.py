"""
Tests for the research package's tube_sizing module.
"""

import unittest
from aguaclara.core.units import u
import aguaclara.research.peristaltic_pump as pp


class TestTubeSizing(unittest.TestCase):

    def assertAlmostEqualQuantity(self, first, second, places=7):
        self.assertAlmostEqual(first.magnitude, second.magnitude, places)
        self.assertAlmostEqual(first.units, second.units, places)

    def test_vol_per_rev_3_stop(self):
        self.assertAlmostEqualQuantity(0.0013286183895203283*u.mL/u.rev, pp.vol_per_rev_3_stop(color="orange-black"))
        self.assertAlmostEqualQuantity(0.14884596727278449*u.mL/u.rev, pp.vol_per_rev_3_stop(color="yellow-blue"))
        self.assertAlmostEqualQuantity(0.0031160704169596186*u.mL/u.rev, pp.vol_per_rev_3_stop(inner_diameter=.20*u.mm))
        self.assertAlmostEqualQuantity(0.4005495805189351*u.mL/u.rev, pp.vol_per_rev_3_stop(inner_diameter=2.79*u.mm))

    def test_ID_colored_tube(self):
        self.assertEqual(1.52*u.mm, pp.ID_colored_tube("yellow-blue"))
        self.assertEqual(0.51*u.mm, pp.ID_colored_tube("orange-yellow"))
        self.assertEqual(2.79*u.mm, pp.ID_colored_tube("purple-white"))

    def test_vol_per_rev_LS(self):
        self.assertEqual(0.06*u.mL/u.rev, pp.vol_per_rev_LS(13))
        self.assertEqual(1.6*u.mL/u.rev, pp.vol_per_rev_LS(15))
        self.assertEqual(3.8*u.mL/u.rev, pp.vol_per_rev_LS(18))
        self.assertEqual(4.8*u.mL/u.rev, pp.vol_per_rev_LS(36))

    def test_flow_rate(self):
        self.assertAlmostEqualQuantity(0.25*u.mL/u.s, pp.flow_rate(3*u.mL/u.rev, 5*u.rev/u.min))
        self.assertAlmostEqualQuantity(0.016666666666666666*u.mL/u.s, pp.flow_rate(.04*u.mL/u.rev, 25*u.rev/u.min))
        self.assertAlmostEqualQuantity(0.01*u.mL/u.s, pp.flow_rate(.001*u.mL/u.rev, 600*u.rev/u.min))
