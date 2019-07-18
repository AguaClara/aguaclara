"""Contains unit process functions pertaining to the design of physical
and chemical unit processes for AguaClara water treatment plants.
"""

from aguaclara.core.units import u
import aguaclara.core.materials as mat
import aguaclara.core.constants as con
import aguaclara.core.utility as ut
import aguaclara.core.pipes as pipe

import numpy as np
from scipy import interpolate, integrate

gravity = con.GRAVITY

######################Air################################
def density_air(Pressure, MolarMass, Temperature):
    """Return the density of the air.

    :param Pressure: pressure of the air in the system
    :type Pressure: float
    :param MolarMass: molar mass of the air in the system
    :type MolarMass: float
    :param Temperature: Temperature of the air in the system
    :type Temperature: float

    :return: density of the air in the system
    :rtype: float
    """
    return (Pressure * MolarMass / (u.R * Temperature)).to(u.kg/u.m**3)

###################### Simple geometry ######################
"""A few equations for useful geometry.
Is there a geometry package that we should be using?
"""

@u.wraps(u.m**2, u.m, False)
def area_circle(DiamCircle):
    """Return the area of a circle."""
    ut.check_range([DiamCircle, ">0", "DiamCircle"])
    return np.pi / 4 * DiamCircle**2


@u.wraps(u.m, u.m**2, False)
def diam_circle(AreaCircle):
    """Return the diameter of a circle."""
    ut.check_range([AreaCircle, ">0", "AreaCircle"])
    return np.sqrt(4 * AreaCircle / np.pi)

######################### Hydraulics #########################

RE_TRANSITION_PIPE = 2100
""" """
K_KOZENY = con.K_KOZENY

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
def viscosity_dynamic(temp):
    """Return the dynamic viscosity of water at a given temperature.

    If given units, the function will automatically convert to Kelvin.
    If not given units, the function will assume Kelvin.
    """
    ut.check_range([temp, ">0", "Temperature in Kelvin"])
    return 2.414 * (10**-5) * 10**(247.8 / (temp-140))


@u.wraps(u.kg/u.m**3, [u.degK], False)
def density_water(temp):
    """Return the density of water at a given temperature.

    If given units, the function will automatically convert to Kelvin.
    If not given units, the function will assume Kelvin.
    """
    ut.check_range([temp, ">0", "Temperature in Kelvin"])
    rhointerpolated = interpolate.CubicSpline(WATER_DENSITY_TABLE[0],
                                                    WATER_DENSITY_TABLE[1])
    return rhointerpolated(temp).item()


@u.wraps(u.m**2/u.s, [u.degK], False)
def viscosity_kinematic(temp):
    """Return the kinematic viscosity of water at a given temperature.

    If given units, the function will automatically convert to Kelvin.
    If not given units, the function will assume Kelvin.
    """
    ut.check_range([temp, ">0", "Temperature in Kelvin"])
    return (viscosity_dynamic(temp).magnitude
            / density_water(temp).magnitude)


@u.wraps(None, [u.m**3/u.s, u.m, u.m**2/u.s], False)
def re_pipe(FlowRate, Diam, Nu):
    """Return the Reynolds Number for a pipe."""
    #Checking input validity
    ut.check_range([FlowRate, ">0", "Flow rate"], [Diam, ">0", "Diameter"],
                   [Nu, ">0", "Nu"])
    return (4 * FlowRate) / (np.pi * Diam * Nu)


@u.wraps(u.m, [u.m, u.m], False)
@ut.list_handler()
def radius_hydraulic(Width, DistCenter, openchannel):
    """Return the hydraulic radius.

    Width and DistCenter are length values and openchannel is a boolean.
    """
    ut.check_range([Width, ">0", "Width"], [DistCenter, ">0", "DistCenter"],
                   [openchannel, "boolean", "openchannel"])
    if openchannel:
        return (Width*DistCenter) / (Width + 2*DistCenter)
        # if openchannel is True, the channel is open. Otherwise, the channel
        # is assumed to have a top.
    else:
        return (Width*DistCenter) / (2 * (Width+DistCenter))


@u.wraps(u.m, [u.m**2, u.m], False)
def radius_hydraulic_general(Area, PerimWetted):
    """Return the general hydraulic radius."""
    ut.check_range([Area, ">0", "Area"], [PerimWetted, ">0", "Wetted perimeter"])
    return Area / PerimWetted


