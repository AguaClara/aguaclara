#-*- coding: utf-8 -*-
"""This file contains constants which represent physical properties and
scientific principles which will be used in AguaClara plant design.

"""
from aguaclara.core.units import unit_registry as u
import aguaclara.core.pipedatabase as pipe
import numpy as np

#####tabulated constants

GRAVITY = 9.80665 * u.m/u.s**2

#Density of water
DENSITY_WATER = 1000 * u.kg/u.m**3

#The kinematic viscosity of water
NU_WATER = 1 * 10**-6 * u.m**2/u.s

#The influence of viscosity on mixing in jet reactors
RATIO_JET_ROUND = 0.5

#This is an estimate for plane jets as created in the flocculator and
# in the sed tank jet reverser.
RATIO_JET_PLANE = 0.225

RATIO_VC_ORIFICE = 0.63

P_ATM = 1*u.atm

#Needed for the filter siphon design
NU_AIR = 12 *u.mm**2/u.s

#Needed for the filter siphon design
RHO_AIR = 1.204 * u.kg/u.mm**3

####General assumptions and constants

PLANT_ORIGIN=[0, 0, 0] * u.m

COUNTRY = 0

LANGUAGE = 0

#Prompts the transition to a low flow plant
FLOW_PLANT_MAX_LF = 16.1 * u.L/u.s

WIDTH_HUMAN_MIN = 0.5 * u.m

#The height of the walkway above the drain channel bottom so that
# someone can walk through the drain channel.
HEIGHT_HUMAN_ACCESS = 1.5 * u.m

#Used to set the minimum height of entrance, floc, and sed walls
HEIGHT_PLANT_FREE_BOARD = 0.1 * u.m

#Minimum space between fittings in a tank or fittings and the wall of
# the tank.
SPACE_FITTING = 5 * u.cm

#Minimum channel width for constructability
WIDTH_CHANNEL_MIN = 15 * u.cm

#RATIO_RECTANGULAR is defined as the optimum "height over width ratio"
# (1/2) for a rectangular open channel
RATIO_RECTANGULAR = 0.5

##Equals 1 to draw boxes showing max water levels, 0 normally
#EN_WATER=0 #ASK Monroe

##If EN_WATER is set to 1, this controls the filter operation mode for
# which water/sand elevations are drawn. 0 for terminal, 1 for clean bed,
# and 2 for backwash.
#EN_WATER=2 #ASK Monroe

WIDTH_DOOR = 1 * u.m

THICKNESS_ACRYLIC = 1 * u.cm

#Due to a 24 in LFOM because that's the biggest pipe we have in our
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

#####Flow orifice meter

#Maximum number of rows or orifices in lfom.
RATIO_LFOM_ORIFICE = 10

#Safety coefficient that ensures free fall at the bottom of the lfom pipe
RATIO_LFOM_SAFETY = 1.5

#Minimum safety coefficient for lfom pipe diameter; only reduced
# between 55 L/s and 70 L/s - the intermediate zone between the using an
# LFOM pipe and an LFOM channel.
#It may be possible to eliminate this if we switch to plate LFOM at 50 Lp
RATIO_LFOM_SAFETY_MIN = 1.15

#Minimum head loss through linear orifice meter
HEADLOSS_LFOM_MIN = 20 * u.cm

#Maximum head loss through linear orifice meter to be used as needed for high flow plants.
HEADLOSS_LFOM_MAX = 40 * u.cm

#Changed from 12 in by pc479 because this is not a constraint anymore
# because we don't have an elbow constraining us. LFOM still needs to fit
# in the entrance tank. Need to check this constraint (mrf222)
NOM_DIAM_LFOM_PIPE_MAX = 36 * u.inch

HEIGHT_LFOM_FREEFALL = 10 * u.cm

#Enumerated type that selects between pipe(1) and plate(0) for the LFOM
def en_lfom_pipe(flow_plant):
    if flow_plant >= 80 * u.L/u.s:
        return 0
    else:
        return 1

####entrance tank

#Used to make a smaller entrance tank if the source water doesn't contain grit.
##0 if we want entrance tank sized to capture grit, 1 for minimum size
##EN_GRIT=0    ASK Monroe

##0 if there is only one inlet, 1 if there is two inlet
##EN_TWO_INLETS=0

