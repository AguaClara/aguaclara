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

print(n_sed_plates_max(2.5*u.cm))

@u.wraps(u.L/u.s, [u.m, u.m], False)
def diffuser_max_flow(W_sed_tank, L_sed_diffuser_outer):
    """Return the flow through each diffuser.

    Parameters
    ----------
    var1 : float
        Width of the sedimentation tank

    var2 : float
        Outer length of the diffusers

    Returns
    -------
    float
        Flow through each diffuser in the sedimentation tank

    Examples
    --------
    >>> from aide_design.play import*
    >>>

    """
    return con.VEL_SED_UP_BOD * W_sed * L_sed_diffuser_outer
