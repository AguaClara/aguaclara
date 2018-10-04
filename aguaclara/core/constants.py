# -*- coding: utf-8 -*-
"""
Constant values of widely-accepted physical properties.
"""

from aguaclara.core.units import unit_registry as u

GRAVITY = 9.80665 * u.m / u.s ** 2

WATER_DENSITY = 1000 * u.kg / u.m ** 3
WATER_NU = 1 * 10 ** -6 * u.m ** 2 / u.s

ATM_P = 1 * u.atm
AIR_NU = 12 * u.mm ** 2 / u.s
AIR_DENSITY = 1.204 * u.kg / u.mm ** 3

# TODO: Consider removing the following section altogether. - Oliver Leung (oal22)
# TODO: START
# The influence of viscosity on mixing in jet reactors
JET_ROUND_RATIO = 0.08
JET_PLANE_RATIO = 0.0124  # Estimate for plane jets in the flocculator and sed tank jet reverser.

LFP_FLOW_MAX = 16.1 * u.L / u.s

FITTING_S_MIN = 5 * u.cm  # Between fittings and tank wall in a tank.
CHANNEL_W_MIN = 15 * u.cm

VC_ORIFICE_RATIO = 0.63
# TODO: END

# TODO: Consider moving the following section to different file. - Oliver Leung (oal22)
# TODO: START
# Walkways and human access
WALKWAY_W_MIN_DEFAULT = 1 * u.m
DC_WALKWAY_W = 1.2 * u.m
ENT_TANK_WALKWAY_W = 1 * u.m
TRAIN_WALKWAY_W = 1.5 * u.m
BASEMENT_STAIRS_W = 0.9 * u.m
ENTRANCE_STAIRS_W = 1.2 * u.m

HUMAN_W_MIN = 0.5 * u.m
DRAIN_CHAN_H_MIN = 1.5 * u.m
PLANT_H_MIN = 0.1 * u.m

DOOR_W = 1 * u.m
# TODO: END
