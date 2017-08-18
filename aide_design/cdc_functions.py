# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 13:57:23 2017

@author: cc2467
"""
import math

import numpy as np

import pandas as pd

from aide_design import physchem as pc

from aide_design.units import unit_registry as u

from aide_design import utility as ut

from aide_design import expert_inputs as exp

#==============================================================================
# Functions for Coagulant Viscosities and Selecting Available Tube Diameters
#==============================================================================

def _DiamTubeAvail(en_tube_series = True):
    if en_tube_series:    
        return 1*u.mm
    else:
        return (1/16)*u.inch
# This section may be unnecessary
#==============================================================================
# def _DiamTubeAvail(en_tube_series = True):
#     if en_tube_series:    
#         return 1*u.mm
#     else:
#         return (1/16)*u.inch
#==============================================================================

NU_WATER = 1*(u.mm**2/u.s)

@u.wraps(u.m**2/u.s, [u.kg/u.m**3], False)
def _nu_alum(conc_alum):
    nu = (1 + (4.255 * 10**-6) * conc_alum**2.289) * NU_WATER
    return nu.to(u.mm**2/u.s)
    
    return nu


@u.wraps(u.m**2/u.s, [u.kg/u.m**3], False)   
def _nu_pacl(conc_pacl):
    nu = (1 + (2.383 * 10**-5) * conc_pacl**1.893) * NU_WATER
    return nu.to(u.mm**2/u.s)
    
    return nu


@u.wraps(u.m**2/u.s, [u.kg/u.m**3, None], False)    
def _nu_chem(conc_chem, en_chem):
    if en_chem == 0:
        return _nu_alum(conc_chem)
        return _nu_pacl(conc_chem)
    else:
        return NU_WATER

  
    
#==============================================================================
# Flow rate Constraints for Laminar Tube Flow, Deviation from Linear Head Loss
# Behavior, and Lowest Possible Flow 
#==============================================================================

# Maximum flow that can be put through a tube of a given diameter without 
# exceeding the allowable deviation from linear head loss behavior

@u.wraps(u.L/u.s, [u.m, u.m], False)
@u.wraps(u.m**3/u.s, [u.m, u.m], False)
def _flow_available(Diam, HeadlossCDC):
    flow = math.pi * Diam**2 / 4 * (((
                2 * exp.RATIO_LINEAR_CDC_ERROR * HeadlossCDC * pc.gravity)/
                    exp.K_MINOR_CDC_TUBE)**1/2)
    sqrt = 2 * exp.RATIO_LINEAR_CDC_ERROR * HeadlossCDC * pc.gravity.magnitude / exp.K_MINOR_CDC_TUBE
    flow = math.pi * Diam**2 / 4 * (sqrt**0.5)
    return flow




#==============================================================================
# Length of Tubing Required Given Head Loss, Max Flow, and Diameter 
#==============================================================================

# Length of tube required to get desired head loss at maximum flow based on 
# the Hagen-Poiseuille equation.    
@u.wraps(u.m, [u.m**3/u.s, u.m, u.m, u.m**2/u.s, None], False)
def _len_tube(flow, Diam, headloss, nu, k_minor):
    len = (((headloss*pc.gravity*math.pi*(Diam**4)/flow
             )-(k_minor*8*flow/math.pi
                ))/(128*nu))
def _len_tube(Flow, Diam, HeadLoss, Nu, KMinor):
    num1 = pc.gravity.magnitude * HeadLoss * math.pi * (Diam**4)
    denom1 = 128 * Nu * Flow
    num2 = Flow * KMinor
    denom2 = 16 * math.pi * Nu
    len = ((num1/denom1) - (num2/denom2))
    return len



#==============================================================================
# Helper Functions     
#==============================================================================
@u.wraps(None, [u.m**3/u.s, u.kg/u.m**3, u.kg/u.m**3, u.m, u.m], False)
def _n_tube_array(FlowPlant, ConcDoseMax, ConcStock, 
                  DiamTubeAvail, HeadlossCDC): 
    
    math.ceil((FlowPlant * ConcDoseMax
               )/ ConcStock*_flow_available(DiamTubeAvail, HeadlossCDC)) 
    return np.ceil((FlowPlant * ConcDoseMax) / 
            (ConcStock * _flow_available(DiamTubeAvail, HeadlossCDC).magnitude)) 


@u.wraps(u.m**3/u.s, [u.m**3/u.s, u.kg/u.m**3, u.kg/u.m**3], False)
def _flow_chem_stock(FlowPlant, ConcDoseMax, ConcStock):
    FlowPlant * ConcDoseMax / ConcStock 
    return FlowPlant * ConcDoseMax / ConcStock 
    

@u.wraps(u.m**3/u.s, [u.m**3/u.s, u.kg/u.m**3, u.kg/u.m**3, u.m, u.m], False)
def _flow_cdc_tube(FlowPlant, ConcDoseMax, ConcStock, 
                   DiamTubeAvail, HeadlossCDC):
    
    (_flow_chem_stock(FlowPlant, ConcDoseMax, ConcStock)
     ) / (_n_tube_array(FlowPlant, ConcDoseMax, ConcStock, 
    return (_flow_chem_stock(FlowPlant, ConcDoseMax, ConcStock).magnitude
            ) / (_n_tube_array(FlowPlant, ConcDoseMax, ConcStock, 
                        DiamTubeAvail, HeadlossCDC)
          )
                ) 
    
    
# Calculate the length of each diameter tube given the corresponding flow rate
# and coagulant 
# Choose the tube that is shorter than the maximum length tube.
@u.wraps(u.m, [u.m**3/u.s, u.kg/u.m**3, u.kg/u.m**3, u.m, u.m, None, None], False)
def _length_cdc_tube_array(FlowPlant, ConcDoseMax, ConcStock, 
                           DiamTubeAvail, HeadlossCDC, ENCoag, MinorLossCDCTube):
    
    _len_tube(_flow_cdc_tube(FlowPlant, ConcDoseMax, ConcStock, 
                             DiamTubeAvail, HeadlossCDC
                             ) , DiamTubeAvail, HeadlossCDC, _nu_chem(ConcStock, ENCoag
                                                                      ), MinorLossCDCTube)
    Flow = _flow_cdc_tube(FlowPlant, ConcDoseMax, ConcStock, DiamTubeAvail, HeadlossCDC).magnitude
    Nu =  _nu_chem(ConcStock, ENCoag).magnitude
    
    return _len_tube(Flow, DiamTubeAvail, HeadlossCDC, Nu, MinorLossCDCTube).magnitude
    

# Find the index of that tube
@u.wraps(None, [u.m**3/u.s, u.kg/u.m**3, u.kg/u.m**3, u.m, u.m, u.m, None, None], False)
def i_cdc(FlowPlant, ConcDoseMax, ConcStock, 
          DiamTubeAvail, HeadlossCDC, LenCDCTubeMax, 
          ENCoag, MinorLossCDCTube):
    
    tube_array = _length_cdc_tube_array(FlowPlant, ConcDoseMax, ConcStock, 
    tube_value = _length_cdc_tube_array(FlowPlant, ConcDoseMax, ConcStock, 
                                        DiamTubeAvail, HeadlossCDC, ENCoag, 
                                        MinorLossCDCTube)
    if tube_array[0] < LenCDCTubeMax:
        y=ut.floor_nearest(LenCDCTubeMax,tube_array)
        x=tube_array.index(y)
                                        MinorLossCDCTube).magnitude

    if tube_value[0] < LenCDCTubeMax:
        y = ut.floor_nearest(LenCDCTubeMax,tube_value)
        x = np.argmax(tube_value >= y)
    else:
        x=0
        x = 0
    return x



#==============================================================================
# Final easy to use functions
#==============================================================================
#The length of tubing may be longer than the max specified if the stock concentration is too
# high to give a viable solution with the specified length of tubing.
@u.wraps(u.m, [u.m**3/u.s, u.kg/u.m**3, u.kg/u.m**3, u.m, u.m, u.m, None, None], False)
def len_cdc_tube(FlowPlant, ConcDoseMax, ConcStock, 
                 DiamTubeAvail, HeadlossCDC, LenCDCTubeMax, 
                 ENCoag, MinorLossCDCTube):
    index=i_cdc(FlowPlant, ConcDoseMax, ConcStock, 
   
    index = i_cdc(FlowPlant, ConcDoseMax, ConcStock, 
                DiamTubeAvail, HeadlossCDC, LenCDCTubeMax, 
                ENCoag, MinorLossCDCTube)
    len_cdc_tube=_length_cdc_tube_array(FlowPlant, ConcDoseMax, ConcStock, 
    len_cdc_tube = _length_cdc_tube_array(FlowPlant, ConcDoseMax, ConcStock, 
                                        DiamTubeAvail, HeadlossCDC, ENCoag, 
                                        MinorLossCDCTube)[index]
                                        MinorLossCDCTube)[index].magnitude
   
    return len_cdc_tube


@u.wraps(u.m, [u.m**3/u.s, u.kg/u.m**3, u.kg/u.m**3, u.m, u.m, u.m, None, None], False)
def diam_cdc_tube(FlowPlant, ConcDoseMax, ConcStock, 
          DiamTubeAvail, HeadlossCDC, LenCDCTubeMax, 
          ENCoag, MinorLossCDCTube):
     index=i_cdc(FlowPlant, ConcDoseMax, ConcStock, 
          DiamTubeAvail, HeadlossCDC, LenCDCTubeMax, 
          ENCoag, MinorLossCDCTube)
     diam_cdc_tube=DiamTubeAvail[index]
     return diam_cdc_tube
 

@u.wraps(None, [u.m**3/u.s, u.kg/u.m**3, u.kg/u.m**3, u.m, u.m, u.m, None, None], False)    
def n_cdc_tube(FlowPlant, ConcDoseMax, ConcStock, 
          DiamTubeAvail, HeadlossCDC, LenCDCTubeMax, 
          ENCoag, MinorLossCDCTube):
    index=i_cdc(FlowPlant, ConcDoseMax, ConcStock, 
          DiamTubeAvail, HeadlossCDC, LenCDCTubeMax, 
          ENCoag, MinorLossCDCTube)
    n_cdc_tube = _n_tube_array(FlowPlant, ConcDoseMax, ConcStock, 
                  DiamTubeAvail, HeadlossCDC)[index]
    return n_cdc_tube




# testing
FLOW_PLANT = 0.01*u.m**3/u.s
DIAM_ENGLISH_TUBE_AVAIL = np.array(np.arange(1/16,6/16,1/16))*u.inch
NU_BLEACH = 1*(u.mm**2/u.s)
HEADLOSS_MAX = 10*(u.cm)
CONC_BLEACH_CL2 = 51.4*(u.gram/u.L)
CONC_CL2 = 2*(u.mg/u.L)                                    
LENGTH_CDC_TUBE_MAX = 2 * u.m
EN_CHEM = 2
K_MINOR = 2
