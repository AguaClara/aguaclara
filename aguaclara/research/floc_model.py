# -*- coding: utf-8 -*-
"""This file contains functions which can be used to model the behavior of
flocs based on the chemical interactions of clay, coagulant, and humic acid.

"""

######################### Imports #########################
import numpy as np
from aguaclara.core.units import unit_registry as u
from aguaclara.core import physchem as pc, utility as ut

u.enable_contexts('chem')

##################### Class Definition #####################


class Material:
    """A particulate material with a name, diameter, density, and
    molecular weight.
    """

    def __init__(self, name, diameter, density, molecWeight):
        """Initialize a material object.

        :param name: Name of the material
        :type name: string
        :param diameter: Diameter of the material in particulate form
        :type diameter: float
        :param density: Density of the material (mass/volume)
        :type density: float
        :param molecWeight: Molecular weight of the material (mass/mole)
        :type moleWeight: float
        """
        self.name = name
        self.Diameter = diameter
        self.Density = density
        self.MolecWeight = molecWeight


class Chemical(Material):
    """A chemical with a name, diameter, density, molecular weight, number of
    aluminum atoms per molecule, and a precipitate.
    """

    def __init__(self, name, diameter, density, molecWeight, Precipitate,
                 AluminumMPM=None):
        Material.__init__(self, name, diameter, density, molecWeight)
        self.AluminumMPM = AluminumMPM
        self.Precip = Precipitate
        if self.Precip == self.name:
            self.PrecipName = name
            self.PrecipDiameter = diameter
            self.PrecipDensity = density
            self.PrecipMolecWeight = molecWeight
            self.PrecipAluminumMPM = AluminumMPM
        else:
            self.PrecipName = Precipitate

    def define_Precip(self, diameter, density, molecweight, alumMPM):
        self.PrecipDiameter = diameter
        self.PrecipDensity = density
        self.PrecipMolecWeight = molecweight
        self.PrecipAluminumMPM = alumMPM


################## Material Definitions ##################
# name, diameter in m, density in kg/m³, molecular weight in kg/mole
Clay = Material('Clay', 7 * 10**-6 * u.m, 2650 * u.kg/u.m**3, None)
PACl = Chemical('PACl', 9 * 10 **-8 * u.m, 1138 * u.kg/u.m**3,
                 1.039 * u.kg/u.mol, 'PACl', AluminumMPM=13)
Alum = Chemical('Alum', 7 * 10 **-8 * u.m, 2420 * u.kg/u.m**3,
                0.59921 * u.kg/u.mol, 'AlOH3', AluminumMPM=2)
Alum.define_Precip(7 * 10 **-8 * u.m, 2420 * u.kg/u.m**3,
                0.078 * u.kg/u.mol, 1)
HumicAcid = Chemical('Humic Acid', 72 * 10**-9 * u.m, 1780 * u.kg/u.m**3, None,
                'Humic Acid')


################### Necessary Constants ###################
# Fractal dimension, based on data from published in Environmental Engineering
# Science, "Fractal Models for Floc Density, Sedimentation Velocity, and Floc
# Volume Fraction for High Peclet Number Reactors" by Monroe Weber-Shirk and
# Leonard Lion (2015).
DIM_FRACTAL = 2.3
# Ratio of clay platelet height to diameter.
RATIO_HEIGHT_DIAM = 0.1
# Ratio between inner viscous length scale and Kolmogorov length scale.
RATIO_KOLMOGOROV = 50
# Shape factor for drag on flocs used in terminal velocity equation.
PHI_FLOC = 45/24
# The Avogadro constant.
NUM_AVOGADRO = 6.0221415 * 10**23
# Molecular weight of aluminum in kg/mole.
MOLEC_WEIGHT_ALUMINUM = 0.027


