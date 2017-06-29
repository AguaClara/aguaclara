# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 16:50:46 2017

@author: Sage Weber-Shirk

Last revised: Wed Jun 28 2017
By: Sage Weber-Shirk
"""

######################### Imports #########################
import numpy as np

from AguaClara_design import physchem as pc
from AguaClara_design.units import unit_registry as u
from AguaClara_design import utility as ut

u.enable_contexts('chem')

##################### Class Definition #####################

class Chemical:
    def __init__(self, name, diameter, density, molecWeight, alumMPM, Precipitate):
        self.name = name
        self.Diameter = diameter
        self.Density = density
        self.MolecWeight = molecWeight
        self.AluminumMPM = alumMPM
        self.Precip = Precipitate
        if self.Precip == self.name:
            self.PrecipName = name
            self.PrecipDiameter = diameter
            self.PrecipDensity = density
            self.PrecipMolecWeight = molecWeight
            self.PrecipAluminumMPM = alumMPM
        else:
            self.PrecipName = Precipitate
        
    def define_Precip(self, diameter, density, molecweight, alumMPM):
        self.PrecipDiameter = diameter
        self.PrecipDensity = density
        self.PrecipMolecWeight = molecweight
        self.PrecipAluminumMPM = alumMPM
    

################## Coagulant Definitions ##################
# name, diameter in nm, density in kg/m³, molecular weight in g/mole
PACl = Chemical('PACl', 50, 1138, 1039, 13, 'PACl')

Alum = Chemical('Alum', 70, 2420, 599.21, 2, 'AlOH3')
Alum.define_Precip(70, 2420, 78.024, 1)

################### Necessary Constants ###################
# Fractal diameter, based on data from Adachi.
DIAM_FRACTAL = 2.3
# Diameter of the clay particles.
DIAM_CLAY = 4 * u.um
# Ratio of clay platelet height to diameter.
RATIO_HEIGHT_DIAM = 0.1
# Density of clay.
DENS_CLAY = 2650 * u.kg/u.m**3
# Ration between inner viscous length scale and Kolmogorov length scale.
RATIO_KOLMOGOROV = 50
# Shape factor for drag on flocs used in terminal velocity equation.
PHI_FLOC = 45/24
# Avogadro's number.
NUM_AVOGADRO = 6.0221415 * 10**23 * u.mole**-1
# Molecular weight of aluminum.
MOLEC_WEIGHT_ALUMINUM = 27 * u.g/u.mole

######################## Functions ########################
def dens_alum_nanocluster(coag):
    """Return the density of the aluminum in the nanocluster.
    
    This is useful for determining the volume of nanoclusters 
    given a concentration of aluminum.
    """
    density =  (coag.PrecipDensity * MOLEC_WEIGHT_ALUMINUM 
                * coag.PrecipAluminumMPM / coag.PrecipMolecWeight)
    return density.to(u.kg/u.m**3)


def dens_pacl_solution(ConcAluminum, temp):
    """Return the density of the PACl solution.
    
    From Stock Tank Mixing report Fall 2013:
    https://confluence.cornell.edu/download/attachments/137953883/20131213_Research_Report.pdf
    """
    density =  ((0.492 * ConcAluminum * PACl.MolecWeight 
                 / (PACl.AluminumMPM * MOLEC_WEIGHT_ALUMINUM)
                 ) + pc.density_water(temp)
                )
    return density.to(u.kg/u.m**3)


def conc_precipitate(ConcAluminum, coag):
    """Return coagulant precipitate concentration given aluminum dose."""
    concentration =  ((ConcAluminum / MOLEC_WEIGHT_ALUMINUM) 
                      * (coag.PrecipMolecWeight / coag.PrecipAluminumMPM)
                      )
    return concentration.to(u.mg/u.L)


def conc_floc(ConcAluminum, concClay, coag):
    return (conc_precipitate(ConcAluminum, coag) + concClay).to(u.mg/u.L)


def moles_aluminum(ConcAluminum):
    """Return the # of moles Aluminum given aluminum concentration."""
    return (ConcAluminum / MOLEC_WEIGHT_ALUMINUM).to(u.mol/u.m**3)