#Angle of the sloped walls of the entrance tank hoppers
ANGLE_ENT_TANK_SLOPE = 45 * u.deg

#Extra space around the float (increase in effective diameter) to ensure
# that float has free travel
SPACE_ENT_TANK_FLOAT = 5 * u.cm

#Increased to get better mixing (10/10/2015 by Monroe)
ENERGY_DIS_RAPID_MIX = 3 * u.W/u.kg

#Distance that the rapid mix coupling extends into the first floc channel
# so that the RM orifice place can be fixed in place.
LENGTH_FLOC_COUPLING_EXT = 5 * u.cm

WIDTH_ENT_TANK_HOPPER_PEAK = 3 * u.cm

#Distance from the front wall to the pipe stubs in the hopper drains so
# that an operator can easily reach them.
LENGTH_ENT_TANK_WALLTODRAIN_MAX = 40 * u.cm

#Entrance tank capture velocity
VEL_ENT_TANK_CAPTURE_BOD = 8 * u.mm/u.s

AN_ENT_TANK_PLATE = 50 * u.deg

SPACE_ENT_TANK_PLATE = 2.5 * u.cm

THICKNESS_ENT_TANK_PLATE = 2 * u.mm

DIST_CENTER_ENT_TANK_PLATE = SPACE_ENT_TANK_PLATE + THICKNESS_ENT_TANK_PLATE

NOM_DIAM_ENT_TANK_MOD = 0.5 * u.inch

NOM_DIAM_ENT_TANK_MOD_SPACER = 0.75 * u.inch

#Thickness of the PVC disk used as the float for the chemical dose
# controller lever arm.
THICKNESS_ENT_TANK_FLOAT = 5 * u.cm

SPACE_ENT_TANK_LAMINA_PIPETOEDGE = 5 * u.cm

NOM_DIAM_RAPID_MIX_PLATE_RESTRAINER = 0.5 * u.inch

#Nom diam of the pipes that are embedded in the entrance tank slope
# to support the plate settler module
NOM_DIAM_ENT_TANK_PLATE_SUPPORT = 3 * u.inch

####chemical dose controller

##0 is alum, 1 is PACl
##EN_COAG=1

M_COAG_SACK = 25 * u.kg

#The coagulant stock is relatively stable and can last many days. Here we
# set the minimum time the coagulant stock will last when applying the
# maximum possible dose to size the stock tanks. In general the dose will
# be less than this and the stock will last much longer.
TIME_COAG_STOCK_MIN_EST = 1 * u.day

#Want chlorine stock to run out on average every day so that the stock
# is made fresh frequently because the chlorine stock degrades with time
# depending on temperature, concentration, and pH.
TIME_CHLOR_STOCK_AVE = 1 * u.day

ID_COAG_TUBE = 0.125 * u.inch
#1/8" tubes are readily available in hardware stores in Honduras
ID_CHLOR_TUBE = 0.125 * u.inch

CONC_COAG_STOCK_EST = 150 * u.g/u.L

CONC_CHLOR_STOCK_EST1 = 15 * u.g/u.L

P_CHLOR = 0.7

#This is the elevation difference between the outlet of the coagulant
# stock tanks and the water level in the constant head tank, which is set
# by the hydraulic head required to provide the desired max chemical flow
# rate through the float valve orifice in the CHT.
#It is treated as constant here to ensure a practical elevation difference
# is left between the stock tanks and the CHT even when a float valve is
# selected which requires very little hydraulic head to deliver the
# required maximum chemical flow rate.
HEIGHT_COAG_TANK_ABOVE_HEAD_TANK = 30 * u.cm

#This is the distance from the bottom of the stock tanks to the outlets
# to allow space for solids to settle.
DIST_CENTER_STOCK_OUTLET = 10 * u.cm

#Distance between a tank and the border of the platform
SPACE_CHEM_TANK_BORDER = 5 * u.cm

#This is the estimated elevation difference between the water level in
# the constant head tank and the top of the entrance tank wall.
#The constant head tank water level is the same as the elevation of the
# outlet of the dosing tube when the lever arm is horizontal (zero flow).
#Therefore this height depends only on the hardware used to make the
# slider/drop tube assembly and to mount the lever arm to the entrance
# tank wall.
#Note that this will vary depending on hardware used, and is only
# defined here to calculate the elevation of the stock tanks, which can
# be approximate.
HEIGHT_DOSER_ASSEMBLY = 6.77 * u.cm