######################## Functions ########################
@u.wraps(u.kg/u.m**3, None, False)
def dens_alum_nanocluster(coag):
    """Return the density of the aluminum in the nanocluster.

    This is useful for determining the volume of nanoclusters
    given a concentration of aluminum.
    """
    density = (coag.PrecipDensity * MOLEC_WEIGHT_ALUMINUM
               * coag.PrecipAluminumMPM / coag.PrecipMolecWeight)
    return density


@u.wraps(u.kg/u.m**3, [u.kg/u.m**3, u.degK], False)
def dens_pacl_solution(ConcAluminum, temp):
    """Return the density of the PACl solution.

    From Stock Tank Mixing report Fall 2013:
    https://confluence.cornell.edu/download/attachments/137953883/20131213_Research_Report.pdf
    """
    return ((0.492 * ConcAluminum * PACl.MolecWeight
             / (PACl.AluminumMPM * MOLEC_WEIGHT_ALUMINUM)
             ) + pc.density_water(temp).magnitude
            )


@u.wraps(u.kg/u.m**3, [u.kg/u.m**3, None], False)
def conc_precipitate(ConcAluminum, coag):
    """Return coagulant precipitate concentration given aluminum dose.

    Note that conc_precipitate returns a value that varies from the equivalent
    MathCAD function beginning at the third decimal place. The majority of
    functions below this point in the file ultimately call on conc_precipitate
    at some point, and will not return the same value as their equivalent
    function in MathCAD. This is known.
    """
    return ((ConcAluminum / MOLEC_WEIGHT_ALUMINUM)
            * (coag.PrecipMolecWeight / coag.PrecipAluminumMPM)
            )


@u.wraps(u.kg/u.m**3, [u.kg/u.m**3, u.kg/u.m**3, None], False)
def conc_floc(ConcAluminum, concClay, coag):
    """Return floc density given aluminum dose, turbidity, and coagulant"""
    return conc_precipitate(ConcAluminum, coag).magnitude + concClay


@u.wraps(u.mol/u.m**3, u.kg/u.m**3, False)
def moles_aluminum(ConcAluminum):
    """Return the # of moles aluminum given aluminum concentration."""
    return (ConcAluminum / MOLEC_WEIGHT_ALUMINUM)


@u.wraps(u.m, u.kg/u.m**3, False)
def sep_dist_aluminum(ConcAluminum):
    """Return the separation distance between aluminum molecules."""
    return (1 / (NUM_AVOGADRO * moles_aluminum(ConcAluminum).magnitude))**(1/3)


@u.wraps(1/u.m**3, [u.kg/u.m**3, u.m], False)
def num_clay(ConcClay, material):
    """Return the number of clay particles in suspension."""
    return ConcClay / ((material.Density * np.pi * material.Diameter**3) / 6)


@u.wraps(u.m, [u.kg/u.m**3, u.m], False)
def sep_dist_clay(ConcClay, material):
    """Return the separation distance between clay particles."""
    return ((material.Density/ConcClay)*((np.pi
                            * material.Diameter ** 3)/6))**(1/3)


@u.wraps(1/u.m**3, [u.kg/u.m**3, None], False)
def num_nanoclusters(ConcAluminum, coag):
    """Return the number of Aluminum nanoclusters."""
    return (ConcAluminum / (dens_alum_nanocluster(coag).magnitude
                            * np.pi * coag.Diameter**3))


@u.wraps(None, [u.kg/u.m**3, u.kg/u.m**3, None, None], False)
def frac_vol_floc_initial(ConcAluminum, ConcClay, coag, material):
    """Return the fraction of flocs initially present."""
    return ((conc_precipitate(ConcAluminum, coag).magnitude/coag.PrecipDensity)
            + (ConcClay / material.Density))


####################### p functions #######################
def p(C, Cprime):
    return -np.log10(C/Cprime)


def invp(pC, Cprime):
    return Cprime * 10**-pC


