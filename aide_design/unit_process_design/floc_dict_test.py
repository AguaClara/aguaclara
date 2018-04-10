"""This file contains all the functions needed to design a flocculator for
an AguaClara plant.

Attributes
----------
L_ent_tank_max : float
    The maximum length of the entrance tank

L_sed : float
    The length of the sedimentation tank

hl : float
    Headloss through the flocculator

coll_pot : int
    Desired collision potential in the flocculator

freeboard: float
    The height between the water and top of the flocculator channels

ratior_HS_min : int
    Minimum allowable ratio between the water depth and edge to edge distance
    between baffles

ratio_HS_max : int
    Maximum allowable ratio between the water depth and edge to edge distance
    between baffles

W_min_construct : float
    Minimum width of a flocculator channel based on the width of the human hip

K_minor : float
    Minor loss coefficient used in flocculator design

"""
from aide_design.play import*

floc_dict = {'L_ent_tank_max': 2.2*u.m,
             'L_sed': 5.8*u.m, 'hl': 40*u.cm, 'coll_pot': 37000,
             'freeboard': 10*u.cm, 'ratio_HS_min': 3, 'ratio_HS_max': 6,
             'W_min_construct': 45*u.cm, 'K_minor': 2.31}

@u.wraps(1/u.s, [u.m, None, u.degK], False)
def G_avg(hl, coll_pot, temp):
    """Return the average velocity gradient of a flocculator given head
    loss, collision potential and temperature.

    Parameters
    ----------
    hl: float
        Headloss through the flocculator

    coll_pot : int
        Desired collision potential in the flocculator

    temp: float
        Design temperature

    Returns
    -------
    float
        average velocity gradient of a flocculator given head
        loss, collision potential and temperature.

    Examples
    --------
    >>> from aide_design.play import*
    >>> floc_dict = {'L_ent_tank_max': 2.2*u.m,
    ...          'L_sed': 5.8*u.m, 'hl': 40*u.cm, 'coll_pot': 37000,
    ...          'freeboard': 10*u.cm, 'ratio_HS_min': 3, 'ratio_HS_max': 6,
    ...          'W_min_construct': 45*u.cm, 'K_minor': 2.31}
    >>> G_avg(40*u.cm, 10, 40 * u.degK)
    T not defined..?

    """
    G = (pc.gravity.magnitude * hl) / (coll_pot * pc.viscosity_kinematic(T).magnitude)
    return G

