import unittest
import aide_design.k_value_of_reductions_utility as k
from aide_design.units import unit_registry as u
from aide_design import pipedatabase as pipe


class KValuesCalculationTest(unittest.TestCase):
    def test_k_value_reduction_square_turbulent(self):
        self.assertEqual(k._k_value_square_reduction(pipe.OD(4), pipe.OD(2), 4 * u.L/u.s), 5.6326628388227808)

    def test_k_value_reduction_laminar(self):
        self.assertEqual(k._k_value_square_reduction(pipe.OD(1), pipe.OD(0.5), 0.1 * u.L / u.s), 2.1647707937770533)

    def test_k_value_reduction_into_very_large_pipe_turbulent(self):
        self.assertEqual(k._k_value_square_reduction(pipe.OD(4), pipe.OD(400), 4 * u.L / u.s), -0.0014458413192567554)

    def test_k_value_reduction_into_very_large_pipe_laminar(self):
        self.assertEqual(k.k_value_reduction(pipe.OD(1), pipe.OD(400), 0.1 * u.L / u.s), -0.00012437233513637997)

    def test_k_value_reduction_from_very_large_pipe_turbulent(self):
        self.assertEqual(k.k_value_reduction(pipe.OD(400), pipe.OD(4), 4 * u.L / u.s), 106269.32639872356)

    def test_k_value_tapered_reduction_turbulent(self):
        self.assertEqual(k.k_value_reduction(pipe.OD(4), pipe.OD(2), 4 * u.L/u.s), 5.6326628388227808)

if __name__ == '__main__':
    unittest.main()
