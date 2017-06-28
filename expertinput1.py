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


##Stacked rapid sand filter
####Construction and Design Inputs

#Design guidelines say 11 mm/s. The success of lab-scale backwashing at 10 mm/s suggests that this is a reasonable and conservative value
VEL_FILTER_Bw_=11*(u.mm/u.s)

N_FILTER_LAYER=6

VEL_FILTER_LAYER=1.833*(u.mm/u.s) ##VEL_FIBER_DIST_CENTER_/N_FIBER_LAYER

##Minimum thickness of each filter layer (can be increased to accomodate larger pipe diameters in the bottom layer)
HEIGHT_FILTER_LAYER_MIN=20*(u.cm)

##center to center distance for slotted pipes
DIST_CENTER_FILTER_MANIFOLD_BRANCH=10*u.cm

##How far the branch extends into the trunk line
LENGTH_FILTER_MAN_BRANCH_EXT=2*u.cm

##The time to drain the filter box of the water above the fluidized bed
TIME_FIBER_BACKWASH_INITIATION_BOD=3*(u.min)

##Mickey suggested this value based on lab experience. This was moved to Expert Inputs 12/4/16 by mrf222 as a result of feedback from Monroe and Skyler. In the Moroceli plant, the Fi Entrance box was overflowing before filtration backwash. The HL of a dirty filter has therefore been increased from 40 to 60 cm.
HEADLOSS_FILTER_DIRTY=60*(u.cm)

##This is the extra head we are going to provide on top of steady state backwash head loss to ensure that we can fluidize the bed to initiate backwash.
HEADLOSS_FIBER_BACKWASH_STEADY_FLOW=20*(u.cm)

##Maximum acceptable head loss through the siphon at steady state; used to calculate a diameter
HEADLOSS_FILTER_SIPHON_MAX=35*(u.cm)

##Diameter of sand drain pipe
NOM_DIAMETER_FILTER_SAND_OUTLET=2*(u.inch)

##Height of the barrier between the exit box and distribution box.
HEIGHT_FILTER_DIST_BARRIER=10*(u.cm)

##Length that the siphon pipe extends up into the plant drain channel. Being able to shorten the stub from which the siphon discharges into the main plant drain channel allows for some flexibility in the hydraulic design.
LENGTH_FILTER_SIPHON_CHANNEL_STUB_MIN=20*(u.cm)

HEADLOSS_FILTER_ENTRANCE_PIPE_MAX=10*(u.cm)

NOM_DIAMETER_FILTER_TRUNK_MAX=6*(u.inch)

NOM_DIAMETER_FILTER_BACK_WASH_SIPHON_MAX=8*(u.inch)

##Purge valves on the trunk lines are angled downwards so that sediment is cleared more effectively. This angle allows the tees to fit on top of one another at the filter wall.
ANGLE_FILTER_TRUNK_VALVES=25*(u.deg)

##Purge valves on the trunk lines are angled downwards so that sediment is cleared more effectively. This angle allows the tees to fit on top of one another at the filter wall.
THICKNESS_FILTER_WEIR=5*(u.cm)

SPACE_FILTER_BRANCH_TO_WALL=5*(u.cm)

FILTER_GATE_VALUE_URL="https://confluence.cornell.edu/download/attachments/173604905/Fi-Scaled-Gate-Valve-Threaded.dwg"
FILTER_BALL_VALVE_URL="https://confluence.cornell.edu/download/attachments/173604905/FiMetalBallValve.dwg"

HEIGTH_FILTER_WALL_TO_PLANT_FLOOR_MIN=10*(u.cm)

HEADLOSS_FILTER_INLET_WEIR_MAX=5*(u.cm)

##Dimensions get too small for construction below a certain flow rate
FLOW_FILTER_MIN=8*(u.l/u.s)

LENGTH_FILTER_MAN_FEMCO_COUPLING=6*(u.cm)

##Nominal diameter of the spacer tees in the four corners of the filter manifold assembly.
NOM_DIAMETER_FILTER_MAN_WING_SPACER=2*(u.inch)

