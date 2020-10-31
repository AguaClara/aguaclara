"""
Tests for the research package's floc_model functions
"""

import unittest
from aguaclara.core.units import u
import aguaclara.research.floc_model as fm


class QuantityTest(unittest.TestCase):

    def assertAlmostEqualQuantity(self, first, second, places=7):
        self.assertAlmostEqual(first.magnitude, second.magnitude, places)
        self.assertEqual(first.units, second.units, places)


class TestMaterials(QuantityTest):

    def test_Material(self):
        self.assertEqual(fm.Clay.name, 'Clay')
        self.assertEqual(fm.Clay.Diameter, 7 * 10**-6 * u.m)
        self.assertEqual(fm.Clay.Density, 2650 * u.kg/u.m**3)
        self.assertEqual(fm.Clay.MolecWeight, None)

    def test_Chemical(self):
        self.assertEqual(fm.PACl.name, 'PACl')
        self.assertEqual(fm.PACl.Diameter, 9 * 10 **-8 * u.m)
        self.assertEqual(fm.PACl.Density, 1138 * u.kg/u.m**3)
        self.assertEqual(fm.PACl.MolecWeight, 1.039 * u.kg/u.mol)
        self.assertEqual(fm.PACl.AluminumMPM, 13)
        self.assertEqual(fm.PACl.Precip, 'PACl')
        self.assertEqual(fm.PACl.PrecipName, 'PACl')
        self.assertEqual(fm.PACl.PrecipDiameter, 9 * 10 **-8 * u.m)
        self.assertEqual(fm.PACl.PrecipDensity, 1138 * u.kg/u.m**3)
        self.assertEqual(fm.PACl.PrecipMolecWeight, 1.039 * u.kg/u.mol)
        self.assertEqual(fm.PACl.PrecipAluminumMPM, 13)

        self.assertEqual(fm.Alum.name, 'Alum')
        self.assertEqual(fm.Alum.Diameter, 7 * 10 **-8 * u.m)
        self.assertEqual(fm.Alum.Density, 2420 * u.kg/u.m**3)
        self.assertEqual(fm.Alum.MolecWeight, 0.59921 * u.kg/u.mol)
        self.assertEqual(fm.Alum.AluminumMPM, 2)
        self.assertEqual(fm.Alum.Precip, 'AlOH3')
        self.assertEqual(fm.Alum.PrecipName, 'AlOH3')
        self.assertEqual(fm.Alum.PrecipDiameter, 7 * 10 **-8 * u.m)
        self.assertEqual(fm.Alum.PrecipDensity, 2420 * u.kg/u.m**3)
        self.assertEqual(fm.Alum.PrecipMolecWeight, 0.078 * u.kg/u.mol)
        self.assertEqual(fm.Alum.PrecipAluminumMPM, 1)

        self.assertEqual(fm.HumicAcid.name, 'Humic Acid')
        self.assertEqual(fm.HumicAcid.Diameter, 72 * 10**-9 * u.m)
        self.assertEqual(fm.HumicAcid.Density, 1780 * u.kg/u.m**3)
        self.assertEqual(fm.HumicAcid.MolecWeight, None)
        self.assertEqual(fm.HumicAcid.Precip, 'Humic Acid')
        self.assertEqual(fm.HumicAcid.AluminumMPM, None)
        self.assertEqual(fm.HumicAcid.Precip, 'Humic Acid')
        self.assertEqual(fm.HumicAcid.PrecipName, 'Humic Acid')
        self.assertEqual(fm.HumicAcid.PrecipDiameter, 72 * 10**-9 * u.m)
        self.assertEqual(fm.HumicAcid.PrecipDensity, 1780 * u.kg/u.m**3)
        self.assertEqual(fm.HumicAcid.PrecipMolecWeight, None)
        self.assertEqual(fm.HumicAcid.PrecipAluminumMPM, None)


