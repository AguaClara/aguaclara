"""
Created on Thu Jun 15 14:07:28 2017

@author: Karan Newatia

Last modified: Wed Jul 5 2017 
By: Sage Weber-Shirk


This file contains unit process functions pertaining to the design of 
physical/chemical unit processes for AguaClara water treatment plants.
"""

######################### Imports #########################
import numpy as np
import scipy

from AguaClara_design.units import unit_registry as u

gravity = 9.80665 * u.m/u.s**2
"""Define the gravitational constant, in m/s²."""

#######################Simple geometry#######################
"""A few equations for useful geometry.
Is there a geometry package that we should be using?
"""

def area_circle(diam_Circle):
    """Return the area of a circle."""
    return np.pi/4*diam_Circle**2


@u.wraps(u.m, u.m**2, False)
def diam_circle(A_Circle):
    """Return the diameter of a circle."""
    return np.sqrt(4*A_Circle/np.pi)

######################### Hydraulics ######################### 
RATIO_VC_ORIFICE = 0.62

RE_TRANSITION_PIPE = 2100



WATER_DENSITY_TABLE = [(273.15, 278.15, 283.15, 293.15, 303.15, 313.15, 
                        323.15, 333.15, 343.15, 353.15, 363.15, 373.15
                        ), (999.9, 1000, 999.7, 998.2, 995.7, 992.2, 
                            988.1, 983.2, 977.8, 971.8, 965.3, 958.4
                            )
                       ]
"""Table of temperatures and the corresponding water density.

Index[0] is a list of water temperatures, in Kelvin.
Index[1] is the corresponding densities, in kg/m³.
"""


@u.wraps(u.kg/(u.m*u.s), [u.degK], False)
def viscosity_dynamic(T):
    """Return the dynamic Visc of water at a given temperature.
    
    If given units, the function will automatically convert them to Kelvin.
    If not given units, the function will assume Kelvin.
    """
    return 2.414 * (10**-5) * 10**((247.8)/(T-140))


@u.wraps(u.kg/u.m**3, [u.degK], False)
def density_water(temp):
    """Return the density of water at a given temperature.
    
    If given units, the function will automatically convert them to Kelvin.
    If not given units, the function will assume Kelvin.
    """
    rhointerpolated = scipy.interpolate.CubicSpline(WATER_DENSITY_TABLE[0], 
                                                    WATER_DENSITY_TABLE[1])
    return rhointerpolated(temp)


@u.wraps(u.m**2/u.s, [u.degK], False)
def viscosity_kinematic(T):
    """Return the kinematic Visc of water at a given temperature.
    
    If given units, the function will automatically convert them to Kelvin.
    If not given units, the function will assume Kelvin.
    """
    return (viscosity_dynamic(T).magnitude 
            / density_water(T).magnitude)


@u.wraps(None, [u.m**3/u.s, u.m, u.m**2/u.s], False)
def re_pipe(FlowRate, Diam, Visc):
    """Return the Reynolds Number for a pipe."""
    return (4 * FlowRate) / (np.pi * Diam * Visc)


@u.wraps(u.m, [u.m, u.m, None], False)
def radius_hydraulic(Width, DistCenter, openchannel):
    """Return the hydraulic radius."""  
    if openchannel:
        h = (Width*DistCenter) / (Width + 2*DistCenter)
        # if openchannel is True, the channel is open. Otherwise, the channel 
        # is assumed to have a top. 
    else:
        h = (Width*DistCenter) / (2 * (Width+DistCenter))
    return h


@u.wraps(u.m, [u.m**2, u.m], False)
def radius_hydraulic_general(Area, WP):
    """Return the general hydraulic radius."""
    return Area / WP 


@u.wraps(None, [u.m**3/u.s, u.m, u.m, u.m**2/u.s, None], False)
def re_rect(FlowRate, Width, DistCenter, Visc, openchannel):
    """Return the Reynolds Number for a rectangular channel."""
    return (4 * FlowRate 
            * radius_hydraulic(Width, DistCenter, openchannel).magnitude
            / (Width * DistCenter * Visc))
    #Reynolds Number for rectangular channel; open = False if all sides
    #are wetted; l = Diam and Diam = 4*R.h     
    

