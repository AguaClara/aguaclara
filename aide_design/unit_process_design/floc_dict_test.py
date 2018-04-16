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

baffle_thickness : float
    Thickness of a baffle

"""
from aide_design.play import*

floc_dict = {'L_ent_tank_max': 2.2*u.m, 'baffle_thickness' : 15*u.cm,
             'L_sed': 5.8*u.m, 'hl': 40*u.cm, 'coll_pot': 37000,
             'freeboard': 10*u.cm, 'ratio_HS_min': 3, 'ratio_HS_max': 6,
             'W_min_construct': 45*u.cm, 'K_minor': 2.31}

@u.wraps(1/u.s, [u.degK, None], False)
def G_avg(temp, floc_inputs=floc_dict):
    """Return the average velocity gradient of a flocculator given head
    loss, collision potential and temperature.

    Parameters
    ----------
    temp : float
        Design temperature

    floc_inputs : dict
        a dictionary of all of the constant inputs needed for flocculator
        calculations

    Returns
    -------
    float
        average velocity gradient of a flocculator given head
        loss, collision potential and temperature.

    Examples
    --------
    >>> from aide_design.play import*
    >>> floc_dict = {'L_ent_tank_max': 2.2*u.m, 'baffle_thickness' : 15*u.cm,
    ...          'L_sed': 5.8*u.m, 'hl': 40*u.cm, 'coll_pot': 37000,
    ...          'freeboard': 10*u.cm, 'ratio_HS_min': 3, 'ratio_HS_max': 6,
    ...          'W_min_construct': 45*u.cm, 'K_minor': 2.31}
    >>> G_avg(15 * u.degC)
    93.24255814245437 1/second
    >>> G_avg(20 * u.degC)
    105.64226282862515 1/second

    """
    G = ((pc.gravity.magnitude * floc_inputs['hl'].to(u.m).magnitude) /
         (floc_inputs['coll_pot'] * pc.viscosity_kinematic(temp).magnitude))
    return G

@u.wraps(u.m**3, [u.m**3/u.s, u.degK, None], False)
def vol_floc(Q_plant, temp, floc_inputs=floc_dict):
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

    floc_inputs : dict
        a dictionary of all of the constant inputs needed for flocculator
        calculations

    Returns
    -------
    float
        total volume of the flocculator given head
        loss, collision potential and temperature.

    Examples
    --------
    >>> from aide_design.play import*
    >>> floc_dict = {'L_ent_tank_max': 2.2*u.m, 'baffle_thickness' : 15*u.cm,
    ...          'L_sed': 5.8*u.m, 'hl': 40*u.cm, 'coll_pot': 37000,
    ...          'freeboard': 10*u.cm, 'ratio_HS_min': 3, 'ratio_HS_max': 6,
    ...          'W_min_construct': 45*u.cm, 'K_minor': 2.31}
    >>> vol_floc(40*u.L/u.s, 15*u.degC,floc_dict)
    15.872580391229524 meter3
    >>> vol_floc(40*u.L/u.s, 20*u.degC,floc_dict)
    14.009544668698396 meter3

    """
    vol = (floc_dict['coll_pot'] / G_avg(temp, floc_inputs).magnitude)*Q_plant
    return vol

