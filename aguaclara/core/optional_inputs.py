"""This file contains the default values which may be overriden by user inputs
for design parameters of AguaClara plants.

"""
from aguaclara.core.units import unit_registry as u

## ETLF

# Entrance Tank
L_ET_MAX = 2.2 * u.m

# LFOM
HL_LFOM = 20 * u.cm

S_LFOM_ORIFICE = 1 * u.cm  # minimum wall distance between orifices, for lfom structural stability

# Flocculator
HL_FLOC = 0.4 * u.m

COLL_POT = 37000  # collision potential, also referred to as Gt

FREEBOARD = 10 * u.cm

# Sedimentation tank
THICKNESS_PLANT_FLOOR = 0.2 * u.m  # plant floor slab thickness

THICKNESS_SED_WALL = 0.15 * u.m  # thickness of sed tank dividing wall

FLOC_BLANKET_HEIGHT = 0.25 * u.m  # vertical height of floc blanket from peak of slope to weir

HL_OUTLET_MAN = 4 * u.cm  # head loss through the outlet manifold
