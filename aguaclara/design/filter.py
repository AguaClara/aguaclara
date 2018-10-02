#Design guidelines say 11 mm/s. The success of lab-scale backwashing at
# 10 mm/s suggests that this is a reasonable and conservative value
VEL_FILTER_Bw_ = 11 * u.mm/u.s

N_FILTER_LAYER = 6

VEL_FILTER_LAYER = 1.833 * u.mm/u.s ##VEL_FIBER_DIST_CENTER_/N_FIBER_LAYER

##Minimum thickness of each filter layer (can be increased to accomodate
# larger pipe diameters in the bottom layer)
FILTER_LAYER_H_MIN = 20 * u.cm

##center to center distance for slotted pipes
CENTER_FILTER_MANIFOLD_BRANCH_DIST = 10 * u.cm

##How far the branch extends into the trunk line
FILTER_MAN_BRANCH_EXT_L = 2 * u.cm

##The time to drain the filter box of the water above the fluidized bed
FIBER_BACKWASH_INITIATION_BOD_TIME = 3 * u.min

##Mickey suggested this value based on lab experience. This was moved to
# Expert Inputs 12/4/16 by mrf222 as a result of feedback from Monroe and
# Skyler. In the Moroceli plant, the Fi Entrance box was overflowing
# before filtration backwash. The HL of a dirty filter has therefore been
# increased from 40 to 60 cm.
HEADLOSS_FILTER_DIRTY = 60 * u.cm

##This is the extra head we are going to provide on top of steady state
# backwash head loss to ensure that we can fluidize the bed to initiate
# backwash.
HEADLOSS_FIBER_BACKWASH_STEADY_FLOW = 20 * u.cm

##Maximum acceptable head loss through the siphon at steady state; used to
# calculate a diameter
HEADLOSS_FILTER_SIPHON_MAX = 35 * u.cm

##Diameter of sand drain pipe
NDETER_FILTER_SAND_OUTLET = 2 * u.inch

##Height of the barrier between the exit box and distribution box.
FILTER_DIST_BARRIER_H = 10 * u.cm

##Length that the siphon pipe extends up into the plant drain channel.
#Being able to shorten the stub from which the siphon discharges into the
# main plant drain channel allows for some flexibility in the hydraulic design.
FILTER_SIPHON_CHANNEL_STUB_MIN_L = 20 * u.cm

HEADLOSS_FILTER_ENTRANCE_PIPE_MAX = 10 * u.cm

NDETER_FILTER_TRUNK_MAX = 6 * u.inch

NDETER_FILTER_BACK_WASH_SIPHON_MAX = 8 * u.inch

##Purge valves on the trunk lines are angled downwards so that sediment is
# cleared more effectively. This angle allows the tees to fit on top of one
# another at the filter wall.
FILTER_TRUNK_VALVES_ANGLE = 25 * u.deg

##Purge valves on the trunk lines are angled downwards so that sediment is
# cleared more effectively. This angle allows the tees to fit on top of one
# another at the filter wall.
FILTER_WEIR_THICKNESS = 5 * u.cm

SPACE_FILTER_BRANCH_TO_WALL = 5 * u.cm

FILTER_GATE_VALUE_URL = "https://confluence.cornell.edu/download/attachments/173604905/Fi-Scaled-Gate-Valve-Threaded.dwg"
FILTER_BALL_VALVE_URL = "https://confluence.cornell.edu/download/attachments/173604905/FiMetalBallValve.dwg"

FILTER_WALL_TO_PLANT_FLOOR_H_MIN = 10 * u.cm

HEADLOSS_FILTER_INLET_WEIR_MAX = 5 * u.cm

##Dimensions get too small for construction below a certain flow rate
FLOW_FILTER_MIN = 8 * u.L/u.s

FILTER_MAN_FEMCO_COUPLING_L = 6 * u.cm

##Nominal diameter of the spacer tees in the four corners of the filter
# manifold assembly.
NDETER_FILTER_MAN_WING_SPACER = 2 * u.inch

##Length of the vertical pipe segment following the valve on the filter
# sand drain. This stub can be capped to allow the sand in the valve to
# settle, so that the valve can be closed without damage from fluidized sand.
FILTER_SAND_OUTLET_PIPE_L = 20 * u.cm

#######Elevation Safety Margins

##Minimum depth in the entrance box during backwash such that there is
# standing water over the inlet.
FILTER_BACKWASH_NO_SUCK_AIR_H = 20 * u.cm

##Minimum water depth over the orifices in the siphon manifold so that air
# is not entrained.
FILTER_SIPHON_NO_SUCK_AIR_H = 10 * u.cm

FILTER_FLUIDIZED_BED_TO_SIPHON_H = 20 * u.cm

FILTER_FORWARD_NO_SUCK_AIR_H = 10 * u.cm

FILTER_WEIR_FREEFALL_H = 3 * u.cm

FILTER_AIR_REMOVAL_BLOCK_SUBMERGED_H = 5 * u.cm

FILTER_BYPASS_SAFETY_H = 10 * u.cm

DRAIN_OUTLET_SAFETY_H = 10 * u.cm

FILTER_OVERFLOW_WEIR_FREEFALL_H = 10 * u.cm
