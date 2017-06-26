# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 16:05:25 2017

@author: cbb67
"""

from AguaClara_design.units import unit_registry as u
##Minor loss coefficients
##Individual K Values

##90 deg elbow
K_MINOR_EL90=0.9

K_MINOR_EL45=0.45
##The loss coefficient for the channel transition in a 90 degree turn
K_MINOR_90=0.4

K_MINOR_ANGLE_VALVE=4.3

K_MINOR_GLOBE_VALVE=10

K_MINOR_GATE_VALVE=0.39

K_MINOR_CHECK_VALVE_CONV=4

K_MINOR_CHECK_VALVE_BALL=4.5

##headloss coefficient of jet
K_MINOR_EXP=1

K_MINOR_TEE_FLOW_run=0.6

K_MINOR_TEE_FLOW_BR=1.8

K_MINOR_PIPE_ENTRANCE=0.5

K_MINOR_PIPE_EXIT=1

K_MINOR_RM_GATE_VIN=25




###Operator access

##combine walkway assumptions!
WIDTH_MP_WALKWAY_MIN=1*(u.m)

##Width of the walkway above the main plant drain channel
WIDTH_DC_WALKWAY=1.2*(u.m)

##Width of the floor space between the flocculator and the rapid mix pipe floor cutout next to the entrance tank.
WIDTH_ET_WALKWAY=1*(u.m)

##for high flow, double train situations
W_TRAIN_WALKWAY=1.5*(u.m)

W_BASEMENT_STAIRS=0.9*(u.m)

W_ENTRANCE_STAIRS=1.2*(u.m)



#######Plant drain channel

###Space beyond the entrance tank in the plant drain channel where the drop pipes from the CDC lever arm can come down and be connected with the chlorine and coagulant dosing points.
LENGTH_CHEM_LEVER_ARM_SPACE=75*(u.cm)




#######Elevation Safety Margins

##Minimum depth in the entrance box during backwash such that there is standing water over the inlet.
HEIGTH_FILTER_BACKWASH_NO_SUCK_AIR=20*(u.cm)

##Minimum water depth over the orifices in the siphon manifold so that air is not entrained.
HEIGTH_FILTER_SIPHON_NO_SUCK_AIR=10*(u.cm)

HEIGTH_FILTER_FLUIDIZED_BED_TO_SIPHON=20*(u.cm)

HEIGTH_FILTER_FORWARD_NO_SUCK_AIR=10*(u.cm)

HEIGTH_FILTER_WEIR_FREEFALL=3*(u.cm)

HEIGTH_FILTER_AIR_REMOVAL_BLOCK_SUBMERGED=5*(u.cm)

HEIGTH_FILTER_BYPASS_SAFETY=10*(u.cm)

HEIGTH_DRAIN_OUTLET_SAFETY=10*(u.cm)

HEIGTH_FILTER_OVERFLOW_WEIR_FREEFALL=10*(u.cm)
