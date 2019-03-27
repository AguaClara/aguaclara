"""
Tests for the research package's tube_sizing module.
"""
import sys
sys.path.append("../../aguaclara/research")
from stock_qc import *

import unittest
from aguaclara.core.units import unit_registry as u

#from aguaclara.research.stock_qc import *
reactor = Variable_C_Stock(1*u.mL/u.s, 2*u.g/u.L, 0.4*u.mL/u.s)

class TestStockQC(unittest.TestCase):


    def test_init(self):
        #reactor = Variable_C_Stock(1*u.mL/u.s, 2*u.g/u.L, 0.3*u.mL/u.s)
        self.assertEqual(1*u.mL/u.s, reactor._Q_sys)
        self.assertEqual(2*u.g/u.L, reactor._C_sys)
        self.assertEqual(0.4*u.mL/u.s, reactor._Q_stock)

    def test_C_Stock(self):
        self.assertEqual(5.0*u.g/u.L, reactor.C_stock())

    def test_rpm(self):
        self.assertEqual(480*u.rev/u.min, reactor.rpm(0.05*u.mL/u.rev))

    def test_Q_stock(self):
        self.assertEqual(0.4*u.mL/u.s, reactor.Q_stock())

    def test_T_stock(self):
        self.assertAlmostEqual(3.4722222222222, reactor.T_stock(5*u.L).magnitude)
        self.assertEqual((1*u.hr).units, reactor.T_stock(5*u.L).units)

    def test_M_stock(self):
        self.assertEqual(25.0*u.g, reactor.M_stock(5*u.L))

    def test_V_super_stock(self):
        self.assertEqual(1, reactor.V_super_stock(5, self._C_stock))

    def dilution_factor(self):
        self.assertEqual(2.5, reactor.dilution_factor(self.C_stock(), 2))


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
