"""This file contains all the functions needed to design an entrance tank for
an AguaClara plant.

Attributes
----------
sdr : int
    Ratio between outer diameter and wall thickness

S_plate : float
    Edge to edge distance between plates in the plate settler module

angle_plate : float
    Angle of plates in the plate settler module

vel_capture : floats
    Design capture velocity

L_max : float
    Maximum length of the entire entrance tank

thickness_plate : float
    thickness of plates in the plate settelr module

"""
from aide_design.play import*

# document what's in ent_tank_dict here
ent_tank_dict = {'sdr': 26, 'S_plate': 2.5*u.cm, 'angle_plate': 50*u.deg,
                 'vel_capture': 8 * u.mm/u.s, 'L_max': 2.2*u.m,
                 'thickness_plate': 2*u.mm}

@u.wraps(u.inch, [u.m**3/u.s, u.degK, u.m, None], False)
def drain_OD(q_plant, temp, depth_end, ent_tank_inputs=ent_tank_dict):
    """Return the outer diameter of the entrance tank drain pipe. Depth at the
    end of the flocculator is used for headloss and length calculation inputs in
    the diam_pipe calculation."""
    nu = pc.viscosity_kinematic(temp)
    K_minor = (con.K_MINOR_PIPE_ENTRANCE
               con.K_MINOR_PIPE_EXIT + con.K_MINOR_EL90)
    drain_ID = pc.diam_pipe(q_plant, depth_end, depth_end, nu, mat.PIPE_ROUGH_PVC, K_minor)
    drain_ND = pipe.ND_SDR_available(drain_ID, ent_tank_inputs['sdr'])
    return pipe.OD(drain_ND)

@u.wraps(None, [u.m**3/u.s, u.m, None], False)
def num_plates_ent_tank(q_plant, W_chan, ent_tank_inputs=ent_tank_dict):
    """Return the number of plates in the entrance tank.

    This number minimizes the total length of the plate settler unit."""
    B_plate = ent_tank_inputs['S_plate'] + ent_tank_inputs['thickness_plate']
    N_plates = np.ceil(np.sqrt(q_plant/B_plate.to(u.m).magnitude
                       * W_chan * ent_tank_inputs['vel_capture'].to(u.m/u.s).magnitude *
                       np.sin(ent_tank_inputs['angle_plate'].to(u.rad).magnitude))))
    return N_plates

@u.wraps(u.m, [u.m**3/u.s, u.m, None], False)
def L_plate_ent_tank(q_plant, W_chan, ent_tank_inputs=ent_tank_dict):
    """Return the length of the plates in the entrance tank."""
    L_plate = ((q_plant/(num_plates_ent_tank(q_plant, W_chan) * W_chan *
               ent_tank_inputs['vel_capture'].to(u.m/u.s).magnitude *
               np.cos(ent_tank_inputs['angle_plate'].to(u.rad).magnitude)))
               - (ent_tank_inputs['S_plate'].to(u.m).magnitude *
               np.tan(ent_tank_inputs['angle_plate'].to(u.rad).magnitude)))
    return L_plate

@u.wraps([u.inch, None, u.m], [u.m**3/u.s, u.degK, u.m, u.m, None], False)
def ent_tank_agg(q_plant, temp, depth_end, W_chan, ent_tank_inputs=ent_tank_dict):
    OD_drain = drain_OD(q_plant, temp, depth_end, ent_tank_inputs).magnitude
    N_plates = num_plates_ent_tank(q_plant, W_chan, ent_tank_inputs).magnitude
    L_plate = L_plate_ent_tank(q_plant, W_chan, ent_tank_inputs).magnitude
    return ent_tank_inputs.update({'OD_drain': OD_drain, 'N_plates': N_plates,
                                   'L_plate': L_plate})
