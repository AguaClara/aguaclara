# -*- coding: utf-8 -*-
"""This file contains functions which can be used to model the behavior of
flocs based on the chemical interactions of clay, coagulant, and humic acid.
"""

######################### Imports #########################
import numpy as np
from aguaclara.core.units import u
from aguaclara.core import physchem as pc, utility as ut

u.enable_contexts('chem')

##################### Class Definition #####################


class Material:
    """A particulate material with a name, diameter, density, and
    molecular weight.
    """

    def __init__(self, name, diameter, density, molecWeight):
        """Initialize a Material object.

        :param name: Name of the material
        :type name: string
        :param diameter: Diameter of the material in particulate form
        :type diameter: float
        :param density: Density of the material (mass/volume)
        :type density: float
        :param molecWeight: Molecular weight of the material (mass/mole)
        :type molecWeight: float
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
        """Initialize a Chemical object.

        :param name: Name of the material
        :type name: string
        :param diameter: Diameter of the material in particulate form
        :type diameter: length
        :param density: Density of the material
        :type density: mass/length**3
        :param molecWeight: Molecular weight of the material
        :type molecWeight: mass/mole
        :param Precipitate: Name of the precipitate
        :type Precipitate: string
        :param AluminumMPM: aluminum atoms per molecule
        :type AluminumMPM: int
        """
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
        """Define a precipitate for the chemical.

        :param diameter: Diameter of the precipitate in particulate form
        :type diameter: float
        :param density: Density of the material (mass/volume)
        :type density: float
        :param molecWeight: Molecular weight of the material (mass/mole)
        :type molecWeight: float
        :param alumMPM: aluminum atoms per molecule
        :type alumMPM: int
        """
        self.PrecipDiameter = diameter
        self.PrecipDensity = density
        self.PrecipMolecWeight = molecweight
        self.PrecipAluminumMPM = alumMPM


################## Material Definitions ##################

#: A Material representing clay with a diameter of 7e-6 m and density of 2650
#: kg/m^3.
Clay = Material('Clay', 7 * 10**-6 * u.m, 2650 * u.kg/u.m**3, None)

#: A Material representing polyaluminum chloride (PACl) with a diameter of
#: 9e-8m, density of 1138 kg/m^2, and molecular weight of 1.039 kg/mol. It is
#: its own precipitate.
PACl = Chemical('PACl', 9 * 10 **-8 * u.m, 1138 * u.kg/u.m**3,
                1.039 * u.kg/u.mol, 'PACl', AluminumMPM=13)

#: A Material representing alum with a diameter of 7e-8 m, density of
#: 2420 kg/m^3, and molecular weight of 0.59921 kg/mol. It's precipitate is
#: AlOH3, with the same diameter and density, and a molecular weight of 0.078
#: kg/mol.
Alum = Chemical('Alum', 7 * 10 **-8 * u.m, 2420 * u.kg/u.m**3,
                0.59921 * u.kg/u.mol, 'AlOH3', AluminumMPM=2)
Alum.define_Precip(7 * 10 **-8 * u.m, 2420 * u.kg/u.m**3,
                   0.078 * u.kg/u.mol, 1)

#: A Material representing humic acid with a diameter of 7.2e-8 m and density
#: of 1780 kg/m^3. It is its own precipitate.
HumicAcid = Chemical('Humic Acid', 72 * 10**-9 * u.m, 1780 * u.kg/u.m**3, None,
                     'Humic Acid')


################### Necessary Constants ###################
#: Fractal dimension, based on data from published in Environmental Engineering
#: Science, "Fractal Models for Floc Density, Sedimentation Velocity, and Floc
#: Volume Fraction for High Peclet Number Reactors" by Monroe Weber-Shirk and
#: Leonard Lion (2015).
DIM_FRACTAL = 2.3

#: Ratio of clay platelet height to diameter.
RATIO_HEIGHT_DIAM = 0.1

#: Ratio between inner viscous length scale and Kolmogorov length scale.
RATIO_KOLMOGOROV = 50

#: Shape factor for drag on flocs used in terminal velocity equation.
PHI_FLOC = 45/24

#: The Avogadro constant.
NUM_AVOGADRO = 6.0221415 * 10**23

#: Molecular weight of aluminum in kg/mole.
MOLEC_WEIGHT_ALUMINUM = 0.027 * u.kg / u.mol


######################## Functions ########################
# @u.wraps(u.kg/u.m**3, None, False)
@ut.list_handler()
def dens_alum_nanocluster(coag):
    """Return the density of the aluminum in the nanocluster.

    This is useful for determining the volume of nanoclusters
    given a concentration of aluminum.
    """
    density = (coag.PrecipDensity * MOLEC_WEIGHT_ALUMINUM
               * coag.PrecipAluminumMPM / coag.PrecipMolecWeight)
    return density.to(u.kg/u.m**3)


# @u.wraps(u.kg/u.m**3, [u.kg/u.m**3, u.degK], False)
@ut.list_handler()
def dens_pacl_solution(ConcAluminum, temp):
    """Return the density of the PACl solution.

    From Stock Tank Mixing report Fall 2013:
    https://confluence.cornell.edu/download/attachments/137953883/20131213_Research_Report.pdf
    """
    return ((0.492 * ConcAluminum * PACl.MolecWeight
             / (PACl.AluminumMPM * MOLEC_WEIGHT_ALUMINUM)
             ) + pc.density_water(temp)
            ).to(u.kg/u.m**3)


@ut.list_handler()
def conc_precipitate(ConcAluminum, coag):
    """Return coagulant precipitate concentration given aluminum dose.

    This function assumes complete precipitation of coagulant into Al13.

    Note that conc_precipitate returns a value that varies from the equivalent
    MathCAD function beginning at the third decimal place. The majority of
    functions below this point in the file ultimately call on conc_precipitate
    at some point, and will not return the same value as their equivalent
    function in MathCAD. This is known.

    :param ConcAluminum: Concentration of aluminum in solution
    :type ConcAluminum: float
    :param coag: Type of coagulant in solution, e.g. floc_model.PACl
    :type coag: floc_model.Material

    :return: Concentration of coagulant precipitates
    :rtype: float
    """
    return ((ConcAluminum / MOLEC_WEIGHT_ALUMINUM)
            * (coag.PrecipMolecWeight / coag.PrecipAluminumMPM)
            ).to(u.kg/u.m**3)


# @u.wraps(u.kg/u.m**3, [u.kg/u.m**3, u.kg/u.m**3, None], False)
@ut.list_handler()
def conc_floc(ConcAluminum, concClay, coag):
    """Return floc density given aluminum dose, turbidity, and coagulant"""
    return (conc_precipitate(ConcAluminum, coag) + concClay).to(u.kg/u.m**3)


# @u.wraps(u.mol/u.m**3, u.kg/u.m**3, False)
@ut.list_handler()
def moles_aluminum(ConcAluminum):
    """Return the # of moles aluminum given aluminum concentration."""
    return (ConcAluminum / MOLEC_WEIGHT_ALUMINUM).to(u.mol/u.m**3)