@u.wraps(None, [u.m**3/u.s, u.m, u.m, u.m**2/u.s], False)
def re_rect(FlowRate, Width, DistCenter, Nu, openchannel):
    """Return the Reynolds Number for a rectangular channel."""
    #Checking input validity - inputs not checked here are checked by
    #functions this function calls.
    ut.check_range([FlowRate, ">0", "Flow rate"], [Nu, ">0", "Nu"])
    return (4 * FlowRate
            * radius_hydraulic(Width, DistCenter, openchannel).magnitude
            / (Width * DistCenter * Nu))
    #Reynolds Number for rectangular channel; open = False if all sides
    #are wetted; l = Diam and Diam = 4*R.h


@u.wraps(None, [u.m/u.s, u.m**2, u.m, u.m**2/u.s], False)
def re_general(Vel, Area, PerimWetted, Nu):
    """Return the Reynolds Number for a general cross section."""
    #Checking input validity - inputs not checked here are checked by
    #functions this function calls.
    ut.check_range([Vel, ">=0", "Velocity"], [Nu, ">0", "Nu"])
    return 4 * radius_hydraulic_general(Area, PerimWetted).magnitude * Vel / Nu


@u.wraps(None, [u.m**3/u.s, u.m, u.m**2/u.s, u.m], False)
def fric(FlowRate, Diam, Nu, PipeRough):
    """Return the friction factor for pipe flow.

    This equation applies to both laminar and turbulent flows.
    """
    #Checking input validity - inputs not checked here are checked by
    #functions this function calls.
    ut.check_range([PipeRough, "0-1", "Pipe roughness"])
    if re_pipe(FlowRate, Diam, Nu) >= RE_TRANSITION_PIPE:
        #Swamee-Jain friction factor for turbulent flow; best for
        #Re>3000 and ε/Diam < 0.02
        f = (0.25 / (np.log10(PipeRough / (3.7 * Diam)
                              + 5.74 / re_pipe(FlowRate, Diam, Nu) ** 0.9
                              )
                     ) ** 2
             )
    else:
        f = 64 / re_pipe(FlowRate, Diam, Nu)
    return f


@u.wraps(None, [u.m**3/u.s, u.m, u.m, u.m**2/u.s, u.m], False)
@ut.list_handler()
def fric_rect(FlowRate, Width, DistCenter, Nu, PipeRough, openchannel):
    """Return the friction factor for a rectangular channel."""
    #Checking input validity - inputs not checked here are checked by
    #functions this function calls.
    ut.check_range([PipeRough, "0-1", "Pipe roughness"])
    if re_rect(FlowRate,Width,DistCenter,Nu,openchannel) >= RE_TRANSITION_PIPE:
        #Swamee-Jain friction factor adapted for rectangular channel.
        #Diam = 4*R_h in this case.
        return (0.25
                / (np.log10((PipeRough
                             / (3.7 * 4
                                * radius_hydraulic(Width, DistCenter,
                                                   openchannel).magnitude
                                )
                             )
                            + (5.74 / (re_rect(FlowRate, Width, DistCenter,
                                               Nu, openchannel) ** 0.9)
                               )
                            )
                    ) ** 2
                )
    else:
        return 64 / re_rect(FlowRate, Width, DistCenter, Nu, openchannel)


@u.wraps(None, [u.m**2, u.m, u.m/u.s, u.m**2/u.s, u.m], False)
@ut.list_handler()
def fric_general(Area, PerimWetted, Vel, Nu, PipeRough):
    """Return the friction factor for a general channel."""
    #Checking input validity - inputs not checked here are checked by
    #functions this function calls.
    ut.check_range([PipeRough, "0-1", "Pipe roughness"])
    if re_general(Vel, Area, PerimWetted, Nu) >= RE_TRANSITION_PIPE:
        #Swamee-Jain friction factor adapted for any cross-section.
        #Diam = 4*R*h
        f= (0.25 /
            (np.log10((PipeRough
                       / (3.7 * 4
                          * radius_hydraulic_general(Area, PerimWetted).magnitude
                          )
                       )
                      + (5.74
                         / re_general(Vel, Area, PerimWetted, Nu) ** 0.9
                         )
                      )
             ) ** 2
            )
    else:
        f = 64 / re_general(Vel, Area, PerimWetted, Nu)
    return f


