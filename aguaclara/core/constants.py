# -*- coding: utf-8 -*-
"""Constant quantities of widely-accepted physical properties."""

from aguaclara.core.units import unit_registry as u

GRAVITY = 9.80665 * u.m / u.s ** 2

WATER_DENSITY = 1000 * u.kg / u.m ** 3
WATER_NU = 1 * 10 ** -6 * u.m ** 2 / u.s

ATM_P = 1 * u.atm
AIR_NU = 12 * u.mm ** 2 / u.s
AIR_DENSITY = 1.204 * u.kg / u.mm ** 3

# The influence of viscosity on mixing in jet reactors
JET_ROUND_RATIO = 0.08
# Estimate for plane jets in the flocculator and sed tank jet reverser.
JET_PLANE_RATIO = 0.0124

LFP_FLOW_MAX = 16.1 * u.L / u.s

FITTING_S_MIN = 5 * u.cm  # Between fittings and tank wall in a tank.
CHANNEL_W_MIN = 15 * u.cm

VC_ORIFICE_RATIO = 0.63

K_KOZENY = 5
