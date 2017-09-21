import unittest
import aide_design.k_value_of_reductions_utility as k
from aide_design.units import unit_registry as u
from aide_design import pipedatabase as pipe

""" There are still many cases to test."""


class KValuesCalculationTest(unittest.TestCase):

    # Test Reductions
    def test_k_value_reduction_square_turbulent(self):
        self.assertEqual(k.k_value_reduction(pipe.OD(4), pipe.OD(2), 4 * u.L/u.s), 5.6326628388227808)

    def test_k_value_reduction_laminar(self):
        self.assertEqual(k.k_value_reduction(pipe.OD(1), pipe.OD(0.5), 0.1 * u.L / u.s), 2.1647707937770533)

    def test_k_value_reduction_from_very_large_pipe_turbulent(self):
        self.assertEqual(k.k_value_reduction(pipe.OD(400), pipe.OD(4), 4 * u.L / u.s), 106269.32639872356)

    def test_k_value_tapered_reduction_turbulent(self):
        self.assertEqual(k.k_value_reduction(pipe.OD(4), pipe.OD(2), 4 * u.L/u.s), 5.6326628388227808)

    # Test Expansions
    def test_k_value_expansion_into_large_tank(self):
        self.assertEqual(k.k_value_expansion(pipe.OD(4), pipe.OD(400), 4 * u.L / u.s), 1.0048002172406769)

    def test_k_value_expansion_into_very_large_pipe_laminar(self):
        self.assertEqual(k.k_value_expansion(pipe.OD(1), pipe.OD(400), 0.1 * u.L / u.s), 1.0143969859745399)

if __name__ == '__main__':
    unittest.main()
