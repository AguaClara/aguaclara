"""This file contains all the functions needed to design a flocculator for
an AguaClara plant.

"""
import numpy as np
from aide_design.shared.units import unit_registry as u
import aide_design.shared.physchem as pc
import aide_design.shared.constants as con


@u.wraps(1/u.s, [u.degK, u.m, None], False)
def G_avg(temp, hl, coll_pot):
    """Return the average velocity gradient of a flocculator given head
    loss, collision potential and temperature.

    Parameters
    ----------
    temp : float
        Design temperature

    hl : float
        Headloss through the flocculator

    coll_pot : int
        Desired collision potential in the flocculator

    Returns
    -------
    float
        average velocity gradient of a flocculator given head
        loss, collision potential and temperature.

    Examples
    --------
    >>> from aide_design.play import*
    >>> G_avg(15 * u.degC, 40*u.cm, 37000)
    <Quantity(93.24255814245437, '1 / second')>
    >>> G_avg(20 * u.degC, 40*u.cm, 37000)
    <Quantity(105.64226282862515, '1 / second')>

    """
    G = ((con.GRAVITY.magnitude * hl) /
         (coll_pot * pc.viscosity_kinematic(temp).magnitude))
    return G

@u.wraps(u.m**3, [u.m**3/u.s, u.degK, u.m, None], False)
def vol_floc(Q_plant, temp, hl, coll_pot):
    """Return the total volume of the flocculator using plant flow rate, head
    loss, collision potential and temperature.

    Uses an estimation of flocculator residence time (ignoring the decrease
    in water depth caused by head loss in the flocculator.) Volume does not take
    into account the extra volume that the flocculator will have due to changing
    water level caused by head loss.

    Parameters
    ----------
    Q_plant: float
        Flow through the plant

    temp: float
        Design temperature

    hl : float
        Headloss through the flocculator

    coll_pot : int
        Desired collision potential in the flocculator

    Returns
    -------
    float
        total volume of the flocculator given head
        loss, collision potential and temperature.

    Examples
    --------
    >>> from aide_design.play import*
    >>> vol_floc(40*u.L/u.s, 15*u.degC, 40*u.cm, 37000)
    <Quantity(15.872580391229524, 'meter ** 3')>
    >>> vol_floc(40*u.L/u.s, 20*u.degC, 40*u.cm, 37000)
    <Quantity(14.009544668698396, 'meter ** 3')>

    """
    try:
        vol = ((coll_pot / G_avg(temp, hl, coll_pot).magnitude)*Q_plant).magnitude
    except AttributeError:
        vol = (coll_pot / G_avg(temp, hl, coll_pot).magnitude)*Q_plant
    finally:
        return vol

@u.wraps(u.s, [u.m**3/u.s, u.degK, u.m, None], False)
def res_time(Q_plant, temp, hl, coll_pot):
    """Return the residence time of water in the flocculator using flow rate and
    volume.

    Parameters
    ----------
    Q_plant: float
        Flow through the plant

    temp: float
        Design temperature

    hl : float
        Headloss through the flocculator

    coll_pot : int
        Desired collision potential in the flocculator

    Returns
    -------
    float
        residence time of water in flocculator

    Examples
    --------
    >>> from aide_design.play import*
    >>> res_time(40*u.L/u.s, 15*u.degC, 40*u.cm, 37000)
    <Quantity(396.8145097807381, 'second')>

    """
    return vol_floc(Q_plant, temp, hl, coll_pot).magnitude/Q_plant

@u.wraps(u.m, [u.m**3/u.s, u.degK, u.m, u.m, None, None], False)
def width_HS_min(Q_plant, temp, depth_end, hl, coll_pot, ratio_HS_min=3):
    """Return the minimum channel width required to achieve H/S > 3.

    The channel can be wider than this, but this is the absolute minimum width
    for a channel. The minimum width occurs when there is only one expansion per
    baffle and thus the distance between expansions is the same as the depth of
    water at the end of the flocculator.

    Parameters
    ----------
    Q_plant : float
        Plant flow rate

    temp: float
        Design temperature

    depth_end: float
        The depth of water at the end of the flocculator

    hl : float
        Headloss through the flocculator

    coll_pot : int
        Desired collision potential in the flocculator

    ratio_HS_min : int
        Minimum allowable ratio between the water depth and edge to edge distance
        between baffles

    Returns
    -------
    float
        The minimum channel width required to achieve H/S > 3

    Examples
    --------
    >>> from aide_design.play import*
    >>> width_HS_min(20*u.L/u.s, 25*u.degC, 2*u.m, 40*u.cm, 37000)
    <Quantity(0.11026896890543642, 'meter')>
    >>> width_HS_min(40*u.L/u.s, 15*u.degC, 5*u.m, 40*u.cm, 37000, 3)
    <Quantity(0.07044662697031184, 'meter')>

    """
    nu = pc.viscosity_kinematic(temp).magnitude

    w = (ratio_HS_min *
         ((con.K_MINOR_FLOC_BAFFLE /
          (2 * depth_end * (G_avg(temp, hl, coll_pot).magnitude**2)
          * nu))**(1/3))*Q_plant/depth_end)
    return w

