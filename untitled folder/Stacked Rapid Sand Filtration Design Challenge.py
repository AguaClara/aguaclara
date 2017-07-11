#Stacked Rapid Sand Filtration Design Challenge
#The stacked rapid sand filter at Tamara is treating 12 L/s with 6 20 cm deep layers of sand with effective size 0.5 mm and uniformity coefficient of 1.6. The backwash velocity is 11 mm/s. I've defined many of the necessary inputs for the filtration analysis below

import math

from scipy import constants, interpolate

import numpy as np

import pandas as pd

import matplotlib.pyplot as plt

import sys, os

import os.path
dir_path = os.path.dirname(__file__)
csv_path = os.path.join(dir_path, 'SRSF.csv')
with open(csv_path) as srsf:
    srsf = pd.read_csv(srsf)


myGitHubdir=os.path.expanduser('~\\Documents\\GitHub')
if myGitHubdir not in sys.path:
    sys.path.append(myGitHubdir)

from AguaClara_design import physchem as pc

from AguaClara_design import pipedatabase as pipe

from AguaClara_design.units import unit_registry as u

from AguaClara_design import utility as ut

FLOW_PLANT = 12 * u.L / u.s
RHO_FILTER_SAND = 2650 * u.kg / u.m**3
K_KOZENY = 5
HEIGHT_FILTER_LAYER = 20 * u.cm
RHO_WATER = 1000 * u.kg / u.m**3
NU_WATER = 1 *u.mm**2 / u.s
N_FILTER_LAYER = 6
DEPTH_FILTER_SAND_EFFECTIVE_SIZE = 0.5 * u.mm
UNIFORMITY_COEFF_FILTER_SAND = 1.6
PHI_FILTER_SAND = 0.4
VELOCITY_FILTER_BACKWASH = 11 * u.mm / u.s
g = 9.80665 * u.m / u.s**2

#1) Calculate the total sand depth.
HEIGHT_FILTER = (HEIGHT_FILTER_LAYER * N_FILTER_LAYER).to(u.m)

print("#1. " + str(HEIGHT_FILTER) + "\n")

#2) Calculate the D.60 for the sand grain size.

DEPTH_FILTER_SAND_60 = DEPTH_FILTER_SAND_EFFECTIVE_SIZE * UNIFORMITY_COEFF_FILTER_SAND
print("#2. " + str(DEPTH_FILTER_SAND_60) + "\n")

#3) What is the filter bed plan view area for Tamara?
AREA_FILTER = (FLOW_PLANT / VELOCITY_FILTER_BACKWASH).to(u.m**2)
print("#3. " + str(AREA_FILTER) + "\n")

#4) What is the filtration velocity?
VELOCITY_FILTER = VELOCITY_FILTER_BACKWASH / N_FILTER_LAYER
print("#4. " + str(VELOCITY_FILTER) + "\n")

#5) What is the head loss thorugh the filter at the beginning of the filtration run with a clean filter bed?
def head_loss_kozeny(epsilon_filter_sand, depth_filter_sand, velocity_filter, height_filter):
    return (36*K_KOZENY*((1 - epsilon_filter_sand)**2 / epsilon_filter_sand**3) * (NU_WATER*velocity_filter)/(g * depth_filter_sand**2)* height_filter).to(u.cm)

HEAD_LOSS_FILTER_SAND_CLEAN = head_loss_kozeny(PHI_FILTER_SAND, DEPTH_FILTER_SAND_60, VELOCITY_FILTER, HEIGHT_FILTER_LAYER)
print("#5. " + str(HEAD_LOSS_FILTER_SAND_CLEAN) + "\n")

#6)Estimate the minimum fluidization velocity for this filter bed. Note that this is not the actual velocity used for backwashing the sand.
def velocity_backwash_min(epsilon, depth_filter_sand_60):
    return ((epsilon**3 * g * depth_filter_sand_60**2)/(36*K_KOZENY*NU_WATER*(1-epsilon))*(RHO_FILTER_SAND/RHO_WATER-1)).to(u.mm/u.s)
print("#6. " + str(velocity_backwash_min(PHI_FILTER_SAND, DEPTH_FILTER_SAND_60)) + "\n")

#7)What is the residence time in the fluidized bed during backwash? You may assume the expansion ratio is 1.3.
II_FILTER_BACKWASH_EXPANSION = 1.3
def theta_filter_backwash():
    return (PHI_FILTER_SAND * HEIGHT_FILTER + (II_FILTER_BACKWASH_EXPANSION - 1)*HEIGHT_FILTER)/VELOCITY_FILTER_BACKWASH

print("#7. " + str(theta_filter_backwash())+ "\n")

#8)Our next goal is to determine what fraction of the water is wasted due to backwash in a SRSF. Given that the backwash water that ends up above the filter bed never returns to the filter it isn't necessary to completely clear the water above the filter bed during a backwash cycle. Therefore we anticipate that backwash can be ended after approximately 3 expanded bed residence times. In addition it takes about 1 minute to initiate backwash by lowering the water level above the filter bed. Estimate the time between beginning backwash and finishing the cleaning of the bed.
TIME_FILTER_BACWASH_DRAIN = 1 * u.min
def time_filter_backwash():
    return theta_filter_backwash() * 3 + TIME_FILTER_BACWASH_DRAIN