@u.wraps(u.m, [u.m**3/u.s, u.m, u.m, u.m**2/u.s, u.m], False)
def headloss_fric(FlowRate, Diam, Length, Nu, PipeRough):
    """Return the major head loss (due to wall shear) in a pipe.

    This equation applies to both laminar and turbulent flows.
    """
    #Checking input validity - inputs not checked here are checked by
    #functions this function calls.
    ut.check_range([Length, ">0", "Length"])
    return (fric(FlowRate, Diam, Nu, PipeRough)
            * 8 / (gravity.magnitude * np.pi**2)
            * (Length * FlowRate**2) / Diam**5
            )


@u.wraps(u.m, [u.m**3/u.s, u.m], False)
def headloss_exp(FlowRate, Diam, KMinor):
    """Return the minor head loss (due to expansions) in a pipe.

    This equation applies to both laminar and turbulent flows.
    """
    #Checking input validity
    ut.check_range([FlowRate, ">0", "Flow rate"], [Diam, ">0", "Diameter"],
                   [KMinor, ">=0", "K minor"])
    return KMinor * 8 / (gravity.magnitude * np.pi**2) * FlowRate**2 / Diam**4


@u.wraps(u.m, [u.m**3/u.s, u.m, u.m, u.m**2/u.s, u.m], False)
def headloss(FlowRate, Diam, Length, Nu, PipeRough, KMinor):
    """Return the total head loss from major and minor losses in a pipe.

    This equation applies to both laminar and turbulent flows.
    """
    #Inputs do not need to be checked here because they are checked by
    #functions this function calls.
    return (headloss_fric(FlowRate, Diam, Length, Nu, PipeRough).magnitude
            + headloss_exp(FlowRate, Diam, KMinor).magnitude)


@u.wraps(u.m, [u.m**3/u.s, u.m, u.m, u.m, u.m**2/u.s, u.m], False)
def headloss_fric_rect(FlowRate, Width, DistCenter, Length, Nu, PipeRough, openchannel):
    """Return the major head loss due to wall shear in a rectangular channel.

    This equation applies to both laminar and turbulent flows.
    """
    #Checking input validity - inputs not checked here are checked by
    #functions this function calls.
    ut.check_range([Length, ">0", "Length"])
    return (fric_rect(FlowRate, Width, DistCenter, Nu,
                      PipeRough, openchannel)
            * Length
            / (4 * radius_hydraulic(Width, DistCenter, openchannel).magnitude)
            * FlowRate**2
            / (2 * gravity.magnitude * (Width*DistCenter)**2)
            )


@u.wraps(u.m, [u.m**3/u.s, u.m, u.m], False)
def headloss_exp_rect(FlowRate, Width, DistCenter, KMinor):
    """Return the minor head loss due to expansion in a rectangular channel.

    This equation applies to both laminar and turbulent flows.
    """
    #Checking input validity
    ut.check_range([FlowRate, ">0", "Flow rate"], [Width, ">0", "Width"],
                   [DistCenter, ">0", "DistCenter"], [KMinor, ">=0", "K minor"])
    return (KMinor * FlowRate**2
            / (2 * gravity.magnitude * (Width*DistCenter)**2)
            )


@u.wraps(u.m, [u.m**3/u.s, u.m, u.m, u.m, None, u.m**2/u.s, u.m], False)
def headloss_rect(FlowRate, Width, DistCenter, Length,
                  KMinor, Nu, PipeRough, openchannel):
    """Return the total head loss in a rectangular channel.

    Total head loss is a combination of the major and minor losses.
    This equation applies to both laminar and turbulent flows.
    """
    #Inputs do not need to be checked here because they are checked by
    #functions this function calls.
    return (headloss_exp_rect(FlowRate, Width, DistCenter, KMinor).magnitude
              + headloss_fric_rect(FlowRate, Width, DistCenter, Length,
                                   Nu, PipeRough, openchannel).magnitude)