@u.wraps(u.cm, [u.m**3/u.s, u.degK, u.m, u.m, None, None], False)
def width_floc_min(Q_plant, temp, depth_end, hl, coll_pot, ratio_HS_min=3, W_min_construct=45*u.cm):
    """Return the minimum channel width required.

    This takes the maximum of the minimum required to achieve H/S > 3 and the
    minimum required for constructability based on the width of the human hip.

    Parameters
    ----------
    Q_plant : float
        Plant flow rate

    temp: float
        Design temperature

    depth_end: float
        The depth of water at the end of the flocculator

    hl : float
        Headloss through the flocculator

    coll_pot : int
        Desired collision potential in the flocculator

    ratio_HS_min : int
        Minimum allowable ratio between the water depth and edge to edge distance
        between baffles

    W_min_construct : float
        Minimum width of a flocculator channel based on the width of the human hip

    Returns
    -------
    float
        minimum channel width required.

    Examples
    --------
    >>> from aide_design.play import*
    >>> width_floc_min(20*u.L/u.s, 25*u.degC, 2*u.m, 40*u.cm, 37000)
    <Quantity(45, 'centimeter')>
    >>> width_floc_min(40*u.L/u.s, 15*u.degC, 2*u.m, 40*u.cm, 37000)
    <Quantity(45, 'centimeter')>
    """
    W_min_construct = W_min_construct.to(u.cm).magnitude
    return max(width_HS_min(Q_plant, temp, depth_end, hl, coll_pot, ratio_HS_min).to(u.cm).magnitude,
               W_min_construct)

@u.wraps(None, [u.m**3/u.s, u.degK, u.m, u.m, None, u.m, None], False)
def num_channel(Q_plant, temp, depth_end, hl, coll_pot, W_tot, ratio_HS_min=3, W_min_construct=45*u.cm):
    """Return the number of channels in the entrance tank/flocculator (ETF).

    This takes the total width of the flocculator and divides it by the minimum
    channel width. A floor function is used to ensure that there are an even
    number of channels.

    Parameters
    ----------
    Q_plant : float
        Plant flow rate

    temp: float
        Design temperature

    depth_end: float
        The depth of water at the end of the flocculator

    hl : float
        Headloss through the flocculator

    coll_pot : int
        Desired collision potential in the flocculator

    W_tot: float
        Total width

    ratio_HS_min : int
        Minimum allowable ratio between the water depth and edge to edge distance
        between baffles

    W_min_construct : float
        Minimum width of a flocculator channel based on the width of the human hip

    Returns
    -------
    int
        the number of channels in the entrance tank/flocculator (ETF)

    Examples
    --------
    >>> from aide_design.play import*
    >>> num_channel(20*u.L/u.s, 25*u.degC, 2*u.m, 40*u.cm, 37000, 5*u.m)
    10
    >>> num_channel(40*u.L/u.s, 15*u.degC, 4*u.m, 40*u.cm, 37000, 10*u.m, 3, 45*u.cm)
    22

    """
    num = W_tot/((width_floc_min(Q_plant, temp, depth_end, hl, coll_pot,
                                ratio_HS_min, W_min_construct)).to(u.m).magnitude)
    # floor function with step size 2
    num = np.floor(num/2)*2
    return int(max(num, 2))