# @u.wraps(u.m, u.kg/u.m**3, False)
@ut.list_handler()
def sep_dist_aluminum(ConcAluminum):
    """Return the separation distance between aluminum molecules."""
    return ((1 / (NUM_AVOGADRO / u.mol * moles_aluminum(ConcAluminum)))**(1/3)).to(u.m)


@ut.list_handler()
def particle_number_concentration(ConcMat, material):
    """Return the number of particles in suspension.

    :param ConcMat: Concentration of the material
    :type ConcMat: float
    :param material: The material in solution
    :type material: floc_model.Material
    """
    return (ConcMat / ((material.Density * np.pi * material.Diameter**3) / 6)).to(u.m**-3)


# @u.wraps(u.m, [u.kg/u.m**3, u.m], False)
@ut.list_handler()
def sep_dist_clay(ConcClay, material):
    """Return the separation distance between clay particles."""
    return (((material.Density/ConcClay)
             * ((np.pi * material.Diameter ** 3) / 6)) ** (1 / 3)).to(u.m)


# @u.wraps(1/u.m**3, [u.kg/u.m**3, None], False)
@ut.list_handler()
def num_nanoclusters(ConcAluminum, coag):
    """Return the number of Aluminum nanoclusters."""
    return (ConcAluminum / (dens_alum_nanocluster(coag)
                            * np.pi * coag.Diameter**3)).to(1/u.m**3)