def sep_dist_aluminum(ConcAluminum):
    """Return the separation distance between aluminum molecules."""
    return ((1 / (NUM_AVOGADRO*moles_aluminum(ConcAluminum)))**(1/3)).to(u.nm)


def num_clay(ConcClay, DiamClay):
    return (ConcClay / ((DENS_CLAY * np.pi * DiamClay**3) / 6)).to(1/u.mm**3)


def sep_dist_clay(ConcClay, DiamClay):
    """Return the separation distance between clay particles."""
    return (((DENS_CLAY / ConcClay) * ((np.pi * DiamClay**3) / 6))**(1/3)
            ).to(u.nm)


def num_nanoclusters(ConcAluminum, coag):
    return ((ConcAluminum / (dens_alum_nanocluster(coag) 
                             * np.pi * (coag.Diameter**3)
                             ))).to(1/u.L)


def phi_floc_initial(ConcAluminum, ConcClay, coag):
    return ((conc_precipitate(ConcAluminum, coag) / coag.PrecipDensity)
            + (ConcClay / DENS_CLAY)).to(u.dimensionless)

####################### p functions #######################
def p(C, Cprime):
    return -np.log10(C/Cprime)


def invp(pC, Cprime):
    return Cprime * 10**-pC

#################### Fractal functions ####################
def diam_fractal(DiamFractal, DiamInitial, NumCol):
    """Return the diameter of a floc given NumCol doubling collisions."""
    return (DiamInitial * 2**(NumCol / DiamFractal)).to(u.um)


def num_coll_reqd(DiamFractal, DiamInit, DiamTarget):
    """Return the number of doubling collisions required.
    
    Calculates the number of doubling collisions required to produce
    a floc of diameter DiamTarget.
    """
    return DiamFractal * np.log2(DiamTarget/DiamInit)


def sep_dist_floc(ConcAluminum, ConcClay, coag, 
                  DiamFractal, DiamInit, DiamTarget):
    """Return separation distance as a function of floc size."""
    return (DiamInit 
            * (np.pi/(6*phi_floc_initial(ConcAluminum, ConcClay, coag)))**(1/3)
            * (DiamTarget / DiamInit)**(DiamFractal / 3)
            ).to(u.nm)


def phi(ConcAluminum, ConcClay, coag, DiamFractal, DiamInit, DiamTarget):
    """Return the floc volume fraction."""
    return (phi_floc_initial(ConcAluminum, ConcClay, coag) 
            * (DiamTarget / DiamInit)**(3-DiamFractal)
            ).to(u.dimensionless)


def dens_floc_init(ConcAluminum, ConcClay, coag):
    """Return the density of the initial floc.
    
    Initial floc is made primarily of the primary colloid and nanoglobs.
    """
    return (conc_floc(ConcAluminum, ConcClay, coag) 
            / phi_floc_initial(ConcAluminum, ConcClay, coag)
            ).to(u.kg/u.m**3)

#################### Flocculation Model ####################
def ratio_clay_sphere(RatioHeightDiameter):
    """Return the surface area to volume ratio for clay.
    
    Normalized by surface area to volume ratio for a sphere.
    """
    return (1/2 + RatioHeightDiameter) * (2 / (3*RatioHeightDiameter))**(2/3)


def ratio_area_clay_total(ConcClay, DiamClay, DiamTube, 
                          DensityClay, RatioHeightDiameter):
    """Return the surface area of clay normalized by total surface area.
    
    Total surface area is a combination of clay and reactor wall
    surface areas. This function is used to estimate how much coagulant
    actually goes to the clay.
    """
    return (1 
            / (1 
               + (2 * DiamClay 
                  / (3 * DiamTube * ratio_clay_sphere(RatioHeightDiameter)
                     * (ConcClay / DensityClay)
                     )
                  )
               )
            )


