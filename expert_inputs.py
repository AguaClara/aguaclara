# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 15:54:16 2017

@author: Karan Newatia

Last modified Wed Jul 5 2017
By: Sage Weber-Shirk
"""
from AguaClara_design.units import unit_registry as u

##### Tabulated constants

# Density of water, in kilograms per cubic meter
DENSITY_WATER = 1000

# The kinematic viscosity of water, in square meters per second
NU_WATER = 1 * 10**-6

# The influence of viscosity on mixing in jet reactors
RATIO_JET_ROUND = 0.5

# This is an estimate for plane jets as created in the flocculator and in 
# the sed tank jet reverser.
RATIO_JET_PLANE = 0.225

RATIO_VC_ORIFICE = 0.63

#Atmospheric pressure
P_ATM = 1 * u.atm

# Needed for the filter siphon design, in square meters per second
NU_AIR = 1.2 * 10**-5

# Needed for the filter siphon design, in kilograms per cubic meter
RHO_AIR = 1.204

#### General assumptions and constants

PLANT_ORIGIN = [0, 0, 0] * u.m

COUNTRY = 0

LANGUAGE = 0

# Prompts the transition to a low flow plant, in cubic meters per second
FLOW_PLANT_MAX_LF = 0.0161

# Minimum width for human passage, in meters
WIDTH_HUMAN_MIN = 0.5

# The height of the walkway above the drain channel bottom so that someone 
# can walk through the drain channel, in meters.
HEIGHT_HUMAN_ACCESS = 1.5

# Used to set the minimum height of entrance, floc, and sed walls, in meters
HEIGHT_PLANT_FREE_BOARD = 0.1

# Minimum space between fittings in a tank or fittings and the wall of 
# the tank, in meters
SPACE_FITTING = 0.05

# Minimum channel width for constructability, in meters
WIDTH_CHANNEL_MIN = 0.15

# RATIO_RECTANGULAR is defined as the optimum "height over width ratio" (1/2)
# for a rectangular open channel
RATIO_RECTANGULAR = 0.5 

## Equals 1 to draw boxes showing max water levels, 0 normally
#EN_WATER=0 #ASK Monroe

##If EN_WATER is set to 1, this controls the filter operation mode for which 
# water/sand elevations are drawn. 0 for terminal, 1 for clean bed, and 
# 2 for backwash.
#EN_WATER=2 #ASK Monroe

# Width of a door, in meters
WIDTH_DOOR = 1

#Width of acrylics, in meters
THICKNESS_ACRYLIC = 0.01

# Due to a 24 in LFOM because that's the biggest pipe we have in our 
# database right now. if we need a bigger single train, we can do that by 
# adding that pipe size into the pipe database. 
# Given in cubic meters per second.
FLOW_TRAIN_MAX = 0.1501

@u.wraps(None, u.m**3/u.s, False)
def en_multiple_train(flow_plant):
    if flow_plant > 0.06:
        return 1
    else:
        return 0


@u.wraps(None, u.m**3/u.s, False)
def n_train(FlowPlant):
    if FlowPlant > 0.06:
        return 1
    elif FlowPlant > 0.06 and FlowPlant <= 0.12:
        return 2
    else:
        return 4


@u.wraps(u.m**3/u.s, u.m**3/u.s, False)
def flow_train(FlowPlant):
    return FlowPlant / n_train(FlowPlant).magnitude

##### Flow orifice meter

# Maximum number of rows or orifices in lfom.
RATIO_LFOM_ORIFICE = 10

#safety coefficient that ensures free fall at the bottom of the lfom pipe
RATIO_LFOM_SAFETY = 1.5

# Minimum safety coefficient for lfom pipe diameter; only reduced between 
# 55 L/s and 70 L/s - the intermediate zone between the using an LFOM pipe
# and an LFOM channel.
# It may be possible to eliminate this if we switch to plate LFOM at 50 Lp
RATIO_LFOM_SAFETY_MIN = 1.15

# Minimum head loss through linear orifice meter, in meters
HEADLOSS_LFOM_MIN = 0.2

# Maximum head loss through linear orifice meter to be used as needed for 
# high flow plants.
# Given in meters
HEADLOSS_LFOM_MAX = 0.4

#changed from 12 in by pc479 because this is not a constraint anymore 
# because we don't have an elbow constraining us. LFOM still needs to 
# fit in the entrance tank. Need to check this constraint (mrf222)
# This terminology allows the user to input the value in inches without 
# risking error in other conversion methods
NOM_DIAM_LFOM_PIPE_MAX = (36 * u.inch).to(u.m).magnitude

# Given in meters.
HEIGHT_LFOM_FREEFALL = 0.1

#enumerate type that selects between pipe(1) and plate(0) for the LFOM
@u.wraps(None, u.m**3/u.s, False)
def en_lfom_pipe(flow_plant):
    if flow_plant >= 0.08:
        return 0
    else:
        return 1

####entrance tank

# Used to make a smaller entrance tank if the source water doesn't contain grit.
# 0 if we want entrance tank sized to capture grit, 1 for minimum size
##EN_GRIT=0    ASK Monroe

# 0 if there is only one inlet, 1 if there is two inlet
##EN_TWO_INLETS=0

# Angle of the sloped walls of the entrance tank hoppers, in degrees
ANGLE_ENT_TANK_SLOPE = 45

# Extra space around the float (increase in effective diameter) to ensure 
# that float has free travel, in meters
SPACE_ENT_TANK_FLOAT = 0.05 

# Increased to get better mixing (10/10/2015 by Monroe)
# Given in Watts per kilogram
ENERGY_DIS_RAPID_MIX = 3

# Distance that the rapid mix coupling extends into the first floc channel 
# so that the RM orifice place can be fixed in place
# Given in meters.
LENGTH_FLOC_COUPLING_EXT = 0.05

# Given in meters
WIDTH_ENT_TANK_HOPPER_PEAK = 0.03

# Distance from the front wall to the pipe stubs in the hopper drains so that 
# an operator can easily reach them. Given in meters.
LENGTH_ENT_TANK_WALLTODRAIN_MAX = 0.4

#Entrance tank capture velocity, in meters
VEL_ENT_TANK_CAPTURE_BOD = 8 * 10**-3

# Angle of the entrance tank plates, in degrees
AN_ENT_TANK_PLATE = 50

# Spacing between entrance tank plates, in meters
SPACE_ENT_TANK_PLATE = 0.025

# Thickness of the entrance tank plates, in meters
THICKNESS_ENT_TANK_PLATE = 0.002

DIST_CENTER_ENT_TANK_PLATE = SPACE_ENT_TANK_PLATE + THICKNESS_ENT_TANK_PLATE

# Nominal diameter of the entrance tank mod, in meters. 
NOM_DIAM_ENT_TANK_MOD = (0.5 * u.inch).to(u.m).magnitude

NOM_DIAM_ENT_TANK_MOD_SPACER = (0.75 * u.inch).to(u.m).magnitude

# Thickness of the PVC disk used as the float for the chemical dose controller 
# lever arm. Given in meters.
THICKNESS_ENT_TANK_FLOAT = 0.05

# Given in meters.
SPACE_ENT_TANK_LAMINA_PIPETOEDGE = 0.05

NOM_DIAM_RAPID_MIX_PLATE_RESTRAINER = (0.5 * u.inch).to(u.m).magnitude

#Nom diam of the pipes that are embedded in the entrance tank slope to support the plate settler module
NOM_DIAM_ENT_TANK_PLATE_SUPPORT = (3 * u.inch).to(u.m).magnitude

####chemical dose controller

##0 is alum, 1 is PACl
##EN_COAG=1

# Given in kilograms
M_COAG_SACK = 25

# The coagulant stock is relatively stable and can last many days. Here 
# we set the minimum time the coagulant stock will last when applying the 
# maximum possible dose to size the stock tanks. In general the dose will
# be less than this and the stock will last much longer.
TIME_COAG_STOCK_MIN_EST = (1 * u.day).to(u.s).magnitude

# Want chlorine stock to run out on average every day so that the stock is
# made fresh frequently because the chlorine stock degrades with time 
# depending on temperature, concentration, and pH.
TIME_CHLOR_STOCK_AVE = (1 * u.day).to(u.s).magnitude

ID_COAG_TUBE = (0.125 * u.inch).to(u.m).magnitude
#1/8" tubes are readily available in hardware stores in Honduras
ID_CHLOR_TUBE = (0.125 * u.inch).to(u.m).magnitude

# Given in kilograms per liter.
CONC_COAG_STOCK_EST = 0.150

# Given in kilograms per liter.
CONC_CHLOR_STOCK_EST1 = 0.015

P_CHLOR = 0.7

# This is the elevation difference between the outlet of the coagulant 
# stock tanks and the water level in the constant head tank, which is set 
# by the hydraulic head required to provide the desired max chemical flow 
# rate through the float valve orifice in the CHT.
# It is treated as constant here to ensure a practical elevation difference
# is left between the stock tanks and the CHT even when a float valve is 
# selected which requires very little hydraulic head to deliver the 
# required maximum chemical flow rate.
# Given in meters.
HEIGHT_COAG_TANK_ABOVE_HEAD_TANK = 0.3

# This is the distance from the bottom of the stock tanks to the outlets 
# to allow space for solids to settle. Given in meters.
DIST_CENTER_STOCK_OUTLET = 0.1

# Distance between a tank and the border of the platform, in meters
SPACE_CHEM_TANK_BORDER = 0.05

# This is the estimated elevation difference between the water level in
# the constant head tank and the top of the entrance tank wall.
# The constant head tank water level is the same as the elevation of the 
# outlet of the dosing tube when the lever arm is horizontal (zero flow).
# Therefore this height depends only on the hardware used to make the 
# slider/drop tube assembly and to mount the lever arm to the entrance 
# tank wall.
# Note that this will vary depending on hardware used, and is only 
# defined here to calculate the elevation of the stock tanks, which can
# be approximate.
# Given in meters.
HEIGHT_DOSER_ASSEMBLY = 0.0677

# Maximum error allowed between a linear flow vs tube head loss 
# relationship and the actual performance (which is affected by 
# non-linear minor losses), assuming calibration at the maximum flow rate.
RATIO_LINEAR_CDC_ERROR = 0.1

# Estimated minor loss coefficient for the small-diameter flexible tubing 
# using fittings that have larger ID than the tubing
K_MINOR_CDC_TUBE = 2

# Head loss through the doser at maximum flow rate.
# Maximum head loss through the small-diameter dosing tubing, which 
# corresponds to the variation in water levels in the entrance tank and 
# the difference between the maximum and minimum elevation of the dosing 
# tube outlet attached to the lever arm.
# Given in meters.
HEADLOSS_CDC = 0.2

# Estimated distance between fluid level in constant head tank and float
# valve orifice, in meters.
HEIGHT_CDC_FLOAT_VALVE = 0.05

# Nominal diameter of the PVC plumbing for the chlorine dosing system.
NOM_DIAM_CHLOR_PIPE = (0.5 * u.inch).to(u.m).magnitude

# Nominal diameter of the PVC plumbing for the coagulant dosing system.
NOM_DIAM_COAG_PIPE = (0.5 * u.inch).to(u.m).magnitude

#Supplier Information:
#http://www.rotoplas.com/assets/files/industria/catalogo.pdf
#5-gallon bucket
#http://www.mcmaster.com/#storage-buckets/=kd23oh
#35-gallon drum
#http://www.jlmovingsupplies.com/c31/DIXIE-OPEN-CLOSED-HEAD-DRUMS-p36721.html
VOL_CHEM_TANK_AVAIL = [(5 * u.gal).to(u.m**3).magnitude, 
                       (35 * u.gal).to(u.m**3).magnitude,
                       (55 * u.gal).to(u.m**3).magnitude, 
                       (450 * u.L).to(u.m**3).magnitude,
                       (750 * u.L).to(u.m**3).magnitude, 
                       (1100 * u.L).to(u.m**3).magnitude,
                       (2500 * u.L).to(u.m**3).magnitude]

DIAM_CHEM_TANK_AVAIL = [(11.875 * u.inch).to(u.m).magnitude, 
                        (20.75 * u.inch).to(u.m).magnitude, 
                        (22.5 * u.inch).to(u.m).magnitude, 
                         (0.85 * u.m).magnitude, (1.10 * u.m).magnitude, 
                         (1.10 * u.m).magnitude, (1.55 * u.m).magnitude]

HEIGHT_CHEM_TANK_AVAIL = ([17.75, 31.75, 33.5, 0.99, 1.02, 1.39, 
                          1.65] * u.inch).to(u.m).magnitude

####Chemical dose controller dimensions (based on inserted drawings)

#st587 addition
# Length of the CDC Lever Arm, in meters
LENGTH_CDC_LEVER_ARM = 0.5

DIAM_CDC_LEVER_CYLINDER1 = (1 * u.inch).to(u.m).magnitude

DIAM_CDC_LEVER_CYLINDER4 = (2 * u.inch).to(u.m).magnitude

DIAM_CDC_LEVER_CYLINDER_2 = (0.5 * u.inch).to(u.m).magnitude

# Given in meters
LENGTH_CDC_LEVER_PIVOTTO_CYLINDER2 = 0.06

# Given in meters
LENGTH_CDC_LEVER_CYLINDER_2TO3 = 0.095

LENGTH_CDC_LEVER_PIVOT_BOX = (2 * u.inch).to(u.m).magnitude

WIDTH_CDC_LEVER_PIVOT_BOX = (1 * u.inch).to(u.m).magnitude

HEIGHT_CDC_LEVER_PIVOT_BOX = (1 * u.inch).to(u.m).magnitude

THICKNESS_CDC_LEVER_ARM = (0.125 * u.inch).to(u.m).magnitude

HEIGHT_CDC_LEVER_ARM = (1 * u.inch).to(u.m).magnitude

LENGTH_CDC_LEVER_INNERBAR = (7 * u.inch).to(u.m).magnitude

LENGTH_CDC_LEVER_MOUNTING_PLATE = (6 * u.inch).to(u.m).magnitude

# Given in meters
WIDTH_CDC_LEVER_MOUNTING_PLATE = 0.005

HEIGHT_CDC_LEVER_MOUNTING_PLATE = (2 * u.inch).to(u.m).magnitude

# Given in meters
SPACE_LEVER_TO_ENT_TANK_Z_TOP = 0.01

# Given in meters
THICKNESS_CDC_FLOAT = 0.05

# Given in meters
DIAM_CDC_FLOAT_CABLE = 0.005

LENGTH_CDC_LEVER_SLIDER_ORIGIN_TO_SCREW = (1 * u.inch).to(u.m).magnitude

THICKNESS_CDC_LEVER_SLIDER = (0.25 * u.inch).to(u.m).magnitude

HEIGHT_CDC_LEVER_SLIDER = (1.5 * u.inch).to(u.m).magnitude

LENGTH_CDC_LEVER_SLIDER = (3 * u.inch).to(u.m).magnitude

HEIGHT_CDC_LEVER_SLIDER_SHORT = (0.125 * u.inch).to(u.m).magnitude

LENGTH_CDC_LEVER_CYLINDER = (6 * u.inch).to(u.m).magnitude

# Given in meters
LENGTH_ENT_TANK_FRONT_WALL_TO_CDC_FLOAT = 0.874

# Given in meters
LENGTH_CDC_LEVER = 0.5 #This may be obsolete now... mrf222 2/10/16

# Given in meters
WIDTH_LEVER_ARM = 0.0032

# Given in meters
HEIGHT_LEVER_ARM = 0.0254

DIAM_CDC_CHT = (6 * u.inch).to(u.m).magnitude

# Distance from the top of the entrance tank to the to the middle of
# the lever arm hole for the cable - (minus the) radius of the hole.
# Given in meter.s
HEIGHT_LEVER_HOLE = 0.0132 - (0.0095/2)

DIAM_CABLE = (0.1 * u.inch).to(u.m).magnitude

# Edited DLABOrigintoLAOriginZ to accommodate dimensions from McMaster
# vs Inserted Drawing
# Given in meters.
DIAM_LAB_ORIGIN_TO_LA_ORIGIN_Z = 0.0245

# Distance from the lever arm origin to the outside center of the top part
# of the drop tube in the y direction
# Given in meters.
LENGTH_LA_ORIGIN_TO_DT_Y = 0.7812

# Distance from the lever arm origin to the drop tube in the z direction
# Given in meters.
LENGTH_LA_ORIGIN_TO_DT_Z = 0.0429

# Distance from the lever arm origin to the center of the drop tube in 
# the x direction
# Given in meters.
LENGTH_LA_ORIGIN_TO_DT_CENTER_X = 0.0290

# Measured from CDC research team's apparatus
# Given in meters.
THICKNESS_CDC_REDUCER = 0.0095

# Distance from the lever arm origin to the center of the reducer in 
# the x direction.
# Given in meters.
LENGTH_LA_ORIGIN_TO_REDUCER_X = 0.0290 

# Distance from the lever arm origin to the outside center of the top 
# part of the reducer in the y direction.
# Given in meters.
LENGTH_LA_ORIGIN_TO_REDUCER_Y = 0.007135

# Distance from the lever arm origin to the center of the reducer in the 
# x direction.
# Given in meters.
LENGTH_LA_ORIGIN_TO_REDUCER_CENTER_X = 0.0290

# Distance from the lever arm origin to the center of the reducer in the 
# y directio.
# Given in meters.
LENGTH_LA_ORIGIN_TO_REDUCER_CENTER_Y = 0.7919

WIDTH_LEVER_BRACKET = (0.625 * u.inch).to(u.m).magnitude

LENGTH_LEVER_BRAKCET = (1.5 * u.inch).to(u.m).magnitude

RADIUS_LA_BAR = (0.375 * u.inch).to(u.m).magnitude

THICKNESS_LEVER_BRACKET = (0.08 * u.inch).to(u.m).magnitude

DIAM_LA_BAR = (0.375 * u.inch).to(u.m).magnitude

LENGTH_LA_BAR = (4 * u.inch).to(u.m).magnitude

LENGTH_SLIDER = (3 * u.inch).to(u.m).magnitude

# Given in meters.
WIDTH_SLIDER = 3.2 * 10**-3

NOM_DIAM_DROPTUBE = (0.5 * u.inch).to(u.m).magnitude

HEIGHT_SLIDER = (0.625 * u.inch).to(u.m).magnitude

# Given in meters.
LENGTH_DROPTUBE = 0.61

#The length of the drop tube needs to be calculated. The drop tube must as long as the supercritical flow
#Thus the drop tube must extend down to the elevation of the sed tank effluent weir. This constant should be removed!

#Outer diameter of fitting- measured from CDC research team's fittin
OUTER_DIAM_CDC_FITTING = (5/32 * u.inch).to(u.m).magnitude

#Inner diameter of fitting- measured from CDC research team's fitting
ID_CDC_FITTING = (0.126 * u.inch).to(u.m).magnitude

#Length of fitting - measured from CDC research team's fitting
LENGTH_CDC_FITTING = (0.75 * u.inch).to(u.m).magnitude

#st587 addition
##Constant Head Tank Dimensions

#five gallons bucket dimensions for constant head tanks

# Given in meters.
DIAM_CHT = 0.01

# Given in meters.
HEIGHT_CHT = 0.37/3 

# Given in meters.
THICKNESS_CHT_WALL = 0.01/3 

NOM_DIAM_DELIVERY_PIPE = (0.6 * u.inch).to(u.m).magnitude

PIPE_SCHEDULE_FLEX_TUBE = 2

# Given in meters.
LENGTH_PVC_BALL_VALVE = 0.001625/4

THICKNESS_MOUNTING_BOARD = (1.5 * u.inch).to(u.m).magnitude

##Manifold Dimensions

# Given in meters.
SPACE_CDC_LEVER_TO_MANIFOLD = 0.4

# Given in meters.
LENGTH_CHLOR_AIR_RELEASE_PIPE = 0.3 #Arbitratily selected


####Flocculator
##The minor loss coefficient is 2. According to measurements at Agalteca and according to https://confluence.cornell.edu/display/AGUACLARA/PAHO+Water+Treatment+Publications (page 100 in chapter on flocculation)  
HEIGHT_FLOC_OPTION = 0

##Increased both to provide a safety margin on flocculator head loss and to simultaneously scale back on the actual collision potential we are trying to achieve.
K_MINOR_FLOC_BAFFLE = 2.5

# Given in meters.
SPACE_FLOC_BAFFLE_SET_BACK_PLASTIC= 0.02

###Target flocculator collision potential basis of design
# Given in meters**(2/3).
COLL_POT_FLOC_BOD = 75

##Minimum J/S ratio for flocculator geometry that will provide optimal efficiency.
RATIO_J_S_OPT_MIN = 3

##Ratio of the width of the gap between the baffle and the wall and the spacing between the baffles.
RATIO_FLOC_BAFFLE = 1

##Max energy dissipation rate in the flocculator, basis of design.
# Given in Watts per kilogram.
ENERGY_DIS_FLOC_BOD = 0.01

TIME_FLOC_DRAIN = (15 * u.min).to(u.s).magnitude

NOM_DIAM_FLOC_MOD = (0.5 * u.inch).to(u.m).magnitude

NOM_DIAM_FLOC_SPACER = (0.75 * u.inch).to(u.m).magnitude

# Given in meters.
SPACE_FLOC_MOD_EDGE_TO_LAST_PIPE = 0.1

NOM_DIAM_FLOC_RM_RESTRAINER = (0.5 * u.inch).to(u.m).magnitude

###Height that the drain stub extends above the top of the flocculator wall.
# Given in meters.
LENGTH_FLOC_DRAIN_STUB_EXT = 0.2

# Given in meters.
SPACE_FLOC_MOD_PIPE_TO_EDGE = 0.1

# Given in meters
THICKNESS_FLOC_BAFFLE = 0.002



###Sedimentation tank
##General

# Given in meters per second.
VEL_SED_UP_BOD = 0.001

##Plate settler capture velocity
# Given in meters per second.
VEL_SED_CONC_BOD = 0.00012

# Given in degrees.
ANGLE_SED_SLOPE = 50

##This slope needs to be verified for functionality in the field. A steeper
# slope may be required in the floc hopper.
# Given in degrees.
ANGLE_SED_HOPPER_SLOPE = 45

# Given in meters.
HEIGHT_WATER_SED_EST = 2

SED_GATE_VALVE_URL = "https://confluence.cornell.edu/download/attachments/173604905/Sed-Scaled-Gate-Valve-Threaded.dwg"

SUPPORT_BOLT_URL = "https://confluence.cornell.edu/download/attachments/173604905/PlateSettlerSupportBolt.dwg"

##  Max length of the active part of the sed tank so that single pipe 
# segments can be used for the inlet and outlet manifolds.
# Given in meters.
LENGTH_SED_UP_FLOW_MAX = 5.8

   
##Inlet channel
# Given in meters.
HEADLOSS_SED_WEIR_MAX = 0.05

##Height of the inlet channel overflow weir above the normal water level 
# in the inlet channel so that the far side of the overflow weir does
# not fill with water under normal operating conditions. This means the 
# water level in the inlet channel will increase when the inlet overflow 
# weir is in use.
# Given in meters.
HEIGHT_SED_INLET_WEIR_FREE_BOARD = 0.02

##Exit launder
## Target headloss through the launder orifices.
# Given in meters.
HEADLOSS_SED_LAUNDER_BOD = 0.04

##Acceptable ratio of min to max flow through the launder orifices
RATIO_FLOW_LAUNDER_ORIFICES = 0.80

##Center to center spacing of orifices in the launder.
# Given in meters.
DIST_CENTER_SED_LAUNDER_EST = 0.1

##The additional length needed in the launder cap pipe that is to be 
# inserted into the launder coupling.
# Given in meters.
LENGTH_SED_LAUNDER_CAP_EXCESS = 0.03

##Space between the top of the plate settlers and the bottom of the 
# launder pipe.
# Given in meters.
HEIGHT_LAMELLA_TO_LAUNDER = 0.05

##The additional length needed in the launder cap pipe that is to be 
# inserted into the launder coupling

##Diameter of the pipe used to hold the plate settlers together
NOM_DIAMETER_SED_MOD = (0.5 * u.inch).to(u.m).magnitude

##Diameter of the pipe used to create spacers. The spacers slide over the 
# 1/2" pipe and are between the plates.
NOM_DIAMETER_SED_MOD_SPACER = (0.75 * u.inch).to(u.m).magnitude

##This is the vertical thickness of the lip where the lamella support sits.
# mrf222
# Given in meters.
THICKNESS_SED_LAMELLA_LEDGE = 0.08

# Given in meters.
SPACE_SED_LAMILLA_PIPE_TO_EDGE = 0.05

##Approximate x-dimension spacing between cross pipes in the plate settler
# support frame.
# Given in meters.
DIST_CENTER_SED_PLATE_FRAME_CROSS_EST = 0.8

##Estimated plate length used to get an initial estimate of sedimentation 
# tank active length.
# Given in meters.
LENGTH_SED_PLATE_EST = 0.6

##Pipe size of the support frame that holds up the plate settler modules
NOM_DIAMETER_SED_PLATE_FRAME = (1.5 * u.inch).to(u.m).magnitude

##Floc weir

#Vertical distance from the top of the floc weir to the bottom of the pipe
# frame that holds up the plate settler modules.
# Given in meters.
HEIGHT_FLOC_WEIR_TO_PLATE_FRAME = 0.1

## Minimum length (X dimension) of the floc hopper.
# Given in meters.
LENGTH_SED_HOPPER_MIN = 0.5

##Inlet manifold
##Max energy dissipation rate in the sed diffuser outletSs.
# Given in watts per kilogram.
ENERGY_DIS_SED_INT_MAX = 0.15

##Ratio of min to max flow through the inlet manifold diffusers
RATIO_FLOW_SED_INLET = 0.8

NOM_DIAMETER_SED_MANIFOLD_MAX = (8 * u.inch).to(u.m).magnitude

##This is the minimum distance between the inlet manifold and the slope of 
# the sed tank.
# Given in meters.
SPACE_SED_INLET_MAN_SLOPE = 0.1

##  Length of exposed manifold stub coming out of the floc weir to which 
# the free portion of the inlet manifold is attached with a flexible coupling.
# Given in meters.
LENGTH_SED_MAN_CONNECTION_STUB = 0.4

##Space between the end of the manifold pipe and the edge of the first 
# diffuser's hole, or the first manifold orifice.
# Given in meters.
LENGTH_SED_MANIFOLD_FIRST_DIFFUSER_GAP = 0.3

##Vertical distance from the edge of the jet reverser half-pipe to the 
# tip of the inlet manifold diffusers.
# Given in meters.
HEIGHT_JET_REVERSER_TO_DIFFUSERS = 0.03

##Gap between the end of the inlet manifold pipe and the end wall of the 
# tank to be able to install the pipe.
# Given in meters.
LENGTH_SED_MANIFOLD_PIPE_FROM_TANK_END = 0.02

##Assumed stretch of the PVC pipes as they are heated and molded
RATIO_PVC_STRETCH = 1.2

# Given in meters.
LENGTH_SED_WALL_TO_DIFFUSER_GAP_MIN = 0.03

##Diameter of the holes drilled in the manifold so that the molded 1" 
# diffuser pipes can fit tightly in place (normal OD of a 1" pipe is 
# close to 1-5/16")
DIAM_SED_MANIFOLD_PORT = (1.25 * u.inch).to(u.m).magnitude

##Outlet to filter
#If the plant has two trains, the current design shows the exit channel
# continuing from one set of sed tanks into the filter inlet channel. 
# The execution of this extended channel involves a few calculations.
# Given in meters.
HEADLOSS_SED_TO_FILTER_PIPE_MAX = 0.1

if EN_DOUBLE_TRAIN == 1:
    K_SED_EXIT = 1
else:
    K_SED_EXIT = 0


# Given in meters.
if EN_DOUBLE_TRAIN == 1: 
   HEIGTH_EXIT_FREE = 0.05
else:
   HEIGTH_EXIT_FREE = 0

##added 12/5/16 by mrf222 ensures weir does not overtop backwards if 
# filter weir is too high.
# Given in meters.
HEIGHT_SED_WEIR_FREE_BOARD = 0.05



##Stacked rapid sand filter
####Construction and Design Inputs

#Design guidelines say 11 mm/s. The success of lab-scale backwashing at 
# 10 mm/s suggests that this is a reasonable and conservative value.
# Given in meters per second.
VEL_FILTER_Bw_ = 0.011

N_FILTER_LAYER = 6

# Given in meters per second.
VEL_FILTER_LAYER = 0.001833 ##VEL_FIBER_DIST_CENTER_/N_FIBER_LAYER

##Minimum thickness of each filter layer (can be increased to accomodate 
# larger pipe diameters in the bottom layer).
# Given in meters.
HEIGHT_FILTER_LAYER_MIN = 0.2

##center to center distance for slotted pipes.
# Given in meters.
DIST_CENTER_FILTER_MANIFOLD_BRANCH = 0.1

##How far the branch extends into the trunk line.
# Given in meters.
LENGTH_FILTER_MAN_BRANCH_EXT = 0.02

##The time to drain the filter box of the water above the fluidized bed
# Given in seconds.
TIME_FIBER_BACKWASH_INITIATION_BOD = 180

##Mickey suggested this value based on lab experience. This was moved to 
# Expert Inputs 12/4/16 by mrf222 as a result of feedback from Monroe and
# Skyler. In the Moroceli plant, the Fi Entrance box was overflowing before
# filtration backwash. The HL of a dirty filter has therefore been increased
# from 40 to 60 cm.
# Given in meters.
HEADLOSS_FILTER_DIRTY = 0.6

##This is the extra head we are going to provide on top of steady state
# backwash head loss to ensure that we can fluidize the bed to initiate
# backwash.
# Given in meters.
HEADLOSS_FIBER_BACKWASH_STEADY_FLOW = 0.2

##Maximum acceptable head loss through the siphon at steady state; used 
# to calculate a diameter.
# Given in meters.
HEADLOSS_FILTER_SIPHON_MAX = 0.35

##Diameter of sand drain pipe
NOM_DIAMETER_FILTER_SAND_OUTLET = (2 * u.inch).to(u.m).magnitude

##Height of the barrier between the exit box and distribution box.
# Given in meters.
HEIGHT_FILTER_DIST_BARRIER = 0.1

##Length that the siphon pipe extends up into the plant drain channel. 
# Being able to shorten the stub from which the siphon discharges into 
# the main plant drain channel allows for some flexibility in the hydraulic
# design.
# Given in meters.
LENGTH_FILTER_SIPHON_CHANNEL_STUB_MIN = 0.2

# Given in meters.
HEADLOSS_FILTER_ENTRANCE_PIPE_MAX = 0.1

NOM_DIAMETER_FILTER_TRUNK_MAX = (6 * u.inch).to(u.m).magnitude

NOM_DIAMETER_FILTER_BACK_WASH_SIPHON_MAX = (8 * u.inch).to(u.m).magnitude

##Purge valves on the trunk lines are angled downwards so that sediment
# is cleared more effectively. This angle allows the tees to fit on top 
# of one another at the filter wall.
# Given in degrees.
ANGLE_FILTER_TRUNK_VALVES = 25

##Purge valves on the trunk lines are angled downwards so that sediment
# is cleared more effectively. This angle allows the tees to fit on top
# of one another at the filter wall.
# Given in meters.
THICKNESS_FILTER_WEIR = 0.05

# Given in meters.
SPACE_FILTER_BRANCH_TO_WALL = 0.05

FILTER_GATE_VALUE_URL = "https://confluence.cornell.edu/download/attachments/173604905/Fi-Scaled-Gate-Valve-Threaded.dwg"
FILTER_BALL_VALVE_URL = "https://confluence.cornell.edu/download/attachments/173604905/FiMetalBallValve.dwg"

# Given in meters.
HEIGTH_FILTER_WALL_TO_PLANT_FLOOR_MIN = 0.1

# Given in meters.
HEADLOSS_FILTER_INLET_WEIR_MAX = 0.05

##Dimensions get too small for construction below a certain flow rate.
# Given in cubic meters per second.
FLOW_FILTER_MIN = 0.008

# Given in meters.
LENGTH_FILTER_MAN_FEMCO_COUPLING = 0.06

##Nominal diameter of the spacer tees in the four corners of the filter 
# manifold assembly.
NOM_DIAMETER_FILTER_MAN_WING_SPACER = (2 * u.inch).to(u.m).magnitude

##Length of the vertical pipe segment following the valve on the filter
# sand drain. This stub can be capped to allow the sand in the valve to 
# settle, so that the valve can be closed without damage from fluidized sand.
# Given in meters.
LENGTH_FILTER_SAND_OUTLET_PIPE = 0.2




#######Elevation Safety Margins

##Minimum depth in the entrance box during backwash such that there is
# standing water over the inlet.
# Given in meters.
HEIGTH_FILTER_BACKWASH_NO_SUCK_AIR = 0.2

##Minimum water depth over the orifices in the siphon manifold so that 
# air is not entrained.
# Given in meters.
HEIGTH_FILTER_SIPHON_NO_SUCK_AIR = 0.1

# Given in meters.
HEIGTH_FILTER_FLUIDIZED_BED_TO_SIPHON = 0.2

# Given in meters.
HEIGTH_FILTER_FORWARD_NO_SUCK_AIR = 0.1

# Given in meters.
HEIGTH_FILTER_WEIR_FREEFALL = 0.03

# Given in meters.
HEIGTH_FILTER_AIR_REMOVAL_BLOCK_SUBMERGED = 0.05

# Given in meters.
HEIGTH_FILTER_BYPASS_SAFETY = 0.1

# Given in meters.
HEIGTH_DRAIN_OUTLET_SAFETY = 0.1

# Given in meters.
HEIGTH_FILTER_OVERFLOW_WEIR_FREEFALL = 0.1



#######Plant drain channel

###Space beyond the entrance tank in the plant drain channel where the 
# drop pipes from the CDC lever arm can come down and be connected with 
# the chlorine and coagulant dosing points.
# Given in meters.
LENGTH_CHEM_LEVER_ARM_SPACE = 0.75


###Operator access

##combine walkway assumptions!
# Given in meters.
WIDTH_MP_WALKWAY_MIN = 1

##Width of the walkway above the main plant drain channel.
# Given in meters.
WIDTH_DC_WALKWAY = 1.2

##Width of the floor space between the flocculator and the rapid mix
# pipe floor cutout next to the entrance tank.
# Given in meters.
WIDTH_ET_WALKWAY = 1

##for high flow, double train situations.
# Given in meters.
W_TRAIN_WALKWAY = 1.5

# Given in meters.
W_BASEMENT_STAIRS = 0.9

# Given in meters.
W_ENTRANCE_STAIRS = 1.2


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


