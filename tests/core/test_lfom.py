import unittest
import numpy as np

from aguaclara.core import materials_database as mat

from aguaclara.core.units import unit_registry as u

from aguaclara.unit_process_design import lfom


class LfomTest(unittest.TestCase):
    def test_width_stout(self):
        """"width_stout should give known result with known input.
        Test cases were calculated using outputs from original Mathcad code.

        """
        checks = ((20 * u.cm, 1 * u.cm, 11.408649616179787 * u.s/u.m**2),
                  (40 * u.cm, 40 * u.cm, 0.9019329453483474 * u.s/u.m**2))
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqual(lfom.width_stout(i[0], i[1]), i[2], places=3)

    def test_n_lfom_rows(self):
        """"n_rows should give known result with known input.
        Test cases were calculated using outputs from original Mathcad code.

        """
        checks = ((60 * u.L/u.s, 20 * u.cm, 4),
                  (60 * u.L/u.s, 40 * u.cm, 8),
                  (20 * u.L/u.s, 20 * u.cm, 8),
                  (1 * u.L/u.s, 20 * u.cm, 8),
                  (1 * u.L/u.s, 40 * u.cm, 8))
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqual(lfom.n_lfom_rows(i[0], i[1]), i[2])

    def test_dist_center_lfom_rows(self):
        """b_rows should give known result with known input.
        Test cases were calculated using outputs from original Mathcad code.

        """
        checks = ((60 * u.L/u.s, 20 * u.cm, 0.05 * u.m),
                  (20 * u.L/u.s, 20 * u.cm, 0.025 * u.m),
                  (1 * u.L/u.s, 40 * u.cm, 0.05 * u.m))
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqual(lfom.dist_center_lfom_rows(i[0], i[1]), i[2])

    def test_vel_lfom_pipe_critical(self):
        """vel_critical should give known result with known input.
        Test cases were calculated using outputs from original Mathcad code.

        """
        checks = ((20 * u.cm, 0.8405802802312778 * u.m/u.s),
                  (40 * u.cm, 1.18876003256645 * u.m/u.s))
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqual(lfom.vel_lfom_pipe_critical(i[0]), i[1])

    def test_area_lfom_pipe_min(self):
        """area_lfom_pipe_min should give known result with known input.
        Test cases were calculated using outputs from original Mathcad code.

        """
        checks = ((60 * u.L/u.s, 20 * u.cm, 0.10706889290245702 * u.m**2),
                  (60 * u.L/u.s, 40 * u.cm, 0.07570914022546356 * u.m**2),
                  (20 * u.L/u.s, 20 * u.cm, 0.035689630967485675 * u.m**2),
                  (20 * u.L/u.s, 40 * u.cm, 0.02523638007515452 * u.m**2))
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqual(lfom.area_lfom_pipe_min(i[0], i[1]), i[2])

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
                self.assertAlmostEqual(lfom.nom_diam_lfom_pipe(i[0], i[1]), i[2])

##### Below here is not finished
    def test_area_lfom_orifices_top(self):
        """area_lfom_orifices_top should give known result with known input.
        Test cases were calculated using outputs from original Mathcad code and
        the nominal diameter function written in pipedatabase which has already
        been tested.

        """
        checks = ((60 * u.L/u.s, 20 * u.cm, 0.008181566649077958 * u.m**2),
                  (60 * u.L/u.s, 40 * u.cm, 0.0027945370213839633 * u.m**2),
                  (20 * u.L/u.s, 20 * u.cm, 0.0013173573853983045 * u.m**2),
                  (20 * u.L/u.s, 40 * u.cm, 0.0009315123404613211 * u.m**2))
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqual(lfom.area_lfom_orifices_top(i[0], i[1]), i[2])

    def test_d_lfom_orifices_max(self):
        """d_lfom_orifices_max should give known result with known input.
        Test cases were calculated using outputs from original Mathcad code and
        the nominal diameter function written in pipedatabase which has already
        been tested.

        """
        checks = ((60 * u.L/u.s, 20 * u.cm,  0.10206416704942245* u.m),
                  (60 * u.L/u.s, 40 * u.cm,  0.05964993750920847* u.m),
                  (20 * u.L/u.s, 20 * u.cm,  0.04095499380586013* u.m),
                  (20 * u.L/u.s, 40 * u.cm,  0.03443890747808586* u.m))
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqual(lfom.d_lfom_orifices_max(i[0], i[1]), i[2])

    def test_orifice_diameter(self):
        """orifice_diameter should give known result with known input.
        Test cases were calculated using outputs from original Mathcad code and
        the nominal diameter function written in pipedatabase which has already
        been tested.

        """
        checks = ((60 * u.L/u.s, 20 * u.cm, mat.DIAM_DRILL_ENG, 1* u.m),
                  (60 * u.L/u.s, 40 * u.cm, mat.DIAM_DRILL_ENG, 1* u.m),
                  (20 * u.L/u.s, 20 * u.cm, mat.DIAM_DRILL_ENG, 1* u.m),
                  (20 * u.L/u.s, 40 * u.cm, mat.DIAM_DRILL_ENG, 1* u.m))
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqual(lfom.orifice_diameter(i[0], i[1], i[2]), i[3])

    def test_drillbit_area(self):
        """drillbit_area should give known result with known input.
        Test cases were calculated using outputs from original Mathcad code and
        the nominal diameter function written in pipedatabase which has already
        been tested.

        """
        checks = ((60 * u.L/u.s, 20 * u.cm, mat.DIAM_DRILL_ENG, 0.0007669903939428206 * u.m**2),
                  (60 * u.L/u.s, 40 * u.cm, mat.DIAM_DRILL_ENG, 0.0007669903939428206 * u.m**2),
                  (20 * u.L/u.s, 20 * u.cm, mat.DIAM_DRILL_ENG, 3.141592653589793 * u.m**2),
                  (20 * u.L/u.s, 40 * u.cm, mat.DIAM_DRILL_ENG, 0.0007669903939428206 * u.m**2))
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqual(lfom.drillbit_area(i[0], i[1], i[2]), i[3])




    def test_orifice_diameter(self):
        FLOW = 31 * u.L / u.s
        HL_LFOM = 20 * u.cm
        drill_bits = np.arange(5, 25, 5) * u.mm
        self.assertAlmostEqual(lfom.orifice_diameter(FLOW,HL_LFOM,drill_bits), 0.7874015748031495* u.m)


if __name__ == '__main__':
    unittest.main()