@ut.list_handler()
def frac_vol_floc_initial(ConcAluminum, ConcClay, coag, material):
    """Return the volume fraction of flocs initially present, accounting for both suspended particles and coagulant precipitates.

    :param ConcAluminum: Concentration of aluminum in solution
    :type ConcAluminum: float
    :param ConcClay: Concentration of particle in suspension
    :type ConcClay: float
    :param coag: Type of coagulant in solution
    :type coag: float
    :param material: Type of particles in suspension, e.g. floc_model.Clay
    :type material: floc_model.Material

    :return: Volume fraction of particles initially present
    :rtype: float
    """
    return ((conc_precipitate(ConcAluminum, coag)/coag.PrecipDensity)
            + (ConcClay / material.Density)).to(u.dimensionless)


####################### p functions #######################
@ut.list_handler()
def p(C, C0=1):
    return -np.log10(C/C0)


@ut.list_handler()
def invp(pC, C0=1):
    return C0 * 10**-pC


#################### Fractal functions ####################
# @u.wraps(u.m, [u.dimensionless, u.m, u.dimensionless], False)
@ut.list_handler()
def diam_fractal(DIM_FRACTAL, DiamInitial, NumCol):
    """Return the diameter of a floc given NumCol doubling collisions."""
    return (DiamInitial * 2**(NumCol / DIM_FRACTAL)).to(u.m)


# @u.wraps(None, [u.dimensionless, None, u.m], False)
@ut.list_handler()
def num_coll_reqd(DIM_FRACTAL, material, DiamTarget):
    """Return the number of doubling collisions required.

    Calculates the number of doubling collisions required to produce
    a floc of diameter DiamTarget.
    """
    return (DIM_FRACTAL * np.log(DiamTarget/material.Diameter)/np.log(2)).to(u.dimensionless)


# @u.wraps(u.m, [u.kg/u.m**3, u.kg/u.m**3, None, None,
               # u.dimensionless, u.m], False)
@ut.list_handler()
def sep_dist_floc(ConcAluminum, ConcClay, coag, material,
                  DIM_FRACTAL, DiamTarget):
    """Return separation distance as a function of floc size."""
    return (material.Diameter
            * (np.pi/(6
                      * frac_vol_floc_initial(ConcAluminum, ConcClay,
                                              coag, material)
                      ))**(1/3)
            * (DiamTarget / material.Diameter)**(DIM_FRACTAL / 3)
            ).to(u.m)


# @u.wraps(u.m, [u.kg/u.m**3, u.kg/u.m**3, None, u.dimensionless,
#                None, u.m], False)
@ut.list_handler()
def frac_vol_floc(ConcAluminum, ConcClay, coag, DIM_FRACTAL,
                  material, DiamTarget):
    """Return the floc volume fraction."""
    return (frac_vol_floc_initial(ConcAluminum, ConcClay, coag, material)
            * (DiamTarget / material.Diameter)**(3-DIM_FRACTAL)
            ).to(u.dimensionless)


# @u.wraps(u.kg/u.m**3, [u.kg/u.m**3, u.kg/u.m**3, None, None], False)
@ut.list_handler()
def dens_floc_init(ConcAluminum, ConcClay, coag, material):
    """Return the density of the initial floc.

    Initial floc is made primarily of the primary colloid and nanoglobs.
    """
    return (conc_floc(ConcAluminum, ConcClay, coag)
            / frac_vol_floc_initial(ConcAluminum, ConcClay, coag, material)
            ).to(u.kg/u.m**3)


