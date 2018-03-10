"""This file contains all the functions needed to design a sedimentation tank
for an AguaClara plant.

"""
from aide_design.play import*

@u.wraps(None, [u.cm], False)
def n_sed_plates_max(dist_center_sed_plate):
    """Return the maximum number of plate settlers possible given the center
    to center distance.

    Parameters
    ----------
    var1 : float
        Center to center distance between plate settlers

    Returns
    -------
    int
        Maximum number of plates

    Examples
    --------
    >>> from aide_design.play import*
    >>>

    """
    return math.floor((mat.LENGTH_SED_PLATE_CANTILEVERED/dist_center_sed_plate * np.tan(con.ANGLE_SED_PLATE.to(u.rad).magnitude)) + 1)

@u.wraps(u.m, [u.m], False)
def w_diffuser_inner_min(W_sed_tank):
    """Return the minimum inner width of each diffuser in the sedimentation tank.

    Parameters
    ----------
    var1 : float
        Width of the sedimentation tank

    Returns
    -------
    float
        Minimum inner width of each diffuser in the sedimentation tank

    Examples
    --------
    >>> from aide_design.play import*
    >>>

    """
    return (con.VEL_SED_UP_BOD.magnitude / con.V_SED_DIFFUSER_MAX.magnitude) * W_sed_tank

@u.wraps(u.m, [u.m], False)
def w_diffuser_inner(W_sed_tank):
    """Return the inner width of each diffuser in the sedimentation tank.

    Parameters
    ----------
    var1 : float
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
    return ut.ceil_nearest(w_diffuser_inner_min(W_sed_tank).magnitude, (np.arange(1/16,1/4,1/16)*u.inch).magnitude)

@u.wraps(u.m, [u.m], False)
def w_diffuser_outer(W_sed_tank):
    """Return the outer width of each diffuser in the sedimentation tank.

    Parameters
    ----------
    var1 : float
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
    return w_diffuser_inner_min(W_sed_tank).magnitude + (2 * con.T_DIFFUSER)

@u.wraps(u.m, [u.m], False)
def L_diffuser_outer(W_sed_tank):
    """Return the outer length of each diffuser in the sedimentation tank.

    Parameters
    ----------
    var1 : float
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
    return con.AREA_PVC_DIFFUSER.magnitude / (2 * con.T_DIFFUSER.magnitude) - w_diffuser_inner(W_sed_tank).magnitude

@u.wraps(u.m, [u.m], False)
def L_diffuser_inner(W_sed_tank):
    """Return the inner length of each diffuser in the sedimentation tank.

    Parameters
    ----------
    var1 : float
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
    return L_diffuser_outer(W_sed_tank).magnitude - (2 * con.T_DIFFUSER.magnitude)

@u.wraps(u.L/u.s, [u.m], False)
def flow_diffuser_max(W_sed_tank):
    """Return the flow through each diffuser.

    Parameters
    ----------
    var1 : float
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
    return con.VEL_SED_UP_BOD.magnitude * W_sed_tank * L_diffuser_outer(W_sed_tank).magnitude

# still need to calculate V_sed_diffuser
@u.wraps(u.L/u.s, [u.m], False)
def V_sed_diffuser(W_sed_tank):
    """Return the flow through each diffuser.

    Parameters
    ----------
    var1 : float
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
    return (flow_diffuser_max(W_sed_tank).magnitude
                    / (w_diffuser_inner(W_sed_tank) * L_diffuser_inner(W_sed_tank)).magnitude)
