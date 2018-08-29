"""This file contains all the functions needed to design a flocculator for
an AguaClara plant.

"""
from aguaclara.play import*

# expansion minor loss coefficient for 180 degree bend
K_e = (1 / con.RATIO_VC_ORIFICE**2 - 1)**2

@u.wraps(1/u.s, [u.m, None, u.degK], False)
def G_avg(hl, Gt, T):
    """Return the average velocity gradient of a flocculator given head
    loss, collision potential and temperature.

    Parameters
    ----------
    hl: float
        Headloss through the flocculator

    Gt: float
        Target collision potential

    T: float
        Design temperature

    Returns
    -------
    ?

    Examples
    --------
    >>> from aguaclara.play import*
    >>>G_avg(40*u.cm, 37000, 25*u.degC)
    118.715 1/second
    """
    G = (pc.gravity.magnitude * hl) / (Gt * pc.viscosity_kinematic(T).magnitude)
    return G

@u.wraps(u.m**3, [u.m**3/u.s, u.m, None, u.degK], False)
def vol_floc(q_plant, hl, Gt, T):
    """Return the total volume of the flocculator using plant flow rate, head
    loss, collision potential and temperature.

    Uses an estimation of flocculator residence time (ignoring the decrease
    in water depth caused by head loss in the flocculator.) Volume does not take
    into account the extra volume that the flocculator will have due to changing
    water level caused by head loss.

    Parameters
    ----------
    q_plant: float
        Plant flow rate

    hl: float
        Headloss through the flocculator

    Gt: float
        Target collision potential

    T: float
        Design temperature

    Returns
    -------
    ?

    Examples
    --------
    >>> from aguaclara.play import*
    >>>vol_floc(20*u.L/u.s, 40*u.cm, 37000, 25*u.degC)
    6.233 meter3
    """
    vol = (Gt / G_avg(hl, Gt, T).magnitude)*q_plant
    return vol

@u.wraps(u.cm, [u.m**3/u.s, u.m, None, u.degK, u.m], False)
def width_HS_min(q_plant, hl, Gt, T, depth_end):
    """Return the minimum channel width required to achieve H/S > 3.

    The channel can be wider than this, but this is the absolute minimum width
    for a channel. The minimum width occurs when there is only one expansion per
    baffle and thus the distance between expansions is the same as the depth of
    water at the end of the flocculator.

    Parameters
    ----------
    q_plant: float
        Plant flow rate

    hl: float
        Headloss through the flocculator

    Gt: float
        Target collision potential

    T: float
        Design temperature

    depth_end: float
        The depth of water at the end of the flocculator

    Returns
    -------
    float
        The minimum channel width required to achieve H/S > 3

    Examples
    --------
    >>> from aguaclara.play import*
    >>> width_HS_min(20*u.L/u.s, 40*u.cm, 37000, 25*u.degC, 2*u.m)
    0.1074 centimeter
    """
    nu = pc.viscosity_kinematic(T).magnitude

    w = con.RATIO_HS_MIN*((K_e/(2 * depth_end * (G_avg(hl, Gt, T).magnitude**2)
    * nu))**(1/3))*q_plant/depth_end
    return w



@u.wraps(u.cm, [u.m**3/u.s, u.m, None, u.degK, u.m], False)
def width_floc_min(q_plant, hl, Gt, T, depth_end):
    """Return the minimum channel width required.

    This takes the maximum of the minimum required to achieve H/S > 3 and the
    minimum required for constructability based on the width of the human hip.

    Parameters
    ----------
    q_plant: float
        Plant flow rate

    hl: float
        Headloss through the flocculator

    Gt: float
        Target collision potential

    T: float
        Design temperature

    depth_end: float
        The depth of water at the end of the flocculator

    Returns
    -------
    float
        The minimum channel width required to achieve H/S > 3

    Examples
    --------
    >>> from aguaclara.play import*
    >>> width_floc_min(20*u.L/u.s, 40*u.cm, 37000, 25*u.degC, 2*u.m)
    45 centimeter
    """
    return max(width_HS_min(q_plant, hl, Gt, T, depth_end).magnitude, con.FLOC_WIDTH_MIN_CONST.magnitude)

