import numpy as np
import aide_design.shared.pipedatabase as pipe
from aide_design.shared.units import unit_registry as u
import aide_design.shared.physchem as pc
import aide_design.shared.constants as con
import aide_design.shared.materials_database as mat


class EntTank():
    #I've forced everything into proper units here (meters & radians) so that later functions are actually sane.
    @u.wraps(None, [None, u.m ** 3 / u.s, u.degK, u.m, u.m, None, u.m, u.m, u.m/u.s, u.rad], False)
    def __init__(self, q_plant, temp, depth_end, W_chan, ent_tank_inputs,
                 S_plate, thickness_plate, vel_capture, angle_plate):
        self.q_plant = q_plant
        self.temp = temp
        self.depth_end = depth_end
        self.w_chan = W_chan
        self.inputs = ent_tank_inputs
        self.s_plate = S_plate
        self.thickness_plate = thickness_plate
        self.vel_capture = vel_capture
        self.angle_plate = angle_plate

#inches? Really? That doesn't align with the standards on the wiki. Or do we keep pipe diameters in inches?
    @u.wraps(u.inch, [None, None], False)
    def drain_OD(self, sdr=26):
        nu = pc.viscosity_kinematic(self.temp)
        K_minor = (con.K_MINOR_PIPE_ENTRANCE +
                   con.K_MINOR_PIPE_EXIT + con.K_MINOR_EL90)
        drain_ID = pc.diam_pipe(self.q_plant, self.depth_end, self.depth_end, nu, mat.PIPE_ROUGH_PVC, K_minor)
        drain_ND = pipe.ND_SDR_available(drain_ID, sdr)
        return pipe.OD(drain_ND).magnitude

    @u.wraps(None, None, False)
    def num_plates(self)
        return np.ceil(np.sqrt(self.q_plant/(self.s_plate + self.thickness_plate) * self.w_chan * self.vel_capture
                               * np.sin(self.angle_plate)))

    @u.wraps(u.m, None, False)
    def l_plate(self):
        return ((self.q_plant / (self.num_plates() * self.w_chan * self.vel_capture * np.cos(self.angle_plate)))
                - (self.s_plate * np.tan(self.angle_plate)))

    @u.wraps(None, None, False)
    def agg(self):
        OD_drain = self.drain_OD()
        N_plates = self.num_plates()
        L_plate = self.l_plate()
        self.inputs.update({'OD_drain': OD_drain, 'N_plates': N_plates, 'L_plate': L_plate})
        return self.inputs