@u.wraps(None, [u.m/u.s, u.m**2, u.m, u.m**2/u.s], False)
def re_general(Vel, Area, WP, Visc):
    """Return the Reynolds Number for a general cross section."""
    return 4 * radius_hydraulic_general(Area, WP).magnitude * Vel / Visc
        

@u.wraps(None, [u.m**3/u.s, u.m, u.m**2/u.s, u.m], False)
def fric(FlowRate, Diam, Visc, PipeRough):
    """Return the friction factor for pipe flow.
    
    This equation applies to both laminar and turbulent flows.
    """
    if re_pipe(FlowRate, Diam, Visc) >= RE_TRANSITION_PIPE:
        #Swamee-Jain friction factor for turbulent flow; best for 
        #Re>3000 and ε/Diam < 0.02        
        f = (0.25 / (np.log10(PipeRough/(3.7*Diam) + 5.74 
                                / re_pipe(FlowRate, Diam, Visc)**0.9
                                )
                     ) ** 2
             )
    else:
        f = 64 / re_pipe(FlowRate, Diam, Visc)
    return f


@u.wraps(None, [u.m**3/u.s, u.m, u.m, u.m**2/u.s, u.m, None], False)
def fric_rect(FlowRate, Width, SepDist, Visc, PipeRough, openchannel):
    """Return the friction factor for a rectangular channel."""
    if re_rect(FlowRate,Width,SepDist,Visc,openchannel) >= RE_TRANSITION_PIPE:
        #Swamee-Jain friction factor adapted for rectangular channel.
        #Diam = 4*R_h in this case.         
        f = (0.25 
             / (np.log10(PipeRough 
                           / ((3.7 * 4 
                               * radius_hydraulic(Width, SepDist, openchannel)
                               ) + 5.74
                              ) 
                           /re_rect(FlowRate,Width,SepDist,Visc,openchannel)**0.9
                           )
                ) ** 2
             )
    else:
        f = 64 / re_rect(FlowRate, Width, SepDist, Visc, openchannel)
    return f
 

@u.wraps(None, [u.m**2, u.m, u.m/u.s, u.m**2/u.s, u.m], False)
def fric_general(Area, PerimWetted, Vel, Visc, PipeRough):
    """Return the friction factor for a general channel."""
    if re_general(Vel, Area, PerimWetted, Visc) >= RE_TRANSITION_PIPE:
        #Swamee-Jain friction factor adapted for any cross-section.
        #Diam = 4*R*h 
        f= (0.25 /
            (np.log10(PipeRough
                      / (3.7 * 4 * radius_hydraulic_general(Area, PerimWetted))
                      + 5.74
                      / re_general(Vel, Area, PerimWetted, Visc) ** 0.9
                      )
             ) ** 2
            )
    else:
        f = 64 / re_general(Vel, Area, PerimWetted, Visc)
    return f      
         

@u.wraps(u.m, [u.m**3/u.s, u.m, u.m, u.m**2/u.s, u.m], False)
def headloss_fric(FlowRate, Diam, Length, Visc, PipeRough):
    """Return the major head loss (due to wall shear) in a pipe.
    
    This equation applies to both laminar and turbulent flows.
    """
    return (fric(FlowRate, Diam, Visc, PipeRough) * 8 / (gravity.magnitude * np.pi**2) 
            * (Length * FlowRate**2) / Diam**5
            )


@u.wraps(u.m, [u.m**3/u.s, u.m, None], False)
def headloss_exp(FlowRate, Diam, MinorLoss):
    """Return the minor head loss (due to expansions) in a pipe. 
    
    This equation applies to both laminar and turbulent flows.
    """
    return MinorLoss * 8 / (gravity.magnitude * np.pi**2) * FlowRate**2 / Diam**4


@u.wraps(u.m, [u.m**3/u.s, u.m, u.m, u.m**2/u.s, u.m, None], False)
def headloss(FlowRate, Diam, Length, Visc, PipeRough, MinorLoss):
    """Return the total head loss from major and minor losses in a pipe.
    
    This equation applies to both laminar and turbulent flows.
    """
    return (headloss_fric(FlowRate, Diam, Length, Visc, PipeRough).magnitude
            + headloss_exp(FlowRate, Diam, MinorLoss)).magnitude