@u.wraps(u.m, [u.m**3/u.s, u.degK, u.m, None], False)
def width_HS_min(Q_plant, temp, depth_end, floc_inputs=floc_dict):
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

    floc_inputs : dict
        a dictionary of all of the constant inputs needed for flocculator
        calculations

    Returns
    -------
    float
        The minimum channel width required to achieve H/S > 3

    Examples
    --------
    >>> from aide_design.play import*
    >>> floc_dict = {'L_ent_tank_max': 2.2*u.m, 'baffle_thickness' : 15*u.cm,
    ...          'L_sed': 5.8*u.m, 'hl': 40*u.cm, 'coll_pot': 37000,
    ...          'freeboard': 10*u.cm, 'ratio_HS_min': 3, 'ratio_HS_max': 6,
    ...          'W_min_construct': 45*u.cm, 'K_minor': 2.31}
    >>> width_HS_min(20*u.L/u.s, 25*u.degC, 2*u.m, floc_dict)
    0.10740157183590993 meter
    >>> width_HS_min(40*u.L/u.s, 15*u.degC, 5*u.m, floc_dict)
    0.06861475664688545 meter

    """
    nu = pc.viscosity_kinematic(temp).magnitude

    w = (floc_inputs['ratio_HS_min'] *
         ((floc_inputs['K_minor'] /
          (2 * depth_end * (G_avg(temp, floc_inputs).magnitude**2)
          * nu))**(1/3))*Q_plant/depth_end)
    return w

@u.wraps(u.cm, [u.m**3/u.s, u.degK, u.m, None], False)
def width_floc_min(Q_plant, temp, depth_end, floc_inputs=floc_dict):
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

    floc_inputs : dict
        a dictionary of all of the constant inputs needed for flocculator
        calculations

    Returns
    -------
    float
        minimum channel width required.

    Examples
    --------
    >>> from aide_design.play import*
    >>> floc_dict = {'L_ent_tank_max': 2.2*u.m, 'baffle_thickness' : 15*u.cm,
    ...          'L_sed': 5.8*u.m, 'hl': 40*u.cm, 'coll_pot': 37000,
    ...          'freeboard': 10*u.cm, 'ratio_HS_min': 3, 'ratio_HS_max': 6,
    ...          'W_min_construct': 45*u.cm, 'K_minor': 2.31}
    >>> width_floc_min(20*u.L/u.s, 25*u.degC, 2*u.m, floc_dict)
    45 centimeter
    >>> width_floc_min(40*u.L/u.s, 15*u.degC, 2*u.m, floc_dict)
    45 centimeter
    """
    return max(width_HS_min(Q_plant, temp, depth_end, floc_inputs).to(u.cm).magnitude,
               floc_inputs['W_min_construct'].magnitude)

@u.wraps(None, [u.m**3/u.s, u.degK, u.m, u.cm, None], False)
def num_channel(Q_plant, temp, depth_end, W_tot, floc_inputs=floc_dict):
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

    W_tot: float
        Total width

    floc_inputs : dict
        a dictionary of all of the constant inputs needed for flocculator
        calculations

    Returns
    -------
    int
        the number of channels in the entrance tank/flocculator (ETF)

    Examples
    --------
    >>> from aide_design.play import*
    >>> from aide_design.play import*
    >>> floc_dict = {'L_ent_tank_max': 2.2*u.m, 'baffle_thickness' : 15*u.cm,
    ...          'L_sed': 5.8*u.m, 'hl': 40*u.cm, 'coll_pot': 37000,
    ...          'freeboard': 10*u.cm, 'ratio_HS_min': 3, 'ratio_HS_max': 6,
    ...          'W_min_construct': 45*u.cm, 'K_minor': 2.31}
    >>> num_channel(20*u.L/u.s, 25*u.degC, 2*u.m, 5*u.m, floc_dict)
    10
    >>> num_channel(40*u.L/u.s, 15*u.degC, 4*u.m, 10*u.m, floc_dict)
    22

    """
    num = W_tot/(width_floc_min(Q_plant, temp, depth_end, floc_inputs).magnitude)
    # floor function with step size 2
    num = np.floor(num/2)*2
    return int(max(num, 2))

@u.wraps(u.m**2, [u.m**3/u.s, u.degK, u.m, None], False)
def area_ent_tank(Q_plant, temp, depth_end, floc_inputs=floc_dict):
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

    floc_inputs : dict
        a dictionary of all of the constant inputs needed for flocculator
        calculations

    Returns
    -------
    float
        The planview area of the entrance tank

    Examples
    --------
    >>> from aide_design.play import*
    >>> floc_dict = {'L_ent_tank_max': 2.2*u.m, 'baffle_thickness' : 15*u.cm,
    ...          'L_sed': 5.8*u.m, 'hl': 40*u.cm, 'coll_pot': 37000,
    ...          'freeboard': 10*u.cm, 'ratio_HS_min': 3, 'ratio_HS_max': 6,
    ...          'W_min_construct': 45*u.cm, 'K_minor': 2.31}
    >>> area_ent_tank(20*u.L/u.s, 25*u.degC, 2*u.m, floc_dict)
    1 meter ** 2
    >>> area_ent_tank(40*u.L/u.s, 15*u.degC, 2*u.m, floc_dict)
    1 meter ** 2
    """
    # guess the planview area before starting iteration
    A_new = 1*u.m**2
    A_ratio = 0

    while (A_ratio) > 1.01 and (A_ET_PV/A_new) < 0.99:
        A_ET_PV = A_new

        vol_floc = vol_floc(Q_plant, temp, floc_inputs)
        A_floc_PV = vol_floc/(depth_end + hl/2)
        A_ETF_PV = A_ET_PV + A_floc_PV

        W_min = width_floc_min(Q_plant, temp, depth_end, floc_inputs)

        W_tot = A_ETF_PV/floc_inputs['L_sed']

        num_chan = num_channel(Q_plant, temp, depth_end, W_tot, floc_inputs)
        W_chan = W_tot/num_chan

        A_new = floc_inputs['L_ent_tank_max']*W_chan

        A_ratio = A_new/A_ET_PV

    return A_new.to(u.m**2).magnitude