#################### Fractal functions ####################
@u.wraps(u.m, [u.dimensionless, u.m, u.dimensionless], False)
def diam_fractal(DIM_FRACTAL, DiamInitial, NumCol):
    """Return the diameter of a floc given NumCol doubling collisions."""
    return DiamInitial * 2**(NumCol / DIM_FRACTAL)


@u.wraps(None, [u.dimensionless, None, u.m], False)
def num_coll_reqd(DIM_FRACTAL, material, DiamTarget):
    """Return the number of doubling collisions required.

    Calculates the number of doubling collisions required to produce
    a floc of diameter DiamTarget.
    """
    return DIM_FRACTAL * np.log2(DiamTarget/material.Diameter)


@u.wraps(u.m, [u.kg/u.m**3, u.kg/u.m**3, None, None,
               u.dimensionless, u.m], False)
def sep_dist_floc(ConcAluminum, ConcClay, coag, material,
                  DIM_FRACTAL, DiamTarget):
    """Return separation distance as a function of floc size."""
    return (material.Diameter
            * (np.pi/(6
                      * frac_vol_floc_initial(ConcAluminum, ConcClay,
                                              coag, material)
                      ))**(1/3)
            * (DiamTarget / material.Diameter)**(DIM_FRACTAL / 3)
            )


@u.wraps(u.m, [u.kg/u.m**3, u.kg/u.m**3, None, u.dimensionless,
               None, u.m], False)
def frac_vol_floc(ConcAluminum, ConcClay, coag, DIM_FRACTAL,
                  material, DiamTarget):
    """Return the floc volume fraction."""
    return (frac_vol_floc_initial(ConcAluminum, ConcClay, coag, material)
            * (DiamTarget / material.Diameter)**(3-DIM_FRACTAL)
            )


@u.wraps(u.kg/u.m**3, [u.kg/u.m**3, u.kg/u.m**3, None, None], False)
def dens_floc_init(ConcAluminum, ConcClay, coag, material):
    """Return the density of the initial floc.

    Initial floc is made primarily of the primary colloid and nanoglobs.
    """
    return (conc_floc(ConcAluminum, ConcClay, coag).magnitude
            / frac_vol_floc_initial(ConcAluminum, ConcClay, coag, material)
            )


#################### Flocculation Model ####################
@u.wraps(None, u.m, False)
def ratio_clay_sphere(RatioHeightDiameter):
    """Return the surface area to volume ratio for clay.

    Normalized by surface area to volume ratio for a sphere.
    """
    return (1/2 + RatioHeightDiameter) * (2 / (3*RatioHeightDiameter))**(2/3)


@u.wraps(None, [u.kg/u.m**3, None, u.m, u.dimensionless], False)
def ratio_area_clay_total(ConcClay, material, DiamTube, RatioHeightDiameter):
    """Return the surface area of clay normalized by total surface area.

    Total surface area is a combination of clay and reactor wall
    surface areas. This function is used to estimate how much coagulant
    actually goes to the clay.
    """
    return (1
            / (1
               + (2 * material.Diameter
                  / (3 * DiamTube * ratio_clay_sphere(RatioHeightDiameter)
                     * (ConcClay / material.Density)
                     )
                  )
               )
            )


@u.wraps(None, [u.kg/u.m**3, u.kg/u.m**3, None, None,
                u.m, u.dimensionless], False)
def gamma_coag(ConcClay, ConcAluminum, coag, material,
               DiamTube, RatioHeightDiameter):
    """Return the coverage of clay with nanoglobs.

    This function accounts for loss to the tube flocculator walls
    and a poisson distribution on the clay given random hits by the
    nanoglobs. The poisson distribution results in the coverage only
    gradually approaching full coverage as coagulant dose increases.
    """
    return (1 - np.exp((
                       (-frac_vol_floc_initial(ConcAluminum, 0, coag, material)
                         * material.Diameter)
                        / (frac_vol_floc_initial(0, ConcClay, coag, material)
                           * coag.Diameter))
                       * (1 / np.pi)
                       * (ratio_area_clay_total(ConcClay, material,
                                                DiamTube, RatioHeightDiameter)
                          / ratio_clay_sphere(RatioHeightDiameter))
                       ))