#Maximum error allowed between a linear flow vs tube head loss
# relationship and the actual performance (which is affected by non-linear
# minor losses), assuming calibration at the maximum flow rate.
RATIO_LINEAR_CDC_ERROR = 0.1

#Estimated minor loss coefficient for the small-diameter flexible tubing
# using fittings that have larger ID than the tubing.
K_MINOR_CDC_TUBE = 2

#Head loss through the doser at maximum flow rate.
#Maximum head loss through the small-diameter dosing tubing, which
# corresponds to the variation in water levels in the entrance tank and
# the difference between the maximum and minimum elevation of the dosing
# tube outlet attached to the lever arm.
HEADLOSS_CDC = 20 * u.cm

#Estimated distance between fluid level in constant head tank and float valve orifice
HEIGHT_CDC_FLOAT_VALVE = 5 * u.cm

#Nominal diameter of the PVC plumbing for the chlorine dosing system.
NOM_DIAM_CHLOR_PIPE = 0.5 * u.inch

#Nominal diameter of the PVC plumbing for the coagulant dosing system.
NOM_DIAM_COAG_PIPE = 0.5 * u.inch

#Supplier Information:
# http://www.rotoplas.com/assets/files/industria/catalogo.pdf
#5-gallon bucket
# http://www.mcmaster.com/#storage-buckets/=kd23oh
#35-gallon drum
# http://www.jlmovingsupplies.com/c31/DIXIE-OPEN-CLOSED-HEAD-DRUMS-p36721.html
VOL_CHEM_TANK_AVAIL = [5 * u.gal, 35 * u.gal, 55 * u.gal,
                       450 * u.L, 750 * u.L, 1100 * u.L, 2500 * u.L]

DIAM__CHEM_TANK_AVAIL = [11.875 * u.inch, 20.75 * u.inch, 22.5 * u.inch,
                         0.85 * u.m, 1.10 * u.m, 1.10 * u.m, 1.55 * u.m]

HEIGHT_CHEM_TANK_AVAIL = [17.75 * u.inch, 31.75 * u.inch, 33.5 * u.inch,
                          0.99 * u.inch, 1.02 * u.inch, 1.39 * u.inch,
                          1.65 * u.inch]

####Chemical dose controller dimensions (based on inserted drawings)

#st587 addition
LENGTH_CDC_LEVER_ARM = 0.5 * u.m

DIAM_CDC_LEVER_CYLINDER1 = 1 * u.inch

DIAM_CDC_LEVER_CYLINDER4 = 2 * u.inch

DIAM_CDC_LEVER_CYLINDER_2 = 0.5 * u.inch

LENGTH_CDC_LEVER_PIVOTTO_CYLINDER2 = 6 * u.cm

LENGTH_CDC_LEVER_CYLINDER_2TO3 = 9.5 * u.cm

LENGTH_CDC_LEVER_PIVOT_BOX = 2 * u.inch

WIDTH_CDC_LEVER_PIVOT_BOX = 1 * u.inch

HEIGHT_CDC_LEVER_PIVOT_BOX = 1 * u.inch

THICKNESS_CDC_LEVER_ARM = 0.125 * u.inch

HEIGHT_CDC_LEVER_ARM = 1 * u.inch

LENGTH_CDC_LEVER_INNERBAR = 7 * u.inch

LENGTH_CDC_LEVER_MOUNTING_PLATE = 6 * u.inch

WIDTH_CDC_LEVER_MOUNTING_PLATE = 0.5 * u.cm

HEIGHT_CDC_LEVER_MOUNTING_PLATE = 2 * u.inch

SPACE_LEVER_TO_ENT_TANK_Z_TOP = 1 * u.cm

THICKNESS_CDC_FLOAT = 5 * u.cm

DIAM_CDC_FLOAT_CABLE = 0.5 * u.cm

LENGTH_CDC_LEVER_SLIDER_ORIGIN_TO_SCREW = 1 * u.inch

THICKNESS_CDC_LEVER_SLIDER = 0.25 * u.inch

HEIGHT_CDC_LEVER_SLIDER = 1.5 * u.inch

