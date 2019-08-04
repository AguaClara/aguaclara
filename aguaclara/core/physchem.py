"""Contains unit process functions pertaining to the design of physical
and chemical unit processes for AguaClara water treatment plants.
"""

from aguaclara.core.units import unit_registry as u
import aguaclara.core.constants as con
import aguaclara.core.utility as ut

import numpy as np
from scipy import interpolate, integrate

gravity = u.gravity

############################ Air ##############################
@ut.list_handler()
def density_air(Pressure, MolarMass, Temperature):
    """Return the density of air at the given pressure, molar mass, and
    temperature.

    :param Pressure: pressure of air in the system
    :type Pressure: u.pascal
    :param MolarMass: molar mass of air in the system
    :type MolarMass: u.gram/u.mol
    :param Temperature: Temperature of air in the system
    :type Temperature: u.degK

    :return: density of air in the system
    :rtype: u.kg/u.m**3
    """
    return (Pressure * MolarMass / (u.R * Temperature)).to(u.kg/u.m**3)

###################### Simple geometry ######################

"""A few equations for useful geometry.
Is there a geometry package that we should be using?"""

@ut.list_handler()
def area_circle(DiamCircle):
    """Return the area of a circle given its diameter.

    :param DiamCircle: diameter of circle
    :type DiamCircle: u.m

    :return: area of circle
    :rtype: u.m**2
    """
    ut.check_range([DiamCircle.magnitude, ">0", "DiamCircle"])
    return np.pi / 4 * DiamCircle**2


@ut.list_handler()
def diam_circle(AreaCircle):
    """Return the diameter of a circle given its area.

    :param AreaCircle: area of circle
    :type AreaCircle: u.m**2

    :return: diameter of circle
    :rtype: u.m
    """

    ut.check_range([AreaCircle.magnitude, ">0", "AreaCircle"])
    return np.sqrt(4 * AreaCircle / np.pi)

######################### Hydraulics #########################

#:
RE_TRANSITION_PIPE = 2100

K_KOZENY = con.K_KOZENY

#: Table of temperatures and the corresponding water density.
#:
#: WATER_DENSITY_TABLE[0] is a list of water temperatures, in Kelvin.
#: WATER_DENSITY_TABLE[1] is the corresponding densities, in kg/m³.
WATER_DENSITY_TABLE = [(273.15, 278.15, 283.15, 293.15, 303.15, 313.15,
                        323.15, 333.15, 343.15, 353.15, 363.15, 373.15
                        ), (999.9, 1000, 999.7, 998.2, 995.7, 992.2,
                            988.1, 983.2, 977.8, 971.8, 965.3, 958.4
                            )
                       ]


@ut.list_handler()
def viscosity_dynamic(temp):
    """Return the dynamic viscosity of water at a given temperature.

    :param temp: temperature of water
    :type temp: u.degK

    :return: dynamic viscosity of water
    :rtype: u.kg/(u.m*u.s)
    """
    ut.check_range([temp.magnitude, ">0", "Temperature in Kelvin"])
    return 2.414*(10**-5)*u.kg/(u.m*u.s) * 10**(247.8*u.degK / (temp - 140*u.degK))


@ut.list_handler()
def density_water(temp):
    """Return the density of water at a given temperature.

    :param temp: temperature of water
    :type temp: u.degK

    :return: density of water
    :rtype: u.kg/u.m**3
    """
    ut.check_range([temp.magnitude, ">0", "Temperature in Kelvin"])
    rhointerpolated = interpolate.CubicSpline(WATER_DENSITY_TABLE[0],
                                              WATER_DENSITY_TABLE[1])
    temp = temp.to(u.degK).magnitude
    return rhointerpolated(temp).item() * u.kg/u.m**3


@ut.list_handler()
def viscosity_kinematic(temp):
    """Return the kinematic viscosity of water at a given temperature.

    :param temp: temperature of water
    :type temp: u.degK

    :return: kinematic viscosity of water
    :rtype: u.m**2/u.s
    """
    ut.check_range([temp.magnitude, ">0", "Temperature in Kelvin"])
    return (viscosity_dynamic(temp) / density_water(temp))