class TestFunctions(QuantityTest):

    def test_dens_alum_nanocluster(self):
        self.assertAlmostEqualQuantity(fm.dens_alum_nanocluster(fm.PACl),
                                       384.44465833*u.kg/u.m**3)

    def test_dens_pacl_solution(self):
        self.assertAlmostEqualQuantity(fm.dens_pacl_solution(0.5*u.g/u.L, 298*u.degK),
                                       997.84564733*u.kg/u.m**3)

    def test_conc_precipitate(self):
        self.assertAlmostEqualQuantity(fm.conc_precipitate(0.5*u.g/u.L, fm.PACl),
                                       1.48005698*u.kg/u.m**3)

    def test_conc_floc(self):
        self.assertAlmostEqualQuantity(fm.conc_floc(0.5*u.g/u.L, 10*u.g/u.L, fm.PACl),
                                       11.48005698*u.kg/u.m**3)

    def test_moles_aluminum(self):
        self.assertAlmostEqualQuantity(fm.moles_aluminum(0.45*u.g/u.L),
                                       16.66666667*u.mol/u.m**3)

    def test_sep_dist_alumimum(self):
        self.assertAlmostEqualQuantity(fm.sep_dist_aluminum(0.45*u.g/u.L),
                                       4.63589330e-9 * u.m, 16)

    def test_particle_number_concentration(self):
        self.assertAlmostEqualQuantity(fm.particle_number_concentration(10*u.g/u.L, fm.Clay) / 10**5,
                                       21011709303102/u.m**3 / 10**5, 0)

    def test_sep_dist_clay(self):
        self.assertAlmostEqualQuantity(fm.sep_dist_clay(10*u.g/u.L, fm.Clay),
                                       3.62392782e-5 * u.m, 12)

    def test_num_nanoclusters(self):
        self.assertAlmostEqualQuantity(fm.num_nanoclusters(0.7*u.g/u.L, fm.PACl) / 10**17,
                                       7.95036025e17 / 10**17 / u.m**3)

    def test_frac_vol_floc_initial(self):
        self.assertAlmostEqualQuantity(fm.frac_vol_floc_initial(0.5*u.g/u.L, 10*u.g/u.L, fm.PACl, fm.Clay),
                                       0.005074162217*u.dimensionless, 10)


class TestPFunctions(QuantityTest):

    def test_p(self):
        self.assertAlmostEqual(fm.p(100, 0.1), -3)

    def test_invp(self):
        self.assertAlmostEqual(fm.invp(-3, 0.1), 100)


class TestFractalFunctions(QuantityTest):

    def diam_fractal(self):
        self.assertAlmostEqualQuantity(fm.diam_fractal(fm.DIM_FRACTAL, 5e-5*u.m, 10),
                                       0.00101811321*u.m, 9)

    def test_num_coll_reqd(self):
        self.assertAlmostEqualQuantity(fm.num_coll_reqd(fm.DIM_FRACTAL, fm.Clay, 0.001*u.m),
                                       16.464387532*u.dimensionless)

    def test_sep_dist_floc(self):
        self.assertAlmostEqualQuantity(fm.sep_dist_floc(0.5*u.g/u.L, 10*u.g/u.L, fm.PACl, fm.Clay, fm.DIM_FRACTAL, 0.001*u.m),
                                       0.001473672461*u.m, 9)

    def test_frac_vol_floc(self):
        self.assertAlmostEqualQuantity(fm.frac_vol_floc(0.5*u.g/u.L, 10*u.g/u.L, fm.PACl, fm.DIM_FRACTAL,  fm.Clay, 0.001*u.m),
                                       0.1636046786*u.dimensionless)

    def test_dens_floc_init(self):
        self.assertAlmostEqualQuantity(fm.dens_floc_init(0.5*u.g/u.L, 10*u.g/u.L, fm.PACl, fm.Clay) / 10**3,
                                       2.2624536798e3 / 10**3 * u.kg/u.m**3)