@u.wraps(u.m, [u.m**3/u.s, u.m, u.m, u.m, u.m**2/u.s, u.m, None], False)
def headloss_fric_rect(FlowRate, Width, SepDist, Length, Visc, PipeRough, openchannel):
    """Return the major head loss due to wall shear in a rectangular channel.
    
    This equation applies to both laminar and turbulent flows.
    """
    return (fric_rect(FlowRate, Width, SepDist, Visc, 
                      PipeRough, openchannel).magnitude 
            * Length 
            / (4 * radius_hydraulic(Width, SepDist, openchannel)) 
            * FlowRate**2 
            / (2 * gravity.magnitude * (Width*SepDist)**2)
            )


@u.wraps(u.m, [u.m**3/u.s, u.m, u.m, None], False)
def headloss_exp_rect(FlowRate, Width, SepDist, MinorLoss):
     """Return the minor head loss due to expansion in a rectangular channel.
     
     This equation applies to both laminar and turbulent flows.
     """
     return MinorLoss * FlowRate**2 / (2 * gravity.magnitude * (Width*SepDist)**2) 
 

@u.wraps(u.m, [u.m**3/u.s, u.m, u.m, u.m, None, u.m**2/u.s, u.m, None], False)
def headloss_rect(FlowRate, Width, SepDist, Length, 
                  MinorLoss, Visc, PipeRough, openchannel):
      """Return the total head loss in a rectangular channel. 
      
      Total head loss is a combination of the major and minor losses.
      This equation applies to both laminar and turbulent flows.
      """
      return (headloss_exp_rect(FlowRate, Width, SepDist, MinorLoss).magnitude
              + headloss_fric_rect(FlowRate, Width, SepDist, Length, 
                                   Visc, PipeRough, openchannel).magnitude)
    

@u.wraps(u.m, [u.m**2, u.m, u.m/u.s, u.m, u.m**2/u.s, u.m], False)
def headloss_fric_general(Area, PerimWetted, Vel, Length, Visc, PipeRough):
     """Return the major head loss due to wall shear in the general case.
     
     This equation applies to both laminar and turbulent flows.
     """
     return (fric_general(Area, PerimWetted, Vel, Visc, PipeRough) * Length 
             / (4 * radius_hydraulic_general(Area, PerimWetted).magnitude) 
             * Vel**2 / (2*gravity.magnitude)
             )
     

@u.wraps(u.m, [u.m/u.s, None], False)
def headloss_exp_general(Vel, MinorLoss):
    """Return the minor head loss due to expansion in the general case.
    
    This equation applies to both laminar and turbulent flows.
    """
    return MinorLoss * Vel**2 / (2*gravity.magnitude)


@u.wraps(u.m, [u.m**2, u.m/u.s, u.m, u.m, None, u.m**2/u.s, u.m], False)
def headloss_gen(Area, Vel, PerimWetted, Length, MinorLoss, Visc, PipeRough):
     """Return the total head lossin the general case.
     
     Total head loss is a combination of major and minor losses.
     This equation applies to both laminar and turbulent flows.
     """
     return (headloss_exp_general(Vel, MinorLoss).magnitude 
             + headloss_fric_general(Area, PerimWetted, Vel,
                                     Length, Visc, PipeRough).magnitude)

 
@u.wraps(u.m, [u.m**2/u.s, u.m, u.m, None, u.m**2/u.s, u.m, None], False)  
def headloss_manifold(FlowRate, Diam, Length, MinorLoss, Visc, PipeRough, NumOutlets):
    """Return the total head loss through the manifold."""
    return (headloss(FlowRate,Diam,Length,Visc,PipeRough,MinorLoss).magnitude
            * (1/3 
               + 1 / (2*NumOutlets) 
               + 1 / ((6*NumOutlets)**2))
            )


@u.wraps(u.m**3/u.s, [u.m, u.m, None], False)
def flow_orifice(Diam, Height, RatioVCOrifice):
    """Return the flow rate of the orifice."""
    Height=np.array(Height)
    flow_orifice=[]
    for i in range(len(Height)):
         if Height[i] > 0:
            flow_orifice.append(RatioVCOrifice * area_circle(Diam) 
                * np.sqrt(2 * gravity.magnitude * Height[i]))
         else:
             flow_orifice.append(0)
    return flow_orifice