#################### Flocculation Model ####################
# @u.wraps(None, u.m, False)
@ut.list_handler()
def ratio_clay_sphere(RatioHeightDiameter):
    """Return the surface area to volume ratio for clay.

    Normalized by surface area to volume ratio for a sphere.
    """
    return ((1/2 + RatioHeightDiameter) * (2 / (3*RatioHeightDiameter))**(2/3))*u.dimensionless


@ut.list_handler()
def ratio_area_clay_total(ConcClay, material, DiamTube, RatioHeightDiameter):
    """Return the surface area of clay normalized by total surface area.

    Total surface area is a combination of clay and reactor wall
    surface areas. This function is used to estimate how much coagulant
    actually goes to the clay.

    :param ConcClay: Concentration of clay in suspension
    :type ConcClay: float
    :param material: Type of clay in suspension, e.g. floc_model.Clay
    :type material: floc_model.Material
    :param DiamTube: Diameter of flocculator tube (assumes tube flocculator for calculation of reactor surface area)
    :type DiamTube: float
    :param RatioHeightDiameter: Dimensionless ratio describing ratio of clay height to clay diameter
    :type RatioHeightDiameter: float

    :return: The ratio of clay surface area to total available surface area (accounting for reactor walls)
    :rtype: float
    """
    return (1
            / (1
               + (2 * material.Diameter
                  / (3 * DiamTube * ratio_clay_sphere(RatioHeightDiameter)
                     * (ConcClay / material.Density)
                     )
                  )
               )
            ).to(u.dimensionless)


@ut.list_handler()
def gamma_coag(ConcClay, ConcAluminum, coag, material,
               DiamTube, RatioHeightDiameter):
    """Return the coverage of clay with nanoglobs.

    This function accounts for loss to the tube flocculator walls
    and a poisson distribution on the clay given random hits by the
    nanoglobs. The poisson distribution results in the coverage only
    gradually approaching full coverage as coagulant dose increases.

    :param ConcClay: Concentration of clay in suspension
    :type ConcClay: float
    :param ConcAluminum: Concentration of aluminum in solution
    :type ConcAluminum: float
    :param coag: Type of coagulant in solution, e.g. floc_model.PACl
    :type coag: floc_model.Material
    :param material: Type of clay in suspension, e.g. floc_model.Clay
    :type material: floc_model.Material
    :param DiamTube: Diameter of flocculator tube (assumes tube flocculator for calculation of reactor surface area)
    :type DiamTube: float
    :param RatioHeightDiameter: Dimensionless ratio of clay height to clay diameter
    :type RatioHeightDiameter: float

    :return: Fraction of the clay surface area that is coated with coagulant precipitates
    :rtype: float
    """
    return (1 - np.exp((
                       (-frac_vol_floc_initial(ConcAluminum, 0*u.kg/u.m**3, coag, material)
                        * material.Diameter)
                        / (frac_vol_floc_initial(0*u.kg/u.m**3, ConcClay, coag, material)
                           * coag.Diameter))
                       * (1 / np.pi)
                       * (ratio_area_clay_total(ConcClay, material,
                                                DiamTube, RatioHeightDiameter)
                          / ratio_clay_sphere(RatioHeightDiameter))
                       )).to(u.dimensionless)


# @u.wraps(None, [u.kg/u.m**3, u.kg/u.m**3, None, None], False)
@ut.list_handler()
def gamma_humic_acid_to_coag(ConcAl, ConcNatOrgMat, NatOrgMat, coag):
    """Return the fraction of the coagulant that is coated with humic acid.

    :param ConcAl: Concentration of alumninum in solution
    :type ConcAl: float
    :param ConcNatOrgMat: Concentration of natural organic matter in solution
    :type ConcNatOrgMat: float
    :param NatOrgMat: type of natural organic matter, e.g. floc_model.HumicAcid
    :type NatOrgMat: floc_model.Material
    :param coag: Type of coagulant in solution, e.g. floc_model.PACl
    :type coag: floc_model.Material

    :return: fraction of the coagulant that is coated with humic acid
    :rtype: float
    """
    return (min(((ConcNatOrgMat / conc_precipitate(ConcAl, coag))
                 * (coag.Density / NatOrgMat.Density)
                 * (coag.Diameter / (4 * NatOrgMat.Diameter))
                 ),
                1*u.dimensionless)).to(u.dimensionless)