@u.wraps(u.m**3, [u.m**3/u.s, u.m, None, u.degK], False)
def vol_floc(Q_plant, hl, coll_pot, temp):
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

    hl: float
        Headloss through the flocculator

    coll_pot : int
        Desired collision potential in the flocculator

    temp: float
        Design temperature

    Returns
    -------
    float
        total volume of the flocculator given head
        loss, collision potential and temperature.

    Examples
    --------
    >>> from aide_design.play import*
    >>> floc_dict = {'L_ent_tank_max': 2.2*u.m,
    ...          'L_sed': 5.8*u.m, 'hl': 40*u.cm, 'coll_pot': 37000,
    ...          'freeboard': 10*u.cm, 'ratio_HS_min': 3, 'ratio_HS_max': 6,
    ...          'W_min_construct': 45*u.cm, 'K_minor': 2.31}
    >>> vol_floc(40*u.L/u.s, 10, 40 * u.degK)

    """
    vol = (coll_pot / G_avg(hl, coll_pot, temp).magnitude)*Q_plant
    return vol

@u.wraps(u.cm, [u.m**3/u.s, u.m, None, u.degK, u.m], False)
def width_HS_min(Q_plant, hl, coll_pot, temp, depth_end, floc_inputs=floc_dict):
    """Return the minimum channel width required to achieve H/S > 3.

    The channel can be wider than this, but this is the absolute minimum width
    for a channel. The minimum width occurs when there is only one expansion per
    baffle and thus the distance between expansions is the same as the depth of
    water at the end of the flocculator.

    Parameters
    ----------
    Q_plant : float
        Plant flow rate

    hl: float
        Headloss through the flocculator

    coll_pot: float
        Target collision potential

    temp: float
        Design temperature

    depth_end: float
        The depth of water at the end of the flocculator

    Returns
    -------
    float
        The minimum channel width required to achieve H/S > 3

    Examples
    --------
    >>> from aide_design.play import*
    >>> width_HS_min(20*u.L/u.s, 40*u.cm, 37000, 25*u.degC, 2*u.m)
    0.1074 centimeter
    """
    nu = pc.viscosity_kinematic(temp).magnitude

    w = (floc_inputs['ratio_HS_min'] *
         ((floc_inputs['K_minor'] /
          (2 * depth_end * (G_avg(hl, coll_pot, temp).magnitude**2)
          * nu))**(1/3))*Q_plant/depth_end)
    return w

@u.wraps(u.cm, [u.m**3/u.s, u.m, None, u.degK, u.m], False)
def width_floc_min(Q_plant, hl, coll_pot, temp, depth_end, floc_inputs=floc_dict):
    """Return the minimum channel width required.

    This takes the maximum of the minimum required to achieve H/S > 3 and the
    minimum required for constructability based on the width of the human hip.

    Parameters
    ----------
    Q_plant : float
        Plant flow rate

    hl: float
        Headloss through the flocculator

    coll_pot : int
        Desired collision potential in the flocculator

    temp: float
        Design temperature

    depth_end: float
        The depth of water at the end of the flocculator

    Returns
    -------
    float
        minimum channel width required.

    Examples
    --------
    >>> from aide_design.play import*
    ???Getting that issue that Zoe and Fletcher talked about!

    """
    return max(width_HS_min(Q_plant, hl, coll_pot, temp, depth_end, floc_inputs).magnitude,
               floc_inputs['W_min_construct'].magnitude)


@u.wraps(None, [u.m**3/u.s, u.m, None, u.degK, u.m, u.m], False)
def num_channel(Q_plant, hl, coll_pot, temp, W_tot, depth_end, floc_inputs=floc_dict):
    """Return the number of channels in the entrance tank/flocculator (ETF).

    This takes the total width of the flocculator and divides it by the minimum
    channel width. A floor function is used to ensure that there are an even
    number of channels.

    Parameters
    ----------
    Q_plant : float
        Plant flow rate

    hl: float
        Headloss through the flocculator

    coll_pot : int
        Desired collision potential in the flocculator

    temp: float
        Design temperature

    W_tot: float
        Total width

    depth_end: float
        The depth of water at the end of the flocculator

    Returns
    -------
    int?
        the number of channels in the entrance tank/flocculator (ETF)

    Examples
    --------
    >>> from aide_design.play import*
    ???Getting same issue

    """
    N = W_tot/(width_floc_min(Q_plant, hl, coll_pot, temp, depth_end, floc_inputs).magnitude)
    # floor function with step size 2
    N = np.floor(num/2)*2
    return int(max(N, 2))


@u.wraps(u.m**2, [u.m**3/u.s, u.m, None, u.degK, u.m], False)
def area_ent_tank(Q_plant, hl, coll_pot, temp, depth_end, floc_inputs=floc_dict):
    """Return the planview area of the entrance tank given plant flow rate,
    headloss, target collision potential, design temperature, and depth of
    water at the end of the flocculator.

    Parameters
    ----------
    Q_plant: float
        Plant flow rate

    hl: float
        Headloss through the flocculator

    coll_pot: float
        Target collision potential

    temp: float
        Design temperature

    depth_end: float
        The depth of water at the end of the flocculator

    Returns
    -------
    float
        The planview area of the entrance tank

    Examples
    --------
    >>> from aide_design.play import*
    >>> area_ent_tank(20*u.L/u.s, 40*u.cm, 37000, 25*u.degC, 2*u.m)
    1 meter ** 2
    """
    # guess the planview area before starting iteration
    A_new = 1*u.m**2
    A_ratio = 0

    while (A_ratio) > 1.01 and (A_ET_PV/A_new) < 0.99:
        A_ET_PV = A_new

        vol_floc = vol_floc(Q_plant, hl, coll_pot, temp)
        A_floc_PV = vol_floc/(depth_end + hl/2)
        A_ETF_PV = A_ET_PV + A_floc_PV

        W_min = width_floc_min(Q_plant, hl, coll_pot, temp, depth_end, lfom_inputs)

        W_tot = A_ETF_PV/floc_inputs['L_sed']

        num_chan = num_channel(Q_plant, hl, coll_pot, temp, W_tot, floc_inputs)
        W_chan = W_tot/num_chan

        A_new = floc_inputs['L_ent_tank_max']*W_chan

        A_ratio = A_new/A_ET_PV

    return A_new.to(u.m**2).magnitude

### Baffle calculations
@u.wraps(u.m, [u.m**3/u.s, u.m, None, u.degK, u.m], False)
def expansion_dist_max(Q_plant, hl, coll_pot, temp, W_chan, floc_inputs=floc_dict):
    """"Return the maximum distance between expansions for the largest
    allowable H/S ratio.

    Parameters
    ----------
    Q_plant: float
        Plant flow rate

    hl: float
        Headloss through the flocculator

    coll_pot: float
        Target collision potential

    temp: float
        Design temperature

    W_chan: float
        Channel width

    Returns
    -------
    float
        maximum distance between expansions for the largest
        allowable H/S ratio.

    Examples
    --------
    >>> from aide_design.play import*
    ???Same Issue!!
    """
    g_avg = G_avg(hl, coll_pot, temp).magnitude
    nu = pc.viscosity_kinematic(temp).magnitude
    term1 = (floc_inputs['K_minor']/(2 * (g_avg**2) * nu))**(1/4)
    term2 = (floc_inputs['ratio_HS_max']*Q_plant/W_chan)**(3/4)
    exp_dist_max = term1*term2
    return exp_dist_max

@u.wraps(None, [u.m**3/u.s, u.m, None, u.degK, u.m], False)
def num_expansions(Q_plant, hl, coll_pot, temp, depth_end, floc_inputs=floc_dict):
    """"Return the minimum number of expansions per baffle space.

    Parameters
    ----------
    Q_plant: float
        Plant flow rate

    hl: float
        Headloss through the flocculator

    coll_pot: float
        Target collision potential

    temp: float
        Design temperature

    depth_end: float
        The depth of water at the end of the flocculator

    Returns
    -------
    float
        minimum number of expansions per baffle space

    Examples
    --------
    >>> from aide_design.play import*
    ???Same Issue!!
    """
    return int(np.ceil(depth_end/(expansion_dist_max(Q_plant, hl, coll_pot, temp, floc_inputs)).magnitude))

@u.wraps(u.m, [u.m**3/u.s, u.m, None, u.degK, u.m], False)
def height_exp(Q_plant, hl, coll_pot, temp, depth_end, floc_inputs=floc_dict):
    """Return the actual distance between expansions given the integer
    requirement for the number of expansions per flocculator depth."""
    return depth_end/num_expansions(Q_plant, hl, coll_pot, temp, floc_inputs)

@u.wraps(u.m, [u.m**3/u.s, u.m, None, u.degK, u.m], False)
def baffle_spacing(Q_plant, hl, coll_pot, temp, W_chan, floc_inputs=floc_dict):
    """Return the spacing between baffles based on the target velocity gradient
    ."""
    g_avg = G_avg(hl, coll_pot, temp).magnitude
    nu = pc.viscosity_kinematic(temp).magnitude
    term1 = (floc_inputs['K_minor']/(2 * expansion_dist_max(Q_plant, hl, coll_pot, temp, W_chan, floc_inputs).magnitude * (g_avg**2) * nu))**(1/3)
    return term1 * Q_plant/W_chan

@u.wraps(None, [u.m**3/u.s, u.m, None, u.degK, u.m, u.m, u.m], False)
def num_baffles(Q_plant, hl, coll_pot, temp, W_chan, L, baffle_thickness, lfom_inputs=floc_dict):
    """Return the number of baffles that would fit in the channel given the
    channel length and spacing between baffles."""
    N = round((L / (baffle_spacing(Q_plant, hl, coll_pot, temp, W_chan, lfom_inputs).magnitude + baffle_thickness)))
    # the one is subtracted because the equation for num gives the number of
    # baffle spaces and there is always one less baffle than baffle spaces due
    # to geometry
    return int(N) - 1
