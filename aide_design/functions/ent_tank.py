"""This file contains all the functions needed to design an entrance tank for
an AguaClara plant.

"""
import numpy as np
from aide_design.shared.units import unit_registry as u
import aide_design.shared.physchem as pc
import aide_design.shared.constants as con
import aide_design.shared.materials_database as mat

@u.wraps(u.inch, [u.m**3/u.s, u.degK, u.m, None], False)
def drain_OD(q_plant, temp, depth_end, sdr=26):
    """Return the outer diameter of the entrance tank drain pipe. Depth at the
    end of the flocculator is used for headloss and length calculation inputs in
    the diam_pipe calculation.

    Parameters
    ----------
    q_plant : float
        Plant flow rate

    temp: float
        Design temperature

    depth_end: float
        The depth of water at the end of the flocculator

    sdr : float
        Standard dimension ratio

    Returns
    -------
    float
        the outer diameter of the entrance tank drain pipe

    Examples
    --------
    >>> from aide_design.play import*
    >>> drain_OD(20*u.L/u.s, 15*u.degC, 2*u.m)
    4.5 inch

    """
    nu = pc.viscosity_kinematic(temp)
    K_minor = (con.K_MINOR_PIPE_ENTRANCE +
               con.K_MINOR_PIPE_EXIT + con.K_MINOR_EL90)
    drain_ID = pc.diam_pipe(q_plant, depth_end, depth_end, nu, mat.PIPE_ROUGH_PVC, K_minor)
    drain_ND = pipe.ND_SDR_available(drain_ID, sdr)
    return pipe.OD(drain_ND).magnitude

@u.wraps(None, [u.m**3/u.s, u.m], False)
def num_plates(q_plant, W_chan, S_plate=2.5*u.cm, thickness_plate=2*u.mm,
               vel_capture=8*u.mm/u.s, angle_plate=50*u.deg):
    """Return the number of plates in the entrance tank.

    This number minimizes the total length of the plate settler unit.

    Parameters
    ----------
    q_plant : float
        Plant flow rate

    W_chan : float
        Width of channel

    S_plate : float
        Edge to edge distance between plate settlers

    thickness_plate : float
        Thickness of PVC sheet used to make plate settlers

    vel_capture : float
        Capture velocity of the plate settlers. This is the velocity of the
        floc that is only barely settled-out, or "captured", during the
        sedimentation process

    angle_plate : float
        Angle of plates in the plate settler module

    Returns
    -------
    float
        the number of plates in the entrance tank

    Examples
    --------
    >>> from aide_design.play import *
    >>> num_plates_ent_tank(20*u.L/u.s,0.25*u.m)
    >>> 1.0
    >>> num_plates_ent_tank(120*u.L/u.s,125*u.m)
    >>> 2.0
    """
    B_plate = S_plate + thickness_plate
    N_plates = np.ceil(np.sqrt(q_plant/B_plate.to(u.m).magnitude
                       * W_chan * vel_capture.to(u.m/u.s).magnitude *
                       np.sin(angle_plate.to(u.rad).magnitude)))
    return N_plates

@u.wraps(u.m, [u.m**3/u.s, u.m, None], False)
def L_plate(q_plant, W_chan, S_plate=2.5*u.cm, vel_capture=8*u.mm/u.s,
            angle_plate=50*u.deg):
    """Return the length of the plates in the entrance tank.

    Parameters
    ----------
    q_plant : float
        Plant flow rate

    W_chan : float
        Width of channel

    S_plate : float
        Edge to edge distance between plate settlers

    vel_capture : float
        Capture velocity of the plate settlers. This is the velocity of the
        floc that is only barely settled-out, or "captured", during the
        sedimentation process

    angle_plate : float
        Angle of plates in the plate settler module

    Returns
    -------
    float
        the length of the plates in the entrance tank

    Examples
    --------
    >>> from aide_design.play import *
    >>> L_plate_ent_tank(20*u.L/u.s, 0.25*u.m)
    >>> 15.527444428789268 meter
    >>> L_plate_ent_tank(30*u.L/u.s, 125*u.m)
    >>> 0.016877874990957113 meter
    """
    L_plate = ((q_plant/(num_plates_ent_tank(q_plant, W_chan) * W_chan *
               vel_capture.to(u.m/u.s).magnitude *
               np.cos(angle_plate.to(u.rad).magnitude)))
               - (S_plate.to(u.m).magnitude *
               np.tan(angle_plate.to(u.rad).magnitude)))
    return L_plate

@u.wraps(None, [u.m**3/u.s, u.degK, u.m, u.m, None], False)
def ent_tank_agg(q_plant, temp, depth_end, W_chan, ent_tank_inputs=ent_tank_dict):
    """Aggregates the entrance tank functions into a single function which
    outputs a dictionary of all the necessary design parameters.

    Parameters
    ----------
    q_plant : float
        Plant flow rate

    temp: float
        Design temperature

    depth_end: float
        The depth of water at the end of the flocculator

    W_chan: float
        The width of the channel

    Returns
    -------
    float
        ?

    Examples
    --------
    >>> from aide_design.play import*
    >>> ent_tank_dict = {'sdr': 26, 'S_plate': 2.5*u.cm, 'angle_plate': 50*u.deg,
    ...                  'vel_capture': 8 * u.mm/u.s, 'L_max': 2.2*u.m,
    ...                  'thickness_plate': 2*u.mm}
    >>> ent_tank_agg(20*u.L/u.s, 20*u.degC, 2*u.m, 45*u.cm, ent_tank_dict)
    {'L_max': <Quantity(2.2, 'meter')>,
    'L_plate': <Quantity(8.613116309409655, 'meter')>
    'N_plates': 1.0
    'OD_drain': <Quantity(4.5, 'inch')>
    'S_plate': <Quantity(2.5, 'centimeter')>,
    'angle_plate': <Quantity(50, 'degree')>,
    'sdr': 26,
    'thickness_plate': <Quantity(2, 'millimeter')>,
    'vel_capture': <Quantity(8.0, 'millimeter / second')>}

    """
    # calculate the outer diameter of the drain pipe
    OD_drain = drain_OD(q_plant, temp, depth_end, sdr)
    # calculate the number of plates in the plate settler module
    N_plates = num_plates_ent_tank(q_plant, W_chan, ent_tank_inputs)
    # calculate the length of of a plate in the entrance tank
    L_plate = L_plate_ent_tank(q_plant, W_chan, ent_tank_inputs)
    ent_tank_inputs.update({'OD_drain': OD_drain, 'N_plates': N_plates,
                            'L_plate': L_plate})
    return ent_tank_inputs