# @u.wraps(None, [u.m, u.kg/u.m**3, u.kg/u.m**3, u.kg/u.m**3, None,
#                 None, None, u.dimensionless], False)
@ut.list_handler()
def pacl_term(DiamTube, ConcClay, ConcAl, ConcNatOrgMat, NatOrgMat,
              coag, material, RatioHeightDiameter):
    """Return the fraction of the surface area that is covered with coagulant
    that is not covered with humic acid.

    :param DiamTube: Diameter of the dosing tube
    :type Diamtube: float
    :param ConcClay: Concentration of clay in solution
    :type ConcClay: float
    :param ConcAl: Concentration of alumninum in solution
    :type ConcAl: float
    :param ConcNatOrgMat: Concentration of natural organic matter in solution
    :type ConcNatOrgMat: float
    :param NatOrgMat: type of natural organic matter, e.g. floc_model.HumicAcid
    :type NatOrgMat: floc_model.Material
    :param coag: Type of coagulant in solution, e.g. floc_model.PACl
    :type coag: floc_model.Material
    :param material: Type of clay in suspension, e.g. floc_model.Clay
    :type material: floc_model.Material
    :param RatioHeightDiameter: Dimensionless ratio of clay height to clay diameter
    :type RatioHeightDiameter: float

    :return: fraction of the surface area that is covered with coagulant that is not covered with humic acid
    :rtype: float
    """
    return (gamma_coag(ConcClay, ConcAl, coag, material, DiamTube,
                       RatioHeightDiameter)
            * (1 - gamma_humic_acid_to_coag(ConcAl, ConcNatOrgMat,
                                            NatOrgMat, coag))
            ).to(u.dimensionless)


# @u.wraps(None, [u.m, u.kg/u.m**3, u.kg/u.m**3, u.kg/u.m**3,
#                 None, None, None, u.dimensionless], False)
@ut.list_handler()
def alpha_pacl_clay(DiamTube, ConcClay, ConcAl, ConcNatOrgMat,
                    NatOrgMat, coag, material, RatioHeightDiameter):
    """"""
    PAClTerm = pacl_term(DiamTube, ConcClay, ConcAl, ConcNatOrgMat,
                         NatOrgMat, coag, material, RatioHeightDiameter)
    return (2 * (PAClTerm * (1 - gamma_coag(ConcClay, ConcAl, coag, material,
                                            DiamTube, RatioHeightDiameter)))).to(u.dimensionless)


# @u.wraps(None, [u.m, u.kg/u.m**3, u.kg/u.m**3, u.kg/u.m**3,
#                 None, None, None, u.dimensionless], False)
@ut.list_handler()
def alpha_pacl_pacl(DiamTube, ConcClay, ConcAl, ConcNatOrgMat,
                    NatOrgMat, coag, material, RatioHeightDiameter):
    """"""
    PAClTerm = pacl_term(DiamTube, ConcClay, ConcAl, ConcNatOrgMat,
                         NatOrgMat, coag, material, RatioHeightDiameter)
    return PAClTerm ** 2