LENGTH_CDC_LEVER_SLIDER = 3 * u.inch

HEIGHT_CDC_LEVER_SLIDER_SHORT = 0.125 * u.inch

LENGTH_CDC_LEVER_CYLINDER = 6 * u.inch

LENGTH_ENT_TANK_FRONT_WALL_TO_CDC_FLOAT = 0.874 * u.m

LENGTH_CDC_LEVER = 0.5 * u.m #This may be obsolete now... mrf222 2/10/16

WIDTH_LEVER_ARM = 0.0032 * u.m

HEIGHT_LEVER_ARM = 0.0254 * u.m

DIAM_CDC_CHT = 6 * u.inch

#Distance from the top of the entrance tank to the to the middle of the
# lever arm hole for the cable - (minus the) radius of the hole.
HEIGHT_LEVER_HOLE = 0.0132 * u.m - (0.0095/2 * u.m)

DIAM_CABLE = 0.1 * u.inch

#Edited DLABOrigintoLAOriginZ to accommodate dimensions from McMaster
# vs Inserted Drawing
DIAM_LAB_ORIGIN_TO_LA_ORIGIN_Z = 0.0245 * u.m

#Distance from the lever arm origin to the outside center of the top part
# of the drop tube in the y direction.
LENGTH_LA_ORIGIN_TO_DT_Y = 0.7812 * u.m

#Distance from the lever arm origin to the drop tube in the z direction.
LENGTH_LA_ORIGIN_TO_DT_Z = 0.0429 * u.m

#Distance from the lever arm origin to the center of the drop tube in the
#x direction.
LENGTH_LA_ORIGIN_TO_DT_CENTER_X = 0.0290 * u.m

#Measured from CDC research team's apparatus.
THICKNESS_CDC_REDUCER = 9.5 * u.mm

#Distance from the lever arm origin to the center of the reducer in the
# x direction.
LENGTH_LA_ORIGIN_TO_REDUCER_X = 0.0290 * u.m

#Distance from the lever arm origin to the outside center of the top part
# of the reducer in the y direction.
LENGTH_LA_ORIGIN_TO_REDUCER_Y = 0.7135 * u.cm

#Distance from the lever arm origin to the center of the reducer in the
# x direction.
LENGTH_LA_ORIGIN_TO_REDUCER_CENTER_X = 0.0290 * u.m

#Distance from the lever arm origin to the center of the reducer in the
# y direction.
LENGTH_LA_ORIGIN_TO_REDUCER_CENTER_Y = 0.7919 * u.m

WIDTH_LEVER_BRACKET = 0.625 * u.inch

LENGTH_LEVER_BRAKCET = 1.5 * u.inch

RADIUS_LA_BAR = 0.375 * u.inch

THICKNESS_LEVER_BRACKET = 0.08 * u.inch

DIAM_LA_BAR = 0.375 * u.inch

LENGTH_LA_BAR = 4 * u.inch

LENGTH_SLIDER = 3 * u.inch

WIDTH_SLIDER = 3.2 * 10**-3 * u.m

NOM_DIAM_DROPTUBE = 0.5 * u.inch

HEIGHT_SLIDER = 0.625 * u.inch

LENGTH_DROPTUBE = 0.61 * u.m

#The length of the drop tube needs to be calculated. The drop tube must be
# as long as the supercritical flow.
#Thus the drop tube must extend down to the elevation of the sed tank
# effluent weir. This constant should be removed!

#Outer diameter of fitting- measured from CDC research team's fittin
OUTER_DIAM_CDC_FITTING = 5/32 * u.inch

#Inner diameter of fitting- measured from CDC research team's fitting
ID_CDC_FITTING = 0.126 * u.inch

#Length of fitting - measured from CDC research team's fitting
LENGTH_CDC_FITTING = 0.75 * u.inch

#st587 addition
##Constant Head Tank Dimensions

#five gallons bucket dimensions for constant head tanks

DIAM_CHT = 10 * u.cm

HEIGHT_CHT = 37/3 * u.cm

THICKNESS_CHT_WALL = 1/3 * u.cm

NOM_DIAM_DELIVERY_PIPE = 0.6 * u.inch

PIPE_SCHEDULE_FLEX_TUBE = 2

LENGTH_PVC_BALL_VALVE = 0.1625/4 * u.cm

