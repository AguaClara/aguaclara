"""This file contains all the functions needed to design a sedimentation tank
for an AguaClara plant.

"""
from aide_design.play import*

@u.wraps(None, [u.cm], False)
def n_sed_plates_max(B_sed_plate):
    """Return the maximum possible number of plate settlers in a module given
    the center to center distance between plates.

    Parameters
    ----------
    B_sed_plate : float
        Center to center distance between plate settlers

    Returns
    -------
    int
        Maximum number of plates

    Examples
    --------
    >>> from aide_design.play import*
    >>> n_sed_plates_max(1*u.cm)
    35
    >>> n_sed_plates_max(2.52*u.cm)
    14

    """
    return math.floor((mat.LENGTH_SED_PLATE_CANTILEVERED.magnitude/dist_center_sed_plate
                      * np.tan(con.ANGLE_SED_PLATE.to(u.rad).magnitude)) + 1)

@u.wraps(u.inch, [u.inch], False)
def w_diffuser_inner_min(W_tank):
    """Return the minimum inner width of each diffuser in the sedimentation tank.

    Parameters
    ----------
    W_tank : float
        Width of the sedimentation tank

    Returns
    -------
    float
        Minimum inner width of each diffuser in the sedimentation tank

    Examples
    --------
    >>> from aide_design.play import*
    >>> w_diffuser_inner_min(42*u.inch)
    0.09483615870787537 inch

    """
    return ((con.VEL_SED_UP_BOD.to(u.inch/u.s).magnitude /
             con.V_SED_DIFFUSER_MAX.to(u.inch/u.s).magnitude) * W_tank)

@u.wraps(u.m, [u.m], False)
def w_diffuser_inner(w_tank):
    """Return the inner width of each diffuser in the sedimentation tank.

    Parameters
    ----------
    w_tank : float
        Width of the sedimentation tank

    Returns
    -------
    float
        Inner width of each diffuser in the sedimentation tank

    Examples
    --------
    >>> from aide_design.play import*
    >>>

    """
    return ut.ceil_nearest(w_diffuser_inner_min(w_tank).magnitude, (np.arange(1/16,1/4,1/16)*u.inch).magnitude)

@u.wraps(u.m, [u.m], False)
def w_diffuser_outer(w_tank):
    """Return the outer width of each diffuser in the sedimentation tank.

    Parameters
    ----------
    w_tank : float
        Width of the sedimentation tank

    Returns
    -------
    float
        Outer width of each diffuser in the sedimentation tank

    Examples
    --------
    >>> from aide_design.play import*
    >>>

    """
    return w_diffuser_inner_min(w_tank).magnitude + (2 * con.T_DIFFUSER)

@u.wraps(u.m, [u.m], False)
def L_diffuser_outer(w_tank):
    """Return the outer length of each diffuser in the sedimentation tank.

    Parameters
    ----------
    w_tank : float
        Width of the sedimentation tank

    Returns
    -------
    float
        Outer length of each diffuser in the sedimentation tank

    Examples
    --------
    >>> from aide_design.play import*
    >>>

    """
    return con.AREA_PVC_DIFFUSER.magnitude / (2 * con.T_DIFFUSER.magnitude) - w_diffuser_inner(w_tank).magnitude

@u.wraps(u.m, [u.m], False)
def L_diffuser_inner(w_tank):
    """Return the inner length of each diffuser in the sedimentation tank.

    Parameters
    ----------
    w_tank : float
        Width of the sedimentation tank

    Returns
    -------
    float
        Inner length of each diffuser in the sedimentation tank

    Examples
    --------
    >>> from aide_design.play import*
    >>>

    """
    return L_diffuser_outer(w_tank).magnitude - (2 * con.T_DIFFUSER.magnitude)

@u.wraps(u.m**3/u.s, [u.m], False)
def q_diffuser_max(w_tank):
    """Return the flow through each diffuser.

    Parameters
    ----------
    w_tank : float
        Width of the sedimentation tank

    Returns
    -------
    float
        Flow through each diffuser in the sedimentation tank

    Examples
    --------
    >>> from aide_design.play import*
    >>>

    """
    return con.VEL_SED_UP_BOD.magnitude * w_sed_tank * L_diffuser_outer(w_tank).magnitude

# still need to calculate V_sed_diffuser
@u.wraps(u.m/u.s, [u.m], False)
def v_sed_diffuser(w_tank):
    """Return the velocity through each diffuser.

    Parameters
    ----------
    w_tank : float
        Width of the sedimentation tank

    Returns
    -------
    float
        Flow through each diffuser in the sedimentation tank

    Examples
    --------
    >>> from aide_design.play import*
    >>>

    """
    return (q_diffuser_max(w_tank).magnitude
            / (w_diffuser_inner(w_tank) * L_diffuser_inner(w_tank)).magnitude)

@u.wraps(u.m**3/u.s, [u.m, u.m], False)
def q_tank_max(w_tank, L_upflow_max):
    """Return the maximum flow throughout one sedimentation tank.

    Parameters
    ----------
    w_tank : float
        Width of the sedimentation tank

    L_upflow_max : float
        Length of the active part of the sedimentation tank

    Returns
    -------
    float
        Maximum flow through one sedimentation tank

    Examples
    --------
    >>> from aide_design.play import*
    >>>

    """
    return (L_upflow_max * con.VEL_SED_UP_BOD * w_tank)


@u.wraps(None, [u.m**3/u.s, u.m, u.m], False)
def n_tanks(q_plant, w_tank, L_upflow_max):
    """Return the number of sedimentation tanks required for a given flow rate.

    Parameters
    ----------
    var1 : float
        Total plant flow rate

    var2 : float
        Width of the sedimentation tank

    var3 : float
        Length of the active part of the sedimentation tank

    Returns
    -------
    int
        Number of sedimentation tanks required for a given flow rate.

    Examples
    --------
    >>> from aide_design.play import*
    >>>

    """
    q_max = q_tank_max(w_tank, L_upflow_max).magnitude
    return (int(np.ceil(q_plant / q_max)))

@u.wraps(u.m, [u.m**3/u.s, u.m, u.m], False)
def L_channel(q_plant, w_tank, L_upflow_max):
    """Return the length of the inlet and exit channels for the sedimentation tank.

    Parameters
    ----------
    var1 : float
        Total plant flow rate

    var2 : float
        Width of the sedimentation tank

    var3 : float
        Length of the active part of the sedimentation tank

    Returns
    -------
    float
        Length of the inlet and exit channels for the sedimentation tank.

    Examples
    --------
    >>> from aide_design.play import*
    >>>

    """
    n_tanks = n_tanks(q_plant, w_tank, L_upflow_max)
    return ((n_tanks * w_tank) + opt.THICKNESS_SED_WALL + ((n_tanks-1) * opt.THICKNESS_SED_WALL))