# @u.wraps(None, [u.m, u.kg/u.m**3, u.kg/u.m**3, u.kg/u.m**3,
#                 None, None, None, u.dimensionless], False)
@ut.list_handler()
def alpha_pacl_nat_org_mat(DiamTube, ConcClay, ConcAl, ConcNatOrgMat,
                           NatOrgMat, coag, material, RatioHeightDiameter):
    """"""
    PAClTerm = pacl_term(DiamTube, ConcClay, ConcAl, ConcNatOrgMat,
                         NatOrgMat, coag, material, RatioHeightDiameter)
    return (2 * PAClTerm
            * gamma_coag(ConcClay, ConcAl, coag, material, DiamTube,
                         RatioHeightDiameter)
            * gamma_humic_acid_to_coag(ConcAl, ConcNatOrgMat, NatOrgMat, coag)).to(u.dimensionless)


# @u.wraps(None, [u.m, u.kg/u.m**3, u.kg/u.m**3, u.kg/u.m**3,
#                 None, None, None, u.dimensionless], False)
@ut.list_handler()
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
            ).to(u.dimensionless)


# @u.wraps(None, [u.W/u.kg, u.degK, u.s, u.m,
#                 u.kg/u.m**3, u.kg/u.m**3, u.kg/u.m**3, None,
#                 None, None, u.dimensionless, u.dimensionless], False)
@ut.list_handler()
def pc_viscous(EnergyDis, Temp, Time, DiamTube,
               ConcClay, ConcAl, ConcNatOrgMat, NatOrgMat,
               coag, material, FittingParam, RatioHeightDiameter):
    """"""
    return ((3/2)
            * np.log10((2/3) * np.pi * FittingParam * Time
                       * np.sqrt(EnergyDis / (pc.viscosity_kinematic_water(Temp))
                                 )
                       * alpha(DiamTube, ConcClay, ConcAl, ConcNatOrgMat,
                               NatOrgMat, coag, material, RatioHeightDiameter)
                       * (np.pi/6)**(2/3)
                       * (material.Diameter / sep_dist_clay(ConcClay, material)
                          ) ** 2
                       + 1
                       ) * u.dimensionless
            ).to(u.dimensionless)


# @u.wraps(u.kg/u.m**3, [u.kg/u.m**3, u.kg/u.m**3, u.dimensionless, u.m,
#                        None, None, u.degK], False)
@ut.list_handler()
def dens_floc(ConcAl, ConcClay, DIM_FRACTAL, DiamTarget, coag, material, Temp):
    """Calculate floc density as a function of size."""
    WaterDensity = pc.density_water(Temp)
    return ((dens_floc_init(ConcAl, ConcClay, coag, material)
             - WaterDensity
             )
            * (material.Diameter / DiamTarget)**(3 - DIM_FRACTAL)
            + WaterDensity
            ).to(u.kg/u.m**3)


# @u.wraps(u.m/u.s, [u.kg/u.m**3, u.kg/u.m**3, None, None, u.dimensionless,
#                    u.m, u.degK], False)
@ut.list_handler()
def vel_term_floc(ConcAl, ConcClay, coag, material, DIM_FRACTAL,
                  DiamTarget, Temp):
    """Calculate floc terminal velocity."""
    WaterDensity = pc.density_water(Temp)
    return (((u.gravity * material.Diameter**2)
             / (18 * PHI_FLOC * pc.viscosity_kinematic_water(Temp))
             )
            * ((dens_floc_init(ConcAl, ConcClay, coag, material)
                - WaterDensity
                )
               / WaterDensity
               )
            * (DiamTarget / material.Diameter) ** (DIM_FRACTAL - 1)
            ).to(u.m/u.s)


# @u.wraps(u.m, [u.kg/u.m**3, u.kg/u.m**3, None, None,
#                u.dimensionless, u.m/u.s, u.degK], False)
@ut.list_handler()
def diam_floc_vel_term(ConcAl, ConcClay, coag, material,
                       DIM_FRACTAL, VelTerm, Temp):
    """Calculate floc diamter as a function of terminal velocity."""
    WaterDensity = pc.density_water(Temp)
    return (material.Diameter * (((18 * VelTerm * PHI_FLOC
                                   * pc.viscosity_kinematic_water(Temp)
                                   )
                                  / (u.gravity * material.Diameter**2)
                                  )
                                 * (WaterDensity
                                    / (dens_floc_init(ConcAl, ConcClay, coag,
                                                      material)
                                       - WaterDensity
                                       )
                                    )
                                 ) ** (1 / (DIM_FRACTAL - 1))
            ).to(u.m)


