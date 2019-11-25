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
    .. deprecated:: 0.1.13
        `density_air` is deprecated; use `density_gas` instead.
    """
    warnings.warn('density_air is deprecated; use density_gas instead.',
                  FutureWarning)
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
    .. deprecated:: 0.1.13
        `viscosity_dynamic` is deprecated; use `viscosity_dynamic_water`
        instead.
    """
    warnings.warn('viscosity_dynamic is deprecated; use '
                  'viscosity_dynamic_water instead.', FutureWarning)
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
    """
    .. deprecated:: 0.1.13
        `viscosity_kinematic` is deprecated; use `viscosity_kinematic_water`
        instead.
    """
    warnings.warn('viscosity_kinematic is deprecated; use '
                  'viscosity_kinematic_water instead.', FutureWarning)
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
    .. deprecated:: 0.1.13
        `radius_hydraulic` is deprecated; use `radius_hydraulic_rect` instead.
    """
    warnings.warn('radius_hydraulic is deprecated; use radius_hydraulic_rect '
                  'instead.', FutureWarning)
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
                   [OpenChannel, "boolean", "openchannel"])
    if OpenChannel:
        return (Width*Depth) / (Width + 2*Depth)
    else:
        return (Width*Depth) / (2 * (Width+Depth))


@ut.list_handler()
def radius_hydraulic_general(Area, PerimWetted):
    """
    .. deprecated:: 0.1.13
        `radius_hydraulic_general` is deprecated; use
        `radius_hydraulic_channel` instead.
    """
    warnings.warn('radius_hydraulic_general is deprecated; use '
                  'radius_hydraulic_channel instead.', FutureWarning)
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
    return Area / PerimWetted

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
    return ((4 * FlowRate) / (np.pi * Diam * Nu))


@ut.list_handler()
def re_rect(FlowRate, Width, Depth, Nu, openchannel):
    """Return the Reynolds number of flow through a rectangular channel.

    :param FlowRate: flow rate through channel
    :type FlowRate: u.m**3/u.s
    :param Width: width of channel
    :type Width: u.m
    :param Depth: depth of water in channel
    :type Depth: u.m
    :param Nu: kinematic viscosity of fluid
    :type Nu: u.m**2/u.s
    :param openchannel: true if channel is open, false if closed
    :type openchannel: boolean

    :return: Reynolds number of flow through rectangular channel
    :rtype: u.dimensionless
    """
    ut.check_range([FlowRate.magnitude, ">0", "Flow rate"],
                   [Nu.magnitude, ">0", "Nu"])
    return (4 * FlowRate * radius_hydraulic_rect(Width, Depth, openchannel)
            / (Width * Depth * Nu))


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

########################### Friction ###########################


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
def fric_rect(FlowRate, Width, Depth, Nu, PipeRough, openchannel):
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
    :param PipeRough: roughness of channel
    :type PipeRough: u.m
    :param openchannel: true if channel is open, false if closed
    :type openchannel: boolean

    :return: friction factor of flow through rectangular channel
    :rtype: u.dimensionless
    """
    ut.check_range([PipeRough.magnitude, "0-1", "Pipe roughness"])
    if re_rect(FlowRate, Width, Depth, Nu, openchannel) >= RE_TRANSITION_PIPE:
        # Diam = 4*R_h in adapted Swamee-Jain equation
        return (0.25 * u.dimensionless
                / (np.log10((PipeRough
                             / (3.7 * 4
                                * radius_hydraulic_rect(Width, Depth,
                                                   openchannel)
                                )
                             )
                            + (5.74 / (re_rect(FlowRate, Width, Depth,
                                               Nu, openchannel) ** 0.9)
                               )
                            )
                   ) ** 2
                )
    else:
        return 64 * u.dimensionless / re_rect(FlowRate, Width, Depth, Nu,
                                              openchannel)


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
    :param PipeRough: roughness of channel
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

######################### Head Loss #########################