@u.wraps(u.m**3/u.s, [u.m, u.m, None], False)
def flow_orifice_vert(Diam, Height, RatioVCOrifice):
    """Return the vertical flow rate of the orifice."""
    Height=np.array(Height)
    FlowRate=[]
    for i in range(len(Height)):
        if Height > -Diam / 2:
           FlowRate.append(scipy.integrate.quad(lambda z: (Diam 
           * np.sin(np.acos(z/(Diam/2)))* np.sqrt(Height[i] - z)
           ), -Diam/2,min(Diam/2,Height)))
           FlowRateNew = FlowRate[0]
           return RatioVCOrifice * np.sqrt(2 * gravity.magnitude) * FlowRateNew * 1000
    else:
       return 0


@u.wraps(u.m, [u.m, None, u.m**3/u.s], False)
def head_orifice(Diam, RatioVCOrifice, FlowRate):
     """Return the head of the orifice."""
     return ((FlowRate 
              / (RatioVCOrifice * area_circle(Diam))
              )**2 
             / (2*gravity.magnitude)
             )

 
@u.wraps(u.m**2, [u.m, None, u.m**3/u.s], False)
def area_orifice(h, RatioVCOrifice, FlowRate):
    """Return the area of the orifice."""
    return FlowRate / (RatioVCOrifice * np.sqrt(2 * gravity.magnitude * h))
    

@u.wraps(None, [u.m**3/u.s, None, u.m, u.m], False)
def num_orifices(FlowPlant, RatioVCOrifice, HeadLossOrifice, DiamOrifice):
     """Return the number of orifices."""
     return np.ceil(area_orifice(HeadLossOrifice, RatioVCOrifice, 
                                 FlowPlant).magnitude
                    / area_circle(DiamOrifice)
                    )
 

@u.wraps(u.m, [None, u.m**3/u.s, u.m, u.m, None, None, u.m**2/u.s, u.m, None],
         False)
def diam_orifice_manifold(FlowManifoldRatio, FlowTank, DiamPipe, Length, 
                          MinorLossTotal, NumOrifices, Visc, PipeRough, 
                          RatioVCOrifice):
     """Return the diameter of the orifice in the manifold."""
     return ((((1 - FlowManifoldRatio)*DiamPipe) ** 4 
              / ((((MinorLossTotal 
                    + (fric(FlowTank, DiamPipe, Visc, PipeRough) * Length/DiamPipe)
                    )
                   * (FlowManifoldRatio)
                   ) 
                   - MinorLossTotal 
                   - (fric(FlowTank,DiamPipe,Visc,PipeRough) 
                      * Length / DiamPipe
                      ) 
                   * RatioVCOrifice**2 
                   * NumOrifices**2
                   )
                 )
              ) ** (1/4))
 
    
# Here we define functions that return the flow rate.
@u.wraps(u.m**3/u.s, [u.m, u.m**2/u.s], False)
def flow_transition(Diam, Visc):
    """Return the flow rate for the laminar/turbulent transition.
    
    This equation is used in some of the other equations for flow.
    """
    return np.pi * Diam * RE_TRANSITION_PIPE * Visc / 4


@u.wraps(u.m**3/u.s, [u.m, u.m, u.m, u.m**2/u.s], False)
def flow_hagen(Diam, HeadLossFric, Length, Visc):
    """Return the flow rate for laminar flow with only major losses."""
    return (np.pi * Diam**4) / (128*Visc) * gravity.magnitude * HeadLossFric / Length


@u.wraps(u.m**3/u.s, [u.m, u.m, u.m, u.m**2/u.s, u.m], False)
def flow_swamee(Diam, HeadLossFric, Length, Visc, PipeRough):
    """Return the flow rate for turbulent flow with only major losses."""
    logterm = -np.log10(PipeRough
                        / (3.7 * Diam) 
                        + 2.51 * Visc * np.sqrt(Length / (2 
                                                          * gravity.magnitude
                                                          * HeadLossFric
                                                          * Diam**3)
                                                )
                        )
    return ((np.pi / np.sqrt(2)) * Diam**(5/2) 
            * np.sqrt(gravity.magnitude * HeadLossFric / Length) * logterm
            )