THICKNESS_MOUNTING_BOARD = 1.5 * u.inch

##Manifold Dimensions

SPACE_CDC_LEVER_TO_MANIFOLD = 40 * u.cm

LENGTH_CHLOR_AIR_RELEASE_PIPE = 30 * u.cm #Arbitratily selected


####Flocculator
##The minor loss coefficient is 2. According to measurements at Agalteca
# and according to
# https://confluence.cornell.edu/display/AGUACLARA/PAHO+Water+Treatment+Publications
# (page 100 in chapter on flocculation)
HEIGHT_FLOC_OPTION = 0

##Increased both to provide a safety margin on flocculator head loss and
# to simultaneously scale back on the actual collision potential we are
# trying to achieve.
K_MINOR_FLOC_BAFFLE = 2.5

SPACE_FLOC_BAFFLE_SET_BACK_PLASTIC= 2 * u.cm

###Target flocculator collision potential basis of design
COLL_POT_FLOC_BOD = 75 * u.m**(2/3)

##Minimum width of flocculator channel required for constructability based
# on the width of the human hip
FLOC_WIDTH_MIN_CONST = 45 * u.cm

##Minimum and maximum distance between expansions to baffle spacing ratio for
#flocculator geometry that will provide optimal efficiency.
RATIO_HS_MIN = 3
RATIO_HS_MAX = 6

##Ratio of the width of the gap between the baffle and the wall and the
# spacing between the baffles.
RATIO_FLOC_BAFFLE = 1

##Max energy dissipation rate in the flocculator, basis of design.
ENERGY_DIS_FLOC_BOD = 10* u.mW/u.kg

TIME_FLOC_DRAIN = 15 * u.min

NOM_DIAM_FLOC_MOD = 0.5 * u.inch

NOM_DIAM_FLOC_SPACER = 0.75 * u.inch

SPACE_FLOC_MOD_EDGE_TO_LAST_PIPE = 10 * u.cm

NOM_DIAM_FLOC_RM_RESTRAINER = 0.5 * u.inch

###Height that the drain stub extends above the top of the flocculator wall
LENGTH_FLOC_DRAIN_STUB_EXT = 20 * u.cm

SPACE_FLOC_MOD_PIPE_TO_EDGE = 10 * u.cm

THICKNESS_FLOC_BAFFLE = 2 * u.mm



###Sedimentation tank
##General

VEL_SED_UP_BOD = 1 * u.mm/u.s

##Plate settler
VEL_SED_CONC_BOD = 0.12 * u.mm/u.s  # capture velocity

ANGLE_SED_PLATE = 60 * u.deg

SPACE_SED_PLATE = 2.5*u.cm

N_SED_MODULE_PLATES_MIN = 8

# This is moved to template because THICKNESS_SED_PLATE is in materials.yaml
# DIST_CENTER_SED_PLATE = SPACE_SED_PLATE + THICKNESS_SED_PLATE

# Bottom of channel
ANGLE_SED_SLOPE = 50 * u.deg

##This slope needs to be verified for functionality in the field.
# A steeper slope may be required in the floc hopper.
ANGLE_SED_HOPPER_SLOPE = 45 * u.deg

HEIGHT_WATER_SED_EST = 2 * u.m

SED_GATE_VALVE_URL = "https://confluence.cornell.edu/download/attachments/173604905/Sed-Scaled-Gate-Valve-Threaded.dwg"

SUPPORT_BOLT_URL = "https://confluence.cornell.edu/download/attachments/173604905/PlateSettlerSupportBolt.dwg"

##Inlet channel
HEADLOSS_SED_WEIR_MAX = 5 * u.cm

##Height of the inlet channel overflow weir above the normal water level
# in the inlet channel so that the far side of the overflow weir does not
# fill with water under normal operating conditions. This means the water
# level in the inlet channel will increase when the inlet overflow weir
# is in use.
HEIGHT_SED_INLET_WEIR_FREE_BOARD = 2 * u.cm

THICKNESS_SED_WEIR = 5*u.cm

HL_SED_INLET_MAX = 1 * u.cm

# ratio of the height to the width of the sedimentation tank inlet channel.
RATIO_HW_SED_INLET = 0.95