@ut.list_handler()
def radius_hydraulic(Width, DistCenter, openchannel):
    """Return the hydraulic radius of a rectangular channel, given width and
    depth of flow.

    :param Width: width of channel
    :type Width: u.m
    :param DistCenter: depth of flow in channel
    :type DistCenter: u.m
    :param openchannel: true if channel is open, false if closed
    :type openchannel: boolean

    :return: hydraulic radius of rectangular channel
    :rtype: u.m
    """
    ut.check_range([Width.magnitude, ">0", "Width"],
                   [DistCenter.magnitude, ">0", "DistCenter"],
                   [openchannel, "boolean", "openchannel"])
    if openchannel:
        return (Width*DistCenter) / (Width + 2*DistCenter)
    else:
        return (Width*DistCenter) / (2 * (Width+DistCenter))


@ut.list_handler()
def radius_hydraulic_general(Area, PerimWetted):
    """Return the hydraulic radius of a general channel, given cross sectional
    area and wetted perimeter.

    :param Area: cross sectional area of channel
    :type Area: u.m**2
    :param PerimWetted: wetted perimeter of channel
    :type PerimWetted: u.m

    :return: hydraulic radius of general channel
    :rtype: u.m
    """
    ut.check_range([Area.magnitude, ">0", "Area"],
                   [PerimWetted.magnitude, ">0", "Wetted perimeter"])
    return Area / PerimWetted


@ut.list_handler()
def re_pipe(FlowRate, Diam, Nu):
    """Return the Reynolds number of flow through a pipe.

    :param FlowRate: flow rate through pipe
    :type FlowRate: u.m**3/u.s
    :param Diam: diameter of pipe
    :type Diam: u.m
    :param Nu: kinematic viscosity of fluid
    :type Nu: u.m**2/u.s

    :return: Reynolds number of flow through pipe
    :rtype: u.dimensionless
    """
    ut.check_range([FlowRate.magnitude, ">0", "Flow rate"],
                   [Diam.magnitude, ">0", "Diameter"],
                   [Nu.magnitude, ">0", "Nu"])
    return ((4 * FlowRate) / (np.pi * Diam * Nu))


@ut.list_handler()
def re_rect(FlowRate, Width, DistCenter, Nu, openchannel):
    """Return the Reynolds number of flow through a rectangular channel.

    :param FlowRate: flow rate through channel
    :type FlowRate: u.m**3/u.s
    :param Width: width of channel
    :type Width: u.m
    :param DistCenter: depth of flow in channel
    :type DistCenter: u.m
    :param Nu: kinematic viscosity of fluid
    :type Nu: u.m**2/u.s
    :param openchannel: true if channel is open, false if closed
    :type openchannel: boolean

    :return: Reynolds number of flow through rectangular channel
    :rtype: u.dimensionless
    """
    ut.check_range([FlowRate.magnitude, ">0", "Flow rate"],
                   [Nu.magnitude, ">0", "Nu"])
    return (4 * FlowRate * radius_hydraulic(Width, DistCenter, openchannel)
            / (Width * DistCenter * Nu))


@ut.list_handler()
def re_general(Vel, Area, PerimWetted, Nu):
    """Return the Reynolds number of flow through a general cross section.

    :param Vel: velocity of fluid
    :type Vel: u.m/u.s
    :param Area: cross sectional area of channel
    :type Area: u.m**2
    :param PerimWetted: wetted perimeter of channel
    :type PerimWetted: u.m
    :param Nu: kinematic viscosity of fluid
    :type Nu: u.m**2/u.s

    :return: Reynolds number of flow through general cross section
    :rtype: u.dimensionless
    """
    ut.check_range([Vel.magnitude, ">=0", "Velocity"],
                   [Nu.magnitude, ">0", "Nu"])
    return 4 * radius_hydraulic_general(Area, PerimWetted) * Vel / Nu


@ut.list_handler()
def fric(FlowRate, Diam, Nu, PipeRough):
    """Return the friction factor for pipe flow.

    For laminar flow, the friction factor is 64 is divided the Reynolds number.
    For turbulent flows, friction factor is calculated using the Swamee-Jain
    equation, which works best for Re > 3000 and ε/Diam < 0.02.

    :param FlowRate: flow rate through pipe
    :type FlowRate: u.m**3/u.s
    :param Diam: diameter of pipe
    :type Diam: u.m
    :param Nu: kinematic viscosity of fluid
    :type Nu: u.m**2/u.s
    :param PipeRough: roughness of pipe
    :type PipeRough: u.m

    :return: friction factor of flow through pipe
    :rtype: u.dimensionless
    """
    ut.check_range([PipeRough.magnitude, "0-1", "Pipe roughness"])
    if re_pipe(FlowRate, Diam, Nu) >= RE_TRANSITION_PIPE:
        f = (0.25 / (np.log10(PipeRough / (3.7 * Diam)
                              + 5.74 / re_pipe(FlowRate, Diam, Nu) ** 0.9
                              )
                     ) ** 2
             )
    else:
        f = 64 / re_pipe(FlowRate, Diam, Nu)
    return f * u.dimensionless