@u.wraps(u.m, [u.m**2, u.m, u.m/u.s, u.m, u.m**2/u.s, u.m], False)
def headloss_fric_general(Area, PerimWetted, Vel, Length, Nu, PipeRough):
    """Return the major head loss due to wall shear in the general case.

    This equation applies to both laminar and turbulent flows.
    """
    #Checking input validity - inputs not checked here are checked by
    #functions this function calls.
    ut.check_range([Length, ">0", "Length"])
    return (fric_general(Area, PerimWetted, Vel, Nu, PipeRough) * Length
            / (4 * radius_hydraulic_general(Area, PerimWetted).magnitude)
            * Vel**2 / (2*gravity.magnitude)
            )


@u.wraps(u.m, [u.m/u.s], False)
def headloss_exp_general(Vel, KMinor):
    """Return the minor head loss due to expansion in the general case.

    This equation applies to both laminar and turbulent flows.
    """
    #Checking input validity
    ut.check_range([Vel, ">0", "Velocity"], [KMinor, '>=0', 'K minor'])
    return KMinor * Vel**2 / (2*gravity.magnitude)


@u.wraps(u.m, [u.m**2, u.m/u.s, u.m, u.m, None, u.m**2/u.s, u.m], False)
def headloss_gen(Area, Vel, PerimWetted, Length, KMinor, Nu, PipeRough):
    """Return the total head lossin the general case.

    Total head loss is a combination of major and minor losses.
    This equation applies to both laminar and turbulent flows.
    """
    #Inputs do not need to be checked here because they are checked by
    #functions this function calls.
    return (headloss_exp_general(Vel, KMinor).magnitude
            + headloss_fric_general(Area, PerimWetted, Vel,
                                     Length, Nu, PipeRough).magnitude)


@u.wraps(u.m, [u.m**3/u.s, u.m, u.m, None,
               u.m**2/u.s, u.m], False)
def headloss_manifold(FlowRate, Diam, Length, KMinor, Nu, PipeRough, NumOutlets):
    """Return the total head loss through the manifold."""
    #Checking input validity - inputs not checked here are checked by
    #functions this function calls.
    ut.check_range([NumOutlets, ">0, int", 'Number of outlets'])
    return (headloss(FlowRate, Diam, Length, Nu, PipeRough, KMinor).magnitude
            * ((1/3 )
               + (1 / (2*NumOutlets))
               + (1 / (6*NumOutlets**2))
              )
            )


@u.wraps(u.m**3/u.s, [u.m, u.m], False)
@ut.list_handler()
def flow_orifice(Diam, Height, RatioVCOrifice):
    """Return the flow rate of the orifice."""
    #Checking input validity
    ut.check_range([Diam, ">0", "Diameter"],
                   [RatioVCOrifice, "0-1", "VC orifice ratio"])
    if Height > 0:
        return (RatioVCOrifice * area_circle(Diam).magnitude
                * np.sqrt(2 * gravity.magnitude * Height))
    else:
        return 0


#Deviates from the MathCad at the 6th decimal place. Worth investigating or not?
@u.wraps(u.m**3/u.s, [u.m, u.m], False)
@ut.list_handler()
def flow_orifice_vert(Diam, Height, RatioVCOrifice):
    """Return the vertical flow rate of the orifice."""
    #Checking input validity
    ut.check_range([RatioVCOrifice, "0-1", "VC orifice ratio"])
    if Height > -Diam / 2:
        flow_vert = integrate.quad(lambda z: (Diam * np.sin(np.arccos(z/(Diam/2)))
                                                   * np.sqrt(Height - z)
                                                   ),
                                                   - Diam / 2,
                                                   min(Diam/2, Height))
        return flow_vert[0] * RatioVCOrifice * np.sqrt(2 * gravity.magnitude)
    else:
        return 0


@u.wraps(u.m, [u.m, None, u.m**3/u.s], False)
def head_orifice(Diam, RatioVCOrifice, FlowRate):
    """Return the head of the orifice."""
    #Checking input validity
    ut.check_range([Diam, ">0", "Diameter"], [FlowRate, ">0", "Flow rate"],
                   [RatioVCOrifice, "0-1", "VC orifice ratio"])
    return ((FlowRate
             / (RatioVCOrifice * area_circle(Diam).magnitude)
             )**2
            / (2*gravity.magnitude)
            )


