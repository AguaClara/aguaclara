"""
Tests for the research package's tube_sizing module.
"""

import unittest

import sys
sys.path.append("../../aguaclara/research")
from peristaltic_pump import *
# from aguaclara.research.peristaltic_pump import *

class TestTubeSizing(unittest.TestCase):

    def assertAlmostEqualQuantity(self, first, second, places=7):
        self.assertAlmostEqual(first.magnitude, second.magnitude, places)
        self.assertAlmostEqual(first.units, second.units, places)

    def test_vol_per_rev_3_stop(self):
        answer = 0.0013286183895203283*u.mL/u.rev
        self.assertAlmostEqualQuantity(vol_per_rev_3_stop(color="orange-black"), answer)

        answer = 0.14884596727278449*u.mL/u.rev
        self.assertAlmostEqualQuantity(vol_per_rev_3_stop(color="yellow-blue"), answer)

        answer = 0.0031160704169596186*u.mL/u.rev
        self.assertAlmostEqualQuantity(vol_per_rev_3_stop(inner_diameter=.20*u.mm), answer)

        answer = 0.4005495805189351*u.mL/u.rev
        self.assertAlmostEqualQuantity(vol_per_rev_3_stop(inner_diameter=2.79*u.mm), answer)

    def test_ID_colored_tube(self):
        answer = 1.52*u.mm
        self.assertEqual(ID_colored_tube("yellow-blue"), answer)

        answer = 0.51*u.mm
        self.assertEqual(ID_colored_tube("orange-yellow"), answer)

        answer = 2.79*u.mm
        self.assertEqual(ID_colored_tube("purple-white"), answer)

    def test_vol_per_rev_LS(self):
        answer = 0.06*u.mL/u.rev
        self.assertEqual(vol_per_rev_LS(13), answer)

        answer = 0.21*u.mL/u.rev
        self.assertEqual(vol_per_rev_LS(14), answer)

        answer = 1.6*u.mL/u.rev
        self.assertEqual(vol_per_rev_LS(15), answer)

        answer = 0.8*u.mL/u.rev
        self.assertEqual(vol_per_rev_LS(16), answer)

        answer = 2.8*u.mL/u.rev
        self.assertEqual(vol_per_rev_LS(17), answer)

        answer = 3.8*u.mL/u.rev
        self.assertEqual(vol_per_rev_LS(18), answer)

        answer = 2.8*u.mL/u.rev
        self.assertEqual(vol_per_rev_LS(24), answer)

        answer = 3.8*u.mL/u.rev
        self.assertEqual(vol_per_rev_LS(35), answer)

        answer = 4.8*u.mL/u.rev
        self.assertEqual(vol_per_rev_LS(36), answer)

    def test_flow_rate(self):
        answer = 0.25*u.mL/u.s
        self.assertAlmostEqualQuantity(flow_rate(3*u.mL/u.rev, 5*u.rev/u.min), answer)

        answer = 0.016666666666666666*u.mL/u.s
        self.assertAlmostEqualQuantity(flow_rate(.04*u.mL/u.rev, 25*u.rev/u.min), answer)

        answer = 0.01*u.mL/u.s
        self.assertAlmostEqualQuantity(flow_rate(.001*u.mL/u.rev, 600*u.rev/u.min), answer)