@ut.list_handler()
def headloss_fric(FlowRate, Diam, Length, Nu, PipeRough):
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
    :param PipeRough: roughness of pipe
    :type PipeRough: u.m

    :return: major head loss in pipe
    :rtype: u.m
    """
    ut.check_range([Length.magnitude, ">0", "Length"])
    return (fric(FlowRate, Diam, Nu, PipeRough)
            * 8 / (u.gravity * np.pi**2)
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
    return KMinor * 8 / (u.gravity * np.pi**2) * FlowRate**2 / Diam**4


@ut.list_handler()
def headloss(FlowRate, Diam, Length, Nu, PipeRough, KMinor):
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
    :param PipeRough: roughness of pipe
    :type PipeRough: u.m
    :param KMinor: minor loss coefficient
    :type KMinor: u.dimensionless or unitless

    :return: total head loss in pipe
    :rtype: u.m
    """
    return (headloss_fric(FlowRate, Diam, Length, Nu, PipeRough)
            + headloss_exp(FlowRate, Diam, KMinor))


@ut.list_handler()
def headloss_fric_rect(FlowRate, Width, Depth, Length, Nu, PipeRough, openchannel):
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
    :param PipeRough: roughness of channel
    :type PipeRough: u.m
    :param openchannel: true if channel is open, false if closed
    :type openchannel: boolean

    :return: major head loss in rectangular channel
    :rtype: u.m
    """
    ut.check_range([Length.magnitude, ">0", "Length"])
    return (fric_rect(FlowRate, Width, Depth, Nu,
                      PipeRough, openchannel)
            * Length
            / (4 * radius_hydraulic_rect(Width, Depth, openchannel))
            * FlowRate**2
            / (2 * u.gravity * (Width*Depth)**2)
            )


@ut.list_handler()
def headloss_exp_rect(FlowRate, Width, Depth, KMinor):
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
            )


@ut.list_handler()
def headloss_rect(FlowRate, Width, Depth, Length,
                  KMinor, Nu, PipeRough, openchannel):
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
    :param PipeRough: roughness of channel
    :type PipeRough: u.m
    :param openchannel: true if channel is open, false if closed
    :type openchannel: boolean

    :return: total head loss in rectangular channel
    :rtype: u.m
    """
    return (headloss_exp_rect(FlowRate, Width, Depth, KMinor)
            + headloss_fric_rect(FlowRate, Width, Depth, Length,
                                 Nu, PipeRough, openchannel))


@ut.list_handler()
def headloss_fric_general(Area, PerimWetted, Vel, Length, Nu, PipeRough):
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
    :param PipeRough: roughness of channel
    :type PipeRough: u.m

    :return: major head loss in general channel
    :rtype: u.m
    """
    ut.check_range([Length.magnitude, ">0", "Length"])
    return (fric_general(Area, PerimWetted, Vel, Nu, PipeRough) * Length
            / (4 * radius_hydraulic_general(Area, PerimWetted))
            * Vel**2 / (2*u.gravity)
            )


@ut.list_handler()
def headloss_exp_general(Vel, KMinor):
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
    return KMinor * Vel**2 / (2*u.gravity)


@ut.list_handler()
def headloss_gen(Area, Vel, PerimWetted, Length, KMinor, Nu, PipeRough):
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
    :param PipeRough: roughness of channel
    :type PipeRough: u.m

    :return: total head loss in general channel
    :rtype: u.m
    """
    return (headloss_exp_general(Vel, KMinor)
            + headloss_fric_general(Area, PerimWetted, Vel,
                                    Length, Nu, PipeRough)).to(u.m)


@ut.list_handler()
def headloss_manifold(FlowRate, Diam, Length, KMinor, Nu, PipeRough, NumOutlets):
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
    :param PipeRough: roughness of manifold
    :type PipeRough: u.m
    :param NumOutlets: number of outlets from manifold

    :return: total headloss through manifold
    :rtype: u.m
    """
    ut.check_range([NumOutlets, ">0, int", 'Number of outlets'])
    return (headloss(FlowRate, Diam, Length, Nu, PipeRough, KMinor)
            * ((1/3)
               + (1 / (2*NumOutlets))
               + (1 / (6*NumOutlets**2))
               )
            ).to(u.m)


def elbow_minor_loss(q, id_, k):
    vel = q / area_circle(id_)
    minor_loss = k * vel ** 2 / (2 * u.gravity)
    return minor_loss.to(u.m)

######################### Orifices #########################


@ut.list_handler()
def flow_orifice(Diam, Height, RatioVCOrifice):
    """Return the flow rate of the orifice.

    :param Diam: diameter of orifice
    :type Diam: u.m
    :param Height: height of orifice
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
                * np.sqrt(2 * u.gravity * Height))
    else:
        return 0 * u.m**3/u.s


