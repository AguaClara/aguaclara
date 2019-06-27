from aguaclara.core.units import unit_registry as u
import aguaclara.core.constants as con
import aguaclara.core.materials as mat
import aguaclara.core.utility as ut
import aguaclara.core.physchem as pc
import aguaclara.core.pipes as pipe
from aguaclara.design.component import Component

import numpy as np
import math


class SedimentationChannel(Component):

    SED_TANK_Q_RATIO = 0.95
    PLANT_FREE_BOARD_H = 5 * u.cm
    INLET_WEIR_FREE_BOARD_H = 2 * u.cm

    def __init__(self, q=20.0 * u.L / u.s, temp=20.0 * u.degC,
                 sed_tank_n=4,
                 sed_tank_w_inner=42.0 * u.inch,
                 sed_tank_wall_thickness=15.0 * u.cm,
                 sed_tank_inlet_man_nd=60 * u.cm,
                 sed_tank_outlet_man_nd= 60. * u.cm,
                 sed_tank_outlet_man_hl=4*u.cm,
                 sed_wall_thickness = 15.0 * u.cm,
                 sed_tank_diffuser_hl=0.09 * u.mm,

                 weir_thickness = 15.0 * u.cm,
                 w_min = 30.0 * u.cm,
                 outlet_man_bod_hl = 15.0 * u.cm,
                 fitting_s = 15. * u.cm,
                 inlet_depth_max = 50 * u.cm,
                 drain_sdr = 26):
        super().__init__(q = q, temp = temp)

        self.sed_tank_n = sed_tank_n
        self.sed_tank_w_inner = sed_tank_w_inner
        self.sed_tank_wall_thickness = sed_tank_wall_thickness
        self.sed_tank_inlet_man_nd = sed_tank_inlet_man_nd
        self.sed_tank_outlet_man_nd = sed_tank_outlet_man_nd
        self.sed_tank_outlet_man_hl = sed_tank_outlet_man_hl
        self.sed_wall_thickness = sed_wall_thickness
        self.sed_tank_diffuser_hl = sed_tank_diffuser_hl

        self.weir_thickness = weir_thickness
        self.w_min = w_min
        self.outlet_man_bod_hl = outlet_man_bod_hl
        self.fitting_s = fitting_s
        self.inlet_depth_max = inlet_depth_max
        self.drain_sdr = drain_sdr

    @property
    def l(self):
        l = (self.sed_tank_n * self.sed_tank_w_inner) + \
            ((self.sed_tank_n-1) * self.sed_tank_wall_thickness) + \
            self.sed_wall_thickness
        return l

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
            0,
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
        inlet_plumbing_depth_min = self.outlet_man_bod_hl + self.sed_tank_diffuser_hl + \
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
            0)
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
        inlet_chan_h_weir = self.inlet_depth + self.INLET_WEIR_FREE_BOARD_H
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
        drain_nd = pc.pipe_flow_nd(self.q, self.sdr, )

    @property
    def inlet_drain_box_w(self):
        inlet_drain_box_w = max( 2 * self.fitting_s + pipe.fitting_od(self.drain_nd), self.inlet_w_post_weir)
        return inlet_drain_box_w