@u.wraps(u.m**2, [u.m, None, u.m**3/u.s], False)
def area_orifice(Height, RatioVCOrifice, FlowRate):
    """Return the area of the orifice."""
    #Checking input validity
    ut.check_range([Height, ">0", "Height"], [FlowRate, ">0", "Flow rate"],
                   [RatioVCOrifice, "0-1, >0", "VC orifice ratio"])
    return FlowRate / (RatioVCOrifice * np.sqrt(2 * gravity.magnitude * Height))


@u.wraps(None, [u.m**3/u.s, None, u.m, u.m], False)
def num_orifices(FlowPlant, RatioVCOrifice, HeadLossOrifice, DiamOrifice):
    """Return the number of orifices."""
    #Inputs do not need to be checked here because they are checked by
    #functions this function calls.
    return np.ceil(area_orifice(HeadLossOrifice, RatioVCOrifice,
                                 FlowPlant).magnitude
                    / area_circle(DiamOrifice).magnitude)


# Here we define functions that return the flow rate.
@u.wraps(u.m**3/u.s, [u.m, u.m**2/u.s], False)
def flow_transition(Diam, Nu):
    """Return the flow rate for the laminar/turbulent transition.

    This equation is used in some of the other equations for flow.
    """
    #Checking input validity
    ut.check_range([Diam, ">0", "Diameter"], [Nu, ">0", "Nu"])
    return np.pi * Diam * RE_TRANSITION_PIPE * Nu / 4


@u.wraps(u.m**3/u.s, [u.m, u.m, u.m, u.m**2/u.s], False)
def flow_hagen(Diam, HeadLossFric, Length, Nu):
    """Return the flow rate for laminar flow with only major losses."""
    #Checking input validity
    ut.check_range([Diam, ">0", "Diameter"], [Length, ">0", "Length"],
                   [HeadLossFric, ">=0", "Headloss due to friction"],
                   [Nu, ">0", "Nu"])
    return (np.pi*Diam**4) / (128*Nu) * gravity.magnitude * HeadLossFric / Length


@u.wraps(u.m**3/u.s, [u.m, u.m, u.m, u.m**2/u.s, u.m], False)
def flow_swamee(Diam, HeadLossFric, Length, Nu, PipeRough):
    """Return the flow rate for turbulent flow with only major losses."""
    #Checking input validity
    ut.check_range([Diam, ">0", "Diameter"], [Length, ">0", "Length"],
                   [HeadLossFric, ">0", "Headloss due to friction"],
                   [Nu, ">0", "Nu"], [PipeRough, "0-1", "Pipe roughness"])
    logterm = np.log10(PipeRough / (3.7 * Diam)
                       + 2.51 * Nu * np.sqrt(Length / (2 * gravity.magnitude
                                                         * HeadLossFric
                                                         * Diam**3)
                                              )
                       )
    return ((-np.pi / np.sqrt(2)) * Diam**(5/2) * logterm
            * np.sqrt(gravity.magnitude * HeadLossFric / Length)
            )


@u.wraps(u.m**3/u.s, [u.m, u.m, u.m, u.m**2/u.s, u.m], False)
@ut.list_handler()
def flow_pipemajor(Diam, HeadLossFric, Length, Nu, PipeRough):
    """Return the flow rate with only major losses.

    This function applies to both laminar and turbulent flows.
    """
    #Inputs do not need to be checked here because they are checked by
    #functions this function calls.
    FlowHagen = flow_hagen(Diam, HeadLossFric, Length, Nu).magnitude
    if FlowHagen < flow_transition(Diam, Nu).magnitude:
        return FlowHagen
    else:
        return flow_swamee(Diam, HeadLossFric, Length, Nu, PipeRough).magnitude


@u.wraps(u.m**3/u.s, [u.m, u.m], False)
def flow_pipeminor(Diam, HeadLossExpans, KMinor):
    """Return the flow rate with only minor losses.

    This function applies to both laminar and turbulent flows.
    """
    #Checking input validity - inputs not checked here are checked by
    #functions this function calls.
    ut.check_range([HeadLossExpans, ">=0", "Headloss due to expansion"],
                   [KMinor, ">0", "K minor"])
    return (area_circle(Diam).magnitude * np.sqrt(2 * gravity.magnitude
                                                  * HeadLossExpans
                                                  / KMinor)
            )

