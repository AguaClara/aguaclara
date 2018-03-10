"""This file contains the default values which may be overriden by user inputs
for design parameters of AguaClara plants.

"""
from aide_design.units import unit_registry as u

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

ND_JET_REVERSER = 3 * u.inch  # nominal diameter of pipe used for jet reverser in bottom of set tank

ND_DIFFUSER_PIPE = 4 * u.cm  # nominal diameter of pipe used to make diffusers

W_DIFFUSER_OPENING = 0.3175 * u.cm  # opening width of diffusers

L_DIFFUSER_OPENING = 1 * u.cm  # NEED VALUE BECAUSE THIS IS A GUESS

L_DIFFUSER = 15 * u.cm  # vertical length of diffuser

SDR_DIFFUSER = 26  # SDR of diffuser pipe

B_DIFFUSER = 5 * u.cm  # center to center spacing beteen diffusers

HL_OUTLET_MAN = 5 * u.cm  # head loss through the outlet manifold
