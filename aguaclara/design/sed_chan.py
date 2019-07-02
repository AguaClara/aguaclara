from aguaclara.core.units import unit_registry as u
import aguaclara.core.constants as con
import aguaclara.core.materials as mat
import aguaclara.core.utility as ut
import aguaclara.core.physchem as pc
import aguaclara.core.pipes as pipe
import aguaclara.core.head_loss as hl
import aguaclara.design.human_access as ha
from aguaclara.design.component import Component

import numpy as np
import math


class SedimentationChannel(Component):

    SED_TANK_Q_RATIO = 0.95
    PLANT_FREE_BOARD_H = 5 * u.cm
    WEIR_FREE_BOARD_H = 2 * u.cm
    SED_DEPTH_EST = 2 * u.m

    q=20.0 * u.L / u.s
    temp=20.0 * u.degC
    
    sed_tank_n=4
    sed_tank_w_inner=42.0 * u.inch
    sed_tank_wall_thickness=15.0 * u.cm
    sed_tank_inlet_man_nd=60 * u.cm
    sed_tank_outlet_man_nd= 60. * u.cm
    sed_tank_outlet_man_hl=4*u.cm
    sed_wall_thickness = 15.0 * u.cm
    sed_tank_diffuser_hl=0.09 * u.mm

    weir_thickness = 15.0 * u.cm
    weir_hl = 5 * u.cm
    w_min = 30.0 * u.cm
    fitting_s = 15. * u.cm
    inlet_depth_max = 50 * u.cm
    drain_sdr = 26
    outlet_free_h = 5.0 * u.cm
    outlet_pipe_sdr = 41.0
    outlet_pipe_hl_max = 1.0 * u.cm
    outlet_pipe_nd_max = 8 * u.inch

    @property
    def l(self):
        l = (self.sed_tank_n * self.sed_tank_w_inner) + \
            ((self.sed_tank_n-1) * self.sed_tank_wall_thickness) + \
            self.sed_wall_thickness
        return l.to(u.m)

    @property
    def weir_exit_hl(self):
        weir_exit_hl = pc.headloss_weir(self.q, self.l)
        return weir_exit_hl

    @property
    def inlet_hl_max(self):
        inlet_hl_max = (self.sed_tank_outlet_man_hl + self.sed_tank_diffuser_hl) * \
            (1 - self.SED_TANK_Q_RATIO ** 2)
        return inlet_hl_max

    @property
    def _inlet_w_pre_weir_plumbing_min(self):
        inlet_w_pre_weir_plumbing_min = pipe.fitting_od(self.sed_tank_inlet_man_nd) + \
            2 * self.fitting_s
        return inlet_w_pre_weir_plumbing_min
    
    @property
    def _inlet_w_pre_weir_hl_min(self):
        inlet_w_pre_weir_hl_min = pc.horiz_chan_w(
            self.q,
            self.inlet_depth_max,
            self.inlet_hl_max,
            self.l,
            pc.viscosity_kinematic(self.temp),
            mat.CONCRETE_PIPE_ROUGH,
            False,
            0
        )
        return inlet_w_pre_weir_hl_min

    @property
    def inlet_w_pre_weir(self):
        inlet_w_pre_weir = max(
            self._inlet_w_pre_weir_plumbing_min, 
            self._inlet_w_pre_weir_hl_min)
        return inlet_w_pre_weir

    @property
    def inlet_depth_plumbing_min(self):
        inlet_plumbing_depth_min = self.sed_tank_outlet_man_hl + self.sed_tank_diffuser_hl + \
            pipe.fitting_od(self.sed_tank_outlet_man_nd) + \
                self.fitting_s + self.weir_exit_hl
        return inlet_plumbing_depth_min

    @property
    def inlet_depth_hl(self):
        inlet_chan_hl_depth = pc.horiz_chan_h(
            self.q, 
            self.inlet_w_pre_weir, 
            self.inlet_hl_max, 
            self.l, 
            pc.viscosity_kinematic(self.temp),
            mat.CONCRETE_PIPE_ROUGH,
            False)
        return inlet_chan_hl_depth
    
    @property
    def inlet_depth(self):    
        inlet_depth = max(self.inlet_depth_plumbing_min, self.inlet_depth_hl) 
        return inlet_depth

    @property
    def inlet_weir_hl(self):
        inlet_weir_hl = pc.headloss_weir(self.q, self.l)
        return inlet_weir_hl

    @property
    def inlet_h(self):
        inlet_h = self.inlet_depth + self.PLANT_FREE_BOARD_H
        return inlet_h

    @property
    def inlet_weir_h(self):
        inlet_chan_h_weir = self.inlet_depth + self.WEIR_FREE_BOARD_H
        return inlet_chan_h_weir
        
    @property
    def inlet_w_post_weir(self):
        inlet_w_post_weir = max(
            self.w_min, 
            pc.horiz_chan_w(
                self.q, 
                self.inlet_h, 
                self.inlet_h, 
                self.l,
                pc.viscosity_kinematic(self.temp), 
                mat.CONCRETE_PIPE_ROUGH, 
                1,
                0 ))
        return inlet_w_post_weir

    @property
    def inlet_w(self):
        inlet_w = self.inlet_w_pre_weir + self.weir_thickness + self.inlet_w_post_weir
        return inlet_w

    @property
    def drain_nd(self):
        drain_nd = pc.pipe_flow_nd(
            self.q,
            self.drain_sdr,
            self.SED_DEPTH_EST,
            self.SED_DEPTH_EST + self.inlet_w,
            pc.viscosity_kinematic(self.temp),
            mat.PVC_PIPE_ROUGH,
            hl.PIPE_ENTRANCE_K_MINOR + hl.PIPE_EXIT_K_MINOR + hl.EL90_K_MINOR
        )
        return drain_nd

    @property
    def inlet_drain_box_w(self):
        inlet_drain_box_w = max( 2 * self.fitting_s + pipe.fitting_od(self.drain_nd), self.inlet_w_post_weir)
        return inlet_drain_box_w

    @property
    def outlet_depth(self):
        outlet_depth = self.inlet_depth - self.sed_tank_outlet_man_hl - \
           self.sed_tank_diffuser_hl
        return outlet_depth
    
    @property
    def outlet_weir_depth(self):
        outlet_weir_depth = self.outlet_depth - self.weir_hl - self.WEIR_FREE_BOARD_H
        return outlet_weir_depth

    @property
    def outlet_pre_weir_w(self):
        return self.w_min
    @property
    def outlet_pipe_l(self):
        outlet_pipe_l = ha.DRAIN_CHAN_WALKWAY_W + self.inlet_w + 1.0 * u.m
        return outlet_pipe_l
        
    @property
    def outlet_pipe_q_max(self):
        outlet_pipe_q_max = pc.flow_pipe(
            pipe.ID_SDR(self.outlet_pipe_nd_max, self.outlet_pipe_sdr),
            self.outlet_pipe_hl_max,
            self.outlet_pipe_l,
            pc.viscosity_kinematic(self.temp),
            mat.PVC_PIPE_ROUGH, 
            2 * hl.EL90_K_MINOR + hl.PIPE_ENTRANCE_K_MINOR + \
                 hl.PIPE_EXIT_K_MINOR
        )
        return outlet_pipe_q_max.to(u.L / u.s)

    @property
    def outlet_pipe_n(self):
        outlet_pipe_n = math.ceil(self.q / self.outlet_pipe_q_max)
        return outlet_pipe_n

    @property
    def outlet_pipe_q(self):
        outlet_pipe_q = self.q / self.outlet_pipe_n
        return outlet_pipe_q

    @property
    def outlet_pipe_nd(self):
        outlet_pipe_nd = pc.pipe_flow_nd(
            self.outlet_pipe_q, 
            self.outlet_pipe_sdr, 
            self.outlet_pipe_hl_max, 
            self.outlet_pipe_l, 
            pc.viscosity_kinematic(self.temp), 
            mat.PVC_PIPE_ROUGH, 
            2 * hl.EL90_K_MINOR + hl.PIPE_ENTRANCE_K_MINOR + \
                 hl.PIPE_EXIT_K_MINOR
        )
        return outlet_pipe_nd
    @property
    def outlet_post_weir_w(self):
        outlet_post_weir_w = max(
            #need self.outlet_to_filter_nd
            self.fitting_s + pipe.fitting_od(self.outlet_pipe_nd), 
            self.fitting_s + pipe.fitting_od(self.drain_nd), 
            self.w_min, 
            pc.horiz_chan_w(
                self.q,
                self.outlet_weir_depth - self.outlet_free_h, #what is outlet_free_h
                self.outlet_weir_depth,
                self.l,
                pc.viscosity_kinematic(self.temp),
                mat.PVC_PIPE_ROUGH,
                1,
                hl.PIPE_ENTRANCE_K_MINOR + hl.PIPE_EXIT_K_MINOR + hl.EL90_K_MINOR
            )
        )
        return outlet_post_weir_w

    @property
    def outlet_w(self):
        outlet_w = self.outlet_pre_weir_w + self.weir_thickness + \
            self.outlet_post_weir_w
        return outlet_w

    @property
    def outlet_drain_box_w(self):
        outlet_drain_box_w = max(
            self.fitting_s + pipe.fitting_od(self.drain_nd),
            self.outlet_post_weir_w
            )
        return outlet_drain_box_w

    @property
    def outlet_weir_h(self):
        outlet_weir_h = self.outlet_weir_depth + self.WEIR_FREE_BOARD_H
        return outlet_weir_h
    
    @property
    def w_outer(self):
        w_outer = self.outlet_w + 2 * self.weir_thickness + self.inlet_w + self.sed_wall_thickness
        return w_outer
    
    @property
    def inlet_last_coupling_h(self):
        last_coupling_h = self.outlet_weir_depth - 2 * u.cm
        return last_coupling_h
    
    @property
    def inlet_step_h(self):
        step_h = self.inlet_last_coupling_h / max(1, self.sed_tank_n - 1)
        return step_h
    
    @property
    def inlet_slope_l(self):
        inlet_slope_l = self.l + self.sed_wall_thickness - \
            pipe.fitting_od(self.sed_tank_inlet_man_nd) - self.fitting_s 
        return inlet_slope_l