@u.wraps(None, [u.m**3/u.s, u.m, None, u.degK, u.m, u.m], False)
def num_channel(q_plant, hl, Gt, T, W_tot, depth_end):
    """Return the number of channels in the entrance tank/flocculator (ETF).

    This takes the total width of the flocculator and divides it by the minimum
    channel width. A floor function is used to ensure that there are an even
    number of channels.

    Parameters
    ----------
    q_plant: float
        Plant flow rate

    hl: float
        Headloss through the flocculator

    Gt: float
        Target collision potential

    T: float
        Design temperature

    W_tot: float
        Total width

    depth_end: float
        The depth of water at the end of the flocculator

    Returns
    -------
    ?

    Examples
    --------
    >>> from aguaclara.play import*
    >>> num_channel(20*u.L/u.s, 40*u.cm, 37000, 25*u.degC, 20*u.m, 2*u.m)
    2
    """
    num = W_tot/(width_floc_min(q_plant, hl, Gt, T, depth_end).magnitude)
    # floor function with step size 2
    num = np.floor(num/2)*2
    return int(max(num, 2))


@u.wraps(u.m**2, [u.m**3/u.s, u.m, None, u.degK, u.m], False)
def area_ent_tank(q_plant, hl, Gt, T, depth_end):
    """Return the planview area of the entrance tank given plant flow rate,
    headloss, target collision potential, design temperature, and depth of
    water at the end of the flocculator.

    Parameters
    ----------
    q_plant: float
        Plant flow rate

    hl: float
        Headloss through the flocculator

    Gt: float
        Target collision potential

    T: float
        Design temperature

    depth_end: float
        The depth of water at the end of the flocculator

    Returns
    -------
    float
        The planview area of the entrance tank

    Examples
    --------
    >>> from aguaclara.play import*
    >>> area_ent_tank(20*u.L/u.s, 40*u.cm, 37000, 25*u.degC, 2*u.m)
    1 meter ** 2
    """
    # guess the planview area before starting iteration
    A_new = 1*u.m**2
    A_ratio = 0

    while (A_ratio) > 1.01 and (A_ET_PV/A_new) < 0.99:
        A_ET_PV = A_new

        vol_floc = vol_floc(q_plant, hl, Gt, T)
        A_floc_PV = vol_floc/(depth_end + hl/2)
        A_ETF_PV = A_ET_PV + A_floc_PV

        W_min = width_floc_min(q_plant, hl, Gt, T, depth_end)

        W_tot = A_ETF_PV/opt.L_sed

        num_chan = num_channel(q_plant, hl, Gt, T, W_tot)
        W_chan = W_tot/num_chan

        A_new = opt.L_ET_max*W_chan

        A_ratio = A_new/A_ET_PV

    return A_new.to(u.m**2).magnitude

### Baffle calculations
@u.wraps(u.m, [u.m**3/u.s, u.m, None, u.degK, u.m], False)
def exp_dist_max(q_plant, hl, Gt, T, W_chan):
    """"Return the maximum distance between expansions for the largest
    allowable H/S ratio.

    Parameters
    ----------
    q_plant: float
        Plant flow rate

    hl: float
        Headloss through the flocculator

    Gt: float
        Target collision potential

    T: float
        Design temperature

    W_chan: float
        Channel width

    Returns
    -------
    ?

    Examples
    --------
    >>> from aguaclara.play import*
    >>> exp_dist_max(20*u.L/u.s, 40*u.cm, 37000, 25*u.degC, 2*u.m)
    0.375 meter
    """
    g_avg = G_avg(hl, Gt, T).magnitude
    nu = pc.viscosity_kinematic(T).magnitude
    term1 = (K_e/(2 * (g_avg**2) * nu))**(1/4)
    term2 = (con.RATIO_HS_MAX*q_plant/W_chan)**(3/4)
    exp_dist_max = term1*term2
    return exp_dist_max