@u.wraps(u.m**2, [u.m**3/u.s, u.degK, u.m, u.m, None, None], False)
def area_ent_tank(Q_plant, temp, depth_end, hl, coll_pot, ratio_HS_min=3,
                  W_min_construct=45*u.cm, L_sed=7.35*u.m, L_ent_tank_max=2.2*u.m):
    """Return the planview area of the entrance tank given plant flow rate,
    headloss, target collision potential, design temperature, and depth of
    water at the end of the flocculator.

    Parameters
    ----------
    Q_plant: float
        Plant flow rate

    temp: float
        Design temperature

    depth_end: float
        The depth of water at the end of the flocculator

    hl : float
        Headloss through the flocculator

    coll_pot : int
        Desired collision potential in the flocculator

    ratio_HS_min : int
        Minimum allowable ratio between the water depth and edge to edge distance
        between baffles

    W_min_construct : float
        Minimum width of a flocculator channel based on the width of the human hip

    L_sed : float
        The length of the sedimentation unit process, including tank length,
        inlet and exit channel width, inlet weir thickness, and tank wall thickness

    L_ent_tank_max : float
        The maximum length of the entrance tank

    Returns
    -------
    float
        The planview area of the entrance tank

    Examples
    --------
    >>> from aide_design.play import*
    >>> area_ent_tank(20*u.L/u.s, 25*u.degC, 2*u.m, 40*u.cm, 37000, 3, 45*u.cm, 7.35*u.m, 2.2*u.cm)
    <Quantity(1, 'meter ** 2')>
    >>> area_ent_tank(40*u.L/u.s, 15*u.degC, 2*u.m, 40*u.cm, 37000)
    <Quantity(1, 'meter ** 2')>
    """
    L_sed = L_sed.to(u.m)
    L_ent_tank_max = L_ent_tank_max.to(u.m)

    # guess the planview area before starting iteration
    A_new = 1*u.m**2
    A_ratio = 0

    while (A_ratio) > 1.01 and (A_ET_PV/A_new) < 0.99:
        A_ET_PV = A_new

        vol_floc = vol_floc(Q_plant, temp, hl, coll_pot)
        A_floc_PV = vol_floc/(depth_end + hl/2)
        A_ETF_PV = A_ET_PV + A_floc_PV

        W_min = width_floc_min(Q_plant, temp, depth_end, hl, coll_pot,
                               ratio_HS_min, W_min_construct).to(u.m)

        W_tot = A_ETF_PV / L_sed

        num_chan = num_channel(Q_plant, temp, depth_end, hl, coll_pot, W_tot,
                               ratio_HS_min, W_min_construct)
        W_chan = W_tot / num_chan

        A_new = L_ent_tank_max * W_chan

        A_ratio = A_new / A_ET_PV

    return A_new.magnitude

### Baffle calculations
@u.wraps(u.m, [u.m**3/u.s, u.degK, u.m, u.m, None, None], False)
def expansion_dist_max(Q_plant, temp, W_chan, hl, coll_pot, ratio_HS_max=6):
    """"Return the maximum distance between expansions for the largest
    allowable H/S ratio.

    Parameters
    ----------
    Q_plant: float
        Plant flow rate

    temp: float
        Design temperature

    W_chan: float
        Channel width

    hl : float
        Headloss through the flocculator

    coll_pot : int
        Desired collision potential in the flocculator

    ratio_HS_max : int
        Maximum allowable ratio between the water depth and edge to edge distance
        between baffles

    Returns
    -------
    float
        maximum distance between expansions for the largest
        allowable H/S ratio.

    Examples
    --------
    >>> from aide_design.play import*
    >>> expansion_dist_max(20*u.L/u.s, 15*u.degC, 0.45*u.m, 40*u.cm, 37000)
    <Quantity(1.244387877682417, 'meter')>
    >>> expansion_dist_max(40*u.L/u.s, 25*u.degC, 0.45*u.m, 40*u.cm, 37000)
    <Quantity(1.9701785617907324, 'meter')>

    """
    g_avg = G_avg(temp, hl, coll_pot).magnitude
    nu = pc.viscosity_kinematic(temp).magnitude
    term1 = (con.K_MINOR_FLOC_BAFFLE/(2 * (g_avg**2) * nu))**(1/4)
    term2 = (ratio_HS_max*Q_plant/W_chan)**(3/4)
    exp_dist_max = term1*term2
    return exp_dist_max

@u.wraps(None, [u.m**3/u.s, u.degK, u.m, u.m, u.m, None, None], False)
def num_expansions(Q_plant, temp, depth_end, W_chan, hl, coll_pot, ratio_HS_max=6):
    """"Return the minimum number of expansions per baffle space.

    Parameters
    ----------
    Q_plant: float
        Plant flow rate

    temp: float
        Design temperature

    depth_end: float
        The depth of water at the end of the flocculator

    W_chan: float
        Channel width

    hl : float
        Headloss through the flocculator

    coll_pot : int
        Desired collision potential in the flocculator

    ratio_HS_max : int
        Maximum allowable ratio between the water depth and edge to edge distance
        between baffles

    Returns
    -------
    int
        minimum number of expansions per baffle space

    Examples
    --------
    >>> from aide_design.play import*
    >>> num_expansions(20*u.L/u.s, 15*u.degC, 2*u.m, 0.45*u.m, 40*u.cm, 37000)
    2
    >>> num_expansions(40*u.L/u.s, 25*u.degC, 4*u.m, 0.45*u.m, 40*u.cm, 37000)
    3

    """
    return int(np.ceil(depth_end /
               (expansion_dist_max(Q_plant, temp, W_chan, hl, coll_pot, ratio_HS_max)).magnitude))


