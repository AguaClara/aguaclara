"""Contains functions pertaining to the design of physical and chemical unit
processes of AguaClara water treatment plants.
"""

from aguaclara.core.units import u
import aguaclara.core.constants as con
import aguaclara.core.utility as ut
import aguaclara.core.pipes as pipe

import numpy as np
from scipy import interpolate, integrate
import warnings

############################ Gas ##############################


@ut.list_handler()
def density_air(Pressure, MolarMass, Temperature):
    """
    .. deprecated::
        `density_air` is deprecated; use `density_gas` instead.
    """
    warnings.warn('density_air is deprecated; use density_gas instead.',
                  UserWarning)
    return density_gas(Pressure, MolarMass, Temperature)


@ut.list_handler()
def density_gas(Pressure, MolarMass, Temperature):
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

########################## Geometry ###########################


@ut.list_handler()
def area_circle(DiamCircle):
    """Return the area of a circle given its diameter.

    :param DiamCircle: diameter of circle
    :type DiamCircle: u.m

    :return: area of circle
    :rtype: u.m**2
    """
    ut.check_range([DiamCircle.magnitude, ">0", "DiamCircle"])
    return (np.pi / 4 * DiamCircle**2)


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

####################### Water Properties #######################


#:
RE_TRANSITION_PIPE = 2100

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
    """
    .. deprecated::
        `viscosity_dynamic` is deprecated; use `viscosity_dynamic_water`
        instead.
    """
    warnings.warn('viscosity_dynamic is deprecated; use '
                  'viscosity_dynamic_water instead.', UserWarning)
    return viscosity_dynamic_water(temp)


@ut.list_handler()
def viscosity_dynamic_water(Temperature):
    """Return the dynamic viscosity of water at a given temperature.

    :param Temperature: temperature of water
    :type Temperature: u.degK

    :return: dynamic viscosity of water
    :rtype: u.kg/(u.m*u.s)
    """
    ut.check_range([Temperature.magnitude, ">0", "Temperature in Kelvin"])
    return 2.414 * (10**-5) * u.kg/(u.m*u.s) * 10**(247.8*u.degK /
                                                    (Temperature - 140*u.degK))


@ut.list_handler()
def density_water(Temperature=None, *, temp=None):
    """Return the density of water at a given temperature.

    :param Temperature: temperature of water
    :type Temperature: u.degK

    :param temp: deprecated; use Temperature instead

    :return: density of water
    :rtype: u.kg/u.m**3
    """
    if Temperature is not None and temp is not None:
        raise TypeError("density_water received both Temperature and temp")
    elif Temperature is None and temp is None:
        raise TypeError("density_water missing Temperature argument")
    elif temp is not None:
        warnings.warn("temp is deprecated; use Temperature instead.",
                      UserWarning)
        Temperature = temp

    ut.check_range([Temperature.magnitude, ">0", "Temperature in Kelvin"])
    rhointerpolated = interpolate.CubicSpline(WATER_DENSITY_TABLE[0],
                                              WATER_DENSITY_TABLE[1])
    Temperature = Temperature.to(u.degK).magnitude
    return rhointerpolated(Temperature).item() * u.kg/u.m**3


@ut.list_handler()
def viscosity_kinematic(temp):
    """
    .. deprecated::
        `viscosity_kinematic` is deprecated; use `viscosity_kinematic_water`
        instead.
    """
    warnings.warn('viscosity_kinematic is deprecated; use '
                  'viscosity_kinematic_water instead.', UserWarning)
    return viscosity_kinematic_water(temp)


@ut.list_handler()
def viscosity_kinematic_water(Temperature):
    """Return the kinematic viscosity of water at a given temperature.

    :param Temperature: temperature of water
    :type Temperature: u.degK

    :return: kinematic viscosity of water
    :rtype: u.m**2/u.s
    """
    ut.check_range([Temperature.magnitude, ">0", "Temperature in Kelvin"])
    return (viscosity_dynamic_water(Temperature) / density_water(Temperature))

####################### Hydraulic Radius #######################


@ut.list_handler()
def radius_hydraulic(Width, Depth, openchannel):
    """
    .. deprecated::
        `radius_hydraulic` is deprecated; use `radius_hydraulic_rect` instead.
    """
    warnings.warn('radius_hydraulic is deprecated; use radius_hydraulic_rect '
                  'instead.', UserWarning)
    return radius_hydraulic_rect(Width, Depth, openchannel)


@ut.list_handler()
def radius_hydraulic_rect(Width, Depth, OpenChannel):
    """Return the hydraulic radius of a rectangular channel given width and
    depth of water.

    :param Width: width of channel
    :type Width: u.m
    :param Depth: depth of water in channel
    :type Depth: u.m
    :param OpenChannel: true if channel is open, false if closed
    :type OpenChannel: boolean

    :return: hydraulic radius of rectangular channel
    :rtype: u.m
    """
    ut.check_range([Width.magnitude, ">0", "Width"],
                   [Depth.magnitude, ">0", "Depth"],
                   [OpenChannel, "boolean", "OpenChannel"])
    if OpenChannel:
        return ((Width*Depth) / (Width + 2*Depth))
    else:
        return ((Width*Depth) / (2 * (Width+Depth)))


@ut.list_handler()
def radius_hydraulic_general(Area, PerimWetted):
    """
    .. deprecated::
        `radius_hydraulic_general` is deprecated; use
        `radius_hydraulic_channel` instead.
    """
    warnings.warn('radius_hydraulic_general is deprecated; use '
                  'radius_hydraulic_channel instead.', UserWarning)
    return radius_hydraulic_channel(Area, PerimWetted)


@ut.list_handler()
def radius_hydraulic_channel(Area, PerimWetted):
    """Return the hydraulic radius of a general channel given cross sectional
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
    return (Area / PerimWetted)

####################### Reynolds Number #######################


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
    return ((4 * FlowRate) / (np.pi * Diam * Nu)).to(u.dimensionless)


@ut.list_handler()
def re_rect(FlowRate, Width, Depth, Nu, OpenChannel=None, *, openchannel=None):
    """Return the Reynolds number of flow through a rectangular channel.

    :param FlowRate: flow rate through channel
    :type FlowRate: u.m**3/u.s
    :param Width: width of channel
    :type Width: u.m
    :param Depth: depth of water in channel
    :type Depth: u.m
    :param Nu: kinematic viscosity of fluid
    :type Nu: u.m**2/u.s
    :param OpenChannel: true if channel is open, false if closed
    :type OpenChannel: boolean

    :param openchannel: deprecated; use OpenChannel instead

    :return: Reynolds number of flow through rectangular channel
    :rtype: u.dimensionless
    """
    ut.check_range([FlowRate.magnitude, ">0", "Flow rate"],
                   [Nu.magnitude, ">0", "Nu"])
    if OpenChannel is not None and openchannel is not None:
        raise TypeError("re_rect received both OpenChannel and openchannel")
    elif OpenChannel is None and openchannel is None:
        raise TypeError("re_rect missing OpenChannel argument")
    elif openchannel is not None:
        warnings.warn("openchannel is deprecated; use OpenChannel instead.",
                      UserWarning)
        OpenChannel = openchannel

    return (4 * FlowRate * radius_hydraulic_rect(Width, Depth, OpenChannel)
            / (Width * Depth * Nu)).to(u.dimensionless)


@ut.list_handler()
def re_general(Vel, Area, PerimWetted, Nu):
    """
    .. deprecated::
        `re_general` is deprecated; use `re_channel` instead.
    """
    warnings.warn('re_general is deprecated; use re_channel instead.',
                  UserWarning)
    return re_channel(Vel, Area, PerimWetted, Nu)


@ut.list_handler()
def re_channel(Vel, Area, PerimWetted, Nu):
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
    return (4 * radius_hydraulic_channel(Area, PerimWetted) * Vel / Nu).to(u.dimensionless)

########################### Friction ###########################


@ut.list_handler()
def fric(FlowRate, Diam, Nu, PipeRough):
    """
    .. deprecated::
        `fric` is deprecated; use `fric_pipe` instead.
    """
    warnings.warn('fric is deprecated; use fric_pipe instead', UserWarning)
    return fric_pipe(FlowRate, Diam, Nu, PipeRough)


@ut.list_handler()
def fric_pipe(FlowRate, Diam, Nu, Roughness):
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
    :param Roughness: roughness of pipe
    :type Roughness: u.m

    :return: friction factor of flow through pipe
    :rtype: u.dimensionless
    """
    ut.check_range([Roughness.magnitude, ">=0", "Pipe roughness"])
    if re_pipe(FlowRate, Diam, Nu) >= RE_TRANSITION_PIPE:
        f = (0.25 / (np.log10(Roughness / (3.7 * Diam)
                              + 5.74 / re_pipe(FlowRate, Diam, Nu) ** 0.9
                              )
                     ) ** 2
             )
    else:
        f = 64 / re_pipe(FlowRate, Diam, Nu)
    return f * u.dimensionless