### Baffle calculations
@u.wraps(u.m, [u.m**3/u.s, u.degK, u.m, None], False)
def expansion_dist_max(Q_plant, temp, W_chan, floc_inputs=floc_dict):
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

    floc_inputs : dict
        a dictionary of all of the constant inputs needed for flocculator
        calculations

    Returns
    -------
    float
        maximum distance between expansions for the largest
        allowable H/S ratio.

    Examples
    --------
    >>> from aide_design.play import*
    >>> floc_dict = {'L_ent_tank_max': 2.2*u.m, 'baffle_thickness' : 15*u.cm,
    ...          'L_sed': 5.8*u.m, 'hl': 40*u.cm, 'coll_pot': 37000,
    ...          'freeboard': 10*u.cm, 'ratio_HS_min': 3, 'ratio_HS_max': 6,
    ...          'W_min_construct': 45*u.cm, 'K_minor': 2.31}
    >>> expansion_dist_max(20*u.L/u.s, 15*u.degC, 0.45*u.m, floc_dict)
    1.2200391430074593 meter
    >>> expansion_dist_max(40*u.L/u.s, 25*u.degC, 0.45*u.m, floc_dict)
    1.931628399157619 meter

    """
    g_avg = G_avg(temp, floc_inputs).magnitude
    nu = pc.viscosity_kinematic(temp).magnitude
    term1 = (floc_inputs['K_minor']/(2 * (g_avg**2) * nu))**(1/4)
    term2 = (floc_inputs['ratio_HS_max']*Q_plant/W_chan)**(3/4)
    exp_dist_max = term1*term2
    return exp_dist_max

@u.wraps(None, [u.m**3/u.s, u.degK, u.m, u.m, None], False)
def num_expansions(Q_plant, temp, depth_end, W_chan, floc_inputs=floc_dict):
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

    floc_inputs : dict
        a dictionary of all of the constant inputs needed for flocculator
        calculations

    Returns
    -------
    int
        minimum number of expansions per baffle space

    Examples
    --------
    >>> from aide_design.play import*
    >>> floc_dict = {'L_ent_tank_max': 2.2*u.m, 'baffle_thickness' : 15*u.cm,
    ...          'L_sed': 5.8*u.m, 'hl': 40*u.cm, 'coll_pot': 37000,
    ...          'freeboard': 10*u.cm, 'ratio_HS_min': 3, 'ratio_HS_max': 6,
    ...          'W_min_construct': 45*u.cm, 'K_minor': 2.31}
    >>> num_expansions(20*u.L/u.s, 15*u.degC, 2*u.m, 0.45*u.m, floc_dict)
    2
    >>> num_expansions(40*u.L/u.s, 25*u.degC, 4*u.m, 0.45*u.m, floc_dict)
    3

    """
    return int(np.ceil(depth_end /
               (expansion_dist_max(Q_plant, temp, W_chan, floc_inputs)).magnitude))