##Length of the vertical pipe segment following the valve on the filter sand drain. This stub can be capped to allow the sand in the valve to settle, so that the valve can be closed without damage from fluidized sand.
LENGTH_FILTER_SAND_OUTLET_PIPE=20*(u.cm)





###Sedimentation tank
##General

VEL_SED_UP_BOD=1*(u.mm/u.s)

##Plate settler capture velocity
VEL_SED_CONC_BOD=0.12*(u.mm/u.s)

ANGLE_SED_SLOPE=50*(u.deg)

##This slope needs to be verified for functionality in the field. A steeper slope may be required in the floc hopper.
ANGLE_SED_HOPPER_SLOPE=45(u.deg)

HEIGHT_WATER_SED_EST=2*(u.m)

SED_GATE_VALVE_URL="https://confluence.cornell.edu/download/attachments/173604905/Sed-Scaled-Gate-Valve-Threaded.dwg"

SUPPORT_BOLT_URL= "https://confluence.cornell.edu/download/attachments/173604905/PlateSettlerSupportBolt.dwg"

##  Max length of the active part of the sed tank so that single pipe segments can be used for the inlet and outlet manifoldS
LENGTH_SED_UP_FLOW_MAX= 5.8*(u.m)

   
##Inlet channel
HEADLOSS_SED_WEIR_MAX=5*(u.cm)

##Height of the inlet channel overflow weir above the normal water level in the inlet channel so that the far side of the overflow weir does not fill with water under normal operating conditions. This means the water level in the inlet channel will increase when the inlet overflow weir is in use.
HEIGHT_SED_INLET_WEIR_FREE_BOARD=2*(u.cm)

##Exit launder
## Target headloss through the launder orifices
HEADLOSS_SED_LAUNDER_BOD=4*(u.cm)

##Acceptable ratio of min to max flow through the launder orifices
RATIO_FLOW_LAUNDER_ORIFICES=0.80

##Center to center spacing of orifices in the launder
DIST_CENTER_SED_LAUNDER_EST=10*(u.cm)

##The additional length needed in the launder cap pipe that is to be inserted into the launder coupling
LENGTH_SED_LAUNDER_CAP_EXCESS=3*(u.cm)

##Space between the top of the plate settlers and the bottom of the launder pipe
HEIGHT_LAMELLA_TO_LAUNDER=5*(u.cm)

##The additional length needed in the launder cap pipe that is to be inserted into the launder coupling

##Diameter of the pipe used to hold the plate settlers together
NOM_DIAMETER_SED_MOD=0.5*(u.inch)

##Diameter of the pipe used to create spacers. The spacers slide over the 1/2" pipe and are between the plates
NOM_DIAMETER_SED_MOD_SPACER=(3/4)*(u.inch)

##This is the vertical thickness of the lip where the lamella support sits. mrf222
THICKNESS_SED_LAMELLA_LEDGE=8*(u.cm)

SPACE_SED_LAMILLA_PIPE_TO_EDGE=5*(u.cm)

##Approximate x-dimension spacing between cross pipes in the plate settler support frame.
DIST_CENTER_SED_PLATE_FRAME_CROSS_EST=0.8*(u.m)

##Estimated plate length used to get an initial estimate of sedimentation tank active length.
LENGTH_SED_PLATE_EST=60*(u.cm)

##Pipe size of the support frame that holds up the plate settler modules
NOM_DIAMETER_SED_PLATE_FRAME=1.5*(u.inch)

##Floc weir

#Vertical distance from the top of the floc weir to the bottom of the pipe frame that holds up the plate settler modules
HEIGHT_FLOC_WEIR_TO_PLATE_FRAME=10*(u.cm)

## Minimum length (X dimension) of the floc hopper
LENGTH_SED_HOPPER_MIN=50*(u.cm)

##Inlet manifold
##Max energy dissipation rate in the sed diffuser outletS
ENERGY_DIS_SED_INT_MAX=150*(u.mW/u.kg)

##Ratio of min to max flow through the inlet manifold diffusers
RATIO_FLOW_SED_INLET=0.8