@u.wraps(u.m**3/u.s, [u.m, u.m, u.m, u.m**2/u.s, u.m], False)
def flow_pipemajor(Diam, HeadLossFric, Length, Visc, PipeRough):
    """Return the flow rate with only major losses.
    
    This function applies to both laminar and turbulent flows.
    """
    FlowHagen = flow_hagen(Diam, HeadLossFric, Length, Visc).magnitude
    if FlowHagen < flow_transition(Diam, Visc).magnitude:
        return FlowHagen
    else:
        return flow_swamee(Diam, HeadLossFric, Length, Visc, PipeRough).magnitude


@u.wraps(u.m**3/u.s, [u.m, u.m, None], False)
def flow_pipeminor(Diam, HeadLossExpans, MinorLoss):
    """Return the flow rate with only minor losses.
    
    This function applies to both laminar and turbulent flows.
    """ 
    return (area_circle(Diam) * np.sqrt(2 * gravity.magnitude 
                                                  * HeadLossExpans 
                                                  / MinorLoss)
            )

# Now we put all of the flow equations together and calculate the flow in a 
# straight pipe that has both major and minor losses and might be either
# laminar or turbulent.
@u.wraps(u.m**3/u.s, [u.m, u.m, u.m, u.m**2/u.s, u.m, None], False)
def flow_pipe(Diam, HeadLoss, Length, Visc, PipeRough, MinorLoss):
    """Return the the flow in a straight pipe.
    
    This function works for both major and minor losses and 
    works whether the flow is laminar or turbulent.
    """
    if MinorLoss == 0:
        FlowRate = flow_pipemajor(Diam, HeadLoss, Length, Visc, 
                                  PipeRough).magnitude
    else:
        FlowRatePrev = 0
        err = 1
        FlowRate = min(flow_pipemajor(Diam, HeadLoss, Length, 
                                      Visc, PipeRough).magnitude, 
                       flow_pipeminor(Diam, HeadLoss, MinorLoss).magnitude
                       )
        while err > 0.01:
            FlowRatePrev = FlowRate
            HLFricNew = (HeadLoss * headloss_fric(FlowRate, Diam, Length, 
                                                  Visc, PipeRough).magnitude 
                         / (headloss_fric(FlowRate, Diam, Length, 
                                          Visc, PipeRough).magnitude
                            + headloss_exp(FlowRate, Diam, MinorLoss).magnitude
                            )
                         )
            FlowRate = flow_pipemajor(Diam, HLFricNew, Length, 
                                      Visc, PipeRough).magnitude
            if FlowRate == 0:
                err = 0
            else:
                err = abs(FlowRate - FlowRatePrev) / (FlowRate + FlowRatePrev)
    return FlowRate	
 

@u.wraps(u.m, [u.m**3/u.s, u.m, u.m, u.m**2/u.s], False)
def diam_hagen(FlowRate, HeadLossFric, Length, Visc):
    return ((128 * Visc * FlowRate * Length) 
            / (gravity.magnitude * HeadLossFric * np.pi)
            ) ** (1/4)


@u.wraps(u.m, [u.m**3/u.s, u.m, u.m, u.m**2/u.s, u.m], False)
def diam_swamee(FlowRate, HeadLossFric, Length, Visc, PipeRough):
    """Return the inner diameter of a pipe.
    
    The Swamee Jain equation is dimensionally correct and returns the 
    inner diameter of a pipe given the flow rate and the head loss due
    to shear on the pipe walls. The Swamee Jain equation does NOT take 
    minor losses into account. This equation ONLY applies to turbulent 
    flow.
    Pint has trouble adding two Numbers that are raised to the 25th 
    power. This function strips the units before adding the two 
    terms and then reattaches the units.
    """
    a = ((PipeRough**1.25) 
         * ((Length * FlowRate**2) 
            / (gravity.magnitude * HeadLossFric)
            )**4.75
         )
    b = (Visc * (FlowRate**9.4) * (Length / (gravity.magnitude*HeadLossFric))**5.2)
    return 0.66 * (a+b)**0.04


