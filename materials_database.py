# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 12:05:59 2017

@author: kn348
"""

import numpy as np
import scipy
import math

try:
    from AguaClara_design.units import unit_registry as u
    from AguaClara_design import utility as ut
except ModuleNotFoundError:
    from units import unit_registry as u
    import utility as ut

gravity = 9.80665 * u.m/u.s**2
"""Define the gravitational constant, in m/s²."""

########### Materials Constants - general ############

PIPE_ROUGH_PVC = 0.12*u.mm

PIPE_ROUGH_CONCRETE = 2*u.mm

RHO_CONCRETE = 2400*(u.kg/(u.m**3)) #used in the sed tank drawing

THICKNESS_CONCRETE_MIN = 5*u.cm  #used throughout the code

#0 is English, 1 is metric, drill series is needed for the 
#drill series at the bottom of this sheet and tube series 
#is needed for the Cdc code
EN_DRILL_SERIES = 0

EN_TUBE_SERIES = 0

DIAM_REBAR = (1/2)*u.inch

########### Material constants - entrance tank ############

THICKNESS_LFOM_SHEET = THICKNESS_CONCRETE_MIN

NOM_DIAM_ENT_TANK_FLOAT =  8*u.inch

#Minimum pipe size to handle grit and to ensure that the pipe can be easily unclogged
NOM_DIAM_ENT_TANK_DRAIN_MIN =  3*u.inch

NOM_DIAM_ENT_TANK_DRAIN =  3*u.inch #This is constant for now

THICKNESS_ENT_TANK_REMOVABLE_WALL = 5*u.cm

#Parameters are arbitrary - need to be calculated
HEIGHT_ENT_TANK_REMOVABLE_WALL_SUPPORT = 4*u.cm

THICKNESS_ENT_TANK_REMOVABLE_WALL_SUPPORT = 5*u.cm

THICKNESS_ENT_TANK_HOPPER_LEDGE = 15*u.cm

THICKNESS_RAPID_MIX_ORIFICE_PLATE = 2*u.cm

NOM_DIAM_RAPID_MIX_AIR_RELEASE = 1*u.inch

 ############ Material constants - chem storage tanks  ############
 
THICKNESS_CHEM_TANK_WALL = 5*u.mm
 
 #Supplier Information:
#http://www.rotoplas.com/assets/files/industria/catalogo.pdf

#each element in the following array is tank volume

VOL_SUPPLIER_CHEM_TANK = [208.198, 450, 600, 750, 1100, 2500]*u.L

#the following array is a 2D array in which 
#in each element, the first element is tank diameter 
#and the second element is tank height

DIMENSIONS_SUPPLIER_CHEM_TANK = [[0.571, 0.851], [0.85, 0.99], [0.96, 1.10], [1.10, 1.02], [1.10, 1.39], [1.55, 1.65]]*u.m

FACTOR = [1.05, 1.05, 1.05, 1.05, 1.05, 1.05]

############ Material constants - chemical dose controller ###########

DIAM_TUBE_ENGLISH = [1, 2, 3 ,4 ,5 ,6, 7]*u.inch/16

DIAM_TUBE_METRIC = [2, 3, 4, 6, 8, 10]*u.mm

DIAM_FLT_VLV_ORIFICES_AVAIL = [0.093, 0.187, 0.25, 0.312]*u.inch

############# Material constants - flocculator #####################

THICKNESS_FLOC_BAFFLE_RIGID_HEIGHT = 15*u.cm

#The piping size for the main part of the floc modules
NOM_DIAM_FLOC_MODULES_MAIN = (1/2)*u.inch

#The diameter of the oversized cap used to assemble the floc modules
NOM_DIAM_FLOC_MODULES_LARGE = 1.5*u.inch

############ Material constants - sedimentation  #############

WIDTH_SED_PLATE = 1.06*u.m

THICKNESS_SED_PLATE = 0.2*u.cm

SPACE_SED_PLATE = 2.5*u.cm

ANGLE_SED_PLATE = 60*u.deg

THICKNESS_SED_WEIR = 5*u.cm

#Maximum length of sed plate sticking out past module pipes without any 
#additional support. The goal is to prevent floppy modules that don't maintain
# constant distances between the plates

LENGTH_SED_PLATE_CANTILEVERED = 20*u.cm

DIST_CENTER_SED_PLATE = SPACE_SED_PLATE + THICKNESS_SED_PLATE

N_SED_MODULE_PLATES_MAX = math.floor((LENGTH_SED_PLATE_CANTILEVERED/DIST_CENTER_SED_PLATE*np.tan(ANGLE_SED_PLATE ))+1)

N_SED_MODULE_PLATES_MIN = 8

NOM_DIAM_SED_HOPPER_DRAIN = 1*u.inch

NOM_DIAM_SED_HOPPER_VIEWER = 2*u.inch

NOM_DIAM_SED_HOPPER_SKIMMER = 2*u.inch

##Diffusers/Jet Reverser

NOM_DIAM_SED_DIFFUSER = 1*u.inch

NOM_DIAM_SED_JET_REVERSER = 3*u.inch

