# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 11:55:37 2017

@author: kn348
"""
########################## Imports ##########################
import math
from scipy import constants, interpolate
import numpy as np
import pandas as pd

try:
    from AguaClara_design.units import unit_registry as u
    from AguaClara_design import utility as ut
except ModuleNotFoundError:
    from units import unit_registry as u
    import utility as ut


g=9.80665*(u.m/(u.s**2))
#==============================================================================
# Coagulant dose controller
#==============================================================================



NU_WATER = 1* u.mm**2/u.s

#==============================================================================
# #coagulant viscosity
#==============================================================================
def nu_alum(ConcAlum):
    ConcAlum = ConcAlum.to(1/u.kg/(u.m**3))
    return (1 + (4.255 * 10**(-6) * (ConcAlum)**2.289))*NU_WATER

def nu_pacl(ConcPacl):
    ConcPacl = ConcPacl.to(1/u.kg/(u.m**3))
    return (1 + (2.383 * 10**(-5) * (ConcPacl)**1.893))*NU_WATER

def nu_coag(ConcCoag, ENCoag):
    
    if ENCoag == 0:
        return nu_alum(ConcCoag)
    elif ENCoag == 1:
        return nu_pacl(ConcCoag)

#==============================================================================
# stock volume and concentration
#==============================================================================
def flow_coag_max_est(flow_train,conc_coag_dose_max,conc_coag_stock_est):
    return flow_train*conc_coag_dose_max/conc_coag_stock_est

def vol_coag_stock():
    pass
    