# @u.wraps(u.s, [u.W/u.kg, u.degK, u.kg/u.m**3, u.kg/u.m**3, None, None,
#                u.m, u.m, u.dimensionless, u.dimensionless],
#          False)
@ut.list_handler()
def time_col_laminar(EnergyDis, Temp, ConcAl, ConcClay, coag, material,
                     DiamTarget, DiamTube, DIM_FRACTAL, RatioHeightDiameter):
    """Calculate single collision time for laminar flow mediated collisions.

    Calculated as a function of floc size.
    """
    return (((1/6) * ((6/np.pi)**(1/3))
             * frac_vol_floc_initial(ConcAl, ConcClay, coag, material) ** (-2/3)
             * (pc.viscosity_kinematic_water(Temp) / EnergyDis) ** (1 / 2)
             * (DiamTarget / material.Diameter) ** (2*DIM_FRACTAL/3 - 2)
             )  # End of the numerator
            / (gamma_coag(ConcClay, ConcAl, coag, material, DiamTube,
                          RatioHeightDiameter)
               )  # End of the denominator
            ).to(u.s)


# @u.wraps(u.s, [u.W/u.kg, u.kg/u.m**3, u.kg/u.m**3, None, None,
#                u.m, u.dimensionless], False)
@ut.list_handler()
def time_col_turbulent(EnergyDis, ConcAl, ConcClay, coag, material,
                       DiamTarget, DIM_FRACTAL):
    """Calculate single collision time for turbulent flow mediated collisions.

    Calculated as a function of floc size.
    """
    return((1/6) * (6/np.pi)**(1/9) * EnergyDis**(-1/3) * DiamTarget**(2/3)
           * frac_vol_floc_initial(ConcAl, ConcClay, coag, material)**(-8/9)
           * (DiamTarget / material.Diameter)**((8*(DIM_FRACTAL-3)) / 9)
           ).to(u.s)


########### Kolmogorov and viscous length scales ###########

# @u.wraps(u.m, [u.W/u.kg, u.degK], False)
@ut.list_handler()
def eta_kolmogorov(EnergyDis, Temp):
    return (((pc.viscosity_kinematic_water(Temp) ** 3) / EnergyDis) ** (1 / 4)).to(u.m)


# @u.wraps(u.m, [u.W/u.kg, u.degK], False)
@ut.list_handler()
def lambda_vel(EnergyDis, Temp):
    return (RATIO_KOLMOGOROV * eta_kolmogorov(EnergyDis, Temp)).to(u.m)


# @u.wraps(u.m, [u.W/u.kg, u.degK, u.kg/u.m**3, u.kg/u.m**3, None, None,
#                u.dimensionless], False)
@ut.list_handler()
def diam_kolmogorov(EnergyDis, Temp, ConcAl, ConcClay, coag, material,
                    DIM_FRACTAL):
    """Return the size of the floc with separation distances equal to
    the Kolmogorov length and the inner viscous length scale.
    """
    return (material.Diameter
            * ((eta_kolmogorov(EnergyDis, Temp) / material.Diameter)
               * ((6 * frac_vol_floc_initial(ConcAl, ConcClay, coag, material))
                  / np.pi
                  )**(1/3)
               )**(3 / DIM_FRACTAL)
            ).to(u.m)


# @u.wraps(u.m, [u.W/u.kg, u.degK, u.kg/u.m**3, u.kg/u.m**3, None, None,
#                u.dimensionless], False)
@ut.list_handler()
def diam_vel(EnergyDis, Temp, ConcAl, ConcClay, coag, material, DIM_FRACTAL):
    return (material.Diameter
            * ((lambda_vel(EnergyDis, Temp) / material.Diameter)
               * ((6 * frac_vol_floc_initial(ConcAl, ConcClay, coag, material))
                  / np.pi
                  )**(1/3)
               )**(3/DIM_FRACTAL)
            ).to(u.m)


