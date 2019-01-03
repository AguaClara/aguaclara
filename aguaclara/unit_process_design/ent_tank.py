"""This file contains all the functions needed to design an entrance tank for
an AguaClara plant.

"""
import design.ent_tank
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
    K_minor = con.PIPE_ENTRANCE_K_MINOR + con.PIPE_EXIT_K_MINOR + con.EL90_K_MINOR
    drain_ID = pc.diam_pipe(q_plant, depth_end, depth_end, nu, mat.PVC_PIPE_ROUGH, K_minor)
    drain_ND = pipe.SDR_available_ND(drain_ID, SDR)
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
    num_plates = np.ceil(np.sqrt(q_plant / (design.ent_tank.CENTER_PLATE_DIST.magnitude
                                            * W_chan * design.ent_tank.CAPTURE_BOD_VEL.magnitude * np.sin(
                design.ent_tank.PLATE_ANGLE.to(u.rad).magnitude))))
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
    L_plate = (q_plant / (num_plates_ET(q_plant, W_chan) * W_chan *
                          design.ent_tank.CAPTURE_BOD_VEL.magnitude * np.cos(
                design.ent_tank.PLATE_ANGLE.to(u.rad).magnitude)))
    - (design.ent_tank.PLATE_S.magnitude * np.tan(design.ent_tank.PLATE_ANGLE.to(u.rad).magnitude))
    return L_plate