class TestFlocculationModel(QuantityTest):

    def test_ratio_clay_sphere(self):
        self.assertAlmostEqualQuantity(fm.ratio_clay_sphere(1.5),
                                       1.164773953*u.dimensionless)

    def test_ratio_area_clay_total(self):
        self.assertAlmostEqualQuantity(fm.ratio_area_clay_total(10*u.g/u.L, fm.Clay, 0.0254*u.m, 1.5),
                                       0.9598770465*u.dimensionless)

    def test_gamma_coag(self):
        self.assertAlmostEqualQuantity(fm.gamma_coag(10*u.g/u.L, 0.5*u.g/u.L, fm.PACl, fm.Clay, 0.025*u.m, 1.5),
                                       0.999112596*u.dimensionless, 5)

    def test_gamma_humic_acid_to_coag(self):
        self.assertAlmostEqualQuantity(fm.gamma_humic_acid_to_coag(0.5*u.g/u.L, 1.5*u.g/u.L, fm.HumicAcid, fm.PACl),
                                       0.2024813861*u.dimensionless)

    def test_pacl_term(self):
        self.assertAlmostEqualQuantity(fm.pacl_term(0.025*u.m, 10*u.g/u.L, 0.5*u.g/u.L, 1.5*u.g/u.L, fm.HumicAcid, fm.PACl, fm.Clay, 1.5),
                                       0.7968108928*u.dimensionless)

    def test_alpha_pacl_clay(self):
        self.assertAlmostEqualQuantity(fm.alpha_pacl_clay(0.025*u.m, 10*u.g/u.L, 0.5*u.g/u.L, 1.5*u.g/u.L, fm.HumicAcid, fm.PACl, fm.Clay, 1.5),
                                       0.001414186281*u.dimensionless)

    def test_alpha_pacl_pacl(self):
        self.assertAlmostEqualQuantity(fm.alpha_pacl_pacl(0.025*u.m, 10*u.g/u.L, 0.5*u.g/u.L, 1.5*u.g/u.L, fm.HumicAcid, fm.PACl, fm.Clay, 1.5),
                                       0.6349075988*u.dimensionless)

    def test_alpha_pacl_nat_org_mat(self):
        self.assertAlmostEqualQuantity(fm.alpha_pacl_nat_org_mat(0.025*u.m, 10*u.g/u.L, 0.5*u.g/u.L, 1.5*u.g/u.L, fm.HumicAcid, fm.PACl, fm.Clay, 1.5),
                                       0.3223924016*u.dimensionless)

    def test_alpha(self):
        self.assertAlmostEqualQuantity(fm.alpha(0.025*u.m, 10*u.g/u.L, 0.5*u.g/u.L, 1.5*u.g/u.L, fm.HumicAcid, fm.PACl, fm.Clay, 1.5),
                                       0.9587141867*u.dimensionless)

    def test_pc_viscous(self):
        self.assertAlmostEqualQuantity(fm.pc_viscous(1*u.W/u.kg, 298*u.degK, 1*u.s, 0.025*u.m, 10*u.g/u.L, 0.5*u.g/u.L, 1.5*u.g/u.L, fm.HumicAcid, fm.PACl, fm.Clay, 1, 1.5),
                                       2.579165715*u.dimensionless)

    def test_dens_floc(self):
        self.assertAlmostEqualQuantity(fm.dens_floc(0.5*u.g/u.L, 10*u.g/u.L, fm.DIM_FRACTAL, 0.001*u.m, fm.PACl, fm.Clay, 298*u.degK),
                                       1036.3615768605*u.kg/u.m**3)

    def test_vel_term_floc(self):
        self.assertAlmostEqualQuantity(fm.vel_term_floc(0.5*u.g/u.L, 10*u.g/u.L, fm.PACl, fm.Clay, fm.DIM_FRACTAL, 0.001*u.m, 298*u.degK),
                                       0.01276232413*u.m/u.s)

    def test_diam_floc_vel_term(self):
        self.assertAlmostEqualQuantity(fm.diam_floc_vel_term(0.5*u.g/u.L, 10*u.g/u.L, fm.PACl, fm.Clay, 2.3, 0.05*u.m/u.s, 298*u.degK),
                                       0.002858806728*u.m, 9)

    def test_time_col_laminar(self):
        self.assertAlmostEqualQuantity(fm.time_col_laminar(1*u.W/u.kg, 298*u.degK, 0.5*u.g/u.L, 10*u.g/u.L, fm.PACl, fm.Clay, 0.001*u.m, 0.025*u.m, fm.DIM_FRACTAL, 1.5),
                                       0.00065495327*u.s)

    def test_time_col_turbulent(self):
        self.assertAlmostEqualQuantity(fm.time_col_turbulent(1*u.W/u.kg, 0.5*u.g/u.L, 10*u.g/u.L, fm.PACl, fm.Clay, 0.001*u.m, fm.DIM_FRACTAL),
                                       0.00895198559*u.s)


