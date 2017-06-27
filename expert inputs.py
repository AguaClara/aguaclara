# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 15:54:16 2017

@author: kn348
"""
from AguaClara_design.units import unit_registry as u

#####tabulated constants

#density of water
RHO_H20=1000*u.kg/(u.m**3)

#the kinematic viscosity of water
NU_WATER=1.10**-6*(u.m**2/u.s)

#THE INFLUENCE OF VISCOSITY ON MIXING IN JET REACTORS
RATIO_JET_ROUND=0.5

#This is an estimate for plane jets as created in the flocculator and in the sed tank jet reverser.
RATIO_JET_PLANE=0.225

RATIO_VC_ORIFICE=0.63

P_ATM=1*u.atm

#needed for the filter siphon design
NU_AIR=12*u.to(u.mm**2/u.s)

#needed for the filter siphon design
RHO_AIR=1.204*u.kg/(u.mm**3)

####general assumptions and constants

PLANT_ORIGIN=[0,0,0]*u.m

COUNTRY=0

LANGUAGE=0

#Prompts the transition to a low flow plant
FLOW_PLANT_MAX_LF=16.1*u.L/u.s

WIDTH_HUMAN_MIN=0.5*u.m

#The height of the walkway above the drain channel bottom so that someone can walk through the drain channel.
HEIGHT_HUMAN_ACCESS=1.5*u.m

#Used to set the minimum height of entrance, floc, and sed walls
HEIGHT_PLANT_FREE_BOARD=0.1*u.m

#minimum space between fittings in a tank or fittings and the wall of the tank.
SPACE_FITTING=5*u.cm

#Minimum channel width for constructability
WIDTH_CHANNEL_MIN=15*u.cm

#RATIO_RECTANGULAR is defined as the optimum "height over width ratio" (1/2) for a rectangular open channel
RATIO_RECTANGULAR=1/2 

##Equals 1 to draw boxes showing max water levels, 0 normally
#EN_WATER=0 #ASK Monroe

##If EN_WATER is set to 1, this controls the filter operation mode for which water/sand elevations are drawn. 0 for terminal, 1 for clean bed, and 2 for backwash.
#EN_WATER=2 #ASK Monroe

WIDTH_DOOR=1*u.m

THICKNESS_ACRYLIC=1*u.cm

#due to a 24 in LFOM because that's the biggest pipe we have in our database right now. if we need a bigger single train, we can do that by adding that pipe size into the pipe database
FLOW_TRAIN_MAX=150.1*u.L/u.s

def en_multiple_train(flow_plant):
    
    if flow_plant>60*u.L/u.s:
        return 1
    else:
        return 0

def n_train(flow_plant):
    
    if flow_plant>60*u.L/u.s:
        return 1
    elif flow_plant>60*u.L/u.s and flow_plant<=120*u.L/u.s:
        return 2
    else:
        return 4

def flow_train(flow_plant):
    
    return flow_plant/(n_train(flow_plant))

#####Flow orifice meter

#Maximum number of rows or orifices in lfom.
RATIO_LFOM_ORIFICE = 10

#safety coefficient that ensures free fall at the bottom of the lfom pipe
RATIO_LFOM_SAFETY = 1.5

#minimum safety coefficient for lfom pipe diameter; only reduced between 55 L/s and 70 L/s - the intermediate zone between the using an LFOM pipe and an LFOM channel 
#It may be possible to eliminate this if we switch to plate LFOM at 50 Lp
RATIO_LFOM_SAFETY_MIN=1.15

#Minimum head loss through linear orifice meter
HEADLOSS_LFOM_MIN=20*u.cm

#Maximum head loss through linear orifice meter to be used as needed for high flow plants.
HEADLOSS_LFOM_MAX=40*u.cm

#changed from 12 in by pc479 because this is not a constraint anymore because we don't have an elbow constraining us. LFOM still needs to fit in the entrance tank. Need to check this constraint (mrf222)
NOM_DIAM_LFOM_PIPE_MAX=36*u.inch

HEIGHT_LFOM_FREEFALL=10*u.cm

#enumerate type that selects between pipe(1) and plate(0) for the LFOM
def en_lfom_pipe(flow_plant):
    
    if flow_plant>=80*u.L/u.s:
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
ANGLE_ENT_TANK_SLOPE=45*u.deg

#Extra space around the float (increase in effective diameter) to ensure that float has free travel 
SPACE_ENT_TANK_FLOAT=5*u.cm

#Increased to get better mixing (10/10/2015 by Monroe)
ENERGY_DIS_RAPID_MIX=3*u.W/u.kg

#Distance that the rapid mix coupling extends into the first floc channel so that the RM orifice place can be fixed in place
LENGTH_FLOC_COUPLING_EXT=5*u.cm

WIDTH_ENT_TANK_HOPPER_PEAK=3*u.cm

#Distance from the front wall to the pipe stubs in the hopper drains so that an operator can easily reach them.
LENGTH_ENT_TANK_WALLTODRAIN_MAX=40*u.cm

#Entrance tank capture velocity
VEL_ENT_TANK_CAPTURE_BOD=8*u.mm/u.s

AN_ENT_TANK_PLATE=50*u.deg

SPACE_ENT_TANK_PLATE=2.5*u.cm

THICKNESS_ENT_TANK_PLATE=2*u.mm

DIST_CENTER_ENT_TANK_PLATE=SPACE_ENT_TANK_PLATE+THICKNESS_ENT_TANK_PLATE

NOM_DIAM_ENT_TANK_MOD=0.5*u.inch

NOM_DIAM_ENT_TANK_MOD_SPACER=0.75*u.inch

#Thickness of the PVC disk used as the float for the chemical dose controller lever arm.
THICKNESS_ENT_TANK_FLOAT=5*u.cm

SPACE_ENT_TANK_LAMINA_PIPETOEDGE=5*u.cm

NOM_DIAM_RAPID_MIX_PLATE_RESTRAINER=0.5*u.inch

#Nom diam of the pipes that are embedded in the entrance tank slope to support the plate settler module
NOM_DIAM_ENT_TANK_PLATE_SUPPORT=3*u.inch

####chemical dose controller

##0 is alum, 1 is PACl
##EN_COAG=1

M_COAG_SACK=25*u.kg

#The coagulant stock is relatively stable and can last many days. Here we set the minimum time the coagulant stock will last when applying the maximum possible dose to size the stock tanks. In general the dose will be less than this and the stock will last much longer.
TIME_COAG_STOCK_MIN_EST=1*u.day

#Want chlorine stock to run out on average every day so that the stock is made fresh frequently because the chlorine stock degrades with time depending on temperature, concentration, and pH.
TIME_CHLOR_STOCK_AVE=1*u.day

ID_COAG_TUBE=1/8*u.inch
#1/8" tubes are readily available in hardware stores in Honduras
ID_CHLOR_TUBE=1/8*u.inch

CONC_COAG_STOCK_EST=150*u.gm/u.L

CONC_CHLOR_STOCK_EST1=15*u.gm/u.L

P_CHLOR=0.7

#This is the elevation difference between the outlet of the coagulant stock tanks and the water level in the constant head tank, which is set by the hydraulic head required to provide the desired max chemical flow rate through the float valve orifice in the CHT.
#It is treated as constant here to ensure a practical elevation difference is left between the stock tanks and the CHT even when a float valve is selected which requires very little hydraulic head to deliver the required maximum chemical flow rate.
HEIGHT_COAG_TANK_ABOVE_HEAD_TANK=30*u.cm

#This is the distance from the bottom of the stock tanks to the outlets to allow space for solids to settle.
DIST_CENTER_STOCK_OUTLET=10*u.cm

#Distance between a tank and the border of the platform
SPACE_CHEM_TANK_BORDER=5*u.cm

#This is the estimated elevation difference between the water level in the constant head tank and the top of the entrance tank wall.
#he constant head tank water level is the same as the elevation of the outlet of the dosing tube when the lever arm is horizontal (zero flow).
#Therefore this height depends only on the hardware used to make the slider/drop tube assembly and to mount the lever arm to the entrance tank wall.
#Note that this will vary depending on hardware used, and is only defined here to calculate the elevation of the stock tanks, which can be approximate.
HEIGHT_DOSER_ASSEMBLY=6.77*u.cm

#Maximum error allowed between a linear flow vs tube head loss relationship and the actual performance (which is affected by non-linear minor losses), assuming calibration at the maximum flow rate
RATIO_LINEAR_CDC_ERROR=0.1

#Estimated minor loss coefficient for the small-diameter flexible tubing using fittings that have larger ID than the tubing
K_MINOR_CDC_TUBE=2

#Head loss through the doser at maximum flow rate.
#Maximum head loss through the small-diameter dosing tubing, which corresponds to the variation in water levels in the entrance tank and the difference between the maximum and minimum elevation of the dosing tube outlet attached to the lever arm.\
HEADLOSS_CDC=20*u.cm

#Estimated distance between fluid level in constant head tank and float valve orifice
HEIGHT_CDC_FLOAT_VALVE=5*u.cm

#Nominal diameter of the PVC plumbing for the chlorine dosing system.
NOM_DIAM_CHLOR_PIPE=0.5*u.inch

#Nominal diameter of the PVC plumbing for the coagulant dosing system.
NOM_DIAM_COAG_PIPE=0.5*u.inch

#Supplier Information:
#http://www.rotoplas.com/assets/files/industria/catalogo.pdf
#5-gallon bucket
#http://www.mcmaster.com/#storage-buckets/=kd23oh
#35-gallon drum
#http://www.jlmovingsupplies.com/c31/DIXIE-OPEN-CLOSED-HEAD-DRUMS-p36721.html
VOL_CHEM_TANK_AVAIL=[5*u.gal,35*u.gal,55*u.gal,450*u.L,750*u.L,1100*u.L,2500*u.L]
DIAM__CHEM_TANK_AVAIL=[11.875*u.inch,20.75*u.inch,22.5*u.inch,0.85*u.m,1.10*u.m,1,10*u.m,1.55*u.m]
HEIGHT_CHEM_TANK_AVAIL=[17.75*u.inch,31.75*u.inch,33.5*u.inch,0.99*u.inch,1.02*u.inch,1.39*u.inch,1.65*u.inch]

####Chemical dose controller dimensions (based on inserted drawings)