@u.wraps(u.m, [u.m**3/u.s, u.degK, u.m, u.m, None], False)
def height_exp(Q_plant, temp, depth_end, W_chan, floc_inputs=floc_dict):
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

    floc_inputs : dict
        a dictionary of all of the constant inputs needed for flocculator
        calculations

    Returns
    -------
    float
        the actual distance between expansions

    Examples
    --------
    >>> from aide_design.play import*
    >>> floc_dict = {'L_ent_tank_max': 2.2*u.m, 'baffle_thickness' : 15*u.cm,
    ...          'L_sed': 5.8*u.m, 'hl': 40*u.cm, 'coll_pot': 37000,
    ...          'freeboard': 10*u.cm, 'ratio_HS_min': 3, 'ratio_HS_max': 6,
    ...          'W_min_construct': 45*u.cm, 'K_minor': 2.31}
    >>> height_exp(20*u.L/u.s, 15*u.degC, 2*u.m, 0.45*u.m, floc_dict)
    1.0 meter
    >>> height_exp(40*u.L/u.s, 25*u.degC, 4*u.m, 0.45*u.m, floc_dict)
    1.3333333333333333 meter

    """
    return depth_end/num_expansions(Q_plant, temp, depth_end, W_chan, floc_inputs)

@u.wraps(u.m, [u.m**3/u.s, u.degK, u.m, None], False)
def baffle_spacing(Q_plant, temp, W_chan, floc_inputs=floc_dict):
    """Return the spacing between baffles based on the target velocity gradient

    Parameters
    ----------
    Q_plant: float
        Plant flow rate

    temp: float
        Design temperature

    W_chan: float
        Channel width

    floc_inputs : dict
        a dictionary of all of the constant inputs needed for flocculator
        calculations

    Returns
    -------
    float
        the spacing between baffles

    Examples
    --------
    >>> from aide_design.play import*
    >>> floc_dict = {'L_ent_tank_max': 2.2*u.m, 'baffle_thickness' : 15*u.cm,
    ...          'L_sed': 5.8*u.m, 'hl': 40*u.cm, 'coll_pot': 37000,
    ...          'freeboard': 10*u.cm, 'ratio_HS_min': 3, 'ratio_HS_max': 6,
    ...          'W_min_construct': 45*u.cm, 'K_minor': 2.31}
    >>> baffle_spacing(40*u.L/u.s, 25*u.degC, 0.45*u.m, floc_dict)
    0.3219380665262699 meter
    >>> baffle_spacing(20*u.L/u.s, 15*u.degC, 0.45*u.m, floc_dict)
    0.2033398571679099 meter
    """
    g_avg = G_avg(temp, floc_inputs).magnitude
    nu = pc.viscosity_kinematic(temp).magnitude
    term1 = (floc_inputs['K_minor']/(2 * expansion_dist_max(Q_plant, temp, W_chan, floc_inputs).magnitude * (g_avg**2) * nu))**(1/3)
    return term1 * Q_plant/W_chan

@u.wraps(None, [u.m**3/u.s, u.degK, u.m, u.m, None], False)
def num_baffles(Q_plant, temp, W_chan, L, floc_inputs=floc_dict):
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

    floc_inputs : dict
        a dictionary of all of the constant inputs needed for flocculator
        calculations

    Returns
    -------
    int
        the number of baffles that would fit in the channel

    Examples
    --------
    >>> from aide_design.play import*
    >>> floc_dict = {'L_ent_tank_max': 2.2*u.m, 'baffle_thickness' : 15*u.cm,
    ...          'L_sed': 5.8*u.m, 'hl': 40*u.cm, 'coll_pot': 37000,
    ...          'freeboard': 10*u.cm, 'ratio_HS_min': 3, 'ratio_HS_max': 6,
    ...          'W_min_construct': 45*u.cm, 'K_minor': 2.31}
    >>> num_baffles(20*u.L/u.s, 15*u.degC, 0.45*u.m, 6*u.m, floc_dict)
    16
    >>> num_baffles(40*u.L/u.s, 25*u.degC, 0.45*u.m, 6*u.m, floc_dict)
    12

    """
    N = round(L / (baffle_spacing(Q_plant, temp, W_chan, floc_inputs).magnitude
        + floc_inputs['baffle_thickness'].to(u.m).magnitude))
    # the one is subtracted because the equation for num gives the number of
    # baffle spaces and there is always one less baffle than baffle spaces due
    # to geometry
    return int(N) - 1

