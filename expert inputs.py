# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 15:54:16 2017

@author: kn348
"""
from AguaClara_design.units import unit_registry as u

#tabulated constants

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

#Flow orifice meter

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
