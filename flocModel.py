# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 16:50:46 2017

@author: Sage Weber-Shirk

Last revised: Tue Jun 27 2017
By: Sage Weber-Shirk
"""

######################### Imports #########################
import math
import numpy as np
import scipy

from AguaClara_design.units import unit_registry as u
from AguaClara_design import physchem as pc
from AguaClara_design import pipedatabase as pipe
from AguaClara_design import utility as ut

u.enable_contexts('chem')

##################### Class Definition #####################

class Chemical:
    def __init__(self, name, diameter, density, molecWeight, alumMPM, Precip):
        self.name = name
        self.Diameter = diameter
        self.Density = density
        self.MolecWeight = molecWeight
        self.AluminumMPM = alumMPM
        self.Precip = Precip
        if self.Precip == self.name:
            self.Precip.name = self.name
            self.Precip.Diameter = self.Diameter
            self.Precip.Density = self.Density
            self.Precip.MolecWeight = self.MolecWeight
            self.Precip.AluminumMPM = self.AluminumMPM
        else:
            self.Precip.name = self.Precip
        
    def define_Precip(self, diameter, density, molecweight, alumMPM):
        self.Precip.Diameter = diameter
        self.Precip.Density = density
        self.Precip.MolecWeight = molecweight
        self.Precip.AluminumMPM = alumMPM
    

################## Coagulant Definitions ##################
PACl = Chemical('PACl', 50 * u.nm, 1138 * u.kg/u.m**3, 1039 * u.g/u.mole, 
                13, 'PACl')

Alum = Chemical('Alum', 70 * u.nm, 2420 * u.kg/u.m**3, 599.21 * u.g/u.mole, 
                2, 'AlOH3')
Alum.define_Precip(70 * u.nm, 2420 * u.kg/u.m**3, 78.024 * u.g/u.mole, 1)

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
    return (coag.Precip.Density * MOLEC_WEIGHT_ALUMINUM 
            * coag.Precip.AluminumMPM / coag.Precip.MolecWeight)


def dens_pacl_solution(ConcAluminum, temp):
    """Return the density of the PACl solution.
    
    From Stock Tank Mixing report Fall 2013:
    https://confluence.cornell.edu/download/attachments/137953883/20131213_Research_Report.pdf
    """
    return ((0.492 * ConcAluminum * PACl.MolecWeight 
             / (PACl.AluminumMPM * MOLEC_WEIGHT_ALUMINUM)
             ) + pc.density_water(temp)
            )


def conc_precipitate(ConcAluminum, coag):
    """Return coagulant precipitate concentration given aluminum dose."""
    return ((ConcAluminum / MOLEC_WEIGHT_ALUMINUM) 
            * (coag.Precip.MolecWeight / coag.Precip.AluminumMPM)
            )


def conc_floc(ConcAluminum, concClay, coag):
    return conc_precipitate(ConcAluminum, coag) + concClay


def moles_aluminum(ConcAluminum):
    """Return the # of moles Aluminum given aluminum concentration."""
    return ConcAluminum / MOLEC_WEIGHT_ALUMINUM


def sep_dist_aluminum(ConcAluminum):
    """Return the separation distance between aluminum molecules."""
    return (1 / (NUM_AVOGADRO * moles_aluminum(ConcAluminum)))**(1/3)


def num_clay(ConcClay, DiamClay):
    return ConcClay / ((DENS_CLAY * np.pi * DiamClay**3) / 6)


def sep_dist_clay(ConcClay, DiamClay):
    """Return the separation distance between clay particles."""
    return ((DENS_CLAY / ConcClay) * ((np.pi * DiamClay**3) / 6))**(1/3)


def num_nanoclusters(ConcAluminum, coag):
    return (ConcAluminum / (dens_alum_nanocluster(coag) 
                            * np.pi * (coag.Diameter**3)
                            ))


def phi_floc_initial(ConcAluminum, ConcClay, coag):
    return ((conc_precipitate(ConcAluminum, coag) / coag.Precipitate.Density)
            + (ConcClay / DENS_CLAY))

####################### p functions #######################
def p(C, Cprime):
    return -np.log10(C/Cprime)


def invp(pC, Cprime):
    return Cprime * 10**-pC

#################### Fractal functions ####################
def diam_fractal(DiamFractal, DiamInitial, NumCol):
    """Return the diameter of a floc given NumCol doubling collisions."""
    return DiamInitial * 2**(NumCol / DiamFractal)


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
            )


def phi(ConcAluminum, ConcClay, coag, DiamFractal, DiamInit, DiamTarget):
    """Return the floc volume fraction."""
    return (phi_floc_initial(ConcAluminum, ConcClay, coag) 
            * (DiamTarget / DiamInit)**(3-DiamFractal)
            )


def dens_floc_init(ConcAluminum, ConcClay, coag):
    """Return the density of the initial floc.
    
    Initial floc is made primarily of the primary colloid and nanoglobs.
    """
    return (conc_floc(ConcAluminum, ConcClay, coag) 
            / phi_floc_initial(ConcAluminum, ConcClay, coag)
            )

#################### Flocculation Model ####################
def ratio_clay_sphere(RatioHeightDistance):
    """Return the surface area to volume ratio for clay.
    
    Normalized by surface area to volume ratio for a sphere.
    """
    return (1/2 + RatioHeightDistance) * (2 / (3*RatioHeightDistance))**(2/3)


def ratio_area_clay_total(ConcClay, DiamClay, DiamTube, RatioHeightDistance):
    """Return the surface area of clay normalized by total surface area.
    
    Total surface area is a combination of clay and reactor wall
    surface areas. This function is used to estimate how much coagulant
    actually goes to the clay.
    """
    return (1 
            / (1 
               + (2 * DiamClay 
                  / (3 * DiamTube * ratio_clay_sphere(RatioHeightDistance)
                     * (ConcClay / DiamClay)
                     )
                  )
               )
            )