class TestKolmogorovAndViscous(QuantityTest):

    def test_eta_kolmogorov(self):
        self.assertAlmostEqualQuantity(fm.eta_kolmogorov(2*u.W/u.kg, 298*u.degK),
                                       2.44907189e-5*u.m)

    def test_lambda_vel(self):
        self.assertAlmostEqualQuantity(fm.lambda_vel(2*u.W/u.kg, 298*u.degK),
                                       0.0012245359*u.m)

    def test_diam_kolmogorov(self):
        self.assertAlmostEqualQuantity(fm.diam_kolmogorov(2*u.W/u.kg, 298*u.degK, 0.5*u.g/u.L, 10*u.g/u.L, fm.PACl, fm.Clay, fm.DIM_FRACTAL),
                                       4.77577893e-6*u.m)

    def test_diam_vel(self):
        self.assertAlmostEqualQuantity(fm.diam_vel(2*u.W/u.kg, 298*u.degK, 0.5*u.g/u.L, 10*u.g/u.L, fm.PACl, fm.Clay, fm.DIM_FRACTAL),
                                       0.00078540208*u.m, 10)

    def test_diam_floc_max(self):
        self.assertRaisesRegex(FutureWarning, "diam_floc_max is deprecated and will be removed after Dec 1 2019. The underlying equation is under suspicion.")

    def test_ener_dis_diam_floc(self):
        self.assertRaisesRegex(FutureWarning, "ener_dis_diam_floc is deprecated and will be removed after Dec 1 2019. The underlying equation is under suspicion.")


class TestVelocityGradient(QuantityTest):

    def test_g_straight(self):
        self.assertAlmostEqualQuantity(fm.g_straight(1*u.mL/u.s, 0.025*u.m),
                                       0.43459910/u.s)

    def test_reynolds_rapid_mix(self):
        self.assertAlmostEqualQuantity(fm.reynolds_rapid_mix(1*u.mL/u.s, 0.025*u.m, 298*u.degK),
                                       56.83616083*u.dimensionless)

    def test_dean_number(self):
        self.assertAlmostEqualQuantity(fm.dean_number(1*u.mL/u.s, 0.025*u.m, 0.1*u.m, 298*u.degK),
                                       20.09461737*u.dimensionless)

    def test_g_coil(self):
        self.assertAlmostEqualQuantity(fm.g_coil(1*u.mL/u.s, 0.025*u.m, 0.1*u.m, 298*u.degK),
                                       0.45480492/u.s)

    def test_time_res_tube(self):
        self.assertAlmostEqualQuantity(fm.time_res_tube(0.025*u.m, 2*u.m, 1*u.mL/u.s),
                                       981.74770424*u.s)

    def test_g_time_res(self):
        self.assertAlmostEqualQuantity(fm.g_time_res(1*u.mL/u.s, 0.025*u.m, 0.1*u.m, 2*u.m, 298*u.degK),
                                       446.50368346*u.dimensionless)
