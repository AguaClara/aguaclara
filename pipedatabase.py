# -*- coding: utf-8 -*-
"""
Created on Thu Jun  8 18:20:38 2017

@author: mw24
"""

#Let's begin to create the pipe database
# https://docs.python.org/2/library/csv.html
from units import unit_registry as u
import numpy as np
# We will use Pandas
import pandas as pd
# load the pipedb from a csv file
    
import os.path    
dir_path = os.path.dirname(__file__)
csv_path = os.path.join(dir_path, 'pipedatabase.csv')
with open(csv_path) as pipedbfile:
    pipedb = pd.read_csv(pipedbfile)
    
# Returns outer diameter of pipe corresponding to nominal diameter. 
# The pipe schedule is not required here because all of the pipes of a given nominal diameter have the same OD

def OD(ND):
    # Extract the magnitude in inches from the nominal diameter
    # Find the index of the closest nominal diameter (Should this be changed to find the next largest ND?)
    # Take the values of the array, subtract the ND, take the absolute value, find the index of the minimium value
    myindex = (np.abs(np.array(pipedb['NDinch']) - (ND.to(u.inch)).magnitude)).argmin()
    return pipedb.iloc[myindex, 1] * u.inch

# Returns the inner diameter for SDR (standard diameter ratio) pipes. 
# For these pipes the wall thickness is the outer diameter divided by the SDR.
def ID_SDR(ND, SDR):
    ID = OD(ND) * (SDR-2) / SDR
    return ID

# Returns the inner diameter for schedule 40 pipes. The wall thickness for these pipes is in the pipedb.
def ID_sch40(ND):
    #take the values of the array, subtract the ND, take the absolute value, find the index of the minimium value
    myindex = (np.abs(np.array(pipedb['NDinch']) - (ND.to(u.inch)).magnitude)).argmin()
    return (pipedb.iloc[myindex, 1] - 2*(pipedb.iloc[myindex,5])) * u.inch

# Returns an array of available nominal diameters that are commonly used based on the 'Used' column in the pipedb
def ND_all_available():
    ND_all_available = []
    for i in range(len(pipedb['NDinch'])):
        if pipedb.iloc[i,4] == 1:
            ND_all_available.append((pipedb['NDinch'][i]))
    return ND_all_available*u.inch

# Returns an array of inner diameters that are commonly used based on the 'Used' column in the pipedb and given an SDR
def ID_SDR_all_available(SDR):
    ID = []
    ND = ND_all_available()
    for i in range(len(ND)):
        ID.append(ID_SDR(ND[i], SDR).magnitude)
    return ID*u.inch

# Return an available ND given an ID and a schedule
# Take the values of the array, compare to the ID, find the index of the first value greater or equal
def ND_SDR_available(ID,SDR):
    nd_list = []
    for i in range(len(np.array(ID_SDR_all_available(SDR)))):
        if np.array(ID_SDR_all_available(SDR))[i] >= (ID.to(u.inch)).magnitude:
            nd_list.append(np.array(ID_SDR_all_available(SDR))[i])
    print (nd_list)
            

    myindex = nd_list.index(max(nd_list))
    return ND_all_available()[myindex]


# Returns the minimum ND that is available.
def ND_available(NDguess):
    # Extract the magnitude in inches from the nominal diameter
    # Find the index of the closest nominal diameter
    # Take the values of the array, subtract the ND, take the absolute value, find the index of the minimium value
    myindex = (ND_all_available() >= NDguess)
    return min(ND_all_available()[myindex])
