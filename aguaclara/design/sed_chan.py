"""The sedimentation channel of an AguaClara water treatment plant ensures that
the sedimentation tanks do not exceed their maximum influent flow. If that were
to happen, the upflow velocity would be too great for flocs to settle out.

Example:
    >>> from aguaclara.design.sed_chan import *
    >>> sed_chan = SedimentationChannel(q = 20 * u.L / u.s, temp = 20 * u.degC)
    >>> sed_chan.inlet_w
    <Quantity(59.52755905511811, 'inch')>
"""
from aguaclara.core.units import u
import aguaclara.core.constants as con
import aguaclara.core.materials as mat
import aguaclara.core.utility as ut
import aguaclara.core.physchem as pc
import aguaclara.core.pipes as pipe
import aguaclara.core.head_loss as hl
import aguaclara.design.human_access as ha
from aguaclara.design.component import Component
from aguaclara.design.pipeline import Pipe

import numpy as np
import math


class SedimentationChannel(Component):
    """Design an AguaClara sedimentation channel.

    The sedimentation channel relies on the number and dimensions of the
    sedimentation tanks in the same plant, but assumed/default values may be
    used to design a sedimentation channel by itself. To design these components
    in tandem, use :class:`aguaclara.design.sed.Sedimentor`.

    Constants:
        - ``SED_TANK_Q_RATIO (float)``: Permissible ratio of influent flow
          between the sedimentation tanks
        - ``PLANT_FREE_BOARD_H (float * u.cm)``: Freeboard height in the plant
        - ``WEIR_FREEBOARD_H (float * u.cm)``: Freeboard height of a channel
          weir
        - ``SED_DEPTH_EST (float * u.m)``: Estimated depth of the sedimentor

    Design Inputs:
        - ``q (float * u.L / u.s)``: Flow rate (recommended, defaults to 20L/s)
        - ``temp (float * u.degC)``: Water temperature (recommended, defaults to
          20°C)
        - ``sed_tank_n (int)``: Number of sedimentation tanks (recommended,
          defaults to 4)
        - ``sed_tank_w_inner (float * u.inch)``: Inner width of the sedimentation
          tank (recommended, defaults to 42 in)
        - ``sed_tank_wall_thickness (float * u.cm)``: Wall thickness of the
          sedimentation tank (recommended, defaults to 15 cm)
        - ``sed_tank_inlet_man_nd (float * u.cm)``: Nominal diameter of the
          sedimentation tank's inlet manifold (recommended, defaults to 60 cm)
        - ``sed_tank_outlet_man_nd (float * u.cm)``: Nominal diameter of the
          sedimentation tank's outlet manifold (recommended, defaults to 60 cm)
        - ``sed_tank_outlet_man_hl (float * u.cm)``: Head loss in the
          sedimentation tank's outlet manifold (recommended, defaults to 4 cm)
        - ``sed_tank_diffuser_hl (float * u.mm)``: Head loss through a
          diffuser in the sedimentation tank (recommended, defaults to 0.09 cm)
        - ``sed_wall_thickness (float * u.cm)``: Wall thickness of the
          sedimentor (recommended, defaults to 15 cm)
        - ``weir_thickness (float * u.cm)``: Weir thickness (optional, defaults
          to 15 cm)
        - ``weir_hl (float * u.cm)``: Head loss over the weir (optional,
          defaults to 5 cm)
        - ``w_min (float * u.cm)``: Minimum width (optional, defaults to 30 cm)
        - ``fitting_s (float * u.cm)``: Fitting spacing (optional, defaults
          to 15 cm)
        - ``inlet_depth_max (float * u.cm)``: Maximum inlet channel depth
          (optional, defaults to 50 cm)
        - ``drain_sdr (int)``: SDR of the drain pipe (optional, defaults to 26)
        - ``outlet_free_h (float * u.cm)``: Permissible increase of water level
          in the outlet channel (optional, defaults to 5 cm)
          ``outlet_weir_depth``:The depth of the outlet weir. (optional, defaults to 5 cm)
        - ``outlet_pipe_sdr (int)``: SDR of the outlet pipe (optional, defaults
          to 41)
        - ``outlet_pipe_hl_max (float * u.cm)``: Maximum head loss through the
          outlet pipe (optional, defaults to 1 cm)
        - ``outlet_pipe_nd_max (float * u.inch)``: Maximum nominal diameter of
          the outlet pipe (optional, defaults to 8 in)
    """
    SED_TANK_Q_RATIO = 0.95
    PLANT_FREEBOARD_H = 5.0 * u.cm
    WEIR_FREEBOARD_H = 2.0 * u.cm
    SED_DEPTH_EST = 2.0 * u.m

    def __init__(self, **kwargs):
        self.sed_tank_n=4
        self.sed_tank_w_inner=42.0 * u.inch
        self.sed_tank_wall_thickness = 15.0 * u.cm
        self.sed_tank_inlet_man_nd = 60.0 * u.cm
        self.sed_tank_outlet_man_nd = 60.0 * u.cm
        self.sed_tank_outlet_man_hl = 4.0 * u.cm
        self.sed_tank_diffuser_hl=0.09 * u.mm
        self.sed_wall_thickness = 15.0 * u.cm

        self.weir_thickness = 15.0 * u.cm
        self.weir_hl = 5 * u.cm
        self.w_min = 30.0 * u.cm
        self.fitting_s = 15. * u.cm
        self.inlet_depth_max = 50 * u.cm
        self.drain_spec = 'sdr26'
        self.outlet_free_h = 5.0 * u.cm
        self.outlet_pipe_spec = 'sdr41'
        self.outlet_pipe_hl_max = 1.0 * u.cm
        self.outlet_pipe_nd_max = 8.0 * u.inch

        self.drain_pipe = Pipe()
        self.outlet_pipe = Pipe()
        self.subcomponents = [self.drain_pipe, self.outlet_pipe]

        super().__init__(**kwargs)
        self._set_drain_pipe()
        self._set_outlet_pipe()
        super().set_subcomponents()

    @property
    def l(self):
        """Length of the sedimentation channel."""
        l = (self.sed_tank_n * self.sed_tank_w_inner) + \
            ((self.sed_tank_n-1) * self.sed_tank_wall_thickness) + \
            self.sed_wall_thickness
        return l.to(u.m)

    @property
    def outlet_weir_hl(self):
        """Head loss over the outlet channel weir."""
        weir_exit_hl = pc.headloss_weir_rect(self.q, self.l)
        return weir_exit_hl

    @property
    def inlet_hl_max(self):
        """Maximum head loss in the inlet channel."""
        inlet_hl_max = (self.sed_tank_outlet_man_hl + self.sed_tank_diffuser_hl) * \
            (1 - self.SED_TANK_Q_RATIO ** 2)
        return inlet_hl_max

    @property
    def _inlet_w_pre_weir_plumbing_min(self):
        """Minimum width of the inlet channel (pre-weir) to fit pipes."""
        inlet_w_pre_weir_plumbing_min = pipe.fitting_od(self.sed_tank_inlet_man_nd) + \
            2 * self.fitting_s
        return inlet_w_pre_weir_plumbing_min

    @property
    def _inlet_w_pre_weir_hl_min(self):
        """Minimum width of the inlet channel (pre-weir) that doesn't exceed
        the permissible head loss.
        """
        inlet_w_pre_weir_hl_min = pc.horiz_chan_w(
            self.q,
            self.inlet_depth_max,
            self.inlet_hl_max,
            self.l,
            pc.viscosity_kinematic_water(self.temp),
            mat.CONCRETE_PIPE_ROUGH,
            False,
            0
        )
        return inlet_w_pre_weir_hl_min

    @property
    def inlet_w_pre_weir(self):
        """Width of the inlet channel (pre-weir)."""
        inlet_w_pre_weir = max(
            self._inlet_w_pre_weir_plumbing_min,
            self._inlet_w_pre_weir_hl_min)
        return inlet_w_pre_weir

    @property
    def _inlet_depth_plumbing_min(self):
        """Minimum depth of the inlet channel to fit pipes."""
        inlet_plumbing_depth_min = self.sed_tank_outlet_man_hl + self.sed_tank_diffuser_hl + \
            pipe.fitting_od(self.sed_tank_outlet_man_nd) + \
                self.fitting_s + self.outlet_weir_hl
        return inlet_plumbing_depth_min

    @property
    def _inlet_depth_hl_min(self):
        """Minimum depth of the inlet channel to stay within acceptable head
        loss.
        """
        inlet_chan_hl_depth = pc.horiz_chan_h(
            self.q,
            self.inlet_w_pre_weir,
            self.inlet_hl_max,
            self.l,
            pc.viscosity_kinematic_water(self.temp),
            mat.CONCRETE_PIPE_ROUGH,
            False)
        return inlet_chan_hl_depth

    @property
    def inlet_depth(self):
        """Depth of the inlet channel."""
        inlet_depth = max(self._inlet_depth_plumbing_min, self._inlet_depth_hl_min)
        return inlet_depth

    @property
    def inlet_weir_hl(self):
        """Head loss through the inlet channel weir."""
        inlet_weir_hl = pc.headloss_weir_rect(self.q, self.l)
        return inlet_weir_hl

    @property
    def inlet_h(self):
        """Height of the inlet channel."""
        inlet_h = self.inlet_depth + self.PLANT_FREEBOARD_H
        return inlet_h

    @property
    def inlet_weir_h(self):
        """Height of the inlet channel weir."""
        inlet_chan_h_weir = self.inlet_depth + self.WEIR_FREEBOARD_H
        return inlet_chan_h_weir

    @property
    def inlet_w_post_weir(self):
        """Width of the inlet channel (post-weir)"""
        inlet_w_post_weir = max(
            self.w_min,
            pc.horiz_chan_w(
                self.q,
                self.inlet_h,
                self.inlet_h,
                self.l,
                pc.viscosity_kinematic_water(self.temp),
                mat.CONCRETE_PIPE_ROUGH,
                1,
                0 ))
        return inlet_w_post_weir

    @property
    def inlet_w(self):
        """Width of the inlet channel"""
        inlet_w = self.inlet_w_pre_weir + self.weir_thickness + self.inlet_w_post_weir
        return inlet_w

    def _set_drain_pipe(self):
        drain_k_minor = hl.PIPE_ENTRANCE_K_MINOR + hl.PIPE_EXIT_K_MINOR + hl.EL90_K_MINOR
        drain_nd = pc.pipe_flow_nd(
            self.q,
            ut.get_sdr(self.drain_spec),
            self.SED_DEPTH_EST,
            self.SED_DEPTH_EST + self.inlet_w,
            pc.viscosity_kinematic_water(self.temp),
            mat.PVC_PIPE_ROUGH,
            drain_k_minor
        )

        self.drain_pipe = Pipe(
            size = drain_nd,
            spec = self.drain_spec,
            k_minor = drain_k_minor,
            )

    @property
    def inlet_drain_box_w(self):
        """Width of the inlet channel drain box"""
        inlet_drain_box_w = max( 2 * self.fitting_s + pipe.fitting_od(self.drain_pipe.size), self.inlet_w_post_weir)
        return inlet_drain_box_w

    @property
    def outlet_depth(self):
        """Depth of the outlet channel."""
        outlet_depth = self.inlet_depth - self.sed_tank_outlet_man_hl - \
           self.sed_tank_diffuser_hl
        return outlet_depth

    @property
    def outlet_weir_depth(self):
        """Depth of the outlet channel weir."""
        outlet_weir_depth = self.outlet_depth - self.weir_hl - self.WEIR_FREEBOARD_H
        return outlet_weir_depth

    @property
    def outlet_w_pre_weir(self):
        """Width of the outlet channel (pre-weir)."""
        return self.w_min

    @property
    def outlet_pipe_k_minor(self):
        outlet_pipe_k_minor = 2 * hl.EL90_K_MINOR + hl.PIPE_ENTRANCE_K_MINOR + \
                 hl.PIPE_EXIT_K_MINOR
        return outlet_pipe_k_minor

    @property
    def outlet_pipe_l(self):
        outlet_pipe_l = ha.DRAIN_CHAN_WALKWAY_W + self.inlet_w + 1.0 * u.m
        return outlet_pipe_l

    @property
    def outlet_pipe_q_max(self):
        """Maximum flow through the outlet pipe."""
        outlet_pipe_q_max = pc.flow_pipe(
            pipe.ID_SDR(self.outlet_pipe_nd_max, ut.get_sdr(self.outlet_pipe_spec)),
            self.outlet_pipe_hl_max,
            self.outlet_pipe_l,
            pc.viscosity_kinematic_water(self.temp),
            mat.PVC_PIPE_ROUGH,
            self.outlet_pipe_k_minor
        )
        return ut.round_step(
            outlet_pipe_q_max.to(u.L / u.s),
            step = 0.0001 * u.L / u.s
        )

    def _set_outlet_pipe(self):
        outlet_pipe_q = self.q / self.outlet_pipe_n

        # outlet_pipe_nd = pc.pipe_flow_nd(
        #     outlet_pipe_q,
        #     ut.get_sdr(self.outlet_pipe_spec),
        #     self.outlet_pipe_hl_max,
        #     self.outlet_pipe_l,
        #     pc.viscosity_kinematic_water(self.temp),
        #     mat.PVC_PIPE_ROUGH,
        #     self.outlet_pipe_k_minor
        # )

        outlet_pipe_nd = pc.pipe_flow_nd(
            outlet_pipe_q,
            ut.get_sdr(self.outlet_pipe_spec),
            self.outlet_pipe_hl_max,
            self.outlet_pipe_l,
            pc.viscosity_kinematic_water(self.temp),
            mat.PVC_PIPE_ROUGH,
            2 * hl.EL90_K_MINOR + hl.PIPE_ENTRANCE_K_MINOR + \
                 hl.PIPE_EXIT_K_MINOR
        )

        self.outlet_pipe = Pipe(
            l = self.outlet_pipe_l,
            q = outlet_pipe_q,
            size = outlet_pipe_nd,
            spec = self.outlet_pipe_spec,
            k_minor = self.outlet_pipe_k_minor
            )

    @property
    def outlet_pipe_n(self):
        """Number of outlet pipes."""
        outlet_pipe_n = math.ceil(self.q / self.outlet_pipe_q_max)
        return outlet_pipe_n

    @property
    def outlet_post_weir_w(self):
        """Width of the outlet channel (post-weir)."""
        outlet_post_weir_w = max(
            #need self.outlet_to_filter_nd
            self.fitting_s + pipe.fitting_od(self.outlet_pipe.size),
            self.fitting_s + pipe.fitting_od(self.drain_pipe.size),
            self.w_min,
            pc.horiz_chan_w(
                self.q,
                self.outlet_weir_depth - self.outlet_free_h, #what is outlet_free_h
                self.outlet_weir_depth,
                self.l,
                pc.viscosity_kinematic_water(self.temp),
                mat.PVC_PIPE_ROUGH,
                1,
                hl.PIPE_ENTRANCE_K_MINOR + hl.PIPE_EXIT_K_MINOR + hl.EL90_K_MINOR
            )
        )
        return outlet_post_weir_w

    @property
    def outlet_w(self):
        """Width of the outlet channel."""
        outlet_w = self.outlet_w_pre_weir + self.weir_thickness + \
            self.outlet_post_weir_w
        return outlet_w

    @property
    def outlet_drain_box_w(self):
        """Width of the outlet channel drain box."""
        outlet_drain_box_w = max(
            self.fitting_s + pipe.fitting_od(self.drain_pipe.size),
            self.outlet_post_weir_w
            )
        return outlet_drain_box_w

    @property
    def outlet_weir_h(self):
        """Height of the outlet channel weir."""
        outlet_weir_h = self.outlet_weir_depth + self.WEIR_FREEBOARD_H
        return outlet_weir_h

    @property
    def w_outer(self):
        """Outer width of the sedimentation channel."""
        w_outer = self.outlet_w + 2 * self.weir_thickness + self.inlet_w + self.sed_wall_thickness
        return w_outer

    @property
    def inlet_last_coupling_h(self):
        """Height of the last coupling in the inlet channel."""
        last_coupling_h = self.outlet_weir_depth - 2 * u.cm
        return last_coupling_h

    @property
    def inlet_step_h(self):
        """Height of the steps between each pipe in the inlet channel."""
        step_h = self.inlet_last_coupling_h / max(1, self.sed_tank_n - 1)
        return step_h

    @property
    def inlet_slope_l(self):
        """Length of the slopes between each pipe in the inlet channel."""
        inlet_slope_l = self.l + self.sed_wall_thickness - \
            pipe.fitting_od(self.sed_tank_inlet_man_nd) - self.fitting_s
        return inlet_slope_l
