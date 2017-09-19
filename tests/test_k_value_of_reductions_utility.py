import unittest
import aide_design.pipe_utility as pipe
from aide_design.units import unit_registry as u


class KValuesCalculationTest(unittest.TestCase):
    def test_k_value_square_reduction(self):
        self.assertEqual(pipe.k_value_square_reduction(pipe.OD(4), pipe.OD(2), 4 * u.L/u.s), 5)


if __name__ == '__main__':
    unittest.main()