##Exit launder
##Target headloss through the launder orifices
HEADLOSS_SED_LAUNDER_BOD = 4 * u.cm

##Acceptable ratio of min to max flow through the launder orifices
RATIO_FLOW_LAUNDER_ORIFICES = 0.80

##Center to center spacing of orifices in the launder
DIST_CENTER_SED_LAUNDER_EST = 10 * u.cm

##The additional length needed in the launder cap pipe that is to be
# inserted into the launder coupling
LENGTH_SED_LAUNDER_CAP_EXCESS = 3 * u.cm

##Space between the top of the plate settlers and the bottom of the
# launder pipe
HEIGHT_LAMELLA_TO_LAUNDER = 5 * u.cm

##The additional length needed in the launder cap pipe that is to be
# inserted into the launder coupling

##Diameter of the pipe used to hold the plate settlers together
NOM_DIAMETER_SED_MOD = 0.5 * u.inch

##Diameter of the pipe used to create spacers. The spacers slide over the
# 1/2" pipe and are between the plates
NOM_DIAMETER_SED_MOD_SPACER = 0.75 * u.inch

SDR_SED_MOD_SPACER = 17

##This is the vertical thickness of the lip where the lamella support sits. mrf222
THICKNESS_SED_LAMELLA_LEDGE = 8 * u.cm

SPACE_SED_LAMELLA_PIPE_TO_EDGE = 5 * u.cm

##Approximate x-dimension spacing between cross pipes in the plate settler
# support frame.
DIST_CENTER_SED_PLATE_FRAME_CROSS_EST = 0.8 * u.m

##Estimated plate length used to get an initial estimate of sedimentation
# tank active length.
LENGTH_SED_PLATE_EST = 60 * u.cm

##Pipe size of the support frame that holds up the plate settler modules
NOM_DIAMETER_SED_PLATE_FRAME = 1.5 * u.inch

##Floc weir

#Vertical distance from the top of the floc weir to the bottom of the pipe
# frame that holds up the plate settler modules
HEIGHT_FLOC_WEIR_TO_PLATE_FRAME = 10 * u.cm

##Minimum length (X dimension) of the floc hopper
LENGTH_SED_HOPPER_MIN = 50 * u.cm

##Inlet manifold
##Max energy dissipation rate in the sed diffuser outletS
ENERGY_DIS_SED_INT_MAX = 150 * u.mW/u.kg

##Ratio of min to max flow through the inlet manifold diffusers
RATIO_FLOW_SED_INLET = 0.8

ND_SED_MANIFOLD_MAX = 8 * u.inch

SDR_SED_MANIFOLD = 41  # SDR of pipe for sed tank inlet manifold

##This is the minimum distance between the inlet manifold and the slope
# of the sed tank.
SPACE_SED_INLET_MAN_SLOPE = 10 * u.cm

##Length of exposed manifold stub coming out of the floc weir to which the
# free portion of the inlet manifold is attached with a flexible coupling.
LENGTH_SED_MAN_CONNECTION_STUB = 4 * u.cm

##Space between the end of the manifold pipe and the edge of the first
# diffuser's hole, or the first manifold orifice.

LENGTH_SED_MANIFOLD_FIRST_DIFFUSER_GAP = 3 * u.cm

##Vertical distance from the edge of the jet reverser half-pipe to the tip
# of the inlet manifold diffusers
HEIGHT_JET_REVERSER_TO_DIFFUSERS = 3 * u.cm

##Gap between the end of the inlet manifold pipe and the end wall of the
# tank to be able to install the pipe
LENGTH_SED_MANIFOLD_PIPE_FROM_TANK_END = 2  *u.cm

LENGTH_SED_WALL_TO_DIFFUSER_GAP_MIN = 3 * u.cm

##Diameter of the holes drilled in the manifold so that the molded 1"
# diffuser pipes can fit tightly in place (normal OD of a 1" pipe is
# close to 1-5/16")
DIAM_SED_MANIFOLD_PORT = 1.25 * u.inch

ND_JET_REVERSER = 3 * u.inch  # nominal diameter of pipe used for jet reverser in bottom of set tank

SDR_REVERSER = 26  # SDR of jet reverser pipe

## Diffuser geometry
SDR_DIFFUSER = 26  # SDR of diffuser pipe

