# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 13:57:23 2017

@author: cc2467
"""
import math

from scipy import constants, interpolate

#see numpy cheat sheet https://www.dataquest.io/blog/images/cheat-sheets/numpy-cheat-sheet.pdf
#The numpy import is needed because it is renamed here as np.
import numpy as np

import pandas as pd

import matplotlib.pyplot as plt

import sys, os

myGitHubdir=os.path.expanduser('~\\Documents\\GitHub')
if myGitHubdir not in sys.path:
    sys.path.append(myGitHubdir)

from AguaClara_design import physchem as pc

from AguaClara_design import pipedatabase as pipe

from AguaClara_design.units import unit_registry as u 

from AguaClara_design import utility as ut

from AguaClara_design import expert_inputs as exp

#==============================================================================
# Functions for Coagulant Viscosities and Selecting Available Tube Diameters
#==============================================================================

def _diam_tube_avail(en_tube_series = True):
    if en_tube_series:    
        return 1*u.mm
    else:
        return (1/16)*u.inch

NU_WATER = 1*(u.mm**2/u.s)

def _nu_alum(conc_alum):
    
    nu = (1 + (4.255 * 10**-6) * conc_alum**2.289) * NU_WATER
    return nu.to(u.mm**2/u.s)
    
def _nu_pacl(conc_pacl):
    
    nu = (1 + (2.383 * 10**-5) * conc_pacl**1.893) * NU_WATER
    return nu.to(u.mm**2/u.s)
    
def _nu_chem(conc_chem, en_chem):
    if en_chem == 0:
        return _nu_alum(conc_chem)
    elif en_chem == 1:
        return _nu_pacl(conc_chem)
    else:
        return NU_WATER
    
#==============================================================================
# Flow rate Constraints for Laminar Tube Flow, Deviation from Linear Head Loss
# Behavior, and Lowest Possible Flow 
#==============================================================================

# Maximum flow that can be put through a tube of a given diameter without 
# exceeding the allowable deviation from linear head loss behavior
def _flow_available(diam, headloss_cdc):
    flow = math.pi * diam**2 / 4 * (((
                2 * exp.RATIO_LINEAR_CDC_ERROR * headloss_cdc * pc.gravity)/
                    exp.K_MINOR_CDC_TUBE)**1/2)
    return flow 


    
    
    