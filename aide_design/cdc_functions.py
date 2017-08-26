# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 13:57:23 2017

@author: cc2467
"""
import math

import numpy as np

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

@u.wraps(u.m**2/u.s, [u.kg/u.m**3, u.degK], False)
def viscosity_kinematic_alum(conc_alum, temp):
    """Return the dynamic viscosity of water at a given temperature.
    
    If given units, the function will automatically convert to Kelvin.
    If not given units, the function will assume Kelvin.
    """
    nu = (1 + (4.255 * 10**-6) * conc_alum**2.289) * pc.viscosity_kinematic(temp).magnitude
    return nu


@u.wraps(u.m**2/u.s, [u.kg/u.m**3, u.degK], False)   
def viscosity_kinematic_pacl(conc_pacl, temp):
    """Return the dynamic viscosity of water at a given temperature.
    
    If given units, the function will automatically convert to Kelvin.
    If not given units, the function will assume Kelvin.
    """
    nu = (1 + (2.383 * 10**-5) * conc_pacl**1.893) * pc.viscosity_kinematic(temp).magnitude
    return nu


@u.wraps(u.m**2/u.s, [u.kg/u.m**3, u.degK, None], False)    
def viscosity_kinematic_chem(conc_chem, temp, en_chem):
     """Return the dynamic viscosity of water at a given temperature.
    
    If given units, the function will automatically convert to Kelvin.
    If not given units, the function will assume Kelvin.
    """
     if en_chem == 0:
         nu = viscosity_kinematic_alum(conc_chem, temp).magnitude
     if en_chem == 1:
         nu =  viscosity_kinematic_pacl(conc_chem, temp).magnitude
     if en_chem not in [0,1]:
         nu =  pc.viscosity_kinematic(temp).magnitude
     return nu

  
    
#==============================================================================
# Flow rate Constraints for Laminar Tube Flow, Deviation from Linear Head Loss
# Behavior, and Lowest Possible Flow 
#==============================================================================


@u.wraps(u.m**3/u.s, [u.m, u.m, None, None], False)
def max_linear_flow(Diam, HeadlossCDC, Ratio_Linear_CDC_Error, KMinor):
    """Return the maximum flow that will meet the linear requirement.
    Maximum flow that can be put through a tube of a given diameter without 
    exceeding the allowable deviation from linear head loss behavior
    """
    flow = (pc.area_circle(Diam)).magnitude * np.sqrt((2 * Ratio_Linear_CDC_Error * HeadlossCDC * pc.gravity)/ KMinor)
    return flow.magnitude




#==============================================================================
# Length of Tubing Required Given Head Loss, Max Flow, and Diameter 
#==============================================================================

# Length of tube required to get desired head loss at maximum flow based on 
# the Hagen-Poiseuille equation.    
@u.wraps(u.m, [u.m**3/u.s, u.m, u.m, u.m**2/u.s, None], False)
def _len_tube(Flow, Diam, HeadLoss, Nu, KMinor):
    """Length of tube required to get desired head loss at maximum flow based on 
    the Hagen-Poiseuille equation."""
    num1 = pc.gravity.magnitude * HeadLoss * np.pi * (Diam**4)
    denom1 = 128 * Nu * Flow
    num2 = Flow * KMinor
    denom2 = 16 * np.pi * Nu
    len = ((num1/denom1) - (num2/denom2))
    return len



#==============================================================================
# Helper Functions     
#==============================================================================
@u.wraps(None, [u.m**3/u.s, u.kg/u.m**3, u.kg/u.m**3, u.m, u.m, None, None], False)
def _n_tube_array(FlowPlant, ConcDoseMax, ConcStock, 
                  DiamTubeAvail, HeadlossCDC,Ratio_Linear_CDC_Error, KMinor): 
    
    np.ceil((FlowPlant * ConcDoseMax
               )/ ConcStock*max_linear_flow(DiamTubeAvail, HeadlossCDC, Ratio_Linear_CDC_Error, KMinor).magnitude) 
    return np.ceil((FlowPlant * ConcDoseMax) / 
            (ConcStock * max_linear_flow(DiamTubeAvail, HeadlossCDC, Ratio_Linear_CDC_Error, KMinor).magnitude)) 


@u.wraps(u.m**3/u.s, [u.m**3/u.s, u.kg/u.m**3, u.kg/u.m**3], False)
def _flow_chem_stock(FlowPlant, ConcDoseMax, ConcStock):
    FlowPlant * ConcDoseMax / ConcStock 
    return FlowPlant * ConcDoseMax / ConcStock 
    

@u.wraps(u.m**3/u.s, [u.m**3/u.s, u.kg/u.m**3, u.kg/u.m**3, u.m, u.m], False)
def _flow_cdc_tube(FlowPlant, ConcDoseMax, ConcStock, 
                   DiamTubeAvail, HeadlossCDC):
    
    (_flow_chem_stock(FlowPlant, ConcDoseMax, ConcStock)
     ) / (_n_tube_array(FlowPlant, ConcDoseMax, ConcStock, DiamTubeAvail, HeadlossCDC))
    return (_flow_chem_stock(FlowPlant, ConcDoseMax, ConcStock).magnitude
            ) / (_n_tube_array(FlowPlant, ConcDoseMax, ConcStock, 
                        DiamTubeAvail, HeadlossCDC))
    
    
    
# 
@u.wraps(u.m, [u.m**3/u.s, u.kg/u.m**3, u.kg/u.m**3, u.m, u.m, u.degK, None, None], False)
def _length_cdc_tube_array(FlowPlant, ConcDoseMax, ConcStock, 
                           DiamTubeAvail, HeadlossCDC, temp, ENCoag, MinorLossCDCTube):
    """Calculate the length of each diameter tube given the corresponding flow rate
    and coagulant. Choose the tube that is shorter than the maximum length tube."""
    
    Flow = _flow_cdc_tube(FlowPlant, ConcDoseMax, ConcStock, DiamTubeAvail, HeadlossCDC).magnitude
    Nu =  viscosity_kinematic_chem(ConcStock, temp, ENCoag).magnitude
                  
    
    return _len_tube(Flow, DiamTubeAvail, HeadlossCDC, Nu, MinorLossCDCTube).magnitude
    

# Find the index of that tube
@u.wraps(None, [u.m**3/u.s, u.kg/u.m**3, u.kg/u.m**3, u.m, u.m, u.m, None, None], False)
def i_cdc(FlowPlant, ConcDoseMax, ConcStock, 
          DiamTubeAvail, HeadlossCDC, LenCDCTubeMax, 
          ENCoag, MinorLossCDCTube):
    
    tube_array = _length_cdc_tube_array(FlowPlant, ConcDoseMax, ConcStock, 
                                        DiamTubeAvail, HeadlossCDC, ENCoag, 
                                        MinorLossCDCTube) 
    
    print(tube_array[0].magnitude)
    print(LenCDCTubeMax)
    
    if tube_array[0].magnitude < float(LenCDCTubeMax):
        y = ut.floor_nearest(LenCDCTubeMax,tube_array)
        x = (tube_array.index(y)).magnitude
    
    else:
        x = 0
    
    return x



#==============================================================================
# Final easy to use functions
#==============================================================================

@u.wraps(u.m, [u.m**3/u.s, u.kg/u.m**3, u.kg/u.m**3, u.m, u.m, u.m, None, None], False)
def len_cdc_tube(FlowPlant, ConcDoseMax, ConcStock, 
                 DiamTubeAvail, HeadlossCDC, LenCDCTubeMax, 
                 ENCoag, MinorLossCDCTube):
   """The length of tubing may be longer than the max specified if the stock 
   concentration is too high to give a viable solution with the specified 
   length of tubing."""
   index = i_cdc(FlowPlant, ConcDoseMax, ConcStock, 
                DiamTubeAvail, HeadlossCDC, LenCDCTubeMax, 
                ENCoag, MinorLossCDCTube)
   len_cdc_tube = (_length_cdc_tube_array(FlowPlant, ConcDoseMax, ConcStock, 
                                        DiamTubeAvail, HeadlossCDC, ENCoag, 
                                        MinorLossCDCTube))[index].magnitude
   
   return len_cdc_tube


@u.wraps(u.m, [u.m**3/u.s, u.kg/u.m**3, u.kg/u.m**3, u.m, u.m, u.m, None, None], False)
def diam_cdc_tube(FlowPlant, ConcDoseMax, ConcStock, 
                  DiamTubeAvail, HeadlossCDC, LenCDCTubeMax, 
                  ENCoag, MinorLossCDCTube):
     
    index = i_cdc(FlowPlant, ConcDoseMax, ConcStock, 
                   DiamTubeAvail, HeadlossCDC, LenCDCTubeMax, 
                   ENCoag, MinorLossCDCTube)
    
    diam_cdc_tube = DiamTubeAvail[index]
     
    return diam_cdc_tube
 

@u.wraps(None, [u.m**3/u.s, u.kg/u.m**3, u.kg/u.m**3, u.m, u.m, u.m, None, None], False)    
def n_cdc_tube(FlowPlant, ConcDoseMax, ConcStock, 
          DiamTubeAvail, HeadlossCDC, LenCDCTubeMax, 
          ENCoag, MinorLossCDCTube):
    
    index = i_cdc(FlowPlant, ConcDoseMax, ConcStock, 
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