@ut.list_handler()
def fric_rect(FlowRate, Width, Depth, Nu, Roughness=None, OpenChannel=None, *,
              PipeRough=None, openchannel=None):
    """Return the friction factor of a rectangular channel.

    The Swamee-Jain equation is adapted for a rectangular channel.

    :param FlowRate: flow rate through channel
    :type FlowRate: u.m**3/u.s
    :param Width: width of channel
    :type Width: u.m
    :param Depth: depth of water in channel
    :type Depth: u.m
    :param Nu: kinematic viscosity of fluid
    :type Nu: u.m**2/u.s
    :param Roughness: roughness of channel
    :type Roughness: u.m
    :param OpenChannel: true if channel is open, false if closed
    :type OpenChannel: boolean

    :param PipeRough: deprecated; use Roughness instead
    :param openchannel: deprecated; use OpenChannel instead

    :return: friction factor of flow through rectangular channel
    :rtype: u.dimensionless
    """
    if Roughness is not None and PipeRough is not None:
        raise TypeError("fric_rect received both Roughness and PipeRough")
    elif Roughness is None and PipeRough is None:
        raise TypeError("fric_rect missing Roughness argument")
    elif OpenChannel is not None and openchannel is not None:
        raise TypeError("fric_rect received both OpenChannel and openchannel")
    elif OpenChannel is None and openchannel is None:
        raise TypeError("fric_rect missing OpenChannel argument")
    else:
        if PipeRough is not None:
            warnings.warn("PipeRough is deprecated; use Roughness instead.",
                          UserWarning)
            Roughness = PipeRough
        if openchannel is not None:
            warnings.warn("openchannel is deprecated; use OpenChannel instead.",
                          UserWarning)
            OpenChannel = openchannel

    ut.check_range([Roughness.magnitude, ">=0", "Pipe roughness"])
    if re_rect(FlowRate, Width, Depth, Nu, OpenChannel) >= RE_TRANSITION_PIPE:
        # Diam = 4*R_h in adapted Swamee-Jain equation
        return (0.25 * u.dimensionless
                / (np.log10((Roughness
                             / (3.7 * 4
                                * radius_hydraulic_rect(Width, Depth,
                                                        OpenChannel)
                                )
                             )
                            + (5.74 / (re_rect(FlowRate, Width, Depth,
                                               Nu, OpenChannel) ** 0.9)
                               )
                            )
                   ) ** 2
                )
    else:
        return 64 * u.dimensionless / re_rect(FlowRate, Width, Depth, Nu,
                                              OpenChannel)


@ut.list_handler()
def fric_general(Area, PerimWetted, Vel, Nu, PipeRough):
    """
    .. deprecated::
        `fric_general` is deprecated; use `fric_channel` instead.
    """
    warnings.warn('fric_general is deprecated; use fric_channel instead.',
                  UserWarning)
    return fric_channel(Area, PerimWetted, Vel, Nu, PipeRough)