def gamma_coag(ConcClay, ConcAluminum, coag, 
               DiamTube, DiamClay, RatioHeightDistance):
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
                          * (ratio_area_clay_total(ConcClay, DiamClay, DiamTube, 
                                                   RatioHeightDistance)
                             / ratio_clay_sphere(RatioHeightDistance)
                             )
                       )
            )

    
def pc_viscous(MinorLoss, EnerDis, Temp, Time, ConcAl, ConcClay, coag, 
               DiamInit, DiamTube, RatioHeightDistance):
    return ((3/2) 
            * np.log10((2/3) * np.pi * MinorLoss * Time
                       * np.sqrt(EnerDis/(pc.viscosity_kinematic(Temp)))
                       * gamma_coag(ConcClay, ConcAl, coag, DiamTube, 
                                    DiamInit, RatioHeightDistance)
                       * (DiamInit / sep_dist_clay(ConcClay, DiamClay)) ** 2
                       + 1
                       )
            )


def dens_floc(ConcAl, ConcClay, DiamFractal, DiamInit, DiamTarget, coag, Temp):
    """Calculate floc density as a function of size."""
    WaterDensity = pc.density_water(Temp)
    return ((dens_floc_init(ConcAl, ConcClay, coag) - WaterDensity)
            * (DiamInit / DiamTarget)**(3 - DiamFractal)
            + WaterDensity
            )


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
            )


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
            )


def time_col_laminar(ConcAl, ConcClay, coag, DiamFractal, DiamInit,
                     DiamTarget, EnerDis, Temp, DiamTube):
    """Calculate single collision time for laminar flow mediated collisions.
    
    Calculated as a function of floc size.
    """
    return (((1/6) * (6/np.pi)**(1/3) 
             * phi_floc_initial(ConcAl, ConcClay, coag)**(-2/3)
             * (pc.viscosity_kinematic(Temp) / EnerDis)**(1/2)
             * (DiamTarget / DiamInit)**(2*DiamFractal/3 - 2)
             ) # End of the numerator
            / (gamma_coag(ConcClay, ConcAl, coag, 
                          DiamTube, DiamInit, RatioHeightDistance)
               ) # End of the denominator
            ) # End of the function


def time_col_turbulent(ConcAl, ConcClay, coag, DiamFractal, DiamInit,
                       DiamTarget, EnerDis):
    """Calculate single collision time for turbulent flow mediated collisions.
    
    Calculated as a function of floc size.
    """
    return((1/6) * (6/np.pi)**(1/9) * EnerDis**(-1/3) * DiamTarget**(2/3)
           * phi_floc_initial(ConcAl, ConcClay, coag)**(-8/9)
           * (DiamTarget / DiamInit)**((8*(DiamFractal-3)) / 9)
           )

########### Kolmogorov and viscous length scales ###########
def eta_kolmogorov(EnerDis, Temp):
    return ((pc.viscosity_kinematic(Temp)**3) / EnerDis)**(1/4)


def lambda_vel(EnerDis, Temp):
    return RATIO_KOLMOGOROV * eta_kolmogorov(EnerDis, Temp)


def diam_kolmogorov(ConcAl, ConcClay, coag, DiamInit, 
                    DiamFractal, EnerDis, Temp):
    """Return the size of the floc with separation distances equal to
    the Kolmogorov length and the inner viscous length scale.
    """
    return (DiamInit
            * ((eta_kolmogorov(EnerDis, Temp) / DiamInit)
               * ((6 * phi_floc_initial(ConcAl,ConcClay,coag)) / np.pi)**(1/3)
               )**(3/DiamFractal)
            )


def diam_vel(ConcAl, ConcClay, coag, DiamInit, DiamFractal, EnerDis, Temp):
    return (DiamInit
            * ((lambda_vel(EnerDis, Temp) / DiamInit)
               * ((6 * phi_floc_initial(ConcAl,ConcClay,coag)) / np.pi)**(1/3)
               )**(3/DiamFractal) #End of squares
            )


def ener_dis_diam_floc(Diam):
    """Return max energy dissipation rate as a function of max floc diameter."""
    return (why95 * u.um / Diam)**3 * u.W/u.kg

##### Velocity gradient in tubing for lab scale laminar flow flocculators #####
def g_straight(PlantFlow, IDTube):
    return 64 * PlantFlow / (3 * np.pi * IDTube)**3


def reynolds_rapid_mix(PlantFlow, IDTube, Temp):
    return 4 * PlantFlow / (np.pi * IDTube * pc.viscosity_kinematic(Temp))


def dean_number(PlantFlow, IDTube, RadiusCoil, Temp):
    """Return the Dean Number.
    
    The Dean Number is a dimensionless parameter that is the unfortunate
    combination of Reynolds and tube curvature. It would have been better
    to keep the Reynolds number and define a simple dimensionless geometric
    parameter.
    """
    do_we_need_this
    return (reynolds_rapid_mix(PlantFlow, IDTube, Temp) 
            * (IDTube / (2 * RadiusCoil))**(1/2)
            )


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
            )


def time_res_tube(IDTube, LengthTube, FlowPlant):
    """Calculate residence time in the flocculator."""
    return (LengthTube * np.pi * (IDTube**2 / 4) / FlowPlant)


def g_time_res(FlowPlant, IDTube, RadiusCoil, LengthTube, Temp):
    """G Residence Time calculated for a coiled tube flocculator."""
    return (g_coil(FlowPlant, IDTube, RadiusCoil, Temp)
            * time_res_tube(IDTube, LengthTube, FlowPlant)
            )