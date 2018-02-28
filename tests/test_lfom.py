import unittest
import numpy as np

import pandas as pd

import matplotlib.pyplot as plt

from aide_design import physchem as pc

from aide_design import utility as ut

from aide_design import optional_inputs as opt

from aide_design import pipedatabase as pipe

from aide_design import materials_database as mat

from aide_design import constants as con

from aide_design.units import unit_registry as u

from aide_design.unit_process_design import lfom


class LfomTest(unittest.TestCase):
    def test_width_stout(self):
        """"width_stout should give known result with known input.
        Test cases were calculated using outputs from original Mathcad code.

        """
        checks = ((20 * u.cm, 1 * u.cm, 11.409 * u.s/u.m**2),
                  (40 * u.cm, 40 * u.cm, 0.902 * u.s/u.m**2))
        for i in checks:
            with self.subTest(i=i):
                self.assertEqual(lfom.width_stout(i[0], i[1]), i[2])

    def test_n_lfom_rows(self):
        """"n_lfom_rows should give known result with known input.
        Test cases were calculated using outputs from original Mathcad code.

        """
        checks = ((60 * u.L/u.s, 20 * u.cm, 4),
                  (60 * u.L/s, 40 * u.cm, 8),
                  (20 * u.L/s, 20 * u.cm, 8),
                  (1 * u.L/s, 20 * u.cm, 8),
                  (1 * u.L/s, 40 * u.cm, 8))
        for i in checks:
            with self.subTest(i=i):
                self.assertEqual(lfom.n_lfom_rows(i[0], i[1]), i[2])

    def test_dist_center_lfom_rows(self):
        """dist_center_lfom_rows should give known result with known input.
        Test cases were calculated using outputs from original Mathcad code.

        """
        checks = ((60 * u.L/u.s, 20 * u.cm, 0.05 * u.m),
                  (20 * u.L/s, 20 * u.cm, 0.025 * u.m),
                  (1 * u.L/s, 40 * u.cm, 0.05 * u.m))
        for i in checks:
            with self.subTest(i=i):
                self.assertEqual(lfom.dist_center_lfom_rows(i[0], i[1]), i[2])

    def test_vel_lfom_pipe_critical(self):
        """vel_lfom_pipe_critical should give known result with known input.
        Test cases were calculated using outputs from original Mathcad code.

        """
        checks = ((20 * u.cm, 0.841 * u.m/u.s),
                  (40 * u.cm, 1.189 * u.m/u.s))
        for i in checks:
            with self.subTest(i=i):
                self.assertEqual(lfom.vel_lfom_pipe_critical(i[0]), i[1])

    def test_area_lfom_pipe_min(self):
        """area_lfom_pipe_min should give known result with known input.
        Test cases were calculated using outputs from original Mathcad code.

        """
        checks = ((60 * u.L/u.s, 20 * u.cm, 0.107 * u.m**2),
                  (60 * u.L/u.s, 40 * u.cm, 0.076 * u.m**2),
                  (20 * u.L/u.s, 20 * u.cm, 0.036 * u.m**2),
                  (20 * u.L/u.s, 40 * u.cm, 0.025 * u.m**2))
        for i in checks:
            with self.subTest(i=i):
                self.assertEqual(lfom.area_lfom_pipe_min(i[0], i[1]), i[2])

    def test_nom_diam_lfom_pipe(self):
        """nom_diam_lfom_pipe should give known result with known input.
        Test cases were calculated using outputs from original Mathcad code and
        the nominal diameter function written in pipedatabase which has already
        been tested.

        """
        checks = ((60 * u.L/u.s, 20 * u.cm, 16.0 * u.inch),
                  (60 * u.L/u.s, 40 * u.cm, 16.0 * u.inch),
                  (20 * u.L/u.s, 20 * u.cm, 10.0 * u.inch),
                  (20 * u.L/u.s, 40 * u.cm, 8.0 * u.inch))
        for i in checks:
            with self.subTest(i=i):
                self.assertEqual(lfom.nom_diam_lfom_pipe(i[0], i[1]), i[2])

##### Below here is not finished
    def test_area_lfom_orifices_top(self):
        """area_lfom_orifices_top should give known result with known input.
        Test cases were calculated using outputs from original Mathcad code and
        the nominal diameter function written in pipedatabase which has already
        been tested.

        """
        checks = ((60 * u.L/u.s, 20 * u.cm,  * u.m**2),
                  (60 * u.L/u.s, 40 * u.cm,  * u.m**2),
                  (20 * u.L/u.s, 20 * u.cm,  * u.m**2),
                  (20 * u.L/u.s, 40 * u.cm,  * u.m**2))
        for i in checks:
            with self.subTest(i=i):
                self.assertEqual(lfom.area_lfom_orifices_top(i[0], i[1]), i[2])

    def test_d_lfom_orifices_max(self):
        """d_lfom_orifices_max should give known result with known input.
        Test cases were calculated using outputs from original Mathcad code and
        the nominal diameter function written in pipedatabase which has already
        been tested.

        """
        checks = ((60 * u.L/u.s, 20 * u.cm,  * u.m),
                  (60 * u.L/u.s, 40 * u.cm,  * u.m),
                  (20 * u.L/u.s, 20 * u.cm,  * u.m),
                  (20 * u.L/u.s, 40 * u.cm,  * u.m))
        for i in checks:
            with self.subTest(i=i):
                self.assertEqual(lfom.d_lfom_orifices_max(i[0], i[1]), i[2])

    def test_orifice_diameter(self):
        """orifice_diameter should give known result with known input.
        Test cases were calculated using outputs from original Mathcad code and
        the nominal diameter function written in pipedatabase which has already
        been tested.

        """
        checks = ((60 * u.L/u.s, 20 * u.cm, mat.DIAM_DRILL_ENG, * u.m),
                  (60 * u.L/u.s, 40 * u.cm, mat.DIAM_DRILL_ENG, * u.m),
                  (20 * u.L/u.s, 20 * u.cm, mat.DIAM_DRILL_ENG, * u.m),
                  (20 * u.L/u.s, 40 * u.cm, mat.DIAM_DRILL_ENG, * u.m))
        for i in checks:
            with self.subTest(i=i):
                self.assertEqual(lfom.orifice_diameter(i[0], i[1], i[2]), i[3])

    def test_drillbit_area(self):
        """drillbit_area should give known result with known input.
        Test cases were calculated using outputs from original Mathcad code and
        the nominal diameter function written in pipedatabase which has already
        been tested.

        """
        checks = ((60 * u.L/u.s, 20 * u.cm, mat.DIAM_DRILL_ENG, * u.m**2),
                  (60 * u.L/u.s, 40 * u.cm, mat.DIAM_DRILL_ENG, * u.m**2),
                  (20 * u.L/u.s, 20 * u.cm, mat.DIAM_DRILL_ENG, * u.m**2),
                  (20 * u.L/u.s, 40 * u.cm, mat.DIAM_DRILL_ENG, * u.m**2))
        for i in checks:
            with self.subTest(i=i):
                self.assertEqual(lfom.drillbit_area(i[0], i[1], i[2]), i[3])




    def test_orifice_diameter(self):
        FLOW = 31 * u.L / u.s
        HL_LFOM = 20 * u.cm
        drill_bits = np.arange(5, 25, 5) * u.mm
        self.assertEqual(lfom.orifice_diameter(FLOW,HL_LFOM,drill_bits), 15* u.mm)


if __name__ == '__main__':
    unittest.main()