def gamma_coag(ConcClay, ConcAluminum, coag, 
               DiamTube, DiamClay, DensityClay, RatioHeightDiameter):
    """Return the coverage of clay with nanoglobs.
    
    This function accounts for loss to the tube flocculator walls
    and a poisson distribution on the clay given random hits by the
    nanoglobs. The poisson distribution results in the coverage only 
    gradually approaching full coverage as coagulant dose increases.
    """
    return (1 - np.exp(
                       ((- phi_floc_initial(ConcAluminum, 0*u.mg/u.L, coag) 
                         * DiamClay
                         ) / (phi_floc_initial(0*u.mg/u.L, ConcClay, coag) 
                              * coag.Diameter
                              )
                        ) * (1/np.pi) 
                          * (ratio_area_clay_total(ConcClay, DiamClay, 
                                                   DiamTube, DensityClay, 
                                                   RatioHeightDiameter)
                             / ratio_clay_sphere(RatioHeightDiameter)
                             )
                       )
            )

    
def pc_viscous(FittingParam, EnerDis, Temp, Time, ConcAl, ConcClay, coag, 
               DiamInit, DiamTube, RatioHeightDiameter, DensityClay):
    return ((3/2) 
            * np.log10((2/3) * np.pi * FittingParam * Time
                       * np.sqrt(EnerDis/(pc.viscosity_kinematic(Temp)))
                       * gamma_coag(ConcClay, ConcAl, coag, DiamTube, 
                                    DiamInit, DensityClay, RatioHeightDiameter)
                       * (DiamInit / sep_dist_clay(ConcClay, DiamInit)) ** 2
                       + 1
                       )
            )


def dens_floc(ConcAl, ConcClay, DiamFractal, DiamInit, DiamTarget, coag, Temp):
    """Calculate floc density as a function of size."""
    WaterDensity = pc.density_water(Temp)
    return ((dens_floc_init(ConcAl, ConcClay, coag) - WaterDensity)
            * (DiamInit / DiamTarget)**(3 - DiamFractal)
            + WaterDensity
            ).to(u.kg/u.m**3)


def vel_term_floc(ConcAl, ConcClay, coag, DiamFractal, 
                  DiamInit, DiamTarget, Temp):
    """Calculate floc terminal velocity."""
    WaterDensity = pc.density_water(Temp)
    return (((pc.gravity*DiamInit**2) 
             / (18*PHI_FLOC*pc.viscosity_kinematic(Temp))
             )
            * ((dens_floc_init(ConcAl, ConcClay, coag) - WaterDensity)
               / WaterDensity
               )
            * (DiamTarget / DiamInit) ** (DiamFractal - 1)
            ).to(u.mm/u.s)


def diam_floc_vel_term(ConcAl, ConcClay, coag, 
                       DiamFractal, DiamInit, VelTerm, Temp):
    """Calculate floc diamter as a function of terminal velocity."""
    WaterDensity = pc.density_water(Temp)
    return (DiamInit * (((18*VelTerm*PHI_FLOC*pc.viscosity_kinematic(Temp)) 
                         / (pc.gravity * DiamInit**2)
                         )
                         * (WaterDensity 
                            / (dens_floc_init(ConcAl, ConcClay, coag)
                               - WaterDensity
                               )
                            )
                        ) ** (1 / (DiamFractal - 1))
            ).to(u.mm)


def time_col_laminar(ConcAl, ConcClay, coag, DiamFractal, DiamInit,
                     DiamTarget, EnerDis, Temp, DiamTube, RatioHeightDiameter, 
                     DensityClay):
    """Calculate single collision time for laminar flow mediated collisions.
    
    Calculated as a function of floc size.
    """
    return (((1/6) * ((6/np.pi)**(1/3))
             * phi_floc_initial(ConcAl, ConcClay, coag)**(-2/3)
             * (pc.viscosity_kinematic(Temp) / EnerDis)**(1/2)
             * (DiamTarget / DiamInit)**(2*DiamFractal/3 - 2)
             ) # End of the numerator
            / (gamma_coag(ConcClay, ConcAl, coag, DiamTube, 
                          DiamInit, DensityClay, RatioHeightDiameter)
               ) # End of the denominator
            ).to(u.s)


