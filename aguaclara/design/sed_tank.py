""" A sedimentation tank of an AguaClara water treatment plant

Example:
    >>> from aguaclara.design.sed_tank import *
    >>> sed_tank = SedimentationTank(q = 60 * u.L / u.s)
    >>> sed_tank.diffuser_hl
    <Quantity(0.009259259259259259, 'centimeter')>
"""
from aguaclara.core.units import u
import aguaclara.core.constants as con
import aguaclara.core.materials as mat
import aguaclara.core.pipes as pipe
from aguaclara.core import drills
import aguaclara.core.utility as ut
from aguaclara.design.component import Component
import aguaclara.core.physchem as pc
import aguaclara.core.head_loss as hl

import numpy as np
import math


class SedimentationTank(Component):
    """Design an AguaClara plant's sedimentation tank.

    An sedimentation tank's design relies on the sedimentation channel's design
    in the same plant, but assumed/default values may be used to design an
    sedimentation tank by itself. To design these components in tandem, use
    :class:`aguaclara.design.sed.Sedimentor`.

    Constants:
        - ``INLET_MAN_Q_RATIO (float)``: The ratio of the flow in the inlet
          manifold.
        - ``OUTLET_MAN_HL (float * u.cm)``: The headloss of the outlet manifold
        - ``JET_REVERSER_ND (float * u.inch)``: The nominal diameter of the jet
          reverser.
        - ``JET_PLANE_RATIO (float)``: The ratio for the jet plane
        - ``JET_REVERSER_TO_DIFFUSERS_H (float * u.cm)``: The height between
          the jet reverser and diffusers.
        - ``WALL_THICKNESS (float * u.m)``: The thickness of the sed tank walls
        - ``DIFFUSER_L (float * u.cm)``: The length of a diffuser.

    Design Inputs:
        - ``q (float * u.L / u.s)``: Plant flow rate
          (recommended, defaults to 20L/s)
        - ``temp (float * u.degC)``: Water temperature (recommended, defaults to
          20°C)
        - ``vel_upflow (float * u.mm / u.s)``: Upflow velocity
          (optional, defaults to 1mm/s)
        - ``l_inner (float * u.m)``: The inner length
          (optional, defaults to 5.8m)
        - ``w_inner (float * u.inch)``: The inner width
          (optional, defaults to 42in.)
        - ``diffuser_vel_max (float * u.cm / u.s)``: The max velocity of a
          diffuser (optional, defaults to 44.29 cm/s)
        - ``diffuser_n (int)``:The nunber of diffusers
          (optional, defaults to 108)
        - ``diffuser_wall_thickness (float * u.inch)``: The thickness of the
          wall of a diffuser (optional, defaults to 1.17in.)
        - ``diffuser_sdr (int)``: The standard dimension ratio of a diffuser
          (optional, defaults to 41)
        - ``inlet_man_hl (float * u.cm)``: The headloss of the inlet manifold
          (optional, defaults to 1cm)
        - ``inlet_man_sdr (float)``: The standard dimension ratio of the inlet
          manifold (optional, defaults to 41)
        - ``jet_reverser_sdr (int)``: The standard dimension ratio of the jet
          reverser (optional, defaults to 26)
        - ``plate_settler_angle (float * u.deg)``: The angle of the plate
          settler (optional, defaults to 60°)
        - ``plate_settler_s (float * u.cm)``: Spacing in between plate settlers
          (optional, defaults to 2.5cm)
        - ``plate_settler_thickness (float * u.mm)``: Thickness of a plate
          settler (optional, defaults to 2mm)
        - ``plate_settler_cantilever_l_max (float * u.cm)``: The max length of
          the plate settler cantilever (optional, defaults to 20cm)
        - ``plate_settler_vel_capture (float * u.mm / u.s)``: The capture
          velocity of a plate settler (optional, defaults to 0.12mm/s)
        - ``outlet_man_orifice_hl (float * u.cm)``: The headloss of the
          orifices in the outlet manifold (optional, defaults to 4cm)
        - ``outlet_man_orifice_q_ratio_max (float)``: The max ratio of the flow
          rate for the orifices of the outlet manifold (optional, defaults to 0.8)
        - ``outlet_man_orifice_n_est (int)``: The estimated number of orifices
          for the outlet manifold (optional, defaults to 58)
        - ``outlet_man_sdr (int)``: The standard dimension ratio of the outlet
          manifold (optional, defaults to 41)
        - ``slope_angle (float * u.deg)``: The angle at the bottom of the sed tank
          (optional, defaults to 50°)
        - ``side_slope_to_floc_weir_h_min (float * u.cm)``: The minimum height
          between the side slope and the floc weir. (optional, defaults to 5cm)
        - ``sed_chan_w_outer (float * u.cm)``: The outer width of the
          sedimentation channel (optional, defaults to 60cm)
        - ``sed_chan_weir_thickness (float * u.cm)``: The thickness of the
          sedimentation channel weir (optional, defaults to 5cm)
        - ``floc_weir_to_plate_frame_h (float * u.cm)``: The height from the
          top of the floc weir to the plate settler frame (optional, defaults
          to 10cm)
        - ``hopper_slope_vertical_angle (float * u.deg)``: The angle of the
          hopper wall slopes to vertical (optional, defaults to 60°)

    """
    INLET_MAN_Q_RATIO = 0.8
    OUTLET_MAN_HL = 4. * u.cm
    JET_REVERSER_ND = 3. * u.inch
    JET_PLANE_RATIO = 0.0124
    JET_REVERSER_TO_DIFFUSERS_H = 3.0* u.cm
    WALL_THICKNESS = 0.15 * u.m
    DIFFUSER_L = 15.0 * u.cm

    def __init__(self, **kwargs):
        self.vel_upflow=1.0 * u.mm / u.s
        self.l_inner=5.8 * u.m
        self.w_inner=42.0 * u.inch

        self.diffuser_vel_max=44.29 * u.cm / u.s
        self.diffuser_n=108
        self.diffuser_wall_thickness=1.17 * u.inch
        self.diffuser_sdr=41

        self.inlet_man_hl=1. * u.cm
        self.inlet_man_sdr = 41
        self.jet_reverser_sdr = 26

        self.plate_settler_angle=60.0 * u.deg
        self.plate_settler_s=2.5 * u.cm
        self.plate_settler_thickness=2.0 * u.mm
        self.plate_settler_cantilever_l_max=20.0 * u.cm
        self.plate_settler_vel_capture=0.12 * u.mm / u.s

        self.outlet_man_orifice_hl=4.0 * u.cm
        self.outlet_man_orifice_q_ratio_max=0.8
        self.outlet_man_orifice_n_est = 58
        self.outlet_man_sdr=41

        self.slope_angle=50. * u.deg
        self.side_slope_to_floc_weir_h_min = 5.0 * u.cm
        self.sed_chan_w_outer = 60.0 * u.cm
        self.sed_chan_weir_thickness = 5.0 * u.cm
        self.floc_weir_to_plate_frame_h = 10.0 * u.cm
        self.hopper_slope_vertical_angle = 60.0 * u.deg

        super().__init__(**kwargs)

    @property
    def q_tank(self):
        """The flow rate present in the tank."""
        q_tank = self.l_inner * self.w_inner * self.vel_upflow
        return q_tank.to(u.L / u.s)

    @property
    def diffuser_hl(self):
        """The headloss of the diffuser."""
        return self.inlet_man_hl / self.diffuser_n

    @property
    def diffuser_vel(self):
        """The velocity of the diffuser"""
        diffuser_vel = np.sqrt(2 * con.GRAVITY * self.diffuser_hl)
        return diffuser_vel.to(u.mm / u.s)

    @property
    def diffuser_w_inner(self):
        """The inner width(neglecting walls) of the diffuser."""
        diffuser_w_inner = self.w_inner * self.vel_upflow / self.diffuser_vel
        return diffuser_w_inner.to(u.cm)

    @property
    def diffuser_a(self):
        """The area of the diffuser"""
        diffuser_a = self.q_tank / (self.diffuser_vel * self.diffuser_n)
        return diffuser_a.to(u.cm ** 2)

    @property
    def inlet_man_v_max(self):
        """The maximumum velocity in the inlet manifold."""
        vel_manifold_max = np.sqrt(4 * con.GRAVITY * self.diffuser_hl *
                (1 - self.INLET_MAN_Q_RATIO ** 2) /
                (self.INLET_MAN_Q_RATIO ** 2 + 1)
            )
        return vel_manifold_max.to(u.m / u.s)

    @property
    def inlet_man_nd(self):
        """The nominal diameter of the inlet manifold"""
        diam_inner = np.sqrt(4 * self.q_tank / (np.pi * self.inlet_man_v_max))
        inlet_man_nd = pipe.ND_SDR_available(diam_inner, self.inlet_man_sdr)
        return inlet_man_nd.to(u.cm)

    @property
    def outlet_man_nd(self):
        """The nominal diameter of the outlet manifold."""
        outlet_man_nd = pc.manifold_nd(
            self.q_tank,
            self.OUTLET_MAN_HL,
            self.l_inner,
            self.outlet_man_orifice_q_ratio_max,
            pc.viscosity_kinematic_water(self.temp),
            mat.PVC_PIPE_ROUGH.to(u.m),
            hl.PIPE_EXIT_K_MINOR,
            self.outlet_man_orifice_n_est,
            self.outlet_man_sdr
        )
        return outlet_man_nd

    @property
    def outlet_man_orifice_d(self):
        """The diameter of the orifices in the outlet manifold."""
        Q_orifice = self.q_tank / self.outlet_man_orifice_n_est
        D_orifice = pc.diam_circle(Q_orifice/(con.VC_ORIFICE_RATIO * \
            np.sqrt(2 * con.GRAVITY* self.outlet_man_orifice_hl)))
        return ut.ceil_nearest(D_orifice, drills.DRILL_BITS_D_METRIC)

    @property
    def plate_l(self):
        """The length of a plate in the plate settlers."""
        L_sed_plate = ((self.plate_settler_s * ((self.vel_upflow / \
             self.plate_settler_vel_capture) - 1)
                        + self.plate_settler_thickness * (
                            self.vel_upflow / self.plate_settler_vel_capture))
                     / (np.sin(self.plate_settler_angle) * \
                         np.cos(self.plate_settler_angle))
                     ).to(u.m)
        return L_sed_plate

    @property
    def outlet_man_orifice_q(self):
        """The flow rate in the orifices of the outlet manifold."""
        outlet_man_orifice_q = pc.flow_orifice_vert(
                self.outlet_man_orifice_d,
                self.outlet_man_orifice_hl,
                con.VC_ORIFICE_RATIO
            )
        return outlet_man_orifice_q.to(u.L / u.s)

    @property
    def outlet_man_orifice_spacing(self):
        """The spacing between orifices on the outlet manifold."""
        outlet_man_orifice_spacing = (
            self.l_inner -
            pipe.socket_depth(self.outlet_man_nd) -
            pipe.cap_thickness(self.outlet_man_nd) -
            self.outlet_man_orifice_d
            ) / ((self.q_tank / self.outlet_man_orifice_q) - 1)
        return outlet_man_orifice_spacing

    @property
    def outlet_man_orifice_n(self):
        """The number of orifices on the outlet manifold."""
        outlet_orifice_n = math.floor(
            (
                self.l_inner -
                pipe.socket_depth(self.outlet_man_nd) -
                pipe.cap_thickness(self.outlet_man_nd) -
                self.outlet_man_orifice_d
            ) / self.outlet_man_orifice_spacing
        ) + 1
        return outlet_orifice_n

    @property
    def outlet_orifice_hl(self):
        """The headloss for the orifices of the outlet"""
        outlet_orifice_hl = pc.head_orifice(
            self.outlet_man_nd,
            con.VC_ORIFICE_RATIO,
            self.q_tank / self.outlet_man_orifice_n
            )
        return outlet_orifice_hl.to(u.mm)

    @property
    def side_slopes_w(self):
        """The width of the side slopes."""
        side_slopes_w = (
            self.w_inner -
            pipe.ID_SDR(self.JET_REVERSER_ND, self.jet_reverser_sdr)
            ) / 2
        return side_slopes_w.to(u.m)

    @property
    def side_slopes_h(self):
        """The height of the side slopes."""
        side_slopes_h = np.tan(self.slope_angle) * self.side_slopes_w
        return side_slopes_h.to(u.m)

    @property
    def inlet_man_h(self):
        """The height of the inlet manifold height."""
        inlet_man_h = self.JET_REVERSER_TO_DIFFUSERS_H + self.DIFFUSER_L + \
             ( pipe.OD(self.inlet_man_nd)/ 2 )
        return inlet_man_h

    @property
    def floc_weir_h(self):
        """The height of the floc weir."""
        floc_weir_h = max(
            self.inlet_man_h + (pipe.OD(self.inlet_man_nd) / 2) + \
                mat.CONCRETE_THICKNESS_MIN,
            self.side_slopes_h + self.side_slope_to_floc_weir_h_min
        )
        return floc_weir_h
