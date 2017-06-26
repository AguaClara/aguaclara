# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 11:55:37 2017

@author: kn348
"""
import math

from scipy import constants, interpolate

#see numpy cheat sheet https://www.dataquest.io/blog/images/cheat-sheets/numpy-cheat-sheet.pdf
#The numpy import is needed because it is renamed here as np.
import numpy as np

import pandas as pd

# sys and os give us access to operating system directory paths and to sys paths.
import sys, os



# If you place your GitHub directory in your documents folder and 
# clone both the design challenge notebook and the AguaClara_design repo, then this code should all work.
# If you have your GitHub directory at a different location on your computer, 
# then you will need to adjust the directory path below.
# add the path to your GitHub directory so that python can find files in other contained folders.
myGitHubdir=os.path.expanduser('~\\Documents\\GitHub')
if myGitHubdir not in sys.path:
    sys.path.append(myGitHubdir)


# units allows us to include units in all of our calculations
from AguaClara_design.units import unit_registry as u

# utility has the significant digit display function
from AguaClara_design import utility as ut

g=9.80665*(u.m/(u.s**2))
#Coagulant dose controller
nu_water=u.mm**2/u.s

#coagulant viscosity
def nu_alum(conc_alum):
    conc_alum=conc_alum.to(1/u.kg/(u.m**3))
    return (1+(4.255*10**(-6)(conc_alum)**2.289))*nu_water

def nu_pacl(conc_pacl):
    conc_pacl=conc_pacl.to(1/u.kg/(u.m**3))
    return (1+(2.383*10**(-5)(conc_pacl)**1.893))*nu_water

def nu_coag(conc_coag,EN_coag):
    
    if EN_coag==0:
        return nu_alum(conc_coag)
    elif EN_coag==1:
        return nu_pacl(conc_coag)

#stock volume and concentration
def flow_coag_max_est(flow_train,conc_coag_dose_max,conc_coag_stock_est):
    return flow_train*conc_coag_dose_max/conc_coag_stock_est

def vol_coag_stock()
    