ND_DIFFUSER_PIPE = 4 * u.cm  # nominal diameter of pipe used to make diffusers

AREA_PVC_DIFFUSER = (np.pi/4) * ((pipe.OD(ND_DIFFUSER_PIPE)**2)
                                 - (pipe.ID_SDR(ND_DIFFUSER_PIPE, SDR_DIFFUSER))**2)

RATIO_PVC_STRETCH = 1.2  # stretch factor applied to the diffuser PVC pipes as they are heated and molded

T_DIFFUSER = ((pipe.OD(ND_DIFFUSER_PIPE) -
                        pipe.ID_SDR(ND_DIFFUSER_PIPE, SDR_DIFFUSER))
                              / (2 * RATIO_PVC_STRETCH))

W_DIFFUSER_INNER = 0.3175 * u.cm  # opening width of diffusers

# Calculating using a minor loss equation with K = 1
V_SED_DIFFUSER_MAX = np.sqrt(2 * GRAVITY * HL_SED_INLET_MAX).to(u.mm/u.s)

L_DIFFUSER = 15 * u.cm  # vertical length of diffuser

B_DIFFUSER = 5 * u.cm  # center to center spacing beteen diffusers

HEADLOSS_SED_DIFFUSER = 0.001 * u.m # Headloss through the diffusers to ensure uniform flow between sed tanks

##Outlet to filter
#If the plant has two trains, the current design shows the exit channel
# continuing from one set of sed tanks into the filter inlet channel.
#The execution of this extended channel involves a few calculations.
HEADLOSS_SED_TO_FILTER_PIPE_MAX = 10 * u.cm
#==============================================================================
# if EN_DOUBLE_TRAIN == 1:
#     K_SED_EXIT = 1
# else:
#     K_SED_EXIT = 0
#
#
# if EN_DOUBLE_TRAIN == 1:
#    HEIGHT_EXIT_FREE = 5 * u.cm
# else:
#    HEIGHT_EXIT_FREE = 0 * u.cm
#==============================================================================

##added 12/5/16 by mrf222 ensures weir does not overtop backwards if
# filter weir is too high
HEIGHT_SED_WEIR_FREE_BOARD = 5 * u.cm



##Stacked rapid sand filter
####Construction and Design Inputs

#Design guidelines say 11 mm/s. The success of lab-scale backwashing at
# 10 mm/s suggests that this is a reasonable and conservative value
VEL_FILTER_Bw_ = 11 * u.mm/u.s

N_FILTER_LAYER = 6

VEL_FILTER_LAYER = 1.833 * u.mm/u.s ##VEL_FIBER_DIST_CENTER_/N_FIBER_LAYER

##Minimum thickness of each filter layer (can be increased to accomodate
# larger pipe diameters in the bottom layer)
HEIGHT_FILTER_LAYER_MIN = 20 * u.cm

##center to center distance for slotted pipes
DIST_CENTER_FILTER_MANIFOLD_BRANCH = 10 * u.cm

##How far the branch extends into the trunk line
LENGTH_FILTER_MAN_BRANCH_EXT = 2 * u.cm

##The time to drain the filter box of the water above the fluidized bed
TIME_FIBER_BACKWASH_INITIATION_BOD = 3 * u.min

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
NOM_DIAMETER_FILTER_SAND_OUTLET = 2 * u.inch

##Height of the barrier between the exit box and distribution box.
HEIGHT_FILTER_DIST_BARRIER = 10 * u.cm

##Length that the siphon pipe extends up into the plant drain channel.
#Being able to shorten the stub from which the siphon discharges into the
# main plant drain channel allows for some flexibility in the hydraulic design.
LENGTH_FILTER_SIPHON_CHANNEL_STUB_MIN = 20 * u.cm

HEADLOSS_FILTER_ENTRANCE_PIPE_MAX = 10 * u.cm

NOM_DIAMETER_FILTER_TRUNK_MAX = 6 * u.inch

NOM_DIAMETER_FILTER_BACK_WASH_SIPHON_MAX = 8 * u.inch

##Purge valves on the trunk lines are angled downwards so that sediment is
# cleared more effectively. This angle allows the tees to fit on top of one
# another at the filter wall.
ANGLE_FILTER_TRUNK_VALVES = 25 * u.deg

