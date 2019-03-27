"""
Tests for the research package's tube_sizing module.
"""
import unittest
from aguaclara.core.units import unit_registry as u

developing = True
if developing:
    import sys
    sys.path.append("../../aguaclara/research")
    import stock_qc as stock_qc
else:
    import aguaclara.research.stock_qc as stock_qc

C_reactor = stock_qc.Variable_C_Stock(1*u.mL/u.s, 2*u.mg/u.L, 0.4*u.mL/u.s)


class TestStockQC(unittest.TestCase):

    def assertAlmostEqualQuantity(self, first, second, places=7):
        self.assertAlmostEqual(first.magnitude, second.magnitude, places)
        self.assertAlmostEqual(first.units, second.units, places)

    def test_init(self):
        self.assertEqual(1*u.mL/u.s, C_reactor.Q_sys())
        self.assertEqual(2*u.mg/u.L, C_reactor.C_sys())
        self.assertEqual(0.4*u.mL/u.s, C_reactor.Q_stock())

    def test_C_Stock(self):
        self.assertEqual(5.0*u.mg/u.L, C_reactor.C_stock())

    def test_rpm(self):
        self.assertEqual(480*u.rev/u.min, C_reactor.rpm(0.05*u.mL/u.rev))

    def test_T_stock(self):
        self.assertAlmostEqualQuantity(3.47222222*u.hr, C_reactor.T_stock(5*u.L))

    def test_M_stock(self):
        self.assertEqual(25.0*u.mg, C_reactor.M_stock(5*u.L))

    def test_V_super_stock(self):
        self.assertAlmostEqualQuantity(0.00035714285714285714*u.L,
            C_reactor.V_super_stock(5*u.L, 70*u.g/u.L))

    def test_dilution_factor(self):
        self.assertEqual(7.142857142857142e-05*u.dimensionless, C_reactor.dilution_factor(70*u.g/u.L))