# @u.wraps(u.m, u.W/u.kg, False)
@ut.list_handler()
def diam_floc_max(epsMax):
    """
    .. deprecated:: 0.1.13
        diam_floc_max is deprecated and will be removed after Dec 1 2019. The
        underlying equation is under suspicion.

    Return floc size as a function of energy dissipation rate.

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
    # return (9.5 * 10**-5 * (1 / (epsMax)**(1/3))).to(u.m)
    raise FutureWarning("diam_floc_max is deprecated and will be removed after Dec"
                    " 1 2019. The underlying equation is under suspicion.")


# @u.wraps(u.W/u.kg, u.m, False)
@ut.list_handler()
def ener_dis_diam_floc(Diam):
    """
    .. deprecated:: 0.1.13
        ener_dis_diam_floc is deprecated and will be removed after Dec 1 2019.
        The underlying equation is under suspicion.

    Return max energy dissipation rate as a function of max floc diameter.
    """
    # return ((9.5 * 10**-5 / Diam) ** 3).to(u.W/u.kg)
    raise FutureWarning("ener_dis_diam_floc is deprecated and will be removed"
                        " after Dec 1 2019. The underlying equation is under"
                        " suspicion.")

##### Velocity gradient in tubing for lab scale laminar flow flocculators #####

# @u.wraps(1/u.s, [u.m**3/u.s, u.m], False)
@ut.list_handler()
def g_straight(PlantFlow, IDTube):
    return (64 * PlantFlow / (3 * np.pi * IDTube**3)).to(1/u.s)


# @u.wraps(None, [u.m**3/u.s, u.m, u.degK], False)
@ut.list_handler()
def reynolds_rapid_mix(PlantFlow, IDTube, Temp):
    return (4 * PlantFlow / (np.pi * IDTube
                             * pc.viscosity_kinematic_water(Temp))).to(u.dimensionless)


# @u.wraps(None, [u.m**3/u.s, u.m, u.m, u.degK], False)
@ut.list_handler()
def dean_number(PlantFlow, IDTube, RadiusCoil, Temp):
    """Return the Dean Number.

    The Dean Number is a dimensionless parameter that is the unfortunate
    combination of Reynolds and tube curvature. It would have been better
    to keep the Reynolds number and define a simple dimensionless geometric
    parameter.
    """
    return (reynolds_rapid_mix(PlantFlow, IDTube, Temp)
            * (IDTube / (2 * RadiusCoil))**(1/2)
            ).to(u.dimensionless)


# @u.wraps(1/u.s, [u.m**3/u.s, u.m, u.m, u.degK], False)
@ut.list_handler()
def g_coil(FlowPlant, IDTube, RadiusCoil, Temp):
    """We need a reference for this.

    Karen's thesis likely has this equation and the reference.
    """
    return (g_straight(FlowPlant, IDTube)
            * (1 + 0.033 *
                np.log10(dean_number(FlowPlant, IDTube, RadiusCoil, Temp)
                        ) ** 4
               ) ** (1/2)
            ).to(1/u.s)


# @u.wraps(u.s, [u.m, u.m, u.m**3/u.s], False)
@ut.list_handler()
def time_res_tube(IDTube, LengthTube, FlowPlant):
    """Calculate residence time in the flocculator."""
    return (LengthTube * np.pi * (IDTube**2 / 4) / FlowPlant).to(u.s)


# @u.wraps(None, [u.m**3/u.s, u.m, u.m, u.m, u.degK], False)
@ut.list_handler()
def g_time_res(FlowPlant, IDTube, RadiusCoil, LengthTube, Temp):
    """G Residence Time calculated for a coiled tube flocculator."""
    return (g_coil(FlowPlant, IDTube, RadiusCoil, Temp)
            * time_res_tube(IDTube, LengthTube, FlowPlant)
            ).to(u.dimensionless)