@u.wraps(None, [u.kg/u.m**3, u.kg/u.m**3, None, None], False)
@ut.list_handler()
def gamma_humic_acid_to_coag(ConcAl, ConcNatOrgMat, NatOrgMat, coag):
    """Return the fraction of the coagulant that is coated with humic acid.

    Parameters
    ----------
    var1 : float
        Concentration of alumninum in solution
    var2 : float
        Concentration of natural organic matter in solution
    var3 : ?
    var4 : ?

    Returns
    -------
    float
        fraction of the coagulant that is coated with humic acid

    """
    return min(((ConcNatOrgMat / conc_precipitate(ConcAl, coag).magnitude)
                * (coag.Density / NatOrgMat.Density)
                * (coag.Diameter / (4 * NatOrgMat.Diameter))
                ),
               1)


@u.wraps(None, [u.m, u.kg/u.m**3, u.kg/u.m**3, u.kg/u.m**3, None,
                None, None, u.dimensionless], False)
def pacl_term(DiamTube, ConcClay, ConcAl, ConcNatOrgMat, NatOrgMat,
               coag, material, RatioHeightDiameter):
    """Return the fraction of the surface area that is covered with coagulant
    that is not covered with humic acid.

    Parameters
    ----------
    var1 : float
        Diameter of the dosing tube
    var2 : float
        Concentration of clay in solution
    var3 : float
        Concentration of alumninum in solution
    var4 : float
        Concentration of natural organic matter in solution
    var5 : ?
    var6 : ?
    var7 : float
        Ratio between inner viscous length scale and Kolmogorov length scale

    Returns
    -------
    float
        fraction of the surface area that is covered with coagulant that is not
        covered with humic acid

    """
    return (gamma_coag(ConcClay, ConcAl, coag, material, DiamTube,
                       RatioHeightDiameter)
            * (1 - gamma_humic_acid_to_coag(ConcAl, ConcNatOrgMat,
                                            NatOrgMat, coag))
            )


@u.wraps(None, [u.m, u.kg/u.m**3, u.kg/u.m**3, u.kg/u.m**3,
                None, None, None, u.dimensionless], False)
def alpha_pacl_clay(DiamTube, ConcClay, ConcAl, ConcNatOrgMat,
                    NatOrgMat, coag, material, RatioHeightDiameter):
    """"""
    PAClTerm = pacl_term(DiamTube, ConcClay, ConcAl, ConcNatOrgMat,
                          NatOrgMat, coag, material, RatioHeightDiameter)
    return 2 * (PAClTerm * (1 - gamma_coag(ConcClay, ConcAl, coag, material,
                                           DiamTube, RatioHeightDiameter)))


@u.wraps(None, [u.m, u.kg/u.m**3, u.kg/u.m**3, u.kg/u.m**3,
                None, None, None, u.dimensionless], False)
def alpha_pacl_pacl(DiamTube, ConcClay, ConcAl, ConcNatOrgMat,
                    NatOrgMat, coag, material, RatioHeightDiameter):
    """"""
    PAClTerm = pacl_term(DiamTube, ConcClay, ConcAl, ConcNatOrgMat,
                          NatOrgMat, coag, material, RatioHeightDiameter)
    return PAClTerm ** 2


@u.wraps(None, [u.m, u.kg/u.m**3, u.kg/u.m**3, u.kg/u.m**3,
                None, None, None, u.dimensionless], False)