NOM_DIAMETER_SED_MANIFOLD_MAX=8*(u.inch)

##This is the minimum distance between the inlet manifold and the slope of the sed tank.
SPACE_SED_INLET_MAN_SLOPE=10*(u.cm)

##  Length of exposed manifold stub coming out of the floc weir to which the free portion of the inlet manifold is attached with a flexible coupling
LENGTH_SED_MAN_CONNECTION_STUB=4*(u.cm)

##Space between the end of the manifold pipe and the edge of the first diffuser's hole, or the first manifold orifice

LENGTH_SED_MANIFOLD_FIRST_DIFFUSER_GAP=3*(u.cm)

##Vertical distance from the edge of the jet reverser half-pipe to the tip of the inlet manifold diffusers
HEIGHT_JET_REVERSER_TO_DIFFUSERS=3*(u.cm)

##Gap between the end of the inlet manifold pipe and the end wall of the tank to be able to install the pipe
LENGTH_SED_MANIFOLD_PIPE_FROM_TANK_END=2*(u.cm)

##Assumed stretch of the PVC pipes as they are heated and molded
RATIO_PVC_STRETCH=1.2

LENGTH_SED_WALL_TO_DIFFUSER_GAP_MIN=3*(u.cm)

##Diameter of the holes drilled in the manifold so that the molded 1" diffuser pipes can fit tightly in place (normal OD of a 1" pipe is close to 1-5/16")
DIAM_SED_MANIFOLD_PORT=1.25*(u.inch)

##Outlet to filter
#If the plant has two trains, the current design shows the exit channel continuing from one set of sed tanks into the filter inlet channel. The execution of this extended channel involves a few calculations
HEADLOSS_SED_TO_FILTER_PIPE_MAX=10*(u.cm)
if EN_DOUBLE_TRAIN==1:
    K_SED_EXIT=1
else:
    K_SED_EXIT=0


if EN_DOUBLE_TRAIN==1: 
   HEIGTH_EXIT_FREE=5*(u.cm)
else:
   HEIGTH_EXIT_FREE=0*(u.cm)

##added 12/5/16 by mrf222 ensures weir does not overtop backwards if filter weir is too high
HEIGHT_SED_WEIR_FREE_BOARD=5*(u.cm)



####Flocculator
##The minor loss coefficient is 2. According to measurements at Agalteca and according to https://confluence.cornell.edu/display/AGUACLARA/PAHO+Water+Treatment+Publications (page 100 in chapter on flocculation)  
HEIGHT_FLOC_OPTION=0

##Increased both to provide a safety margin on flocculator head loss and to simultaneously scale back on the actual collision potential we are trying to achieve.
K_MINOR_FLOC_BAFFLE=2.5

SPACE_FLOC_BAFFLE_SET_BACK_PLASTIC=2*(u.cm)

###Target flocculator collision potential basis of design
COLL_POT_FLOC_BOD=75*(u.m)**(2/3)

##Minimum J/S ratio for flocculator geometry that will provide optimal efficiency.
RATIO_J_S_OPT_MIN=3

##Ratio of the width of the gap between the baffle and the wall and the spacing between the baffles.
RATIO_FLOC_BAFFLE=1

##Max energy dissipation rate in the flocculator, basis of design.
ENERGY_DIS_FLOC_BOD=10*(u.mW/u.kg)

TIME_FLOC_DRAIN=15*(u.min)

NOM_DIAM_FLOC_MOD=(1/2)*(u.inch)

NOM_DIAM_FLOC_SPACER=(3/4)*(u.inch)

SPACE_FLOC_MOD_EDGE_TO_LAST_PIPE=10*(u.cm)

NOM_DIAM_FLOC_RM_RESTRAINER=(1/2)*(u.inch)

###Height that the drain stub extends above the top of the flocculator wall
LENGTH_FLOC_DRAIN_STUB_EXT=20*(u.cm)

SPACE_FLOC_MOD_PIPE_TO_EDGE=10*(u.cm)

THICKNESS_FLOC_BAFFLE=2*(u.mm)