# Now we put all of the flow equations together and calculate the flow in a
# straight pipe that has both major and minor losses and might be either
# laminar or turbulent.
@u.wraps(u.m**3/u.s, (u.m, u.m, u.m, u.m**2/u.s, u.m), False)
@ut.list_handler()
def flow_pipe(Diam, HeadLoss, Length, Nu, PipeRough, KMinor):
    """Return the the flow in a straight pipe.

    This function works for both major and minor losses and
    works whether the flow is laminar or turbulent.
    """
    #Inputs do not need to be checked here because they are checked by
    #functions this function calls.
    if KMinor == 0:
        FlowRate = flow_pipemajor(Diam, HeadLoss, Length, Nu,
                                  PipeRough).magnitude
    else:
        FlowRatePrev = 0
        err = 1.0
        FlowRate = min(flow_pipemajor(Diam, HeadLoss, Length,
                                      Nu, PipeRough).magnitude,
                       flow_pipeminor(Diam, HeadLoss, KMinor).magnitude
                       )
        while err > 0.01:
            FlowRatePrev = FlowRate
            HLFricNew = (HeadLoss * headloss_fric(FlowRate, Diam, Length,
                                                  Nu, PipeRough).magnitude
                         / (headloss_fric(FlowRate, Diam, Length,
                                          Nu, PipeRough).magnitude
                            + headloss_exp(FlowRate, Diam, KMinor).magnitude
                            )
                         )
            FlowRate = flow_pipemajor(Diam, HLFricNew, Length,
                                      Nu, PipeRough).magnitude
            if FlowRate == 0:
                err = 0.0
            else:
                err = (abs(FlowRate - FlowRatePrev)
                       / ((FlowRate + FlowRatePrev) / 2)
                       )
    return FlowRate


@u.wraps(u.m, [u.m**3/u.s, u.m, u.m, u.m**2/u.s], False)
def diam_hagen(FlowRate, HeadLossFric, Length, Nu):
    #Checking input validity
    ut.check_range([FlowRate, ">0", "Flow rate"], [Length, ">0", "Length"],
                   [HeadLossFric, ">0", "Headloss due to friction"],
                   [Nu, ">0", "Nu"])
    return ((128 * Nu * FlowRate * Length)
            / (gravity.magnitude * HeadLossFric * np.pi)
            ) ** (1/4)


@u.wraps(u.m, [u.m**3/u.s, u.m, u.m, u.m**2/u.s, u.m], False)
def diam_swamee(FlowRate, HeadLossFric, Length, Nu, PipeRough):
    """Return the inner diameter of a pipe.

    The Swamee Jain equation is dimensionally correct and returns the
    inner diameter of a pipe given the flow rate and the head loss due
    to shear on the pipe walls. The Swamee Jain equation does NOT take
    minor losses into account. This equation ONLY applies to turbulent
    flow.
    """
    #Checking input validity
    ut.check_range([FlowRate, ">0", "Flow rate"], [Length, ">0", "Length"],
                   [HeadLossFric, ">0", "Headloss due to friction"],
                   [Nu, ">0", "Nu"], [PipeRough, "0-1", "Pipe roughness"])
    a = ((PipeRough ** 1.25)
         * ((Length * FlowRate**2)
            / (gravity.magnitude * HeadLossFric)
            )**4.75
         )
    b = (Nu * FlowRate**9.4
         * (Length / (gravity.magnitude *  HeadLossFric)) ** 5.2
         )
    return 0.66 * (a+b)**0.04


@u.wraps(u.m, [u.m**3/u.s, u.m, u.m, u.m**2/u.s, u.m], False)
@ut.list_handler()
def diam_pipemajor(FlowRate, HeadLossFric, Length, Nu, PipeRough):
    """Return the pipe IDiam that would result in given major losses.
    This function applies to both laminar and turbulent flow.
    """
    #Inputs do not need to be checked here because they are checked by
    #functions this function calls.
    DiamLaminar = diam_hagen(FlowRate, HeadLossFric, Length, Nu).magnitude
    if re_pipe(FlowRate, DiamLaminar, Nu) <= RE_TRANSITION_PIPE:
        return DiamLaminar
    else:
        return diam_swamee(FlowRate, HeadLossFric, Length,
                           Nu, PipeRough).magnitude