def alpha_pacl_nat_org_mat(DiamTube, ConcClay, ConcAl, ConcNatOrgMat,
                           NatOrgMat, coag, material, RatioHeightDiameter):
    """"""
    PAClTerm = pacl_term(DiamTube, ConcClay, ConcAl, ConcNatOrgMat,
                          NatOrgMat, coag, material, RatioHeightDiameter)
    return (2 * PAClTerm
            * gamma_coag(ConcClay, ConcAl, coag, material, DiamTube,
                         RatioHeightDiameter)
            * gamma_humic_acid_to_coag(ConcAl, ConcNatOrgMat, NatOrgMat, coag))


@u.wraps(None, [u.m, u.kg/u.m**3, u.kg/u.m**3, u.kg/u.m**3,
                None, None, None, u.dimensionless], False)
def alpha(DiamTube, ConcClay, ConcAl, ConcNatOrgMat,
          NatOrgMat, coag, material, RatioHeightDiameter):
    """"""
    return (alpha_pacl_nat_org_mat(DiamTube, ConcClay, ConcAl, ConcNatOrgMat,
                                   NatOrgMat, coag, material,
                                   RatioHeightDiameter)
            + alpha_pacl_pacl(DiamTube, ConcClay, ConcAl, ConcNatOrgMat,
                              NatOrgMat, coag, material, RatioHeightDiameter)
            + alpha_pacl_clay(DiamTube, ConcClay, ConcAl, ConcNatOrgMat,
                              NatOrgMat, coag, material, RatioHeightDiameter)
            )


@u.wraps(None, [u.W/u.kg, u.degK, u.s, u.m,
                u.kg/u.m**3, u.kg/u.m**3, u.kg/u.m**3, None,
                None, None, u.dimensionless, u.dimensionless], False)
def pc_viscous(EnergyDis, Temp, Time, DiamTube,
               ConcClay, ConcAl, ConcNatOrgMat, NatOrgMat,
               coag, material, FittingParam, RatioHeightDiameter):
    """"""
    return ((3/2)
            * np.log10((2/3) * np.pi * FittingParam * Time
                       * np.sqrt(EnergyDis / (pc.viscosity_kinematic(Temp).magnitude)
                                 )
                       * alpha(DiamTube, ConcClay, ConcAl, ConcNatOrgMat,
                               NatOrgMat, coag, material, RatioHeightDiameter)
                       * (np.pi/6)**(2/3)
                       * (material.Diameter / sep_dist_clay(ConcClay, material).magnitude
                          ) ** 2
                       + 1
                       )
            )


@u.wraps(u.kg/u.m**3, [u.kg/u.m**3, u.kg/u.m**3, u.dimensionless, u.m,
                       None, None, u.degK], False)
def dens_floc(ConcAl, ConcClay, DIM_FRACTAL, DiamTarget, coag, material, Temp):
    """Calculate floc density as a function of size."""
    WaterDensity = pc.density_water(Temp).magnitude
    return ((dens_floc_init(ConcAl, ConcClay, coag, material).magnitude
             - WaterDensity
             )
            * (material.Diameter / DiamTarget)**(3 - DIM_FRACTAL)
            + WaterDensity
            )


@u.wraps(u.m/u.s, [u.kg/u.m**3, u.kg/u.m**3, None, None, u.dimensionless,
                   u.m, u.degK], False)
def vel_term_floc(ConcAl, ConcClay, coag, material, DIM_FRACTAL,
                  DiamTarget, Temp):
    """Calculate floc terminal velocity."""
    WaterDensity = pc.density_water(Temp).magnitude
    return (((pc.gravity.magnitude * material.Diameter**2)
             / (18 * PHI_FLOC * pc.viscosity_kinematic(Temp).magnitude)
             )
            * ((dens_floc_init(ConcAl, ConcClay, coag, material).magnitude
                - WaterDensity
                )
               / WaterDensity
               )
            * (DiamTarget / material.Diameter) ** (DIM_FRACTAL - 1)
            )


@u.wraps(u.m, [u.kg/u.m**3, u.kg/u.m**3, None, None,
               u.dimensionless, u.m/u.s, u.degK], False)