print("#8. " + str(time_filter_backwash())+ "\n")

#9)Estimate the total depth of water that is wasted during that time.
LENGTH_FILTER_BACKWASH = VELOCITY_FILTER_BACKWASH * time_filter_backwash()
print("#9. " + str(LENGTH_FILTER_BACKWASH) + "\n")

#10)Estimate the total depth of water that is lost due to refilling the filter box at the end of backwash plus the slow refilling to the maximum dirty bed height. You may ignore the influence of plumbing head loss and you may assume that the dirty bed head loss is about 40 cm.
HEAD_LOSS_FILTER_DIRTY = 40 * u.cm

LENGTH__FILTER_BACKWASH_REFILL = HEIGHT_FILTER + 20 * u.cm + HEAD_LOSS_FILTER_DIRTY
print("#10. " + str(LENGTH__FILTER_BACKWASH_REFILL) + "\n")

#11)Now calculate the total length (or depth) of water that is wasted due to backwash by adding the two previous lengths.
LENGTH_FILTER_BACKWASH_WASTED = LENGTH_FILTER_BACKWASH + LENGTH__FILTER_BACKWASH_REFILL
print("#11. " + str(LENGTH_FILTER_BACKWASH_WASTED) + "\n")

#12) Assume that the filter run + backwash time is 12 hours. What is the total height (or length) of water that would enter the filter during this time? This length when multiplied by the area of the filter would give the total volume of water processed by a filter.
TIME_Filter_CYCLE = 12 * u.hr
LENGTH_FILTER_WATER_CYCLE = TIME_Filter_CYCLE * VELOCITY_FILTER_BACKWASH
print("#12. " + str(LENGTH_FILTER_WATER_CYCLE) + "\n")

#13) What fraction of the total water is lost due to backwash and the related water level changes in the filter box?
II_FILTER_BACKWASH_WASTED = LENGTH_FILTER_BACKWASH_WASTED / LENGTH_FILTER_WATER_CYCLE
print("#13. " + str(II_FILTER_BACKWASH_WASTED) + "\n")

#14) Define a new unit in Mathcad. Define NTU based the equation below. You can do this by simply defining an NTU as 1/0.65 mg/L!!!!
#Conc_RAW_WATER = 0.65NTURAW_WATER*u.mg/u.L

NTU = 1/0.65 * u.mg/u.L
print("#14. " + str(NTU)+ "\n")

#15) Now we will evaluate the very first data set from a full scale SRSF. The performance data given below is the settled water turbidity and then the filtered water turbidity during one filter run. The time step is 5 minutes. Use the array column function to create arrays containing the filter influent and effluent data, attach the units of NTU to the arrays, and then calculate pC* for the filter as a function of time and plot that data.

DELTA_TIME_DATA = 5 * u.min
def ntu_influent():
    return srsf.iloc[:, 0] * NTU
print("#15. ")
print(ntu_influent())
print("\n")

def ntu_effluent():
    return srsf.iloc[:, 1] * NTU
print(ntu_effluent())
print("\n")

def p(x):
    return math.log(1/x)

def srsf_time():
    srsf_time=[]
    for i in range(len(ntu_effluent())):
        srsf_time.append(DELTA_TIME_DATA*i)
    return srsf_time
print(srsf_time())
print("\n")


#16) How many kg of suspended solids per square meter of filter were removed during this filter run. Use the plan view area for the filter (don't multiply by the number of layers)

def mass_filter_solids():
    return sum((ntu_influent()-ntu_effluent())* (FLOW_PLANT*DELTA_TIME_DATA)/AREA_FILTER)

print("#16. " + str(mass_filter_solids())+ "\n")

#17) Another useful way to express the solids capacity of the filter is to calculate the turbidty removed * the run time and then express the results with units of NTU *hrs. What was the capacity of the filter in NTU hrs?
def solid_capacity_other():
    return sum((ntu_influent()-ntu_effluent())*DELTA_TIME_DATA)
print("#17. " + str(solid_capacity_other())+ "\n")

#18) How long was the filter run?
def time_filter_cycle_data():
    return float(str(ntu_influent())[-50:-42]) * DELTA_TIME_DATA
print("#18. " + str(time_filter_cycle_data())+ "\n")

#19) What is the total volume of pores per square meter of SRSF filter bed (includes all 6 layers) (in L/m^2)?
volume_filter_pores = HEIGHT_FILTER * PHI_FILTER_SAND
print("#19. " + str(volume_filter_pores) + "\n" )