@ut.list_handler()
def flow_orifice_vert(Diam, Height, RatioVCOrifice):
    """Return the vertical flow rate of the orifice.

    :param Diam: diameter of orifice
    :type Diam: u.m
    :param Height: height of orifice
    :type Height: u.m
    :param RatioVCOrifice: vena contracta ratio of orifice
    :type RatioVCOrifice: u.dimensionless or unitless

    :return: vertical flow rate of orifice
    :rtype: u.m**3/u.s
    """
    ut.check_range([RatioVCOrifice, "0-1", "VC orifice ratio"])
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
    """Return the head of the orifice.

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
            )


@ut.list_handler()
def area_orifice(Height, RatioVCOrifice, FlowRate):
    """Return the area of the orifice.

    :param Height: height of orifice
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
    return np.pi * Diam * RE_TRANSITION_PIPE * Nu / 4


@ut.list_handler()
def flow_hagen(Diam, HeadLossFric, Length, Nu):
    """Return the flow rate for laminar flow with only major losses.

    :param Diam: diameter of pipe
    :type Diam: u.m
    :param HeadLossFric: head loss due to friction
    :type HeadLossFric: u.m
    :param Length: length of pipe
    :type Length: u.m
    :param Nu: kinematic viscosity of fluid
    :type Nu: u.m**2/u.s

    :return: flow rate for laminar flow with only major losses
    :rtype: u.m**3/u.s
    """
    ut.check_range([Diam.magnitude, ">0", "Diameter"],
                   [Length.magnitude, ">0", "Length"],
                   [HeadLossFric.magnitude, ">=0", "Headloss due to friction"],
                   [Nu.magnitude, ">0", "Nu"])
    return ((np.pi*Diam**4) / (128*Nu) * u.gravity * HeadLossFric
            / Length).to(u.m**3/u.s)


@ut.list_handler()
def flow_swamee(Diam, HeadLossFric, Length, Nu, PipeRough):
    """Return the flow rate for turbulent flow with only major losses.

    :param Diam: diameter of pipe
    :type Diam: u.m
    :param HeadLossFric: head loss due to friction
    :type HeadLossFric: u.m
    :param Length: length of pipe
    :type Length: u.m
    :param Nu: kinematic viscosity of fluid
    :type Nu: u.m**2/u.s
    :param PipeRough: roughness of pipe
    :type PipeRough: u.m

    :return: flow rate for turbulent flow with only major losses
    :rtype: u.m**3/u.s
    """
    ut.check_range([Diam.magnitude, ">0", "Diameter"],
                   [Length.magnitude, ">0", "Length"],
                   [HeadLossFric.magnitude, ">0", "Headloss due to friction"],
                   [Nu.magnitude, ">0", "Nu"],
                   [PipeRough.magnitude, "0-1", "Pipe roughness"])
    logterm = np.log10(PipeRough / (3.7 * Diam)
                       + 2.51 * Nu * np.sqrt(Length / (2 * u.gravity
                                                       * HeadLossFric
                                                       * Diam**3)
                                             )
                       )
    return ((-np.pi / np.sqrt(2)) * Diam**(5/2) * logterm
            * np.sqrt(u.gravity * HeadLossFric / Length)
            ).to(u.m**3/u.s)


@ut.list_handler()
def flow_pipemajor(Diam, HeadLossFric, Length, Nu, PipeRough):
    """Return the flow rate with only major losses.

    This function applies to both laminar and turbulent flows.

    :param Diam: diameter of pipe
    :type Diam: u.m
    :param HeadLossFric: head loss due to friction
    :type HeadLossFric: u.m
    :param Length: length of pipe
    :type Length: u.m
    :param Nu: kinematic viscosity of fluid
    :type Nu: u.m**2/u.s
    :param PipeRough: roughness of pipe
    :type PipeRough: u.m

    :return: flow rate with only major losses
    :rtype: u.m**3/u.s
    """
    FlowHagen = flow_hagen(Diam, HeadLossFric, Length, Nu)
    if FlowHagen < flow_transition(Diam, Nu):
        return FlowHagen
    else:
        return flow_swamee(Diam, HeadLossFric, Length, Nu, PipeRough)