def time_col_turbulent(ConcAl, ConcClay, coag, DiamFractal, DiamInit,
                       DiamTarget, EnerDis):
    """Calculate single collision time for turbulent flow mediated collisions.
    
    Calculated as a function of floc size.
    """
    return((1/6) * (6/np.pi)**(1/9) * EnerDis**(-1/3) * DiamTarget**(2/3)
           * phi_floc_initial(ConcAl, ConcClay, coag)**(-8/9)
           * (DiamTarget / DiamInit)**((8*(DiamFractal-3)) / 9)
           ).to(u.s)

########### Kolmogorov and viscous length scales ###########
def eta_kolmogorov(EnerDis, Temp):
    return (((pc.viscosity_kinematic(Temp)**3) / EnerDis)**(1/4)).to(u.mm)


def lambda_vel(EnerDis, Temp):
    return (RATIO_KOLMOGOROV * eta_kolmogorov(EnerDis, Temp)).to(u.mm)


def diam_kolmogorov(ConcAl, ConcClay, coag, DiamInit, 
                    DiamFractal, EnerDis, Temp):
    """Return the size of the floc with separation distances equal to
    the Kolmogorov length and the inner viscous length scale.
    """
    return (DiamInit
            * ((eta_kolmogorov(EnerDis, Temp) / DiamInit)
               * ((6 * phi_floc_initial(ConcAl,ConcClay,coag)) / np.pi)**(1/3)
               )**(3/DiamFractal)
            ).to(u.um)


def diam_vel(ConcAl, ConcClay, coag, DiamInit, DiamFractal, EnerDis, Temp):
    return (DiamInit
            * ((lambda_vel(EnerDis, Temp) / DiamInit)
               * ((6 * phi_floc_initial(ConcAl,ConcClay,coag)) / np.pi)**(1/3)
               )**(3/DiamFractal) #End of squares
            ).to(u.mm)


def ener_dis_diam_floc(Diam):
    """Return max energy dissipation rate as a function of max floc diameter.
    
    This equation is under suspicion.
    """
    return ((95 * u.um / Diam)**3).to(u.mW/u.kg)

##### Velocity gradient in tubing for lab scale laminar flow flocculators #####
def g_straight(PlantFlow, IDTube):
    return (64 * PlantFlow / (3 * np.pi * IDTube)**3).to(1/u.s)


def reynolds_rapid_mix(PlantFlow, IDTube, Temp):
    return (4 * PlantFlow / (np.pi * IDTube * pc.viscosity_kinematic(Temp))
            ).to(u.dimensionless)


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


def g_coil(FlowPlant, IDTube, RadiusCoil, Temp):
    """We need a reference for this. 
    
    Karen's thesis likely has this equation and the reference.
    """
    return (g_straight(FlowPlant, IDTube)
            * (1 
               + 0.033 * np.log10(dean_number(FlowPlant, IDTube, 
                                              RadiusCoil, Temp)
                                  ) ** 4
               ) ** (1/2)
            ).to(1/u.s)


def time_res_tube(IDTube, LengthTube, FlowPlant):
    """Calculate residence time in the flocculator."""
    return (LengthTube * np.pi * (IDTube**2 / 4) / FlowPlant).to(u.s)


def g_time_res(FlowPlant, IDTube, RadiusCoil, LengthTube, Temp):
    """G Residence Time calculated for a coiled tube flocculator."""
    return (g_coil(FlowPlant, IDTube, RadiusCoil, Temp)
            * time_res_tube(IDTube, LengthTube, FlowPlant)
            ).to(u.dimensionless)