@u.wraps(None, [u.m**3/u.s, u.degK, u.m, None], False)
def floc_agg(Q_plant, temp, depth_end, floc_inputs=floc_dict):
    """Aggregates the floc tank functions into a single function which
    outputs a dictionary of all the necessary design parameters.

    Parameters
    ----------

    Returns
    -------

    Examples
    --------
    >>> from aide_design.play import*
    >>> floc_dict = {'L_ent_tank_max': 2.2*u.m, 'baffle_thickness' : 15*u.cm,
    ...          'L_sed': 5.8*u.m, 'hl': 40*u.cm, 'coll_pot': 37000,
    ...          'freeboard': 10*u.cm, 'ratio_HS_min': 3, 'ratio_HS_max': 6,
    ...          'W_min_construct': 45*u.cm, 'K_minor': 2.31}
    >>> floc_agg(20*u.L/u.s, 15*u.degC, 2*u.m, floc_dict)
    {'K_minor': 2.31,
    'L_bottom_baffle': 1.7767028781699596,
    'L_ent_tank_max': <Quantity(2.2, 'meter')>,
    'L_sed': <Quantity(5.8, 'meter')>,
    'L_top_baffle': 2.2767028781699596,
    'W_chan': 0.39719005468709884,
    'W_min_construct': <Quantity(45, 'centimeter')>,
    'baffle_spacing': 0.22329712183004025,
    'baffle_thickness': <Quantity(15, 'centimeter')>,
    'coll_pot': 37000,
    'freeboard': <Quantity(10, 'centimeter')>,
    'h_chan': 2.5,
    'hl': <Quantity(40, 'centimeter')>,
    'num_baffles_chan_1': 15,
    'num_baffles_chan_n': 9,
    'num_chan': 2,
    'obstacles_bool': 1,
    'ratio_HS_max': 6,
    'ratio_HS_min': 3}

    """
    # calculate planview area of the entrance tank
    A_ET_PV = area_ent_tank(Q_plant, temp, depth_end, floc_inputs).magnitude

    # now calculate planview area of entrance tank + flocculator combined
    volume_floc = vol_floc(Q_plant, temp, floc_inputs).magnitude
    A_floc_PV = volume_floc/(depth_end + floc_inputs['hl'].to(u.m).magnitude/2)
    A_ETF_PV = A_ET_PV + A_floc_PV

    L_tank = floc_inputs['L_sed'].to(u.m).magnitude

    # calculate width of the flocculator channels and entrance tank
    W_min = width_floc_min(Q_plant, temp, depth_end, floc_inputs).to(u.m).magnitude
    W_tot = A_ETF_PV/L_tank
    num_chan = num_channel(Q_plant, temp, depth_end, W_tot, floc_inputs)
    W_chan = W_tot/num_chan

    # calculate the height of the channel using depth at the end of the
    # flocculator, headloss, and freeboard
    h_chan = depth_end + floc_inputs['hl'].to(u.m).magnitude + floc_inputs['freeboard'].to(u.m).magnitude

    # calculate baffle spacing and number of baffles in the Flocculator
    baffle_spacing_ = baffle_spacing(Q_plant, temp, W_chan, floc_inputs).magnitude
    num_baffles_chan_1 = num_baffles(Q_plant, temp, W_chan, L_tank, floc_inputs)
    num_baffles_chan_n = num_baffles(Q_plant, temp, W_chan, L_tank - floc_inputs['L_ent_tank_max'].to(u.m).magnitude, floc_inputs)

    # calculate the length of the baffles. The top baffle is set to the top of the
    # channel wall and the bottom baffle is set to the bottom of the channel.
    # The distance between baffles is the same as the vertical distance between
    # the top baffle and the bottom of the channel, which is the same vertical
    # distance as the bottom baffle and the free surface at the end of the flocculator
    L_top_baffle = h_chan - baffle_spacing_
    L_bottom_baffle = depth_end - baffle_spacing_

    # determine if there are obstacles in the flocculator
    if Q_plant > 0.05:
        obstacles_bool = 0
    else:
        obstacles_bool = 1

    # update the floc dictionary with outputs
    floc_inputs.update({'W_chan': W_chan, 'num_chan': num_chan,
        'h_chan': h_chan, 'baffle_spacing': baffle_spacing_,
        'num_baffles_chan_1': num_baffles_chan_1, 'num_baffles_chan_n': num_baffles_chan_n,
        'obstacles_bool': obstacles_bool, 'L_top_baffle': L_top_baffle,
        'L_bottom_baffle': L_bottom_baffle})
    return floc_inputs
