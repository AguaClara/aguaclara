"""This file contains all the functions needed to design an entrance tank for
an AguaClara plant.

"""
from aide_design.play import*

ent_tank_dict = {'sdr': 26, 'K_MINOR_PIPE_ENTRANCE': 0.5,
                 'K_MINOR_PIPE_EXIT': 1, 'K_MINOR_EL90': 0.9,
                 'B_plate': 2.52*u.cm, 'S_plate': 2.5*u.cm,
                 'vel_capture': 8 * u.mm/u.s, 'L_max': 2.2*u.m,
                 'PIPE_ROUGH_PVC': 0.12*u.mm, 'angle_plate': 50*u.deg}

@u.wraps(u.inch, [u.m**3/u.s, u.degK, u.m, None], False)
def drain_OD(q_plant, temp, depth_end, ent_tank_inputs=ent_tank_dict):
    """Return the nominal diameter of the entrance tank drain pipe. Depth at the
    end of the flocculator is used for headloss and length calculation inputs in
    the diam_pipe calculation."""
    nu = pc.viscosity_kinematic(temp)
    K_minor = (ent_tank_dict['K_MINOR_PIPE_ENTRANCE'] +
               ent_tank_dict['K_MINOR_PIPE_EXIT'] + ent_tank_dict['K_MINOR_EL90'])
    drain_ID = pc.diam_pipe(q_plant, depth_end, depth_end, nu, ent_tank_dict['PIPE_ROUGH_PVC'], K_minor)
    drain_ND = pipe.ND_SDR_available(drain_ID, ent_tank_dict['sdr'])
    return pipe.OD(drain_ND)

@u.wraps(None, [u.m**3/u.s, u.m, None], False)
def num_plates_ent_tank(q_plant, W_chan, ent_tank_inputs=ent_tank_dict):
    """Return the number of plates in the entrance tank.

    This number minimizes the total length of the plate settler unit."""
    N_plates = np.ceil(np.sqrt(q_plant/(ent_tank_dict['B_plate'].to(u.m).magnitude
                       * W_chan * ent_tank_dict['vel_capture'].to(u.m/u.s).magnitude *
                       np.sin(ent_tank_dict['angle_plate'].to(u.rad).magnitude))))
    return N_plates

@u.wraps(u.m, [u.m**3/u.s, u.m, None], False)
def L_plate_ent_tank(q_plant, W_chan, ent_tank_inputs=ent_tank_dict):
    """Return the length of the plates in the entrance tank."""
    L_plate = ((q_plant/(num_plates_ent_tank(q_plant, W_chan) * W_chan *
               ent_tank_dict['vel_capture'].to(u.m/u.s).magnitude *
               np.cos(ent_tank_dict['angle_plate'].to(u.rad).magnitude)))
               - (ent_tank_dict['S_plate'].to(u.m).magnitude *
               np.tan(ent_tank_dict['angle_plate'].to(u.rad).magnitude)))
    return L_plate

@u.wraps([u.inch, None, u.m], [u.m**3/u.s, u.degK, u.m, u.m, None], False)
def ent_tank(q_plant, temp, depth_end, W_chan, ent_tank_inputs=ent_tank_dict):
    ND_drain = drain_OD(q_plant, temp, depth_end, ent_tank_inputs=ent_tank_dict).magnitude
    N_plates = num_plates_ent_tank(q_plant, W_chan, ent_tank_inputs=ent_tank_dict).magnitude
    L_plate = L_plate_ent_tank(q_plant, W_chan, ent_tank_inputs=ent_tank_dict).magnitude
    return ND_drain, N_plates, L_plate