@ut.list_handler()
def fric_rect(FlowRate, Width, DistCenter, Nu, PipeRough, openchannel):
    """Return the friction factor of a rectangular channel.

    The Swamee-Jain equation is adapted for a rectangular channel.

    :param FlowRate: flow rate through channel
    :type FlowRate: u.m**3/u.s
    :param Width: width of channel
    :type Width: u.m
    :param DistCenter: depth of flow in channel
    :type DistCenter: u.m
    :param Nu: kinematic viscosity of fluid
    :type Nu: u.m**2/u.s
    :param PipeRough: roughness of channel surface
    :type PipeRough: u.m
    :param openchannel: true if channel is open, false if closed
    :type openchannel: boolean

    :return: friction factor of flow through rectangular channel
    :rtype: u.dimensionless
    """
    ut.check_range([PipeRough.magnitude, "0-1", "Pipe roughness"])
    if re_rect(FlowRate, Width, DistCenter, Nu, openchannel) >= RE_TRANSITION_PIPE:
        # Diam = 4*R_h in adapted Swamee-Jain equation
        return (0.25 * u.dimensionless
                / (np.log10((PipeRough
                             / (3.7 * 4
                                * radius_hydraulic(Width, DistCenter,
                                                   openchannel)
                                )
                             )
                            + (5.74 / (re_rect(FlowRate, Width, DistCenter,
                                               Nu, openchannel) ** 0.9)
                               )
                            )
                   ) ** 2
                )
    else:
        return 64 * u.dimensionless / re_rect(FlowRate, Width, DistCenter, Nu, openchannel)