@u.wraps(u.m, [u.m**3/u.s, u.m, u.m, u.m**2/u.s, u.m], False)
def diam_pipemajor(FlowRate, HeadLossFric, Length, Visc, PipeRough):
    """Return the pipe IDiam that would result in given major losses.
    
    This function applies to both laminar and turbulent flow.
    """
    DiamLaminar = diam_hagen(FlowRate, HeadLossFric, Length, Visc).magnitude
    if re_pipe(FlowRate, DiamLaminar, Visc) <= RE_TRANSITION_PIPE:
        return DiamLaminar
    else:
        return diam_swamee(FlowRate, HeadLossFric, Length, 
                           Visc, PipeRough).magnitude


@u.wraps(u.m, [u.m**3/u.s, u.m, None], False)
def diam_pipeminor(FlowRate, HeadLossExpans, MinorLoss):
    """Return the pipe IDiam that would result in the given minor losses.
    
    This function applies to both laminar and turbulent flow.
    """
    return ((np.sqrt(4 * FlowRate / np.pi)) 
            * (MinorLoss / (2 * gravity.magnitude * HeadLossExpans)) ** (1/4)
            )


@u.wraps(u.m, [u.m**3/u.s, u.m, u.m, u.m**2/u.s, u.m, None], False)
def diam_pipe(FlowRate, HeadLoss, Length, Visc, PipeRough, MinorLoss):
    """Return the pipe IDiam that would result in the given total head loss.
    
    This function applies to both laminar and turbulent flow and
    incorporates both minor and major losses.
    """
    if MinorLoss == 0:
        Diam = diam_pipeminor(FlowRate, HeadLoss, MinorLoss).magnitude
    else:
        Diam = diam_pipemajor(FlowRate, HeadLoss, Length, Visc, PipeRough)
    err = 1.00
    while err > 0.001:
        DiamPrev = Diam
        HLFricNew = (HeadLoss * headloss_fric(FlowRate, Diam, Length, 
                                              Visc, PipeRough
                                              ).magnitude 
                     / (headloss_fric(FlowRate, Diam, Length, 
                                      Visc, PipeRough
                                      ).magnitude 
                                      + headloss_exp(FlowRate, 
                                                     Diam, MinorLoss
                                                     ).magnitude
                        )
                     )
        Diam = diam_pipemajor(FlowRate, HLFricNew, Length, Visc, PipeRough
                              ).magnitude
        err = abs(Diam - DiamPrev) / (Diam + DiamPrev)
    return Diam

# Weir head loss equations
@u.wraps(u.m, [u.m**3/u.m, u.m], False)
def width_rect_weir(FlowRate, Height):
    """Return the width of a rectangular weir."""
    return ((3 / 2) * FlowRate 
            / (RATIO_VC_ORIFICE * (np.sqrt(2*gravity.magnitude) * Height**(3/2)))
            )


# For a pipe, W is the circumference of the pipe.
# Head loss for a weir is the difference in height between the water
# upstream of the weir and the top of the weir.
@u.wraps(u.m, [u.m**3/u.s, u.m], False)
def headloss_weir(FlowRate, Width):
    """Return the headloss of a weir."""
    return (((3/2) * FlowRate 
             / (RATIO_VC_ORIFICE * (np.sqrt(2*gravity.magnitude)*Width))
             ) ** 3)


@u.wraps(u.m, [u.m, u.m], False)
def flow_rect_weir(Height, Width):
    """Return the flow of a rectangular weir."""
    return ((2/3) * RATIO_VC_ORIFICE 
            * (np.sqrt(2*gravity.magnitude) * Height**(3/2)) 
            * Width)


@u.wraps(u.m, [u.m**3/u.s, u.m], False)
def height_water_critical(FlowRate, Width):
    """Return the critical local water depth."""
    return (FlowRate / (Width * gravity.magnitude)) ** (2/3)


@u.wraps(u.m/u.s, u.m, False)
def vel_horizontal(height_water_critical):
    """Return the horizontal velocity."""
    return np.sqrt(gravity.magnitude * height_water_critical)

K_KOZENY=5

@u.wraps(u.m, [u.m, u.m, u.m, u.m**2/u.s], False)
def headloss_kozeny(Length, Diam, Vel, PipeRough, Visc):
    """Return the Carmen Kozeny Sand Bed head loss."""
    return (K_KOZENY * Length * Visc 
            / gravity.magnitude * (1-PipeRough) ** 2 
            / PipeRough**3 * 36 * Vel 
            / Diam ** 2)