def diam_floc_vel_term(ConcAl, ConcClay, coag, material,
                       DIM_FRACTAL, VelTerm, Temp):
    """Calculate floc diamter as a function of terminal velocity."""
    WaterDensity = pc.density_water(Temp).magnitude
    return (material.Diameter * (((18 * VelTerm * PHI_FLOC
                          * pc.viscosity_kinematic(Temp).magnitude
                          )
                         / (pc.gravity.magnitude * material.Diameter**2)
                         )
                         * (WaterDensity
                            / (dens_floc_init(ConcAl, ConcClay, coag,
                                              material).magnitude
                               - WaterDensity
                               )
                            )
                        ) ** (1 / (DIM_FRACTAL - 1))
            )


@u.wraps(u.s, [u.W/u.kg, u.degK, u.kg/u.m**3, u.kg/u.m**3, None, None,
               u.m, u.m, u.dimensionless, u.dimensionless],
         False)
def time_col_laminar(EnergyDis, Temp, ConcAl, ConcClay, coag, material,
                     DiamTarget, DiamTube, DIM_FRACTAL, RatioHeightDiameter):
    """Calculate single collision time for laminar flow mediated collisions.

    Calculated as a function of floc size.
    """
    return (((1/6) * ((6/np.pi)**(1/3))
             * frac_vol_floc_initial(ConcAl, ConcClay, coag, material) ** (-2/3)
             * (pc.viscosity_kinematic(Temp).magnitude / EnergyDis) ** (1 / 2)
             * (DiamTarget / material.Diameter) ** (2*DIM_FRACTAL/3 - 2)
             )  # End of the numerator
            / (gamma_coag(ConcClay, ConcAl, coag, material, DiamTube,
                          RatioHeightDiameter)
               )  # End of the denominator
            )


@u.wraps(u.s, [u.W/u.kg, u.kg/u.m**3, u.kg/u.m**3, None, None,
               u.m, u.dimensionless], False)
def time_col_turbulent(EnergyDis, ConcAl, ConcClay, coag, material,
                       DiamTarget, DIM_FRACTAL):
    """Calculate single collision time for turbulent flow mediated collisions.

    Calculated as a function of floc size.
    """
    return((1/6) * (6/np.pi)**(1/9) * EnergyDis**(-1/3) * DiamTarget**(2/3)
           * frac_vol_floc_initial(ConcAl, ConcClay, coag, material)**(-8/9)
           * (DiamTarget / material.Diameter)**((8*(DIM_FRACTAL-3)) / 9)
           )


########### Kolmogorov and viscous length scales ###########
@u.wraps(u.m, [u.W/u.kg, u.degK], False)
def eta_kolmogorov(EnergyDis, Temp):
    return ((pc.viscosity_kinematic(Temp).magnitude ** 3) / EnergyDis) ** (1 / 4)


@u.wraps(u.m, [u.W/u.kg, u.degK], False)
def lambda_vel(EnergyDis, Temp):
    return RATIO_KOLMOGOROV * eta_kolmogorov(EnergyDis, Temp).magnitude


@u.wraps(u.m, [u.W/u.kg, u.degK, u.kg/u.m**3, u.kg/u.m**3, None, None,
               u.dimensionless], False)
def diam_kolmogorov(EnergyDis, Temp, ConcAl, ConcClay, coag, material,
                    DIM_FRACTAL):
    """Return the size of the floc with separation distances equal to
    the Kolmogorov length and the inner viscous length scale.
    """
    return (material.Diameter
            * ((eta_kolmogorov(EnergyDis, Temp).magnitude / material.Diameter)
               * ((6 * frac_vol_floc_initial(ConcAl, ConcClay, coag, material))
                  / np.pi
                  )**(1/3)
               )**(3 / DIM_FRACTAL)
            )


@u.wraps(u.m, [u.W/u.kg, u.degK, u.kg/u.m**3, u.kg/u.m**3, None, None,
               u.dimensionless], False)
