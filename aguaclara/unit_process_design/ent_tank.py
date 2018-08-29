"""This file contains all the functions needed to design an entrance tank for
an AguaClara plant.

"""
from aguaclara.play import*

@u.wraps(u.inch, [u.m**3/u.s, u.degK, u.m, None], False)
def drain_OD(q_plant, T, depth_end, SDR):
    """Return the nominal diameter of the entrance tank drain pipe. Depth at the
    end of the flocculator is used for headloss and length calculation inputs in
    the diam_pipe calculation.

    Parameters
    ----------
    q_plant: float
        Plant flow rate

    T: float
        Design temperature

    depth_end: float
        The depth of water at the end of the flocculator

    SDR: float
        Standard dimension ratio

    Returns
    -------
    float
        ?

    Examples
    --------
    >>> from aguaclara.play import*
    ??
    """
    nu = pc.viscosity_kinematic(T)
    K_minor = con.K_MINOR_PIPE_ENTRANCE + con.K_MINOR_PIPE_EXIT + con.K_MINOR_EL90
    drain_ID = pc.diam_pipe(q_plant, depth_end, depth_end, nu, mat.PIPE_ROUGH_PVC, K_minor)
    drain_ND = pipe.ND_SDR_available(drain_ID, SDR)
    return pipe.OD(drain_ND).magnitude

@u.wraps(None, [u.m**3/u.s, u.m], False)
def num_plates_ET(q_plant, W_chan):
    """Return the number of plates in the entrance tank.

    This number minimizes the total length of the plate settler unit.

    Parameters
    ----------
    q_plant: float
        Plant flow rate

    W_chan: float
        Width of channel

    Returns
    -------
    float
        ?

    Examples
    --------
    >>> from aguaclara.play import*
    >>> num_plates_ET(20*u.L/u.s,2*u.m)
    1.0
    """
    num_plates = np.ceil(np.sqrt(q_plant/(con.DIST_CENTER_ENT_TANK_PLATE.magnitude
    * W_chan * con.VEL_ENT_TANK_CAPTURE_BOD.magnitude * np.sin(con.AN_ENT_TANK_PLATE.to(u.rad).magnitude))))
    return num_plates

@u.wraps(u.m, [u.m**3/u.s, u.m], False)
def L_plate_ET(q_plant, W_chan):
    """Return the length of the plates in the entrance tank.

    Parameters
    ----------
    q_plant: float
        Plant flow rate

    W_chan: float
        Width of channel

    Returns
    -------
    float
        ?

    Examples
    --------
    >>> from aguaclara.play import*
    >>> L_plate_ET(20*u.L/u.s,2*u.m)
    0.00194
    """
    L_plate = (q_plant/(num_plates_ET(q_plant, W_chan) * W_chan *
    con.VEL_ENT_TANK_CAPTURE_BOD.magnitude * np.cos(con.AN_ENT_TANK_PLATE.to(u.rad).magnitude)))
    - (con.SPACE_ENT_TANK_PLATE.magnitude * np.tan(con.AN_ENT_TANK_PLATE.to(u.rad).magnitude))
    return L_plate
