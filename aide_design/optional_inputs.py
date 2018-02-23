"""This file contains the default values which may be overriden by user inputs
for design parameters of AguaClara plants.

"""
from aide_design.units import unit_registry as u

## ETLF

# Entrance Tank
L_ET_MAX = 2.2*u.m

# LFOM
HL_LFOM = 20*u.cm

# Flocculator
HL_FLOC = 0.4*u.m

COLL_POT = 37000 # collision potential, also referred to as Gt

FREEBOARD = 10*u.cm