@u.wraps(None, [u.m**3/u.s, u.m, None, u.degK, u.m], False)
def num_expansions(q_plant, hl, Gt, T, depth_end):
    """"Return the minimum number of expansions per baffle space.

    Parameters
    ----------
    q_plant: float
        Plant flow rate

    hl: float
        Headloss through the flocculator

    Gt: float
        Target collision potential

    T: float
        Design temperature

    depth_end: float
        The depth of water at the end of the flocculator

    Returns
    -------
    ?

    Examples
    --------
    >>> from aguaclara.play import*
    ???
    """
    return int(np.ceil(depth_end/(exp_dist_max(q_plant, hl, Gt, T)).magnitude))

@u.wraps(u.m, [u.m**3/u.s, u.m, None, u.degK, u.m], False)
def height_exp(q_plant, hl, Gt, T, depth_end):
    """Return the actual distance between expansions given the integer
    requirement for the number of expansions per flocculator depth.

    Parameters
    ----------
    q_plant: float
        Plant flow rate

    hl: float
        Headloss through the flocculator

    Gt: float
        Target collision potential

    T: float
        Design temperature

    depth_end: float
        The depth of water at the end of the flocculator

    Returns
    -------
    ?

    Examples
    --------
    >>> from aguaclara.play import*
    ???
    """
    return depth_end/num_expansions(q_plant, hl, Gt, T)

@u.wraps(u.m, [u.m**3/u.s, u.m, None, u.degK, u.m], False)
def baffle_spacing(q_plant, hl, Gt, T, W_chan):
    """Return the spacing between baffles based on the target velocity gradient

    Parameters
    ----------
    q_plant: float
        Plant flow rate

    hl: float
        Headloss through the flocculator

    Gt: float
        Target collision potential

    T: float
        Design temperature

    W_chan: float
        Channel width

    Returns
    -------
    ?

    Examples
    --------
    >>> from aguaclara.play import*
    >>> baffle_spacing(20*u.L/u.s, 40*u.cm, 37000, 25*u.degC, 2*u.m)
    0.063 meter
    ."""
    g_avg = G_avg(hl, Gt, T).magnitude
    nu = pc.viscosity_kinematic(T).magnitude
    term1 = (K_e/(2 * exp_dist_max(q_plant, hl, Gt, T, W_chan).magnitude * (g_avg**2) * nu))**(1/3)
    return term1 * q_plant/W_chan
baffle_spacing(20*u.L/u.s, 40*u.cm, 37000, 25*u.degC, 2*u.m)

@u.wraps(None, [u.m**3/u.s, u.m, None, u.degK, u.m, u.m, u.m], False)
def num_baffles(q_plant, hl, Gt, T, W_chan, L, baffle_thickness):
    """Return the number of baffles that would fit in the channel given the
    channel length and spacing between baffles.

    Parameters
    ----------
    q_plant: float
        Plant flow rate

    hl: float
        Headloss through the flocculator

    Gt: float
        Target collision potential

    T: float
        Design temperature

    W_chan: float
        Channel width

    L: float
        Length

    baffle_thickness: float
        Baffle thickness

    Returns
    -------
    ?

    Examples
    --------
    >>> from aguaclara.play import*
    >>> num_baffles(20*u.L/u.s, 40*u.cm, 37000, 25*u.degC, 2*u.m, 2*u.m, 2*u.m)
    0
    >>> num_baffles(20*u.L/u.s, 20*u.cm, 37000, 25*u.degC, 2*u.m, 2*u.m, 21*u.m)
    -1
    """
    num = round((L / (baffle_spacing(q_plant, hl, Gt, T, W_chan).magnitude + baffle_thickness)))
    # the one is subtracted because the equation for num gives the number of
    # baffle spaces and there is always one less baffle than baffle spaces due
    # to geometry
    return int(num) - 1
