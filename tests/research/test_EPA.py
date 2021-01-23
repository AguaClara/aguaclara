'''''
research tests.
'''''

import unittest
import aguaclara.research.environmental_processes_analysis as epa
from aguaclara.core.units import u
import numpy as np


class TestEPA(unittest.TestCase):
    '''''
    Test research's Environmental_Processes_Analysis
    '''''
    def assertAlmostEqualSequence(self, a, b, places=7):
        for elt_a, elt_b in zip(a, b):
            self.assertAlmostEqual(elt_a, elt_b, places)

    def test_Hplus_concentration_from_pH(self):
        '''''
        Test function that converts pH to molarity of H+
        '''''
        output = epa.invpH(8.25)
        self.assertEqual(output, 5.623413251903491e-09*u.mol/u.L)

        output = epa.invpH(10)
        self.assertEqual(output, 1e-10*u.mol/u.L)

    def test_E_Advective_Dispersion(self):
        output = epa.E_Advective_Dispersion(0.5, 5)
        self.assertAlmostEqual(output, 0.4774864115)

        output = epa.E_Advective_Dispersion(0, 5)
        self.assertAlmostEqual(output, 0)

        output = epa.E_Advective_Dispersion(np.array([0, 0.5, 1, 1.5, 2]), 5)
        answer = np.array([0, 0.477486411, 0.630783130, 0.418173418, 0.238743205])
        self.assertAlmostEqualSequence(output, answer)
