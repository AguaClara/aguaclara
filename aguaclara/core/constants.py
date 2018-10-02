# -*- coding: utf-8 -*-
"""
Constants which represent physical properties and scientific principles
which will be used in AguaClara plant design.
"""

from aguaclara.core.units import unit_registry as u

GRAVITY = 9.80665 * u.m/u.s**2

WATER_DENSITY = 1000 * u.kg / u.m ** 3
WATER_NU = 1 * 10 ** -6 * u.m ** 2 / u.s

ATM_P = 1 * u.atm
AIR_NU = 12 * u.mm ** 2 / u.s
AIR_DENSITY = 1.204 * u.kg / u.mm ** 3

# The influence of viscosity on mixing in jet reactors
JET_ROUND_RATIO = 0.08
JET_PLANE_RATIO = 0.0124  # Estimate for plane jets in the flocculator and sed tank jet reverser.

LFP_FLOW_MAX = 16.1 * u.L / u.s

HUMAN_W_MIN = 0.5 * u.m
DRAIN_CHAN_H_MIN = 1.5 * u.m
PLANT_H_MIN = 0.1 * u.m

# TODO: What does "mp" mean? This doesn't follow standard names.
MP_WALKWAY_MIN_W = 1 * u.m
DC_WALKWAY_W = 1.2 * u.m

ENT_TANK_WALKWAY_W = 1 * u.m
TRAIN_WALKWAY_W = 1.5 * u.m
BASEMENT_STAIRS_W = 0.9 * u.m
ENTRANCE_STAIRS_W = 1.2 * u.m

FITTING_S_MIN = 5 * u.cm  # Between fittings and tank wall in a tank.
CHANNEL_W_MIN = 15 * u.cm
DOOR_W = 1 * u.m

# TODO: What does "vc" mean? This doesn't follow the standard naming
# conventions.
VC_ORIFICE_RATIO = 0.63

# Due to a 24 in LFOM because that's the biggest pipe we have in our
# database right now. if we need a bigger single train, we can do that
# by adding that pipe size into the pipe database
FLOW_TRAIN_MAX = 150.1 * u.L/u.s


def en_multiple_train(flow_plant):
    if flow_plant > 60 * u.L/u.s:
        return 1
    else:
        return 0


def n_train(flow_plant):
    if flow_plant > 60*u.L/u.s:
        return 1
    elif flow_plant > 60*u.L/u.s and flow_plant <= 120 * u.L/u.s:
        return 2
    else:
        return 4


def flow_train(flow_plant):
    return flow_plant / n_train(flow_plant)
