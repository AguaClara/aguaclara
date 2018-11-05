import unittest
import aguaclara.core.head_loss as k
from aguaclara.core.units import unit_registry as u
from aguaclara.core import pipes as pipe

""" There are still many cases to test."""


class KValuesCalculationTest(unittest.TestCase):

    # Test Reductions
    def test_k_value_reduction_square_turbulent(self):
        self.assertAlmostEqual(k.k_value_reduction(pipe.OD(4), pipe.OD(2), 4 * u.L / u.s), 5.6677039356929662)

    def test_k_value_reduction_laminar(self):
        self.assertAlmostEqual(k.k_value_reduction(pipe.OD(1), pipe.OD(0.5), 0.1 * u.L / u.s), 2.1802730749680945)

    def test_k_value_reduction_from_very_large_pipe_turbulent(self):
        self.assertAlmostEqual(k.k_value_reduction(pipe.OD(400), pipe.OD(4), 4 * u.L / u.s), 105560.31724275621)

    # Test Expansions
    def test_k_value_expansion_into_large_tank(self):
        self.assertAlmostEqual(k.k_value_expansion(pipe.OD(4), pipe.OD(400), 4 * u.L / u.s), 1.0110511331493719)

    def test_k_value_expansion_into_very_large_pipe_laminar(self):
        self.assertAlmostEqual(k.k_value_expansion(pipe.OD(1), pipe.OD(400), 0.1 * u.L / u.s), 1.0216612503304363)

    # Test Orifices

    # Test private functions
    def test_k_value_thick_orifice_high_headloss(self):
        self.assertAlmostEqual(k._k_value_thick_orifice(0.02, 0.002, 0.000002, 2), 1594340.3320537778)

    def test_k_value_thin_orifice_high_headloss(self):
        self.assertAlmostEqual(k._k_value_thin_sharp_orifice(0.02, 0.002, 2), 1594433.5406999998)

    # Test public function
    def test_k_value_thin_orifice_regular_high_headloss(self):
        self.assertAlmostEqual(k.k_value_orifice(0.02 * u.m, 0.002 * u.m, 0 * u.m, 1*u.L/u.s), 1697.9866773221295)

    # def test_k_value_super_thick_orifice_high_headloss(self):
    #     self.assertAlmostEqual(k.k_value_orifice(pipe.OD(6), pipe.OD(4), 60*u.inch, 1 * u.L / u.s), 1.8350488368427034)

    def test_k_value_thin_orifice(self):
        self.assertAlmostEqual(k.k_value_orifice(pipe.OD(6), pipe.OD(4), 0*u.inch, 1 * u.L / u.s), 3.3497584836648246)

    def test_k_value_thick_orifice(self):
        self.assertAlmostEqual(k.k_value_orifice(pipe.OD(6), pipe.OD(4), 1*u.inch, 1 * u.L / u.s),
                         2.9070736824641181)


if __name__ == '__main__':
    unittest.main()
