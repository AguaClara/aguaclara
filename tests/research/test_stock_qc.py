"""
Tests for the research package's tube_sizing module.
"""
import unittest
from aguaclara.core.units import u
import aguaclara.research.stock_qc as stock_qc

C_reactor = stock_qc.Variable_C_Stock(1*u.mL/u.s, 2*u.mg/u.L, 0.4*u.mL/u.s)
Q_reactor = stock_qc.Variable_Q_Stock(4.9*u.mL/u.s, 3.6*u.mg/u.L, 50*u.mg/u.L)


class TestStockQC(unittest.TestCase):

    def assertAlmostEqualQuantity(self, first, second, places=7):
        self.assertAlmostEqual(first.magnitude, second.magnitude, places)
        self.assertAlmostEqual(first.units, second.units, places)

    def test_init(self):
        self.assertEqual(1*u.mL/u.s, C_reactor.Q_sys())
        self.assertEqual(2*u.mg/u.L, C_reactor.C_sys())
        self.assertEqual(0.4*u.mL/u.s, C_reactor.Q_stock())

        self.assertEqual(4.9*u.mL/u.s, Q_reactor.Q_sys())
        self.assertEqual(3.6*u.mg/u.L, Q_reactor.C_sys())
        self.assertEqual(50*u.mg/u.L, Q_reactor.C_stock())

    def test_C_Stock(self):
        self.assertAlmostEqualQuantity(5.0*u.mg/u.L, C_reactor.C_stock())

    def test_Q_Stock(self):
        self.assertAlmostEqualQuantity(0.3528*u.mL/u.s, Q_reactor.Q_stock())

    def test_rpm(self):
        self.assertAlmostEqualQuantity(480*u.rev/u.min, C_reactor.rpm(0.05*u.mL/u.rev))
        self.assertAlmostEqualQuantity(88.2*u.rev/u.min, Q_reactor.rpm(0.24*u.mL/u.rev))

    def test_T_stock(self):
        self.assertAlmostEqualQuantity(3.4722222222222222*u.hr, C_reactor.T_stock(5*u.L))
        self.assertAlmostEqualQuantity(24.722852103804485*u.hr, Q_reactor.T_stock(31.4*u.L))

    def test_M_stock(self):
        self.assertAlmostEqualQuantity(25.0*u.mg, C_reactor.M_stock(5*u.L))
        self.assertAlmostEqualQuantity(1570.0*u.mg, Q_reactor.M_stock(31.4*u.L))

    def test_V_super_stock(self):
        self.assertAlmostEqualQuantity(0.00035714285714285714*u.L,
            C_reactor.V_super_stock(5*u.L, 70*u.g/u.L))
        self.assertAlmostEqualQuantity(0.028035714285714285*u.L,
            Q_reactor.V_super_stock(31.4*u.L, 56*u.g/u.L))

    def test_dilution_factor(self):
        self.assertEqual(7.142857142857142e-05*u.dimensionless, C_reactor.dilution_factor(70*u.g/u.L))
        self.assertEqual(0.0008928571428571429*u.dimensionless, Q_reactor.dilution_factor(56*u.g/u.L))
