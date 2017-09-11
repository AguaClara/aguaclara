import unittest
import numpy as np

import pandas as pd

import matplotlib.pyplot as plt

from aide_design import physchem as pc

from aide_design import expert_inputs as exp

from aide_design import utility as ut

from aide_design.units import unit_registry as u

from aide_design.unit_process_design.prefab import lfom_prefab_functional as lfom


class LfomTest(unittest.TestCase):
    def test_orifice_diameter(self):
        FLOW = 31 * u.L / u.s
        HL_LFOM = 20 * u.cm
        drill_bits = np.arange(5, 25, 5) * u.mm
        self.assertEqual(lfom.orifice_diameter(FLOW,HL_LFOM,drill_bits), 15* u.mm)


if __name__ == '__main__':
    unittest.main()
