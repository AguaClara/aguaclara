from aguaclara.core.units import u
from aguaclara.design.component import Component

class Filter(Component):

    sand_layer_thick = 20 *u.cm
    n_backwash_manifold_diameter = 4 * u.inch
    max_filtration_head_loss = 30 * u.cm

    @property
    def n_tanks():
        tank = math.ceil(self.q/40)
        return (tank.magnitude)*2

    @property
    def flow_rate_per_tank():
        n_tanks = n_tanks()
        return flow_rate/n_tanks

    #def filt_vel():

    #def backwash_vel():

    #def backwash_manifold_diameter():

#Design guidelines say 11 mm/s. The success of lab-scale backwashing at
# 10 mm/s suggests that this is a reasonable and conservative value
BACKWASH_VEL = 11 * u.mm / u.s

LAYER_N = 6

LAYER_VEL = 1.833 * u.mm / u.s ##VEL_FIBER_DIST_CENTER_/N_FIBER_LAYER

##Minimum thickness of each filter layer (can be increased to accomodate
# larger pipe diameters in the bottom layer)
LAYER_H_MIN = 20 * u.cm

##center to center distance for slotted pipes
MAN_CENTER_BRANCH_DIST = 10 * u.cm

##How far the branch extends into the trunk line
MAN_BRANCH_EXTENSION_L = 2 * u.cm

##The time to drain the filter box of the water above the fluidized bed
FIBER_BACKWASH_INITIATION_BOD_TIME = 3 * u.min

##Mickey suggested this value based on lab experience. This was moved to
# Expert Inputs 12/4/16 by mrf222 as a result of feedback from Monroe and
# Skyler. In the Moroceli plant, the Fi Entrance box was overflowing
# before filtration backwash. The HL of a dirty filter has therefore been
# increased from 40 to 60 cm.
HL_DIRTY = 60 * u.cm

##This is the extra head we are going to provide on top of steady state
# backwash head loss to ensure that we can fluidize the bed to initiate
# backwash.
HL_FIBER_BACKWASH_STEADY_FLOW = 20 * u.cm

##Maximum acceptable head loss through the siphon at steady state; used to
# calculate a diameter
SIPHON_HL_MAX = 35 * u.cm

##Diameter of sand drain pipe
SAND_OUTLET_D = 2 * u.inch

##Height of the barrier between the exit box and distribution box.
BARRIER_EXIT_DISTRIBUTION_H = 10 * u.cm

##Length that the siphon pipe extends up into the plant drain channel.
#Being able to shorten the stub from which the siphon discharges into the
# main plant drain channel allows for some flexibility in the hydraulic design.
SIPHON_CHANNEL_STUB_L_MIN = 20 * u.cm

ENTRANCE_PIPE_HL_MAX = 10 * u.cm

TRUNK_D_MAX = 6 * u.inch

BACKWASH_SIPHON_D_MAX = 8 * u.inch

##Purge valves on the trunk lines are angled downwards so that sediment is
# cleared more effectively. This angle allows the tees to fit on top of one
# another at the filter wall.
TRUNK_VALVES_ANGLE = 25 * u.deg

##Purge valves on the trunk lines are angled downwards so that sediment is
# cleared more effectively. This angle allows the tees to fit on top of one
# another at the filter wall.
WEIR_THICKNESS = 5 * u.cm

BRANCH_WALL_S = 5 * u.cm

GATE_VALUE_URL = "https://confluence.cornell.edu/download/attachments/173604905/Fi-Scaled-Gate-Valve-Threaded.dwg"
BALL_VALVE_URL = "https://confluence.cornell.edu/download/attachments/173604905/FiMetalBallValve.dwg"

WALL_PLANT_FLOOR_S_MIN = 10 * u.cm

INLET_WEIR_HL_MAX = 5 * u.cm

##Dimensions get too small for construction below a certain flow rate
Q_MIN = 8 * u.L / u.s

MAN_FEMCO_COUPLING_L = 6 * u.cm

##Nominal diameter of the spacer tees in the four corners of the filter
# manifold assembly.
MAN_WING_SPACER_ND = 2 * u.inch

##Length of the vertical pipe segment following the valve on the filter
# sand drain. This stub can be capped to allow the sand in the valve to
# settle, so that the valve can be closed without damage from fluidized sand.
SAND_OUTLET_PIPE_L = 20 * u.cm

#######Elevation Safety Margins

##Minimum depth in the entrance box during backwash such that there is
# standing water over the inlet.
BACKWASH_NO_SUCK_AIR_H = 20 * u.cm

##Minimum water depth over the orifices in the siphon manifold so that air
# is not entrained.
SIPHON_NO_SUCK_AIR_H = 10 * u.cm

FLUIDIZED_BED_TO_SIPHON_H = 20 * u.cm

FORWARD_NO_SUCK_AIR_H = 10 * u.cm

WEIR_FREEFALL_H = 3 * u.cm

AIR_REMOVAL_BLOCK_SUBMERGED_H = 5 * u.cm

BYPASS_SAFETY_H = 10 * u.cm

DRAIN_OUTLET_SAFETY_H = 10 * u.cm

OVERFLOW_WEIR_FREEFALL_H = 10 * u.cm

#We are going to take this pipe size for the slotted pipes as a given.
# Larger pipes may block too much flow and they are harder to install.
MAN_BRANCH_ND = 1*u.inch

MAN_BRANCH_BACKWASH_ND = 1.5*u.inch

#A slot thickness of 0.008 in or 0.2 mm is selected so that sand
# will not enter the slotted pipes.
MANIFOLD_SLOTS_W = 0.008*u.inch

BRANCH_HOLDER_ND = 2*u.inch

BACKWASH_BRANCH_HOLDER_ND = 2*u.inch

#Minimum vertical spacing between trunk line pipes going through
#the filter wall for concrete construction
TRUNK_S_MIN = 3 * u.cm

#Space between the ends of the branch receiver pipes and the walls so that
#the manifold assemblies are easy to lower into the filter boxes
# (if the branch receivers extended the entire length of the box they would
#just barely fit and it would be hard to get into place)
MAN_ASSEMBLY_S = 1 * u.cm

##Sand Properties

SAND_D_EFFECTIVE = 0.5 * u.mm

SAND_UNIFORMITY_RATIO = 1.65

DIAM_FILTER_SAND_60 = SAND_D_EFFECTIVE * SAND_UNIFORMITY_RATIO

#Porosity in a sand bed
SAND_POROSITY = 0.4

SAND_DENSITY = 2650 * u.kg / (u.m ** 3)

FLUIDIZED_RATIO = 1.3 #Bed expands 30% when fluidized