##Purge valves on the trunk lines are angled downwards so that sediment is
# cleared more effectively. This angle allows the tees to fit on top of one
# another at the filter wall.
THICKNESS_FILTER_WEIR = 5 * u.cm

SPACE_FILTER_BRANCH_TO_WALL = 5 * u.cm

FILTER_GATE_VALUE_URL = "https://confluence.cornell.edu/download/attachments/173604905/Fi-Scaled-Gate-Valve-Threaded.dwg"
FILTER_BALL_VALVE_URL = "https://confluence.cornell.edu/download/attachments/173604905/FiMetalBallValve.dwg"

HEIGHT_FILTER_WALL_TO_PLANT_FLOOR_MIN = 10 * u.cm

HEADLOSS_FILTER_INLET_WEIR_MAX = 5 * u.cm

##Dimensions get too small for construction below a certain flow rate
FLOW_FILTER_MIN = 8 * u.L/u.s

LENGTH_FILTER_MAN_FEMCO_COUPLING = 6 * u.cm

##Nominal diameter of the spacer tees in the four corners of the filter
# manifold assembly.
NOM_DIAMETER_FILTER_MAN_WING_SPACER = 2 * u.inch

##Length of the vertical pipe segment following the valve on the filter
# sand drain. This stub can be capped to allow the sand in the valve to
# settle, so that the valve can be closed without damage from fluidized sand.
LENGTH_FILTER_SAND_OUTLET_PIPE = 20 * u.cm




#######Elevation Safety Margins

##Minimum depth in the entrance box during backwash such that there is
# standing water over the inlet.
HEIGHT_FILTER_BACKWASH_NO_SUCK_AIR = 20 * u.cm

##Minimum water depth over the orifices in the siphon manifold so that air
# is not entrained.
HEIGHT_FILTER_SIPHON_NO_SUCK_AIR = 10 * u.cm

HEIGHT_FILTER_FLUIDIZED_BED_TO_SIPHON = 20 * u.cm

HEIGHT_FILTER_FORWARD_NO_SUCK_AIR = 10 * u.cm

HEIGHT_FILTER_WEIR_FREEFALL = 3 * u.cm

HEIGHT_FILTER_AIR_REMOVAL_BLOCK_SUBMERGED = 5 * u.cm

HEIGHT_FILTER_BYPASS_SAFETY = 10 * u.cm

HEIGHT_DRAIN_OUTLET_SAFETY = 10 * u.cm

HEIGHT_FILTER_OVERFLOW_WEIR_FREEFALL = 10 * u.cm



#######Plant drain channel

###Space beyond the entrance tank in the plant drain channel where the
# drop pipes from the CDC lever arm can come down and be connected with
# the chlorine and coagulant dosing points.
LENGTH_CHEM_LEVER_ARM_SPACE = 75 * u.cm


###Operator access

##combine walkway assumptions!
WIDTH_MP_WALKWAY_MIN = 1 * u.m

##Width of the walkway above the main plant drain channel
WIDTH_DC_WALKWAY = 1.2 * u.m

##Width of the floor space between the flocculator and the rapid mix pipe
# floor cutout next to the entrance tank.
WIDTH_ET_WALKWAY = 1 * u.m

##for high flow, double train situations
W_TRAIN_WALKWAY = 1.5 * u.m

W_BASEMENT_STAIRS = 0.9 * u.m

W_ENTRANCE_STAIRS = 1.2 * u.m


##Minor loss coefficients
##Individual K Values

##90 deg elbow
K_MINOR_EL90 = 0.9

K_MINOR_EL45 = 0.45
##The loss coefficient for the channel transition in a 90 degree turn
K_MINOR_90 = 0.4

K_MINOR_ANGLE_VALVE = 4.3

K_MINOR_GLOBE_VALVE = 10

K_MINOR_GATE_VALVE = 0.39

K_MINOR_CHECK_VALVE_CONV = 4

K_MINOR_CHECK_VALVE_BALL = 4.5

##headloss coefficient of jet
K_MINOR_EXP = 1

K_MINOR_TEE_FLOW_RUN = 0.6

K_MINOR_TEE_FLOW_BR = 1.8

K_MINOR_PIPE_ENTRANCE = 0.5

K_MINOR_PIPE_EXIT = 1

K_MINOR_RM_GATE_VIN = 25