@ut.list_handler()
def flow_pipeminor(Diam, HeadLossExpans, KMinor):
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
    ut.check_range([HeadLossExpans.magnitude, ">=0",
                    "Headloss due to expansion"],
                   [KMinor, ">0", "K minor"])
    return (area_circle(Diam) * np.sqrt(2 * u.gravity * HeadLossExpans
                                        / KMinor)
            ).to(u.m**3/u.s)


@ut.list_handler()
def flow_pipe(Diam, HeadLoss, Length, Nu, PipeRough, KMinor):
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
    :param PipeRough: roughness of pipe
    :type PipeRough: u.m
    :param KMinor: minor loss coefficient
    :type KMinor: u.dimensionless or unitless

    :return: flow rate in pipe
    :rtype: u.m**3/u.s
    """
    if KMinor == 0:
        FlowRate = flow_pipemajor(Diam, HeadLoss, Length, Nu,
                                  PipeRough)
    else:
        FlowRatePrev = 0
        err = 1.0
        FlowRate = min(flow_pipemajor(Diam, HeadLoss, Length,
                                      Nu, PipeRough),
                       flow_pipeminor(Diam, HeadLoss, KMinor)
                       )
        while err > 0.01:
            FlowRatePrev = FlowRate
            HLFricNew = (HeadLoss * headloss_fric(FlowRate, Diam, Length,
                                                  Nu, PipeRough)
                         / (headloss_fric(FlowRate, Diam, Length,
                                          Nu, PipeRough)
                            + headloss_exp(FlowRate, Diam, KMinor)
                            )
                         )
            FlowRate = flow_pipemajor(Diam, HLFricNew, Length,
                                      Nu, PipeRough)
            if FlowRate == 0:
                err = 0.0
            else:
                err = (abs(FlowRate - FlowRatePrev)
                       / ((FlowRate + FlowRatePrev) / 2)
                       )
    return FlowRate

########################## Diameters ##########################


@ut.list_handler()
def diam_hagen(FlowRate, HeadLossFric, Length, Nu):
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

    :return: inner diameter of pipe
    :rtype: u.m
    """
    ut.check_range([FlowRate.magnitude, ">0", "Flow rate"],
                   [Length.magnitude, ">0", "Length"],
                   [HeadLossFric.magnitude, ">0", "Headloss due to friction"],
                   [Nu.magnitude, ">0", "Nu"])
    return (((128 * Nu * FlowRate * Length)
             / (u.gravity * HeadLossFric * np.pi)
             ) ** (1/4)).to(u.m)