def diam_vel(EnergyDis, Temp, ConcAl, ConcClay, coag, material, DIM_FRACTAL):
    return (material.Diameter
            * ((lambda_vel(EnergyDis, Temp).magnitude / material.Diameter)
               * ((6 * frac_vol_floc_initial(ConcAl, ConcClay, coag, material))
                  / np.pi
                  )**(1/3)
               )**(3/DIM_FRACTAL)
            )


@u.wraps(u.m, u.W/u.kg, False)
def diam_floc_max(epsMax):
    """Return floc size as a function of energy dissipation rate.

    Based on Ian Tse's work with floc size as a function of energy
    dissipation rate. This is for the average energy dissipation rate
    in a tube flocculator. It isn't clear how to convert this to the
    turbulent flow case. Maybe the flocs are mostly experiencing viscous
    shear. But that isn't clear. Some authors have made the case that
    floc breakup is due to viscous effects. If that is the case, then
    the results from the tube flocculator should be applicable to the
    turbulent case. We will have to account for the temporal and spatial
    variability in the turbulent energy dissipation rate. The factor of
    95 μm is based on the assumption that the ratio of the max to
    average energy dissipation rate for laminar flow is approximately 2.
    """
    return 9.5 * 10**-5 * (1 / (epsMax)**(1/3))


@u.wraps(u.W/u.kg, u.m, False)
def ener_dis_diam_floc(Diam):
    """Return max energy dissipation rate as a function of max floc diameter.

    This equation is under suspicion.
    """
    return (9.5 * 10**-5 / Diam) ** 3


##### Velocity gradient in tubing for lab scale laminar flow flocculators #####
@u.wraps(1/u.s, [u.m**3/u.s, u.m], False)
def g_straight(PlantFlow, IDTube):
    return 64 * PlantFlow / (3 * np.pi * IDTube**3)


@u.wraps(None, [u.m**3/u.s, u.m, u.degK], False)
def reynolds_rapid_mix(PlantFlow, IDTube, Temp):
    return (4 * PlantFlow / (np.pi * IDTube
                             * pc.viscosity_kinematic(Temp).magnitude))


@u.wraps(None, [u.m**3/u.s, u.m, u.m, u.degK], False)
def dean_number(PlantFlow, IDTube, RadiusCoil, Temp):
    """Return the Dean Number.

    The Dean Number is a dimensionless parameter that is the unfortunate
    combination of Reynolds and tube curvature. It would have been better
    to keep the Reynolds number and define a simple dimensionless geometric
    parameter.
    """
    return (reynolds_rapid_mix(PlantFlow, IDTube, Temp)
            * (IDTube / (2 * RadiusCoil))**(1/2)
            )


@u.wraps(1/u.s, [u.m**3/u.s, u.m, u.m, u.degK], False)
def g_coil(FlowPlant, IDTube, RadiusCoil, Temp):
    """We need a reference for this.

    Karen's thesis likely has this equation and the reference.
    """
    return (g_straight(FlowPlant, IDTube).magnitude
            * (1 + 0.033 *
                np.log10(dean_number(FlowPlant, IDTube, RadiusCoil, Temp)
                        ) ** 4
               ) ** (1/2)
            )


@u.wraps(u.s, [u.m, u.m, u.m**3/u.s], False)
def time_res_tube(IDTube, LengthTube, FlowPlant):
    """Calculate residence time in the flocculator."""
    return LengthTube * np.pi * (IDTube**2 / 4) / FlowPlant


@u.wraps(None, [u.m**3/u.s, u.m, u.m, u.m, u.degK], False)
def g_time_res(FlowPlant, IDTube, RadiusCoil, LengthTube, Temp):
    """G Residence Time calculated for a coiled tube flocculator."""
    return (g_coil(FlowPlant, IDTube, RadiusCoil, Temp).magnitude
            * time_res_tube(IDTube, LengthTube, FlowPlant).magnitude
            )
