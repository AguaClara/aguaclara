"""
Tests for the research package's tube_sizing module.
"""

import unittest
from aguaclara.research.tube_sizing import *


class TestTubeSizing(unittest.TestCase):

    def test_vol_per_rev(self):
        answer = 0.4005495805189351*u.mL/u.rev
        self.assertEqual(vol_per_rev(2.79*u.mm), answer)

        answer = 0.14884596727278446*u.mL/u.rev
        self.assertEqual(vol_per_rev(1.52*u.mm), answer)

        answer = 0.01943899117521222*u.mL/u.rev
        self.assertEqual(vol_per_rev(0.51*u.mm), answer)

    def test_ID_colored_tube(self):
        answer = 1.52*u.mm
        self.assertEqual(ID_colored_tube("yellow-blue"), answer)

        answer = 0.51*u.mm
        self.assertEqual(ID_colored_tube("orange-yellow"), answer)

        answer = 2.79*u.mm
        self.assertEqual(ID_colored_tube("purple-white"), answer)

    def test_C_stock_max(self):
        answer = 159.89684125188708*u.g/u.L
        self.assertEqual(C_stock_max(7*u.mL/u.s, 100*u.NTU, "yellow-blue"),
            answer)

        answer = 14.404039668326215*u.g/u.L
        self.assertEqual(C_stock_max(7*u.mL/u.s, 2*u.mg/u.L, "orange-yellow"),
            answer)

    def test_Q_stock_max(self):
        answer = 0.007442298363639224*u.mL/u.s
        self.assertEqual(Q_stock_max(7*u.mL/u.s, 100*u.NTU, "yellow-blue"),
            answer)

        answer = 0.0009719495587606109*u.mL/u.s
        self.assertEqual(Q_stock_max(7*u.mL/u.s, 2*u.mg/u.L, "orange-yellow"),
            answer)

    def test_T_stock(self):
        answer = 37.324192635827984*u.hr
        self.assertEqual(T_stock(7*u.mL/u.s, 100*u.NTU, "yellow-blue", 1*u.L),
            answer)

        answer = 285.79443786361537*u.hr
        self.assertEqual(T_stock(7*u.mL/u.s, 2*u.mg/u.L, "orange-yellow",1*u.L),
            answer)