@u.wraps(u.m, [u.m**3/u.s, u.m], False)
def diam_pipeminor(FlowRate, HeadLossExpans, KMinor):
    """Return the pipe ID that would result in the given minor losses.

    This function applies to both laminar and turbulent flow.
    """
    #Checking input validity
    ut.check_range([FlowRate, ">0", "Flow rate"], [KMinor, ">=0", "K minor"],
                   [HeadLossExpans, ">0", "Headloss due to expansion"])
    return (np.sqrt(4 * FlowRate / np.pi)
            * (KMinor / (2 * gravity.magnitude * HeadLossExpans)) ** (1/4)
            )


@u.wraps(u.m, [u.m**3/u.s, u.m, u.m, u.m**2/u.s, u.m], False)
@ut.list_handler()
def diam_pipe(FlowRate, HeadLoss, Length, Nu, PipeRough, KMinor):
    """Return the pipe ID that would result in the given total head loss.

    This function applies to both laminar and turbulent flow and
    incorporates both minor and major losses.
    """
    #Inputs do not need to be checked here because they are checked by
    #functions this function calls.
    if KMinor == 0:
        Diam = diam_pipemajor(FlowRate, HeadLoss, Length, Nu,
                              PipeRough).magnitude
    else:
        Diam = max(diam_pipemajor(FlowRate, HeadLoss,
                                  Length, Nu, PipeRough).magnitude,
                   diam_pipeminor(FlowRate, HeadLoss, KMinor).magnitude)
        err = 1.00
        while err > 0.001:
            DiamPrev = Diam
            HLFricNew = (HeadLoss * headloss_fric(FlowRate, Diam, Length,
                                                  Nu, PipeRough
                                                  ).magnitude
                         / (headloss_fric(FlowRate, Diam, Length,
                                          Nu, PipeRough
                                          ).magnitude
                                          + headloss_exp(FlowRate,
                                                         Diam, KMinor
                                                         ).magnitude
                            )
                         )
            Diam = diam_pipemajor(FlowRate, HLFricNew, Length, Nu, PipeRough
                                  ).magnitude
            err = abs(Diam - DiamPrev) / ((Diam + DiamPrev) / 2)
    return Diam

# Weir head loss equations
@u.wraps(u.m, [u.m**3/u.s, u.m], False)
def width_rect_weir(FlowRate, Height):
    """Return the width of a rectangular weir."""
    #Checking input validity
    ut.check_range([FlowRate, ">0", "Flow rate"], [Height, ">0", "Height"])
    return ((3 / 2) * FlowRate
            / (con.VC_ORIFICE_RATIO * np.sqrt(2 * gravity.magnitude) * Height ** (3 / 2))
            )


# For a pipe, Width is the circumference of the pipe.
# Head loss for a weir is the difference in height between the water
# upstream of the weir and the top of the weir.
@u.wraps(u.m, [u.m**3/u.s, u.m], False)
def headloss_weir(FlowRate, Width):
    """Return the headloss of a weir."""
    #Checking input validity
    ut.check_range([FlowRate, ">0", "Flow rate"], [Width, ">0", "Width"])
    return (((3/2) * FlowRate
             / (con.VC_ORIFICE_RATIO * np.sqrt(2 * gravity.magnitude) * Width)
             ) ** (2/3))


@u.wraps(u.m, [u.m, u.m], False)
def flow_rect_weir(Height, Width):
    """Return the flow of a rectangular weir."""
    #Checking input validity
    ut.check_range([Height, ">0", "Height"], [Width, ">0", "Width"])
    return ((2/3) * con.VC_ORIFICE_RATIO
            * (np.sqrt(2*gravity.magnitude) * Height**(3/2))
            * Width)


@u.wraps(u.m, [u.m**3/u.s, u.m], False)
def height_water_critical(FlowRate, Width):
    """Return the critical local water depth."""
    #Checking input validity
    ut.check_range([FlowRate, ">0", "Flow rate"], [Width, ">0", "Width"])
    return (FlowRate / (Width * np.sqrt(gravity.magnitude))) ** (2/3)


@u.wraps(u.m/u.s, u.m, False)
def vel_horizontal(HeightWaterCritical):
    """Return the horizontal velocity."""
    #Checking input validity
    ut.check_range([HeightWaterCritical, ">0", "Critical height of water"])
    return np.sqrt(gravity.magnitude * HeightWaterCritical)