@ut.list_handler()
def diam_swamee(FlowRate, HeadLossFric, Length, Nu, PipeRough):
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

    :return: inner diameter of pipe
    :rtype: u.m
    """
    ut.check_range([FlowRate.magnitude, ">0", "Flow rate"],
                   [Length.magnitude, ">0", "Length"],
                   [HeadLossFric.magnitude, ">0", "Headloss due to friction"],
                   [Nu.magnitude, ">0", "Nu"],
                   [PipeRough.magnitude, "0-1", "Pipe roughness"])
    a = ((PipeRough ** 1.25)
         * ((Length * FlowRate**2)
            / (u.gravity * HeadLossFric)
            )**4.75
         ).to_base_units()
    b = (Nu**5 * FlowRate**47
         * (Length / (u.gravity * HeadLossFric)) ** 26
         ).to_base_units()**0.2
    return 0.66 * (a+b)**0.04


@ut.list_handler()
def diam_pipemajor(FlowRate, HeadLossFric, Length, Nu, PipeRough):
    """Return the pipe inner diameter that would result in given major losses.

    This function applies to both laminar and turbulent flow.

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

    :return: inner diameter of pipe
    :rtype: u.m
    """
    DiamLaminar = diam_hagen(FlowRate, HeadLossFric, Length, Nu)
    if re_pipe(FlowRate, DiamLaminar, Nu) <= RE_TRANSITION_PIPE:
        return DiamLaminar
    else:
        return diam_swamee(FlowRate, HeadLossFric, Length,
                           Nu, PipeRough)


@ut.list_handler()
def diam_pipeminor(FlowRate, HeadLossExpans, KMinor):
    """Return the pipe inner diameter that would result in the given minor losses.

    This function applies to both laminar and turbulent flow.

    :param FlowRate: flow rate of pipe
    :type FlowRate: u.m**3/u.s
    :param HeadLossExpans: head loss due to expansion
    :type HeadLossExpans: u.m
    :param KMinor: minor loss coefficient
    :type KMinor: u.dimensionless or unitless

    :return: inner diameter of pipe
    :rtype: u.m
    """
    ut.check_range([FlowRate.magnitude, ">0", "Flow rate"],
                   [KMinor, ">=0", "K minor"],
                   [HeadLossExpans.magnitude, ">0", "Headloss due to expansion"])
    return (np.sqrt(4 * FlowRate / np.pi)
            * (KMinor / (2 * u.gravity * HeadLossExpans)) ** (1/4)
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
        Diam = diam_pipemajor(FlowRate, HeadLoss, Length, Nu,
                              PipeRough)
    else:
        Diam = max(diam_pipemajor(FlowRate, HeadLoss,
                                  Length, Nu, PipeRough),
                   diam_pipeminor(FlowRate, HeadLoss, KMinor))
        err = 1.00
        while err > 0.001:
            DiamPrev = Diam
            HLFricNew = (HeadLoss * headloss_fric(FlowRate, Diam, Length,
                                                  Nu, PipeRough
                                                  )
                         / (headloss_fric(FlowRate, Diam, Length,
                                          Nu, PipeRough
                                          )
                                          + headloss_exp(FlowRate,
                                                         Diam, KMinor
                                                         )
                            )
                         )
            Diam = diam_pipemajor(FlowRate, HLFricNew, Length, Nu, PipeRough
                                  )
            err = abs(Diam - DiamPrev) / ((Diam + DiamPrev) / 2)
    return Diam


def pipe_ID(FlowRate, Pressure):
    """Return the inner diameter of a pipe for a given pressure
    recovery constraint.

    :param FlowRate: flow rate of pipe
    :type FlowRate: u.m**3/u.s
    :param Pressure: pressure recovery constraint (???????)
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
    """Return the width of a rectangular weir given its flow rate and the
    height of the water above the weir.

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


# For a pipe, Width is the circumference of the pipe.
# Head loss for a weir is the difference in height between the water
# upstream of the weir and the top of the weir.
# @u.wraps(u.m, [u.m**3/u.s, u.m], False)
@ut.list_handler()
def headloss_weir(FlowRate, Width):
    """Return the head loss of a weir.

    Head loss for a weir is the difference in height between the water
    upstream of the weir and the top of the weir.

    :param FlowRate: flow rate over weir
    :type FlowRate: u.m**3/u.s
    :param Width: width of weir or circumference of vertical pipe (length???)
    :type Width: u.m

    :return: head loss of weir
    :rtypes: u.m
    """
    ut.check_range([FlowRate.magnitude, ">0", "Flow rate"],
                   [Width.magnitude, ">0", "Width"])
    return (((3/2) * FlowRate
             / (con.VC_ORIFICE_RATIO * np.sqrt(2 * u.gravity) * Width)
             ) ** (2/3)).to(u.m)


@ut.list_handler()
def flow_rect_weir(Height, Width):
    """Return the flow of a rectangular weir.

    :param Height: height of water above weir
    :type Height: u.m
    :param Width: width of weir
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


