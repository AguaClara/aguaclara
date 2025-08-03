import unittest
import aguaclara.core.head_loss as k
from aguaclara.core.units import u
from aguaclara.core import pipes as pipe

""" There are still many cases to test."""


class KValuesCalculationTest(unittest.TestCase):

    def assertAlmostEqualQuantity(self, first, second, places=7):
        self.assertAlmostEqual(first.magnitude, second.magnitude, places)
        self.assertEqual(first.units, second.units, places)

    # Test Reductions
    def test_k_value_reduction_square_turbulent(self):
        self.assertAlmostEqualQuantity(
            k.k_value_reduction(
                pipe.OD(4 * u.inch), pipe.OD(2 * u.inch), 4 * u.L / u.s
            ),
            5.689246477984541 * u.dimensionless,
        )

    def test_k_value_reduction_laminar(self):
        self.assertAlmostEqualQuantity(
            k.k_value_reduction(
                pipe.OD(1 * u.inch), pipe.OD(0.5 * u.inch), 0.1 * u.L / u.s
            ),
            2.2100363820127233 * u.dimensionless,
        )

    def test_k_value_reduction_from_very_large_pipe_turbulent(self):
        self.assertAlmostEqualQuantity(
            k.k_value_reduction(
                pipe.OD(400 * u.inch), pipe.OD(4 * u.inch), 4 * u.L / u.s
            ),
            222469.482 * u.dimensionless,
            2,
        )

    # Test Expansions
    def test_k_value_expansion_into_large_tank(self):
        self.assertAlmostEqualQuantity(
            k.k_value_expansion(
                pipe.OD(4 * u.inch), pipe.OD(400 * u.inch), 4 * u.L / u.s
            ),
            1.0148940670855733 * u.dimensionless,
        )

    def test_k_value_expansion_into_very_large_pipe_laminar(self):
        self.assertAlmostEqualQuantity(
            k.k_value_expansion(
                pipe.OD(1 * u.inch), pipe.OD(400 * u.inch), 0.1 * u.L / u.s
            ),
            1.9999999165201428 * u.dimensionless,
        )

    # Test Orifices

    # Test private functions
    def test_k_value_thick_orifice_high_headloss(self):
        self.assertAlmostEqual(
            k._k_value_thick_orifice(0.02, 0.002, 0.000002, 2), 1594340.3320537778
        )

    def test_k_value_thin_orifice_high_headloss(self):
        self.assertAlmostEqual(
            k._k_value_thin_sharp_orifice(0.02, 0.002, 2), 1594433.5406999998
        )

    # Test public function
    def test_k_value_thin_orifice_regular_high_headloss(self):
        self.assertAlmostEqualQuantity(
            k.k_value_orifice(0.02 * u.m, 0.002 * u.m, 0 * u.m, 1 * u.L / u.s),
            1697.9866773221295 * u.dimensionless,
        )

    def test_k_value_super_thick_orifice_high_headloss(self):
        self.assertAlmostEqualQuantity(
            k.k_value_orifice(
                pipe.OD(6 * u.inch), pipe.OD(4 * u.inch), 60 * u.inch, 1 * u.L / u.s
            ),
            1.8577290828680884 * u.dimensionless,
        )

    def test_k_value_thin_orifice(self):
        self.assertAlmostEqualQuantity(
            k.k_value_orifice(
                pipe.OD(6 * u.inch), pipe.OD(4 * u.inch), 0 * u.inch, 1 * u.L / u.s
            ),
            3.3497584836648246 * u.dimensionless,
        )

    def test_k_value_thick_orifice(self):
        self.assertAlmostEqualQuantity(
            k.k_value_orifice(
                pipe.OD(6 * u.inch), pipe.OD(4 * u.inch), 1 * u.inch, 1 * u.L / u.s
            ),
            2.9070736824641181 * u.dimensionless,
        )


if __name__ == "__main__":
    unittest.main()