@u.wraps(u.m, [u.m, u.m, u.m/u.s, u.m, u.m**2/u.s], False)
def headloss_kozeny(Length, Diam, Vel, Porosity, Nu):
    """Return the Carmen Kozeny Sand Bed head loss."""
    #Checking input validity
    ut.check_range([Length, ">0", "Length"], [Diam, ">0", "Diam"],
                   [Vel, ">0", "Velocity"], [Nu, ">0", "Nu"],
                   [Porosity, "0-1", "Porosity"])
    return (K_KOZENY * Length * Nu
            / gravity.magnitude * (1-Porosity)**2
            / Porosity**3 * 36 * Vel
            / Diam ** 2)


@u.wraps(u.m, [u.m**3/u.s, u.m], False)
def pipe_ID(FlowRate, Pressure):
    """Return the internal diameter of a pipe for a given pressure
    recovery constraint. """
    #Checking input validity
    ut.check_range([FlowRate, ">0", "Flow rate"], [Pressure, ">0", "Pressure"])
    return np.sqrt(FlowRate/((np.pi/4)*np.sqrt(2*gravity.magnitude*Pressure)))

def manifold_id_alt(q, pr_max):
    """Return the inner diameter of a manifold when major losses are
    negligible.
    """
    manifold_id_alt = np.sqrt(
        4 * q / (
            np.pi * np.sqrt(
                2 * con.GRAVITY * pr_max
            )
        )
    )
    return manifold_id_alt

def manifold_id(q, h, l, q_ratio, nu, eps, k, n):
    id_new = 2 * u.inch
    id_old = 0 * u.inch
    error = 1
    while error > 0.01:
        id_old = id_new
        id_new = (
            ((8 * q ** 2) / (con.GRAVITY * np.pi ** 2 * h)) * 
            (
                (
                    1 + fric(q, id_old, nu, eps) * 
                    (1 / 3 + 1 / (2 * n) + 1 / (6 * n ** 2))
                ) /
                (1 - q_ratio ** 2)
            )
        ) ** (1 / 4)
        error = np.abs(id_old - id_new) / id_new
    return id_new

def manifold_nd(q, h, l, q_ratio, nu, eps, k, n, sdr):
    manifold_nd = pipe.ND_SDR_available(
            manifold_id(q, h, l, q_ratio, nu, eps, k, n), 
            sdr
        )
    return manifold_nd

def horiz_chan_w(q, depth, hl, l, nu, eps, manifold, k):
    hl = min(hl, depth / 3)
    horiz_chan_w_new = q / ((depth - hl) * np.sqrt(2 * con.GRAVITY * hl))
    
    error = 1
    i = 0
    while error > 0.001 and i < 20:
        w = horiz_chan_w_new
        i = i + 1
        horiz_chan_w_new = np.sqrt(
            (
                1 + k +
                    fric_rect(q, w, depth - hl, nu, eps, True) * 
                    (l / (4 * radius_hydraulic(w, depth - hl, True))) *
                    (1 - (2 * (int(manifold) / 3)))
            ) / (2 * con.GRAVITY * hl)
        ) * (q / (depth - hl)) 
        error = np.abs(horiz_chan_w_new - w) / (horiz_chan_w_new + w)
    return horiz_chan_w_new.to(u.m)

def horiz_chan_h(q, w, hl, l, nu, eps, manifold):
    h_new = (q / (w * np.sqrt(2 * con.GRAVITY * hl))) + hl 
    error = 1
    i = 0
    while error > 0.001 and i < 200:
        h = h_new
        hl_local = min(hl, h / 3)
        i = i + 1
        h_new = (q/ w) * np.sqrt((1 + \
            fric_rect(q, w, h - hl_local, nu, eps, True) * (l / (4 * \
                radius_hydraulic(w, h - hl_local, True))) * (1 - 2 * (int(manifold) / 3))
        )/ (2 * con.GRAVITY * hl_local)) + (hl_local) 
        error = np.abs(h_new - h) / (h_new + h)
    return h_new.to(u.m)

def pipe_flow_nd(q, sdr, hl, l, nu, eps, k):
    i = 0
    while q > flow_pipe(pipe.ID_SDR_all_available(sdr)[i], hl, l, nu, eps, k):
        i += 1
    return pipe.ND_SDR_available(pipe.ID_SDR_all_available(sdr)[i], sdr)