@ut.list_handler()
def fric_channel(Area, PerimWetted, Vel, Nu, Roughness):
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
    :param PipeRough: roughness of channel
    :type PipeRough: u.m

    :return: friction factor for flow through general channel
    :rtype: u.dimensionless
    """
    ut.check_range([Roughness.magnitude, ">=0", "Pipe roughness"])
    if re_channel(Vel, Area, PerimWetted, Nu) >= RE_TRANSITION_PIPE:
        # Diam = 4*R_h in adapted Swamee-Jain equation
        f = (0.25 /
             (np.log10((Roughness
                        / (3.7 * 4
                           * radius_hydraulic_channel(Area, PerimWetted)
                           )
                        )
                       + (5.74
                          / re_channel(Vel, Area, PerimWetted, Nu) ** 0.9
                          )
                       )
              ) ** 2
             )
    else:
        f = 64 / re_channel(Vel, Area, PerimWetted, Nu)
    return f * u.dimensionless

######################### Head Loss #########################


@ut.list_handler()
def headloss_fric(FlowRate, Diam, Length, Nu, PipeRough):
    """
    .. deprecated::
        `headloss_fric` is deprecated; use `headloss_major_pipe` instead.
    """
    warnings.warn('headloss_fric is deprecated; use headloss_major_pipe instead',
                  UserWarning)
    return headloss_major_pipe(FlowRate, Diam, Length, Nu, PipeRough)


@ut.list_handler()
def headloss_major_pipe(FlowRate, Diam, Length, Nu, Roughness):
    """Return the major head loss (due to wall shear) in a pipe.

    This function applies to both laminar and turbulent flows.

    :param FlowRate: flow rate through pipe
    :type FlowRate: u.m**3/u.s
    :param Diam: diameter of pipe
    :type Diam: u.m
    :param Length: length of pipe
    :type Length: u.m
    :param Nu: kinematic viscosity of fluid
    :type Nu: u.m**2/u.s
    :param Roughness: roughness of pipe
    :type Roughness: u.m

    :return: major head loss in pipe
    :rtype: u.m
    """
    ut.check_range([Length.magnitude, ">0", "Length"])
    return (fric_pipe(FlowRate, Diam, Nu, Roughness)
            * 8 / (u.gravity * np.pi**2)
            * (Length * FlowRate**2) / Diam**5
            ).to(u.m)


@ut.list_handler()
def headloss_exp(FlowRate, Diam, KMinor):
    """
    .. deprecated::
        `headloss_exp` is deprecated; use `headloss_minor_pipe` instead.
    """
    warnings.warn('headloss_exp is deprecated; use headloss_minor_pipe instead',
                  UserWarning)
    return headloss_minor_pipe(FlowRate, Diam, KMinor)


@ut.list_handler()
def headloss_minor_pipe(FlowRate, Diam, KMinor):
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
    return (KMinor * 8 / (u.gravity * np.pi**2) * FlowRate**2 / Diam**4).to(u.m)


@ut.list_handler()
def headloss(FlowRate, Diam, Length, Nu, PipeRough, KMinor):
    """
    .. deprecated::
        `headloss` is deprecated; use `headloss_pipe` instead.
    """
    warnings.warn('headloss is deprecated; use headloss_pipe instead',
                  UserWarning)
    return headloss_pipe(FlowRate, Diam, Length, Nu, PipeRough, KMinor)


@ut.list_handler()
def headloss_pipe(FlowRate, Diam, Length, Nu, Roughness, KMinor):
    """Return the total head loss from major and minor losses in a pipe.

    This function applies to both laminar and turbulent flows.

    :param FlowRate: flow rate through pipe
    :type FlowRate: u.m**3/u.s
    :param Diam: diameter of pipe
    :type Diam: u.m
    :param Length: length of pipe
    :type Length: u.m
    :param Nu: kinematic viscosity of fluid
    :type Nu: u.m**2/u.s
    :param Roughness: roughness of pipe
    :type Roughness: u.m
    :param KMinor: minor loss coefficient
    :type KMinor: u.dimensionless or unitless

    :return: total head loss in pipe
    :rtype: u.m
    """
    return (headloss_major_pipe(FlowRate, Diam, Length, Nu, Roughness)
            + headloss_minor_pipe(FlowRate, Diam, KMinor))


@ut.list_handler()
def headloss_fric_rect(FlowRate, Width, Depth, Length, Nu, PipeRough, openchannel):
    """
    .. deprecated::
        `headloss_fric_rect` is deprecated; use `headloss_major_rect` instead.
    """
    warnings.warn('headloss_fric_rect is deprecated; use headloss_major_rect instead',
                  UserWarning)
    return headloss_major_rect(FlowRate, Width, Depth, Length, Nu, PipeRough, openchannel)


@ut.list_handler()
def headloss_major_rect(FlowRate, Width, Depth, Length, Nu, Roughness, OpenChannel):
    """Return the major head loss due to wall shear in a rectangular channel.

    This equation applies to both laminar and turbulent flows.

    :param FlowRate: flow rate through channel
    :type FlowRate: u.m**3/u.s
    :param Width: width of channel
    :type Width: u.m
    :param Depth: depth of water in channel
    :type Depth: u.m
    :param Length: length of channel
    :type Length: u.m
    :param Nu: kinematic viscosity of fluid
    :type Nu: u.m**2/u.s
    :param Roughness: roughness of channel
    :type Roughness: u.m
    :param OpenChannel: true if channel is open, false if closed
    :type OpenChannel: boolean

    :return: major head loss in rectangular channel
    :rtype: u.m
    """
    ut.check_range([Length.magnitude, ">0", "Length"])
    return (fric_rect(FlowRate, Width, Depth, Nu,
                      Roughness, OpenChannel)
            * Length
            / (4 * radius_hydraulic_rect(Width, Depth, OpenChannel))
            * FlowRate**2
            / (2 * u.gravity * (Width*Depth)**2)
            ).to(u.m)


@ut.list_handler()
def headloss_exp_rect(FlowRate, Width, Depth, KMinor):
    """
    .. deprecated::
        `headloss_exp_rect` is deprecated; use `headloss_minor_rect` instead.
    """
    warnings.warn('headloss_exp_rect is deprecated; use headloss_minor_rect instead',
                  UserWarning)
    return headloss_minor_rect(FlowRate, Width, Depth, KMinor)


@ut.list_handler()
def headloss_minor_rect(FlowRate, Width, Depth, KMinor):
    """Return the minor head loss due to expansion in a rectangular channel.

    This equation applies to both laminar and turbulent flows.

    :param FlowRate: flow rate through channel
    :type FlowRate: u.m**3/u.s
    :param Width: width of channel
    :type Width: u.m
    :param Depth: depth of water in channel
    :type Depth: u.m
    :param KMinor: minor loss coefficient
    :type KMinor: u.dimensionless or unitless

    :return: minor head loss in rectangular channel
    :rtype: u.m
    """
    ut.check_range([FlowRate.magnitude, ">0", "Flow rate"],
                   [Width.magnitude, ">0", "Width"],
                   [Depth.magnitude, ">0", "Depth"],
                   [KMinor, ">=0", "K minor"])
    return (KMinor * FlowRate**2
            / (2 * u.gravity * (Width*Depth)**2)
            ).to(u.m)


@ut.list_handler()
def headloss_rect(FlowRate, Width, Depth, Length, KMinor, Nu, Roughness=None,
                  OpenChannel=None, *, PipeRough=None, openchannel=None):
    """Return the total head loss from major and minor losses in a rectangular
    channel.

    This equation applies to both laminar and turbulent flows.

    :param FlowRate: flow rate through channel
    :type FlowRate: u.m**3/u.s
    :param Width: width of channel
    :type Width: u.m
    :param Depth: depth of water in channel
    :type Depth: u.m
    :param Length: length of channel
    :type Length: u.m
    :param KMinor: minor loss coefficient
    :type KMinor: u.dimensionless or unitless
    :param Nu: kinematic viscosity of fluid
    :type Nu: u.m**2/u.s
    :param Roughness: roughness of channel
    :type Roughness: u.m
    :param OpenChannel: true if channel is open, false if closed
    :type OpenChannel: boolean

    :param PipeRough: deprecated; use Roughness instead
    :type openchannel: deprecated; use OpenChannel instead

    :return: total head loss in rectangular channel
    :rtype: u.m
    """
    if Roughness is not None and PipeRough is not None:
        raise TypeError("headloss_rect received both Roughness and PipeRough")
    elif Roughness is None and PipeRough is None:
        raise TypeError("headloss_rect missing Roughness argument")
    elif OpenChannel is not None and openchannel is not None:
        raise TypeError("headloss_rect received both OpenChannel and openchannel")
    elif OpenChannel is None and openchannel is None:
        raise TypeError("headloss_rect missing OpenChannel argument")
    else:
        if PipeRough is not None:
            warnings.warn("PipeRough is deprecated; use Roughness instead.",
                          UserWarning)
            Roughness = PipeRough
        if openchannel is not None:
            warnings.warn("openchannel is deprecated; use OpenChannel instead.",
                          UserWarning)
            OpenChannel = openchannel

    return (headloss_minor_rect(FlowRate, Width, Depth, KMinor)
            + headloss_major_rect(FlowRate, Width, Depth, Length,
                                  Nu, Roughness, OpenChannel))


@ut.list_handler()
def headloss_fric_general(Area, PerimWetted, Vel, Length, Nu, PipeRough):
    """
    .. deprecated::
        `headloss_fric_general` is deprecated; use `headloss_major_channel` instead.
    """
    warnings.warn('headloss_fric_general` is deprecated; use `headloss_major_channel` instead',
                  UserWarning)
    return headloss_major_channel(Area, PerimWetted, Vel, Length, Nu, PipeRough)


@ut.list_handler()
def headloss_major_channel(Area, PerimWetted, Vel, Length, Nu, Roughness):
    """Return the major head loss due to wall shear in a general channel.

    This equation applies to both laminar and turbulent flows.

    :param Area: cross sectional area of channel
    :type Area: u.m**2
    :param PerimWetted: wetted perimeter of channel
    :type PerimWetted: u.m
    :param Vel: velocity of fluid
    :type Vel: u.m/u.s
    :param Length: length of channel
    :type Length: u.m
    :param Nu: kinematic viscosity of fluid
    :type Nu: u.m**2/u.s
    :param Roughness: roughness of channel
    :type Roughness: u.m

    :return: major head loss in general channel
    :rtype: u.m
    """
    ut.check_range([Length.magnitude, ">0", "Length"])
    return (fric_channel(Area, PerimWetted, Vel, Nu, Roughness) * Length
            / (4 * radius_hydraulic_channel(Area, PerimWetted))
            * Vel**2 / (2*u.gravity)
            ).to(u.m)


@ut.list_handler()
def headloss_exp_general(Vel, KMinor):
    """
    .. deprecated::
        `headloss_exp_general` is deprecated; use `headloss_minor_channel` instead.
    """
    warnings.warn('headloss_exp_general` is deprecated; use `headloss_minor_channel` instead',
                  UserWarning)
    return headloss_minor_channel(Vel, KMinor)


@ut.list_handler()
def headloss_minor_channel(Vel, KMinor):
    """Return the minor head loss due to expansion in a general channel.

    This equation applies to both laminar and turbulent flows.

    :param Vel: velocity of fluid
    :type Vel: u.m/u.s
    :param KMinor: minor loss coefficient
    :type KMinor: u.dimensionless or unitless

    :return: minor head loss in general channel
    :rtype: u.m
    """
    ut.check_range([Vel.magnitude, ">0", "Velocity"],
                   [KMinor, '>=0', 'K minor'])
    return (KMinor * Vel**2 / (2*u.gravity)).to(u.m)


@ut.list_handler()
def headloss_gen(Area, Vel, PerimWetted, Length, KMinor, Nu, PipeRough):
    """
    .. deprecated::
        `headloss_gen` is deprecated; use `headloss_channel` instead.
    """
    warnings.warn('headloss_gen` is deprecated; use `headloss_channel` instead',
                  UserWarning)
    return headloss_channel(Area, Vel, PerimWetted, Length, KMinor, Nu, PipeRough)


@ut.list_handler()
def headloss_channel(Area, Vel, PerimWetted, Length, KMinor, Nu, Roughness):
    """Return the total head loss from major and minor losses in a general
    channel.

    This equation applies to both laminar and turbulent flows.

    :param Area: cross sectional area of channel
    :type Area: u.m**2
    :param Vel: velocity of fluid
    :type Vel: u.m/u.s
    :param PerimWetted: wetted perimeter of channel
    :type PerimWetted: u.m
    :param Length: length of channel
    :type Length: u.m
    :param KMinor: minor loss coefficient
    :type KMinor: u.dimensionless or unitless
    :param Nu: kinematic viscosity of fluid
    :type Nu: u.m**2/u.s
    :param Roughness: roughness of channel
    :type Roughness: u.m

    :return: total head loss in general channel
    :rtype: u.m
    """
    return (headloss_minor_channel(Vel, KMinor)
            + headloss_major_channel(Area, PerimWetted, Vel,
                                     Length, Nu, Roughness)).to(u.m)


@ut.list_handler()
def headloss_manifold(FlowRate, Diam, Length, KMinor, Nu, Roughness=None, NumOutlets=None, *, PipeRough=None):
    """Return the total head loss through the manifold.

    :param FlowRate: flow rate through manifold
    :type FlowRate: u.m**3/u.s
    :param Diam: diameter of manifold
    :type Diam: u.m
    :param Length: length of manifold
    :type Length: u.m
    :param KMinor: minor loss coefficient
    :type KMinor: u.dimensionless or unitless
    :param Nu: kinematic viscosity of fluid
    :type Nu: u.m**2/u.s
    :param Roughness: roughness of manifold
    :type Roughness: u.m
    :param NumOutlets: number of outlets from manifold
    :type NumOutlets: u.dimensionless or unitless

    :param PipeRough: deprecated; use Roughness instead

    :return: total headloss through manifold
    :rtype: u.m
    """
    ut.check_range([NumOutlets, ">0, int", 'Number of outlets'])

    if Roughness is not None and PipeRough is not None:
        raise TypeError("headloss_manifold received both Roughness and PipeRough")
    elif Roughness is None and PipeRough is None:
        raise TypeError("headloss_manifold missing Roughness argument")
    elif NumOutlets is None:
        raise TypeError("headloss_manifold missing NumOutlets argument")
    elif PipeRough is not None:
        warnings.warn("PipeRough is deprecated; use Roughness instead.",
                      UserWarning)
        Roughness = PipeRough

    return (headloss_pipe(FlowRate, Diam, Length, Nu, Roughness, KMinor)
            * ((1/3)
               + (1 / (2*NumOutlets))
               + (1 / (6*NumOutlets**2))
               )
            ).to(u.m)


@ut.list_handler()
def elbow_minor_loss(q, id_, k):
    """
    .. deprecated::
        `elbow_minor_loss` is deprecated; use `headloss_minor_elbow` instead.
    """
    warnings.warn('elbow_minor_loss is deprecated; use headloss_minor_elbow instead',
                  UserWarning)
    return headloss_minor_elbow(q, id_, k)


@ut.list_handler()
def headloss_minor_elbow(FlowRate, Diam, KMinor):
    """Return the minor head loss (due to changes in geometry) in an elbow.

    :param FlowRate: flow rate through pipe
    :type FlowRate: u.m**3/u.s
    :param Diam: diameter of pipe
    :type Diam: u.m
    :param KMinor: minor loss coefficient
    :type KMinor: u.dimensionless or unitless

    :return: minor head loss in pipe
    :rtype: u.m
    """
    vel = FlowRate / area_circle(Diam)
    minor_loss = KMinor * vel ** 2 / (2 * u.gravity)
    return minor_loss.to(u.m)

######################### Orifices #########################


@ut.list_handler()
def flow_orifice(Diam, Height, RatioVCOrifice):
    """Return the flow rate of the orifice.

    :param Diam: diameter of orifice
    :type Diam: u.m
    :param Height: piezometric height of orifice
    :type Height: u.m
    :param RatioVCOrifice: vena contracta ratio of orifice
    :type RatioVCOrifice: u.dimensionless or unitless

    :return: flow rate of orifice
    :rtype: u.m**3/u.s
    """
    ut.check_range([Diam.magnitude, ">0", "Diameter"],
                   [RatioVCOrifice, "0-1", "VC orifice ratio"])
    if Height.magnitude > 0:
        return (RatioVCOrifice * area_circle(Diam)
                * np.sqrt(2 * u.gravity * Height)).to(u.m**3/u.s)
    else:
        return 0 * u.m**3/u.s


@ut.list_handler()
def flow_orifice_vert(Diam, Height, RatioVCOrifice):
    """Return the vertical flow rate of the orifice.

    :param Diam: diameter of orifice
    :type Diam: u.m
    :param Height: piezometric height of orifice
    :type Height: u.m
    :param RatioVCOrifice: vena contracta ratio of orifice
    :type RatioVCOrifice: u.dimensionless or unitless

    :return: vertical flow rate of orifice
    :rtype: u.m**3/u.s
    """
    ut.check_range([RatioVCOrifice, "0-1", "VC orifice ratio"])
    Diam = Diam.to(u.m)
    Height = Height.to(u.m)
    if Height > -Diam / 2:
        flow_vert = integrate.quad(lambda z: (Diam*np.sin(np.arccos(z*u.m/(Diam/2)))
                                              * np.sqrt(Height - z*u.m)
                                              ).magnitude,
                                   - Diam.magnitude / 2,
                                   min(Diam/2, Height).magnitude)
        return (flow_vert[0] * u.m**2.5 * RatioVCOrifice *
                np.sqrt(2 * u.gravity)).to(u.m**3/u.s)
    else:
        return 0 * u.m**3/u.s


@ut.list_handler()
def head_orifice(Diam, RatioVCOrifice, FlowRate):
    """Return the piezometric head of the orifice.

    :param Diam: diameter of orifice
    :type Diam: u.m
    :param RatioVCOrifice: vena contracta ratio of orifice
    :type RatioVCOrifice: u.dimensionless or unitless
    :param FlowRate: flow rate of orifice
    :type FlowRate: u.m**3/u.s

    :return: head of orifice
    :rtype: u.m
    """
    ut.check_range([Diam.magnitude, ">0", "Diameter"],
                   [FlowRate.magnitude, ">0", "Flow rate"],
                   [RatioVCOrifice, "0-1", "VC orifice ratio"])
    return ((FlowRate
             / (RatioVCOrifice * area_circle(Diam))
             )**2
            / (2*u.gravity)
            ).to(u.m)


@ut.list_handler()
def area_orifice(Height, RatioVCOrifice, FlowRate):
    """Return the area of the orifice.

    :param Height: piezometric height of orifice
    :type Height: u.m
    :param RatioVCOrifice: vena contracta ratio of orifice
    :type RatioVCOrifice: u.dimensionless or unitless
    :param FlowRate: flow rate of orifice
    :type FlowRate: u.m**3/u.s

    :return: area of orifice
    :rtype: u.m**2
    """
    ut.check_range([Height.magnitude, ">0", "Height"],
                   [FlowRate.magnitude, ">0", "Flow rate"],
                   [RatioVCOrifice, "0-1, >0", "VC orifice ratio"])
    return (FlowRate / (RatioVCOrifice * np.sqrt(2 * u.gravity *
                                                 Height))).to(u.m**2)


@ut.list_handler()
def num_orifices(FlowRate, RatioVCOrifice, HeadLossOrifice, DiamOrifice):
    """Return the number of orifices.

    :param FlowRate: flow rate of orifice
    :type FlowRate: u.m**3/u.s
    :param RatioVCOrifice: vena contracta ratio of orifice
    :type RatioVCOrifice: u.dimensionless or unitless
    :param HeadLossOrifice: head loss of orifice
    :type HeadLossOrifice: u.m
    :param DiamOrifice: diameter of orifice
    :type DiamOrifice: u.m

    :return: number of orifices
    :rtype: u.dimensionless
    """
    return np.ceil(area_orifice(HeadLossOrifice, RatioVCOrifice, FlowRate)
                   / area_circle(DiamOrifice)).to(u.dimensionless)

########################### Flows ###########################


@ut.list_handler()
def flow_transition(Diam, Nu):
    """Return the flow rate for the laminar/turbulent transition.

    :param Diam: diameter of pipe
    :type Diam: u.m
    :param Nu: kinematic viscosity of fluid
    :type Nu: u.m**2/u.s

    :return: flow rate for laminar/turbulent transition
    :rtype: u.m**3/u.s
    """
    ut.check_range([Diam.magnitude, ">0", "Diameter"],
                   [Nu.magnitude, ">0", "Nu"])
    return (np.pi * Diam * RE_TRANSITION_PIPE * Nu / 4).to(u.m**3/u.s)


@ut.list_handler()
def flow_hagen(Diam, HeadLossMajor=None, Length=None, Nu=None, *, HeadLossFric=None):
    """Return the flow rate for laminar flow with only major losses.

    :param Diam: diameter of pipe
    :type Diam: u.m
    :param HeadLossMajor: head loss due to friction
    :type HeadLossMajor: u.m
    :param Length: length of pipe
    :type Length: u.m
    :param Nu: kinematic viscosity of fluid
    :type Nu: u.m**2/u.s

    :param HeadLossFric: deprecated; use HeadLossMajor instead

    :return: flow rate for laminar flow with only major losses
    :rtype: u.m**3/u.s
    """
    if HeadLossMajor is not None and HeadLossFric is not None:
        raise TypeError("flow_hagen received both HeadLossMajor and HeadLossFric")
    elif HeadLossMajor is None and HeadLossFric is None:
        raise TypeError("flow_hagen missing HeadLossMajor argument")
    elif Length is None:
        raise TypeError("flow_hagen missing Length argument")
    elif Nu is None:
        raise TypeError("flow_hagen missing Nu argument")
    elif HeadLossFric is not None:
        warnings.warn("HeadLossFric is deprecated; use HeadLossMajor instead.",
                      UserWarning)
        HeadLossMajor = HeadLossFric

    ut.check_range([Diam.magnitude, ">0", "Diameter"],
                   [Length.magnitude, ">0", "Length"],
                   [HeadLossMajor.magnitude, ">=0", "Headloss due to friction"],
                   [Nu.magnitude, ">0", "Nu"])
    return ((np.pi*Diam**4) / (128*Nu) * u.gravity * HeadLossMajor
            / Length).to(u.m**3/u.s)


@ut.list_handler()
def flow_swamee(Diam, HeadLossMajor=None, Length=None, Nu=None, Roughness=None, *, HeadLossFric=None, PipeRough=None):
    """Return the flow rate for turbulent flow with only major losses.

    :param Diam: diameter of pipe
    :type Diam: u.m
    :param HeadLossMajor: head loss due to friction
    :type HeadLossMajor: u.m
    :param Length: length of pipe
    :type Length: u.m
    :param Nu: kinematic viscosity of fluid
    :type Nu: u.m**2/u.s
    :param Roughness: roughness of pipe
    :type Roughness: u.m

    :param HeadLossFric: deprecated; use HeadLossMajor instead
    :param PipeRough: deprecated; use Roughness instead

    :return: flow rate for turbulent flow with only major losses
    :rtype: u.m**3/u.s
    """
    if HeadLossMajor is not None and HeadLossFric is not None:
        raise TypeError("flow_swamee received both HeadLossMajor and HeadLossFric")
    elif HeadLossMajor is None and HeadLossFric is None:
        raise TypeError("flow_swamee missing HeadLossMajor argument")
    elif Length is None:
        raise TypeError("flow_swamee missing Length argument")
    elif Nu is None:
        raise TypeError("flow_swamee missing Nu argument")
    elif Roughness is not None and PipeRough is not None:
        raise TypeError("flow_swamee received both Roughness and PipeRough")
    elif Roughness is None and PipeRough is None:
        raise TypeError("flow_swamee missing Roughness argument")
    else:
        if HeadLossFric is not None:
            warnings.warn("HeadLossFric is deprecated; use HeadLossMajor instead.",
                          UserWarning)
            HeadLossMajor = HeadLossFric
        if PipeRough is not None:
            warnings.warn("PipeRough is deprecated; use Roughness instead.",
                          UserWarning)
            Roughness = PipeRough

    ut.check_range([Diam.magnitude, ">0", "Diameter"],
                   [Length.magnitude, ">0", "Length"],
                   [HeadLossMajor.magnitude, ">0", "Headloss due to friction"],
                   [Nu.magnitude, ">0", "Nu"],
                   [Roughness.magnitude, ">=0", "Pipe roughness"])
    logterm = np.log10(Roughness / (3.7 * Diam)
                       + 2.51 * Nu * np.sqrt(Length / (2 * u.gravity
                                                       * HeadLossMajor
                                                       * Diam**3)
                                             )
                       )
    return ((-np.pi / np.sqrt(2)) * Diam**(5/2) * logterm
            * np.sqrt(u.gravity * HeadLossMajor / Length)
            ).to(u.m**3/u.s)


@ut.list_handler()
def flow_pipemajor(Diam, HeadLossFric, Length, Nu, PipeRough):
    """
    .. deprecated::
        `flow_pipemajor` is deprecated; use `flow_major_pipe` instead.
    """
    warnings.warn('flow_pipemajor is deprecated; use '
                  'flow_major_pipe instead.', UserWarning)
    return flow_major_pipe(Diam, HeadLossFric, Length, Nu, PipeRough)


@ut.list_handler()
def flow_major_pipe(Diam, HeadLossMajor, Length, Nu, Roughness):
    """Return the flow rate with only major losses.

    This function applies to both laminar and turbulent flows.

    :param Diam: diameter of pipe
    :type Diam: u.m
    :param HeadLossMajor: head loss due to friction
    :type HeadLossMajor: u.m
    :param Length: length of pipe
    :type Length: u.m
    :param Nu: kinematic viscosity of fluid
    :type Nu: u.m**2/u.s
    :param Roughness: roughness of pipe
    :type Roughness: u.m

    :return: flow rate with only major losses
    :rtype: u.m**3/u.s
    """
    FlowHagen = flow_hagen(Diam, HeadLossMajor, Length, Nu)
    if FlowHagen < flow_transition(Diam, Nu):
        return FlowHagen
    else:
        return flow_swamee(Diam, HeadLossMajor, Length, Nu, Roughness)


@ut.list_handler()
def flow_pipeminor(Diam, HeadLossExpans, KMinor):
    """
    .. deprecated::
        `flow_pipeminor` is deprecated; use `flow_minor_pipe` instead.
    """
    warnings.warn('flow_pipeminor is deprecated; use '
                  'flow_minor_pipe instead.', UserWarning)
    return flow_minor_pipe(Diam, HeadLossExpans, KMinor)


@ut.list_handler()
def flow_minor_pipe(Diam, HeadLossMinor, KMinor):
    """Return the flow rate with only minor losses.

    This function applies to both laminar and turbulent flows.

    :param Diam: diameter of pipe
    :type Diam: u.m
    :param HeadLossExpans: head loss due to expansion
    :type HeadLossExpans: u.m
    :param KMinor: minor loss coefficient
    :type KMinor: u.dimensionless or unitless

    :return: flow rate with only minor losses
    :rtype: u.m**3/u.s
    """
    ut.check_range([HeadLossMinor.magnitude, ">=0",
                    "Headloss due to expansion"],
                   [KMinor, ">0", "K minor"])
    return (area_circle(Diam) * np.sqrt(2 * u.gravity * HeadLossMinor
                                        / KMinor)
            ).to(u.m**3/u.s)


@ut.list_handler()
def flow_pipe(Diam, HeadLoss, Length, Nu, Roughness=None, KMinor=None, *, PipeRough=None):
    """Return the flow rate in a pipe.

    This function works for both major and minor losses as well as
    both laminar and turbulent flows.

    :param Diam: diameter of pipe
    :type Diam: u.m
    :param HeadLoss: total head loss from major and minor losses
    :type HeadLoss: u.m
    :param Length: length of pipe
    :type Length: u.m
    :param Nu: kinematic viscosity of fluid
    :type Nu: u.m**2/u.s
    :param Roughness: roughness of pipe
    :type Roughness: u.m
    :param KMinor: minor loss coefficient
    :type KMinor: u.dimensionless or unitless

    :param PipeRough: deprecated; use Roughness instead

    :return: flow rate in pipe
    :rtype: u.m**3/u.s
    """
    if Roughness is not None and PipeRough is not None:
        raise TypeError("flow_pipe received both Roughness and PipeRough")
    elif Roughness is None and PipeRough is None:
        raise TypeError("flow_pipe missing Roughness argument")
    elif KMinor is None:
        raise TypeError("flow_pipe missing KMinor argument")
    elif PipeRough is not None:
            warnings.warn("PipeRough is deprecated; use Roughness instead.",
                          UserWarning)
            Roughness = PipeRough

    if KMinor == 0:
        FlowRate = flow_major_pipe(Diam, HeadLoss, Length, Nu,
                                   Roughness)
    else:
        FlowRatePrev = 0
        err = 1.0
        FlowRate = min(flow_major_pipe(Diam, HeadLoss, Length,
                                       Nu, Roughness),
                       flow_minor_pipe(Diam, HeadLoss, KMinor)
                       )
        while err > 0.01:
            FlowRatePrev = FlowRate
            HLFricNew = (HeadLoss * headloss_major_pipe(FlowRate, Diam, Length,
                                                        Nu, Roughness)
                         / (headloss_major_pipe(FlowRate, Diam, Length,
                                                Nu, Roughness)
                            + headloss_minor_pipe(FlowRate, Diam, KMinor)
                            )
                         )
            FlowRate = flow_major_pipe(Diam, HLFricNew, Length,
                                       Nu, Roughness)
            if FlowRate == 0:
                err = 0.0
            else:
                err = (abs(FlowRate - FlowRatePrev)
                       / ((FlowRate + FlowRatePrev) / 2)
                       )
    return FlowRate.to(u.m**3/u.s)

########################## Diameters ##########################


@ut.list_handler()
def diam_hagen(FlowRate, HeadLossMajor=None, Length=None, Nu=None, *, HeadLossFric=None):
    """Return the inner diameter of a pipe with laminar flow and no minor losses.

    The Hagen Poiseuille equation is dimensionally correct and returns the
    inner diameter of a pipe given the flow rate and the head loss due
    to shear on the pipe walls. The Hagen Poiseuille equation does NOT take
    minor losses into account. This equation ONLY applies to laminar flow.

    :param FlowRate: flow rate of pipe
    :type FlowRate: u.m**3/u.s
    :param HeadLossFric: head loss due to friction
    :type HeadLossFric: u.m
    :param Length: length of pipe
    :type Length: u.m
    :param Nu: kinematic viscosity of fluid
    :type Nu: u.m**2/u.s

    :param HeadLossFric: deprecated; use HeadLossMajor instead

    :return: inner diameter of pipe
    :rtype: u.m
    """
    if HeadLossMajor is not None and HeadLossFric is not None:
        raise TypeError("diam_hagen received both HeadLossMajor and HeadLossFric")
    elif HeadLossMajor is None and HeadLossFric is None:
        raise TypeError("diam_hagen missing HeadLossMajor argument")
    elif Length is None:
        raise TypeError("diam_hagen missing Length argument")
    elif Nu is None:
        raise TypeError("diam_hagen missing Nu argument")
    elif HeadLossFric is not None:
        warnings.warn("HeadLossFric is deprecated; use HeadLossMajor instead.",
                      UserWarning)
        HeadLossMajor = HeadLossFric

    ut.check_range([FlowRate.magnitude, ">0", "Flow rate"],
                   [Length.magnitude, ">0", "Length"],
                   [HeadLossMajor.magnitude, ">0", "Headloss due to friction"],
                   [Nu.magnitude, ">0", "Nu"])
    return (((128 * Nu * FlowRate * Length)
             / (u.gravity * HeadLossMajor * np.pi)
             ) ** (1/4)).to(u.m)


@ut.list_handler()
def diam_swamee(FlowRate, HeadLossMajor=None, Length=None, Nu=None, Roughness=None, *, HeadLossFric=None, PipeRough=None):
    """Return the inner diameter of a pipe with turbulent flow and no minor losses.

    The Swamee Jain equation is dimensionally correct and returns the
    inner diameter of a pipe given the flow rate and the head loss due
    to shear on the pipe walls. The Swamee Jain equation does NOT take
    minor losses into account. This equation ONLY applies to turbulent
    flow.

    :param FlowRate: flow rate of pipe
    :type FlowRate: u.m**3/u.s
    :param HeadLossFric: head loss due to friction
    :type HeadLossFric: u.m
    :param Length: length of pipe
    :type Length: u.m
    :param Nu: kinematic viscosity of fluid
    :type Nu: u.m**2/u.s
    :param PipeRough: roughness of pipe
    :type PipeRough: u.m

    :param HeadLossFric: deprecated; use HeadLossMajor instead
    :param PipeRough: deprecated; use Roughness instead

    :return: inner diameter of pipe
    :rtype: u.m
    """
    if HeadLossMajor is not None and HeadLossFric is not None:
        raise TypeError("diam_swamee received both HeadLossMajor and HeadLossFric")
    elif HeadLossMajor is None and HeadLossFric is None:
        raise TypeError("diam_swamee missing HeadLossMajor argument")
    elif Length is None:
        raise TypeError("diam_swamee missing Length argument")
    elif Nu is None:
        raise TypeError("diam_swamee missing Nu argument")
    elif Roughness is not None and PipeRough is not None:
        raise TypeError("diam_swamee received both Roughness and PipeRough")
    elif Roughness is None and PipeRough is None:
        raise TypeError("diam_swamee missing Roughness argument")
    else:
        if HeadLossFric is not None:
            warnings.warn("HeadLossFric is deprecated; use HeadLossMajor instead.",
                          UserWarning)
            HeadLossMajor = HeadLossFric
        if PipeRough is not None:
            warnings.warn("PipeRough is deprecated; use Roughness instead.",
                          UserWarning)
            Roughness = PipeRough

    ut.check_range([FlowRate.magnitude, ">0", "Flow rate"],
                   [Length.magnitude, ">0", "Length"],
                   [HeadLossMajor.magnitude, ">0", "Headloss due to friction"],
                   [Nu.magnitude, ">0", "Nu"],
                   [Roughness.magnitude, ">=0", "Pipe roughness"])
    a = ((Roughness ** 1.25)
         * ((Length * FlowRate**2)
            / (u.gravity * HeadLossMajor)
            )**4.75
         ).to_base_units()
    b = (Nu**5 * FlowRate**47
         * (Length / (u.gravity * HeadLossMajor)) ** 26
         ).to_base_units()**0.2
    return (0.66 * (a+b)**0.04).to(u.m)


@ut.list_handler()
def diam_pipemajor(FlowRate, HeadLossFric, Length, Nu, PipeRough):
    """
    .. deprecated::
        `diam_pipemajor` is deprecated; use `diam_major_pipe` instead.
    """
    warnings.warn('diam_pipemajor is deprecated; use '
                  'diam_major_pipe instead.', UserWarning)
    return diam_major_pipe(FlowRate, HeadLossFric, Length, Nu, PipeRough)


@ut.list_handler()
def diam_major_pipe(FlowRate, HeadLossMajor, Length, Nu, Roughness):
    """Return the pipe inner diameter that would result in given major losses.

    This function applies to both laminar and turbulent flow.

    :param FlowRate: flow rate of pipe
    :type FlowRate: u.m**3/u.s
    :param HeadLossMajor: head loss due to friction
    :type HeadLossMajor: u.m
    :param Length: length of pipe
    :type Length: u.m
    :param Nu: kinematic viscosity of fluid
    :type Nu: u.m**2/u.s
    :param Roughness: roughness of pipe
    :type Roughness: u.m

    :return: inner diameter of pipe
    :rtype: u.m
    """
    DiamLaminar = diam_hagen(FlowRate, HeadLossMajor, Length, Nu)
    if re_pipe(FlowRate, DiamLaminar, Nu) <= RE_TRANSITION_PIPE:
        return DiamLaminar
    else:
        return diam_swamee(FlowRate, HeadLossMajor, Length,
                           Nu, Roughness)


@ut.list_handler()
def diam_pipeminor(FlowRate, HeadLossExpans, KMinor):
    """
    .. deprecated::
        `diam_pipeminor` is deprecated; use `diam_minor_pipe` instead.
    """
    warnings.warn('diam_pipeminor is deprecated; use '
                  'diam_minor_pipe instead.', UserWarning)
    return diam_minor_pipe(FlowRate, HeadLossExpans, KMinor)


@ut.list_handler()
def diam_minor_pipe(FlowRate, HeadLossMinor, KMinor):
    """Return the pipe inner diameter that would result in the given minor losses.

    This function applies to both laminar and turbulent flow.

    :param FlowRate: flow rate of pipe
    :type FlowRate: u.m**3/u.s
    :param HeadLossMinor: head loss due to expansion
    :type HeadLossMinor: u.m
    :param KMinor: minor loss coefficient
    :type KMinor: u.dimensionless or unitless

    :return: inner diameter of pipe
    :rtype: u.m
    """
    ut.check_range([FlowRate.magnitude, ">0", "Flow rate"],
                   [KMinor, ">=0", "K minor"],
                   [HeadLossMinor.magnitude, ">0", "Headloss due to expansion"])
    return (np.sqrt(4 * FlowRate / np.pi)
            * (KMinor / (2 * u.gravity * HeadLossMinor)) ** (1/4)
            ).to(u.m)


@ut.list_handler()
def diam_pipe(FlowRate, HeadLoss, Length, Nu, PipeRough, KMinor):
    """Return the pipe inner diameter that would result in the given total head
    loss.

    This function applies to both laminar and turbulent flow and
    incorporates both minor and major losses.

    :param FlowRate: flow rate of pipe
    :type FlowRate: u.m**3/u.s
    :param HeadLoss: total head loss from major and minor losses
    :type HeadLoss: u.m
    :param Length: length of pipe
    :type Length: u.m
    :param Nu: kinematic viscosity of fluid
    :type Nu: u.m**2/u.s
    :param PipeRough: roughness of pipe
    :type PipeRough: u.m
    :param KMinor: minor loss coefficient
    :type KMinor: u.dimensionless or unitless

    :return: inner diameter of pipe
    :rtype: u.m
    """
    if KMinor == 0:
        Diam = diam_major_pipe(FlowRate, HeadLoss, Length, Nu,
                               PipeRough)
    else:
        Diam = max(diam_major_pipe(FlowRate, HeadLoss,
                                   Length, Nu, PipeRough),
                   diam_minor_pipe(FlowRate, HeadLoss, KMinor))
        err = 1.00
        while err > 0.001:
            DiamPrev = Diam
            HLFricNew = (HeadLoss * headloss_major_pipe(FlowRate, Diam, Length,
                                                        Nu, PipeRough
                                                        )
                         / (headloss_major_pipe(FlowRate, Diam, Length,
                                                Nu, PipeRough
                                                )
                            + headloss_minor_pipe(FlowRate, Diam, KMinor
                                                  )
                            )
                         )
            Diam = diam_major_pipe(FlowRate, HLFricNew, Length, Nu, PipeRough
                                   )
            err = abs(Diam - DiamPrev) / ((Diam + DiamPrev) / 2)
    return Diam.to(u.m)


@ut.list_handler()
def pipe_ID(FlowRate, Pressure):
    """Return the inner diameter of a pipe for a given pressure
    recovery constraint.

    :param FlowRate: flow rate of pipe
    :type FlowRate: u.m**3/u.s
    :param Pressure: pressure recovery constraint
    :type Pressure: u.m

    :return: inner diameter of pipe
    :rtype: u.m
    """
    ut.check_range([FlowRate.magnitude, ">0", "Flow rate"],
                   [Pressure.magnitude, ">0", "Pressure"])
    return np.sqrt(FlowRate/((np.pi/4)*np.sqrt(2*u.gravity*Pressure))).to(u.m)

############################ Weirs ############################


@ut.list_handler()
def width_rect_weir(FlowRate, Height):
    """
    .. deprecated::
        `width_rect_weir` is deprecated; use `width_weir_rect` instead.
    """
    warnings.warn('width_rect_weir is deprecated; use '
                  'width_weir_rect instead.', UserWarning)
    return width_weir_rect(FlowRate, Height)


@ut.list_handler()
def width_weir_rect(FlowRate, Height):
    """Return the width of a rectangular weir given its flow rate and the
    height of the water above the weir. For a weir that is a vertical pipe,
    this value is the circumference.

    :param FlowRate: flow rate over weir
    :type FlowRate: u.m**3/u.s
    :param Height: height of water above weir
    :type Height: u.m

    :return: width of weir
    :rtypes: u.m
    """
    ut.check_range([FlowRate.magnitude, ">0", "Flow rate"],
                   [Height.magnitude, ">0", "Height"])
    return ((3 / 2) * FlowRate / (con.VC_ORIFICE_RATIO
                                  * np.sqrt(2 * u.gravity) * Height ** (3 / 2))
            ).to(u.m)


@ut.list_handler()
def headloss_weir(FlowRate, Width):
    """
    .. deprecated::
        `headloss_weir` is deprecated; use `headloss_weir_rect` instead.
    """
    warnings.warn('headloss_weir is deprecated; use '
                  'headloss_weir_rect instead.', UserWarning)
    return headloss_weir_rect(FlowRate, Width)


@ut.list_handler()
def headloss_weir_rect(FlowRate, Width):
    """Return the head loss of a rectangular or vertical pipe weir.

    Head loss for a weir is the difference in height between the water
    upstream of the weir and the top of the weir.

    :param FlowRate: flow rate over weir
    :type FlowRate: u.m**3/u.s
    :param Width: width of weir (circumference for a vertical pipe)
    :type Width: u.m

    :return: head loss of weir
    :rtypes: u.m
    """
    ut.check_range([FlowRate.magnitude, ">0", "Flow rate"],
                   [Width.magnitude, ">0", "Width"])
    return ((((3/2) * FlowRate
              / (con.VC_ORIFICE_RATIO * np.sqrt(2 * u.gravity) * Width)
              ) ** 2).to(u.m**3)) ** (1/3)


@ut.list_handler()
def flow_rect_weir(Height, Width):
    """
    .. deprecated::
        `flow_rect_weir` is deprecated; use `flow_weir_rect` instead.
    """
    warnings.warn('flow_rect_weir is deprecated; use '
                  'flow_weir_rect instead.', UserWarning)
    return flow_weir_rect(Height, Width)


@ut.list_handler()
def flow_weir_rect(Height, Width):
    """Return the flow rate of a rectangular or vertical pipe weir.

    :param Height: height of water above weir
    :type Height: u.m
    :param Width: width of weir (circumference for a vertical pipe)
    :type Width: u.m

    :return: flow of weir
    :rtype: u.m**3/u.s
    """
    ut.check_range([Height.magnitude, ">0", "Height"],
                   [Width.magnitude, ">0", "Width"])
    return ((2/3) * con.VC_ORIFICE_RATIO
            * (np.sqrt(2*u.gravity) * Height**(3/2))
            * Width).to(u.m**3/u.s)

######################## Porous Media ########################

class DeprecatedFunctionError(Exception):
    def __init__(self, message):
        self.message = message

@ut.list_handler()
def headloss_kozeny(Length, DiamMedia=None, ApproachVel=None, Porosity=None, Nu=None, *, Diam=None, Vel=None):
    """
    .. deprecated::
        `headloss_kozeny` is deprecated; use `headloss_ergun` instead.
    """
    raise DeprecatedFunctionError("This function is deprecated. Please use headloss_ergun.")


@ut.list_handler()
def re_ergun(ApproachVel, DiamMedia, Temperature, Porosity):
    """Return the Reynolds number for flow through porous media.

    :param ApproachVel: approach velocity or superficial fluid velocity
    :type ApproachVel: u.m/u.s
    :param DiamMedia: particle diameter
    :type DiamMedia: u.m
    :param Temperature: temperature of porous medium
    :type Temperature: u.degK
    :param Porosity: porosity of porous medium
    :type Porosity: u.dimensionless or unitless

    :return: Reynolds number for flow through porous media
    :rtype: u.dimensionless
    """
    ut.check_range([ApproachVel.magnitude, ">0", "ApproachVel"],
                   [DiamMedia.magnitude, ">0", "DiamMedia"],
                   [Porosity, "0-1", "Porosity"])
    return (ApproachVel * DiamMedia /
            (viscosity_kinematic_water(Temperature)
             * (1 - Porosity))).to(u.dimensionless)


@ut.list_handler()
def fric_ergun(ApproachVel, DiamMedia, Temperature, Porosity):
    """Return the friction factor for flow through porous media.

    :param ApproachVel: superficial fluid velocity (VelSuperficial?)
    :type ApproachVel: u.m/u.s
    :param DiamMedia: particle diameter
    :type DiamMedia: u.m
    :param Temperature: temperature of porous medium
    :type Temperature: u.degK
    :param Porosity: porosity of porous medium
    :type Porosity: u.dimensionless or unitless

    :return: friction factor for flow through porous media
    :rtype: u.dimensionless
    """
    return (300 / re_ergun(ApproachVel, DiamMedia, Temperature, Porosity)
            + 3.5 * u.dimensionless)


@ut.list_handler()
def headloss_ergun(ApproachVel, DiamMedia, Temperature, Porosity, Length):
    """Return the frictional head loss for flow through porous media.

    :param ApproachVel: superficial fluid velocity (VelSuperficial?)
    :type ApproachVel: u.m/u.s
    :param DiamMedia: particle diameter
    :type DiamMedia: u.m
    :param Temperature: temperature of porous medium
    :type Temperature: u.degK
    :param Porosity: porosity of porous medium
    :type Porosity: u.dimensionless or unitless
    :param Length: length of pipe or duct
    :type Length: u.m

    :return: frictional head loss for flow through porous media
    :rtype: u.m
    """
    return (fric_ergun(ApproachVel, DiamMedia, Temperature, Porosity)
            * Length / DiamMedia * ApproachVel**2 / (2*u.gravity) * (1-Porosity)
            / Porosity**3).to(u.m)


@ut.list_handler()
def g_cs_ergun(ApproachVel, DiamMedia, Temperature, Porosity):
    """Camp Stein velocity gradient for flow through porous media.

    :param ApproachVel: superficial fluid velocity (VelSuperficial?)
    :type ApproachVel: u.m/u.s
    :param DiamMedia: particle diameter
    :type DiamMedia: u.m
    :param Temperature: temperature of porous medium
    :type Temperature: u.degK
    :param Porosity: porosity of porous medium
    :type Porosity: u.dimensionless or unitless

    :return: Camp Stein velocity gradient for flow through porous media
    :rtype: u.Hz
    """
    return np.sqrt(fric_ergun(ApproachVel, DiamMedia, Temperature, Porosity)
                   * ApproachVel**3 * (1-Porosity)
                   / (2 * viscosity_kinematic_water(Temperature) * DiamMedia
                      * Porosity**4)).to(u.Hz)

######################## Miscellaneous ########################


@ut.list_handler()
def height_water_critical(FlowRate, Width):
    """Return the critical local water height.

    :param FlowRate: flow rate of water
    :type FlowRate: u.m**3/u.s
    :param Width: width of channel (????????)
    :type Width: u.m

    :return: critical water height
    :rtype: u.m
    """
    ut.check_range([FlowRate.magnitude, ">0", "Flow rate"],
                   [Width.magnitude, ">0", "Width"])
    return ((FlowRate / (Width * np.sqrt(1*u.gravity))) ** (2/3)).to(u.m)


@ut.list_handler()
def vel_horizontal(HeightWaterCritical):
    """Return the horizontal velocity. (at the critical water depth??????)

    :param HeightWaterCritical: critical water height
    :type HeightWaterCritical: u.m

    :return: horizontal velocity
    :rtype: u.m/u.s
    """
    ut.check_range([HeightWaterCritical.magnitude, ">0", "Critical height of water"])
    return np.sqrt(u.gravity * HeightWaterCritical).to(u.m/u.s)


@ut.list_handler()
def manifold_id_alt(q, pr_max):
    """Return the inner diameter of a manifold when major losses are
    negligible.
    """
    manifold_id_alt = np.sqrt(
        4 * q / (
            np.pi * np.sqrt(
                2 * u.gravity * pr_max
            )
        )
    )
    return manifold_id_alt


@ut.list_handler()
def manifold_id(q, h, l, q_ratio, nu, eps, k, n):
    id_new = 2 * u.inch
    id_old = 0 * u.inch
    error = 1
    while error > 0.01:
        id_old = id_new
        id_new = (
            ((8 * q ** 2) / (u.gravity * np.pi ** 2 * h)) *
            (
                (
                    1 + fric_pipe(q, id_old, nu, eps) *
                    (1 / 3 + 1 / (2 * n) + 1 / (6 * n ** 2))
                ) /
                (1 - q_ratio ** 2)
            )
        ) ** (1 / 4)
        error = np.abs(id_old - id_new) / id_new
    return id_new


@ut.list_handler()
def manifold_nd(q, h, l, q_ratio, nu, eps, k, n, sdr):
    manifold_nd = pipe.ND_SDR_available(
            manifold_id(q, h, l, q_ratio, nu, eps, k, n),
            sdr
        )
    return manifold_nd


@ut.list_handler()
def horiz_chan_w(q, depth, hl, l, nu, eps, manifold, k):
    hl = min(hl, depth / 3)
    horiz_chan_w_new = q / ((depth - hl) * np.sqrt(2 * u.gravity * hl))

    error = 1
    i = 0
    while error > 0.001 and i < 20:
        w = horiz_chan_w_new
        i = i + 1
        horiz_chan_w_new = np.sqrt(
            (
                1 + k +
                    fric_rect(q, w, depth - hl, nu, eps, True) *
                    (l / (4 * radius_hydraulic_rect(w, depth - hl, True))) *
                    (1 - (2 * (int(manifold) / 3)))
            ) / (2 * u.gravity * hl)
        ) * (q / (depth - hl))
        error = np.abs(horiz_chan_w_new - w) / (horiz_chan_w_new + w)
    return horiz_chan_w_new.to(u.m)


@ut.list_handler()
def horiz_chan_h(q, w, hl, l, nu, eps, manifold):
    h_new = (q / (w * np.sqrt(2 * u.gravity * hl))) + hl
    error = 1
    i = 0
    while error > 0.001 and i < 200:
        h = h_new
        hl_local = min(hl, h / 3)
        i = i + 1
        h_new = (q/ w) * np.sqrt((1 + \
            fric_rect(q, w, h - hl_local, nu, eps, True) * (l / (4 * \
                radius_hydraulic_rect(w, h - hl_local, True))) * (1 - 2 * (int(manifold) / 3))
        )/ (2 * u.gravity * hl_local)) + (hl_local)
        error = np.abs(h_new - h) / (h_new + h)
    return h_new.to(u.m)


@ut.list_handler()
def pipe_flow_nd(q, sdr, hl, l, nu, eps, k):
    i = 0
    id_sdr_all_available = pipe.ID_SDR_all_available(sdr)
    while q > flow_pipe(id_sdr_all_available[i], hl, l, nu, eps, k):
        i_d = id_sdr_all_available[i]
        i += 1
    return pipe.ND_SDR_available(i_d, sdr)
