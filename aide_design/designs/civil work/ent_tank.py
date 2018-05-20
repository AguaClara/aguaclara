from aide_design.shared.units import unit_registry as u
from aide_render.builder_classes import DP, HP


class EntTank:

    ############## ATTRIBUTES ################
    S_plate = HP(0.025, u.m)
    thickness_plate = HP(0.002, u.m)
    vel_capture = HP(0.008, u.m/u.s)
    angle_plate = HP(50, u.deg)
    sdr = HP(26)
    temp = HP(15, u.degC)

    ############### METHODS #################
    from aide_design.functions.ent_tank import (
        drain_OD,
        num_plates,
        L_plate
    )

    drain_OD = staticmethod(drain_OD)
    num_plates = staticmethod(num_plates)
    L_plate = staticmethod(L_plate)

    # Init should only require Q_plant and W_chan
    # take a look at how the Floc class handles it with a dictionary for
    # overrides
    def __init__(self, q_plant, depth_end, W_chan, bod=None):

        if bod:
            for k, v in bod.items():
                setattr(self, k, v)

        OD_drain = DP(self.drain_OD(q_plant, self.temp, depth_end, self.sdr))
        N_plates = DP(self.num_plates(q_plant, W_chan, self.S_plate,
                                      self.thickness_plate, self.vel_capture,
                                      self.angle_plate))
        L_plate = DP(self.L_plate(q_plant, W_chan, self.S_plate,
                                  self.vel_capture, self.angle_plate))