@ut.list_handler()
def headloss_kozeny(Length, Diam, Vel, Porosity, Nu):
    """Return the Carman Kozeny sand bed head loss.

    :param Length: height of bed (call Height instead ????)
    :type Length: u.m
    :param Diam: diameter of sand particle (DiamParticle????)
    :type Diam: u.m
    :param Vel: superficial velocity (ApproachVel????)
    :type Vel: u.m/u.s
    :param Porosity: porosity of bed
    :type Porosity: u.dimensionless or unitless
    :param Nu: kinematic viscosity of fluid
    :type Nu: u.m**2/u.s

    :return: head loss in sand bed
    :rtype: u.m
    """
    ut.check_range([Length.magnitude, ">0", "Length"],
                   [Diam.magnitude, ">0", "Diam"],
                   [Vel.magnitude, ">0", "Velocity"],
                   [Nu.magnitude, ">0", "Nu"],
                   [Porosity, "0-1", "Porosity"])
    return (con.K_KOZENY * Length * Nu
            / u.gravity * (1-Porosity)**2
            / Porosity**3 * 36 * Vel
            / Diam ** 2).to(u.m)


@ut.list_handler()
def re_ergun(ApproachVel, DiamParticle, Temperature, Porosity):
    """Return the Reynolds number for flow through porous media.

    :param ApproachVel: approach velocity or superficial fluid velocity
    :type ApproachVel: u.m/u.s
    :param DiamParticle: particle diameter
    :type DiamParticle: u.m
    :param Temperature: temperature of porous medium
    :type Temperature: u.degK
    :param Porosity: porosity of porous medium
    :type Porosity: u.dimensionless or unitless

    :return: Reynolds number for flow through porous media
    :rtype: u.dimensionless
    """
    ut.check_range([ApproachVel.magnitude, ">0", "ApproachVel"],
                   [DiamParticle.magnitude, ">0", "DiamParticle"],
                   [Porosity, "0-1", "Porosity"])
    return (ApproachVel * DiamParticle /
            (viscosity_kinematic(Temperature) * (1 - Porosity)))


@ut.list_handler()
def fric_ergun(ApproachVel, DiamParticle, Temperature, Porosity):
    """Return the friction factor for flow through porous media.

    :param ApproachVel: superficial fluid velocity (VelSuperficial?)
    :type ApproachVel: u.m/u.s
    :param DiamParticle: particle diameter
    :type DiamParticle: u.m
    :param Temperature: temperature of porous medium
    :type Temperature: u.degK
    :param Porosity: porosity of porous medium
    :type Porosity: u.dimensionless or unitless

    :return: friction factor for flow through porous media
    :rtype: u.dimensionless
    """
    return (300 / re_ergun(ApproachVel, DiamParticle, Temperature, Porosity)
            + 3.5 * u.dimensionless)


@ut.list_handler()
def headloss_ergun(ApproachVel, DiamParticle, Temperature, Porosity, Length):
    """Return the frictional head loss for flow through porous media.

    :param ApproachVel: superficial fluid velocity (VelSuperficial?)
    :type ApproachVel: u.m/u.s
    :param DiamParticle: particle diameter (DiamParticle?)
    :type DiamParticle: u.m
    :param Temperature: temperature of porous medium
    :type Temperature: u.degK
    :param Porosity: porosity of porous medium
    :type Porosity: u.dimensionless or unitless
    :param Length: length of pipe or duct
    :type Length: u.m

    :return: frictional head loss for flow through porous media
    :rtype: u.m
    """
    return (fric_ergun(ApproachVel, DiamParticle, Temperature, Porosity)
            * Length / DiamParticle * ApproachVel**2 / (2*u.gravity) * (1-Porosity)
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
    :type Porosity: u.dimensionless or unitless

    :return: Camp Stein velocity gradient for flow through porous media
    :rtype: u.Hz
    """
    return np.sqrt(fric_ergun(ApproachVel, DiamParticle, Temperature, Porosity)
                   * ApproachVel**3 * (1-Porosity)
                   / (2 * viscosity_kinematic(Temperature) * DiamParticle
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


def pipe_flow_nd(q, sdr, hl, l, nu, eps, k):
    i = 0
    id_sdr_all_available = pipe.ID_SDR_all_available(sdr)
    while q > flow_pipe(id_sdr_all_available[i], hl, l, nu, eps, k):
        i_d = id_sdr_all_available[i]
        i += 1
    return pipe.ND_SDR_available(i_d, sdr)