@u.wraps(u.m, [u.m**3/u.s, u.degK, u.m, u.m, u.m, None, None], False)
def height_exp(Q_plant, temp, depth_end, W_chan, hl, coll_pot, ratio_HS_max=6):
    """Return the actual distance between expansions given the integer
    requirement for the number of expansions per flocculator depth.

    Parameters
    ----------
    Q_plant: float
        Plant flow rate

    temp: float
        Design temperature

    depth_end: float
        The depth of water at the end of the flocculator

    W_chan: float
        Channel width

    hl : float
        Headloss through the flocculator

    coll_pot : int
        Desired collision potential in the flocculator

    ratio_HS_max : int
        Maximum allowable ratio between the water depth and edge to edge distance
        between baffles

    Returns
    -------
    float
        the actual distance between expansions

    Examples
    --------
    >>> from aide_design.play import*
    >>> height_exp(20*u.L/u.s, 15*u.degC, 2*u.m, 0.45*u.m, 40*u.cm, 37000)
    <Quantity(1.0, 'meter')>
    >>> height_exp(40*u.L/u.s, 25*u.degC, 4*u.m, 0.45*u.m, 40*u.cm, 37000)
    <Quantity(1.3333333333333333, 'meter')>

    """
    return depth_end / num_expansions(Q_plant, temp, depth_end, W_chan, hl,
                                      coll_pot, ratio_HS_max)

@u.wraps(u.m, [u.m**3/u.s, u.degK, u.m, u.m, None, None], False)
def baffle_spacing(Q_plant, temp, W_chan, hl, coll_pot, ratio_HS_max=6):
    """Return the spacing between baffles based on the target velocity gradient

    Parameters
    ----------
    Q_plant: float
        Plant flow rate

    temp: float
        Design temperature

    W_chan: float
        Channel width

    hl : float
        Headloss through the flocculator

    coll_pot : int
        Desired collision potential in the flocculator

    ratio_HS_max : int
        Maximum allowable ratio between the water depth and edge to edge distance
        between baffles

    Returns
    -------
    float
        the spacing between baffles

    Examples
    --------
    >>> from aide_design.play import *
    >>> baffle_spacing(40*u.L/u.s, 25*u.degC, 0.45*u.m, 40*u.cm, 37000)
    <Quantity(0.3283630936317887, 'meter')>
    >>> baffle_spacing(20*u.L/u.s, 15*u.degC, 0.45*u.m, 40*u.cm, 37000)
    <Quantity(0.2073979796137361, 'meter')>
    """
    g_avg = G_avg(temp, hl, coll_pot).magnitude
    nu = pc.viscosity_kinematic(temp).magnitude
    term1 = (con.K_MINOR_FLOC_BAFFLE /
            (2 * expansion_dist_max(Q_plant, temp, W_chan, hl, coll_pot, ratio_HS_max).magnitude
                * (g_avg**2) * nu))**(1/3)
    try:
        return (term1 * Q_plant/W_chan).magnitude
    except AttributeError:
        return (term1 * Q_plant/W_chan)

@u.wraps(None, [u.m**3/u.s, u.degK, u.m, u.m, u.m, None, None, None], False)
def num_baffles(Q_plant, temp, W_chan, L, hl, coll_pot, ratio_HS_max=6, baffle_thickness=2*u.mm):
    """Return the number of baffles that would fit in the channel given the
    channel length and spacing between baffles.

    Parameters
    ----------
    Q_plant: float
        Plant flow rate

    temp: float
        Design temperature

    W_chan: float
        Channel width

    L : float
        Length of the flocculator

    hl : float
        Headloss through the flocculator

    coll_pot : int
        Desired collision potential in the flocculator

    ratio_HS_max : int
        Maximum allowable ratio between the water depth and edge to edge distance
        between baffles

    baffle_thickness : float
        Thickness of a baffle

    Returns
    -------
    int
        the number of baffles that would fit in the channel

    Examples
    --------
    >>> from aide_design.play import*
    >>> num_baffles(20*u.L/u.s, 15*u.degC, 0.45*u.m, 6*u.m, 40*u.cm, 37000)
    16
    >>> num_baffles(40*u.L/u.s, 25*u.degC, 0.45*u.m, 6*u.m, 40*u.cm, 37000)
    17

    """
    N = round(L / (baffle_spacing(Q_plant, temp, W_chan, hl, coll_pot, ratio_HS_max).magnitude
        + baffle_thickness.to(u.m).magnitude))
    # the one is subtracted because the equation for num gives the number of
    # baffle spaces and there is always one less baffle than baffle spaces due
    # to geometry
    return int(N) - 1