@ut.list_handler()
def fric_general(Area, PerimWetted, Vel, Nu, PipeRough):
    """Return the friction factor for a general channel.

    The Swamee-Jain equation is adapted for a general cross-section.

    :param Area: cross sectional area of channel
    :type Area: u.m**2
    :param PerimWetted: wetted perimeter of channel
    :type PerimWetted: u.m
    :param Vel: velocity of fluid
    :type Vel: u.m/u.s
    :param Nu: kinematic viscosity of fluid
    :type Nu: u.m**2/u.s
    :param PipeRough: roughness of channel surface
    :type PipeRough: u.m

    :return: friction factor for flow through general channel
    :rtype: u.dimensionless
    """
    ut.check_range([PipeRough.magnitude, "0-1", "Pipe roughness"])
    if re_general(Vel, Area, PerimWetted, Nu) >= RE_TRANSITION_PIPE:
        # Diam = 4*R_h in adapted Swamee-Jain equation
        f = (0.25 /
             (np.log10((PipeRough
                        / (3.7 * 4
                           * radius_hydraulic_general(Area, PerimWetted)
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
    return f * u.dimensionless


@ut.list_handler()
def headloss_fric(FlowRate, Diam, Length, Nu, PipeRough):
    """Return the major head loss (due to wall shear) in a pipe.

    This function applies to both laminar and turbulent flows.

    :param FlowRate: flow rate through pipe
    :type FlowRate: u.m**3/u.s
    :param Diam: diameter of pipe
    :type Diam: u.m
    :param Length: depth of pipe
    :type Length: u.m
    :param Nu: kinematic viscosity of fluid
    :type Nu: u.m**2/u.s
    :param PipeRough: roughness of channel surface
    :type PipeRough: u.m

    :return: major head loss in pipe
    :rtype: u.m
    """
    ut.check_range([Length.magnitude, ">0", "Length"])
    return (fric(FlowRate, Diam, Nu, PipeRough)
            * 8 / (gravity * np.pi**2)
            * (Length * FlowRate**2) / Diam**5
            )


@ut.list_handler()
def headloss_exp(FlowRate, Diam, KMinor):
    """Return the minor head loss (due to changes in geometry) in a pipe.

    This function applies to both laminar and turbulent flows.

    :param FlowRate: flow rate through pipe
    :type FlowRate: u.m**3/u.s
    :param Diam: diameter of pipe
    :type Diam: u.m
    :param KMinor: minor loss coefficient
    :type KMinor: u.dimensionless or unitless

    :return: minor head loss in pipe
    :rtype: u.m
    """
    ut.check_range([FlowRate.magnitude, ">0", "Flow rate"],
                   [Diam.magnitude, ">0", "Diameter"],
                   [KMinor, ">=0", "K minor"])
    return KMinor * 8 / (gravity * np.pi**2) * FlowRate**2 / Diam**4


@ut.list_handler()
def headloss(FlowRate, Diam, Length, Nu, PipeRough, KMinor):
    """Return the total head loss from major and minor losses in a pipe.

    This function applies to both laminar and turbulent flows.

    :param FlowRate: flow rate through pipe
    :type FlowRate: u.m**3/u.s
    :param Diam: diameter of pipe
    :type Diam: u.m
    :param Length: depth of pipe
    :type Length: u.m
    :param Nu: kinematic viscosity of fluid
    :type Nu: u.m**2/u.s
    :param PipeRough: roughness of channel surface
    :type PipeRough: u.m
    :param KMinor: minor loss coefficient
    :type KMinor: u.dimensionless or unitless

    :return: major and minor head loss in pipe
    :rtype: u.m
    """
    return (headloss_fric(FlowRate, Diam, Length, Nu, PipeRough)
            + headloss_exp(FlowRate, Diam, KMinor))


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


@ut.list_handler()
def Re_Erdon(ApproachVel, DiamParticle, Temperature, Porosity):
    """Return the Reynolds number for flow through porous media.

    :param ApproachVel: approach velocity or superficial fluid velocity
    :type ApproachVel: u.m/u.s
    :param DiamParticle: particle diameter
    :type DiamParticle: u.m
    :param Temperature: temperature of porous medium
    :type Temperature: u.degK
    :param Porosity: porosity of porous medium
    :type Porosity: u.dimensionless

    :return: Reynolds number for flow through porous media
    :rtype: u.dimensionless
    """
    return (ApproachVel * DiamParticle /
            (viscosity_kinematic(Temperature) * (1 - Porosity)))


@ut.list_handler()
def f_Erdon(ApproachVel, DiamParticle, Temperature, Porosity):
    """Return the friction factor for flow through porous media.

    :param ApproachVel: superficial fluid velocity (VelSuperficial?)
    :type ApproachVel: u.m/u.s
    :param DiamParticle: particle diameter (DiamParticle?)
    :type DiamParticle: u.m
    :param Temperature: temperature of porous medium
    :type Temperature: u.degK
    :param Porosity: porosity of porous medium
    :type Porosity: u.dimensionless

    :return: friction factor for flow through porous media
    :rtype: u.dimensionless
    """
    return (300 / Re_Erdon(ApproachVel, DiamParticle, Temperature, Porosity)
            + 3.5 * u.dimensionless)


@ut.list_handler()
def hf_Erdon(ApproachVel, DiamParticle, Temperature, Porosity, L):
    """Return the frictional head loss for flow through porous media.

    :param ApproachVel: superficial fluid velocity (VelSuperficial?)
    :type ApproachVel: u.m/u.s
    :param DiamParticle: particle diameter (DiamParticle?)
    :type DiamParticle: u.m
    :param Temperature: temperature of porous medium
    :type Temperature: u.degK
    :param Porosity: porosity of porous medium
    :type Porosity: u.dimensionless
    :param L: length of pipe or duct (Length?)
    :type L: u.m

    :return: frictional head loss for flow through porous media
    :rtype: u.m
    """
    return (f_Erdon(ApproachVel, DiamParticle, Temperature, Porosity)
            * L / DiamParticle * ApproachVel**2 / (2*gravity) * (1-Porosity)
            / Porosity**3).to(u.m)


@ut.list_handler()
def G_CS_Ergun(ApproachVel, DiamParticle, Temperature, Porosity):
    """Camp Stein velocity gradient for flow through porous media.

    :param ApproachVel: superficial fluid velocity (VelSuperficial?)
    :type ApproachVel: u.m/u.s
    :param DiamParticle: particle diameter (DiamParticle?)
    :type DiamParticle: u.m
    :param Temperature: temperature of porous medium
    :type Temperature: u.degK
    :param Porosity: porosity of porous medium
    :type Porosity: u.dimensionless

    :return: Camp Stein velocity gradient for flow through porous media
    :rtype: u.Hz
    """
    return np.sqrt(f_Erdon(ApproachVel, DiamParticle, Temperature, Porosity)
                   * ApproachVel**3 * (1-Porosity)
                   / (2 * viscosity_kinematic(Temperature) * DiamParticle
                      * Porosity**4)).to(u.Hz)
