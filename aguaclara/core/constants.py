# -*- coding: utf-8 -*-
"""Constant quantities of widely-accepted physical properties."""

from aguaclara.core.units import u

# NOTE: "#: <optional_description>"  required for Sphinx autodocumentation

#: Gravitational constant
GRAVITY = 9.80665 * u.m / u.s ** 2

#: Density of water
WATER_DENSITY = 1000 * u.kg / u.m ** 3
#: Kinematic viscosity of water
WATER_NU = 1 * 10 ** -6 * u.m ** 2 / u.s

#: Atmospheric pressure
ATM_P = 1 * u.atm
#: Average kinematic viscosity of air
AIR_NU = 12 * u.mm ** 2 / u.s

#: The influence of viscosity on mixing in jet reactors
JET_ROUND_RATIO = 0.08
#: An estimate for plane jet ratios in the flocculator and sed tank jet reverser
JET_PLANE_RATIO = 0.0124

#:
LFP_FLOW_MAX = 16.1 * u.L / u.s

#: Between fittings and tank wall in a tank.
FITTING_S_MIN = 5 * u.cm
#:
CHANNEL_W_MIN = 15 * u.cm

#:
VC_ORIFICE_RATIO = 0.63

#:
K_KOZENY = 5