#20) The next step is to estimate the volume of flocs per plan view area of the filter. Assume the density of the flocs being captured by the filter are approximated by the density of flocs that have a sedimentation velocity of 0.10 mm/s (slightly less than the capture velocity of the plate settlers). (see slides in flocculation notes for size of the floc and then density of that floc. I've provided this value below to simplify the analysis
RHO_FLOC = RHO_WATER + 100 * u.kg/u.m**3
RHO_CLAY = 2650 * u.kg/u.m**3

#I know floc density.
#Calculate fraction of floc volume that is clay.
#Given that floc mass is the sum of clay mass and water mass and given that floc volume is the sum of clay volume and water volume, derive an equation for the volume of flocs per plan view area of a stacked rapid sand filter (includes all 6 layers) given the floc, clay, and water densities and the mass of the clay. Show the equations that you derive

#mass conversion gives


def volume_floc():
    return (mass_filter_solids()/RHO_CLAY) * (RHO_CLAY -RHO_WATER)/(RHO_FLOC - RHO_WATER)
print("#20. " + str(volume_floc()) + "\n" )


#21) What percent of the filter pore volume is occupied by the flocs? This fraction of pore space occupied is quite small and suggests that much of the filter bed has a very low particle concentration at the end of a filter run.
def ii_floc_pores():
    return volume_floc() / volume_filter_pores

print("#21. " + str(ii_floc_pores()) + "\n")

#22) Final head loss for the filter was 50cm. Assume that this is caused by minor losses due to creation of a floc orifice in each pore. Find the minor loss contribution by subtracting off the clean bed head loss to find the head loss created by the flow restrictions that were created by the flocs.
HEAD_LOSS_FINAL = 50 * u.cm
def head_loss_restrictions():
    return HEAD_LOSS_FINAL - HEAD_LOSS_FILTER_SAND_CLEAN

print("#22. " + str(head_loss_restrictions()) + "\n")

#23) If we assume that at the end of the filter run every pore in the filter had a flow restricting orifice from the deposition of flocs in the pore, then what was the diameter of each of the flow restrictions? We will calculate this in several steps. To begin, estimate how many flow restrictions are created by the sand grains before any flocs are added with the assumption that there is one flow restriction per sand grain. How many sand grains are there per cubic meter of filter bed? Use  to estimate the number of sand grains. We will assume there is a one to one correspondence between sand grains and flow restrictions.

VOLUME_FILTER_SAND_GRAIN = DEPTH_FILTER_SAND_60**3 * math.pi/6
VOLUME_FILTER_SAND_GRAIN_WITH_PORE = VOLUME_FILTER_SAND_GRAIN/ (1-PHI_FILTER_SAND)
NUMBER_SAND = 1 /(VOLUME_FILTER_SAND_GRAIN_WITH_PORE)

print("#23. " + str(NUMBER_SAND) + "\n")

#24) Estimate the average vertical distance between flow restrictions based on the cube root of the volume occupied by a sand grain
LENGTH_SAND_SEPARATION = VOLUME_FILTER_SAND_GRAIN_WITH_PORE **(1/3)

print("#24. " + str(LENGTH_SAND_SEPARATION) + "\n")

#25) On average, how many sand grain flow restrictions does a water molecule flow through on its way through the filter?
NUMBER_RESTRICTIONS = HEIGHT_FILTER_LAYER/LENGTH_SAND_SEPARATION

print("#25. " + str(NUMBER_RESTRICTIONS) + "\n")


#26) What is the head loss per flow restriction?
HEAD_LOSS_RESTRICTION = head_loss_restrictions() / NUMBER_RESTRICTIONS

print("#26. " + str(HEAD_LOSS_RESTRICTION) + "\n")

#27) If each restriction was partially clogged with flocs at the end of the filter run, estimate the velocity in the restriction using the expansion head loss equation. You can use the average pore water velocity as a good estimate of the expanded flow velocity.
# HEAD_LOSS_EXPANSION = (VELOCITY_IN - VELOCITY_OUT)**2 / 2*g

VELOCITY_PORE = VELOCITY_FILTER / PHI_FILTER_SAND
VELOCITY_RESTRICTION = ((2 * g * HEAD_LOSS_RESTRICTION)**(1/2) + VELOCITY_PORE).to(u.mm /u.s)

print("#27. " + str(VELOCITY_RESTRICTION) + "\n")

#28) What is flow rate of water through each pore in μL/s? You can estimate this from the number of pores per square meter given the average separation distance.

NUMBER_PORE_PER_AREA = 1/LENGTH_SAND_SEPARATION
FLOW_PORE = ((VELOCITY_FILTER/ NUMBER_PORE_PER_AREA))

print("#28. " + str(FLOW_PORE) + "\n")

#29) What is the inner diameter of the flow restriction created by the flocs if the vena contracta is 0.62?

II_VENA_CONTRACTA = 0.62

AREA_VENA_CONRACTA_RESTRICTION = FLOW_PORE/VELOCITY_RESTRICTION
DIAMETER_RESTRICTION = ( (4 * AREA_VENA_CONRACTA_RESTRICTION/II_VENA_CONTRACTA)/math.pi )**(1/2)

print("#29. " + str(DIAMETER_RESTRICTION) + "\n")



