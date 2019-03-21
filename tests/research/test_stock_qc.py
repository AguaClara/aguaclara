"""
Tests for the research package's tube_sizing module.
"""
import sys
sys.path.append("../../aguaclara/research")
from stock_qc import *

import unittest
from aguaclara.core.units import unit_registry as u

#from aguaclara.research.stock_qc import *

class TestStockQC(unittest.TestCase):

    def test_init(self):
        reactor = Variable_C_Stock(1*u.mL/u.s, 2*u.g/u.L, 0.3*u.mL/u.s)
        self.assertEqual(1*u.mL/u.s, reactor.Q_sys)
        self.assertEqual(2*u.g/u.L, reactor.C_sys)
        self.assertEqual(0.3*u.mL/u.s, reactor.Q_stock)

    # def test_C_Stock:
    #     self.assertEqual(reactor.Q_sys * reactor.
    #
    # def test_T_stock(self):
    #     answer = 37.324192635827984*u.hr
    #     self.assertEqual(reactor.T_stock(7*u.mL/u.s, 100*u.NTU, "yellow-blue", 1*u.L),
    #         answer)
    #
    #     answer = 285.79443786361537*u.hr
    #     self.assertEqual(reactor.T_stock(7*u.mL/u.s, 2*u.mg/u.L, "orange-yellow",1*u.L),
    #         answer)
