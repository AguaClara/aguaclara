"""Calculate hydraulic dimensions of a sedimentation tank bay.

Example:
    >>> from aguaclara.design.sed_tank_bay import SedimentationTankBay
"""
from aguaclara.core.units import unit_registry as u
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
    """Calculates necessary dimensions and values for SedimentationTankBay.

    Example:
        >>> sed_tank_bay = SedimentationTankBay()
    """
    INLET_MAN_Q_RATIO = 0.8
    OUTLET_MAN_HL = 4 * u.cm
    JET_REVERSER_ND = 3 * u.inch
    JET_PLANE_RATIO = 0.0124
    HOPPER_DRAIN_ND = 1 * u.inch
    WALL_THICKNESS = 0.15 * u.m

    q=20.0 * u.L / u.s
    temp=20.0 * u.degC

    vel_upflow=1.0 * u.mm / u.s
    l_inner=5.8 * u.m
    w_inner=42.0 * u.inch

    diffuser_vel_max=44.29 * u.cm / u.s
    diffuser_n=108
    diffuser_wall_thickness=1.17 * u.inch
    diffuser_sdr=41

    inlet_man_hl=1 * u.cm
    inlet_man_sdr = 41
    jet_reverser_sdr = 26

    plate_settler_angle=60.0 * u.deg
    plate_settler_s=2.5 * u.cm
    plate_settler_thickness=2.0 * u.mm
    plate_settler_cantilever_l_max=20.0 * u.cm
    plate_settler_vel_capture=0.12 * u.mm / u.s

    outlet_man_orifice_hl=4.0 * u.cm
    outlet_man_orifice_q_ratio_max=0.8
    outlet_man_orifice_n_est = 58
    outlet_man_sdr=41
    slope_angle=50 * u.deg
    
    upflow_l = 6.0 * u.m
    sed_chan_w_outer = 60 * u.cm
    sed_chan_weir_thickness = 5 * u.cm
    hopper_l_min = 50 * u.cm

    @property
    def q_tank(self):
        """
        Returns:
            Flow rate in a sedimentation tank (float * u.L / u.s).
        """
        q_tank = self.l_inner * self.w_inner * self.vel_upflow
        return q_tank.to(u.L / u.s)
        
    @property
    def diffuser_hl(self):
        return self.inlet_man_hl / self.diffuser_n
    
    @property
    def diffuser_vel(self):
        diffuser_vel = np.sqrt(2 * con.GRAVITY * self.diffuser_hl)
        return diffuser_vel.to(u.mm / u.s)
        
    @property
    def diffuser_w_inner(self):
        diffuser_w_inner = self.w_inner * self.vel_upflow / self.diffuser_vel
        return diffuser_w_inner.to(u.cm)

    @property
    def diffuser_a(self):
        """
        Calculates manifold diffuser area from flow rate.
        """
        diffuser_a = self.q_tank / (self.diffuser_vel * self.diffuser_n)
        return diffuser_a.to(u.cm ** 2)

    # Note: we need to specify in Onshape a 15% stretch difference between
    # the circumference of both diffuser ends' inner/outer circumferences.
    # We can model the aggregate diffuser jet as one continuous flow. Don't
    # correct for the thickness that separates each diffuser's effluent orifice.

    @property
    def inlet_man_v_max(self):
        """Return the maximum velocity through the manifold.

        Returns:
            Maximum velocity through the manifold (float).
        """
        vel_manifold_max = np.sqrt(4 * con.GRAVITY * self.diffuser_hl *
                (1 - self.INLET_MAN_Q_RATIO ** 2) /
                (self.INLET_MAN_Q_RATIO ** 2 + 1)
            )
        return vel_manifold_max.to(u.m / u.s)

    @property 
    def inlet_man_nd(self):
        diam_inner = np.sqrt(4 * self.q_tank / (np.pi * self.inlet_man_v_max))
        inlet_man_nd = pipe.ND_SDR_available(diam_inner, self.inlet_man_sdr)
        return inlet_man_nd.to(u.cm)

    @property
    def outlet_man_nd(self):
        outlet_man_nd = pc.manifold_nd(
            self.q_tank,
            self.OUTLET_MAN_HL,
            self.l_inner,
            self.outlet_man_orifice_q_ratio_max,
            pc.viscosity_kinematic(self.temp), 
            mat.PVC_PIPE_ROUGH.to(u.m), 
            hl.PIPE_EXIT_K_MINOR,
            self.outlet_man_orifice_n_est,
            self.outlet_man_sdr
        )
        return outlet_man_nd

    @property
    def outlet_man_orifice_d(self):
        """Return the diameter of the orifices in the exit manifold for the sedimentation tank.

        Returns:
            Diameter of the orifices in the exit manifold for the sedimentation tank (float).
        """
        Q_orifice = self.q_tank / self.outlet_man_orifice_n_est
        D_orifice = pc.diam_circle(Q_orifice/(con.VC_ORIFICE_RATIO * \
            np.sqrt(2 * con.GRAVITY* self.outlet_man_orifice_hl)))
        return ut.ceil_nearest(D_orifice, drills.DRILL_BITS_D_METRIC)

    @property
    def plate_l(self):
        """Return the length of a single plate in the plate settler module based on
        achieving the desired capture velocity

        Returns:
            Length of a single plate (float).
        """
        L_sed_plate = ((self.plate_settler_s * ((self.vel_upflow / self.plate_settler_vel_capture) - 1)
                        + self.plate_settler_thickness * (self.vel_upflow / self.plate_settler_vel_capture))
                     / (np.sin(self.plate_settler_angle) * np.cos(self.plate_settler_angle))
                     ).to(u.m)
        return L_sed_plate
    
    @property
    def outlet_man_orifice_q(self):
        outlet_man_orifice_q = pc.flow_orifice_vert(
                self.outlet_man_orifice_d,
                self.outlet_man_orifice_hl,
                con.VC_ORIFICE_RATIO
            )
        return outlet_man_orifice_q.to(u.L / u.s)

    @property
    def outlet_man_orifice_spacing(self):
        outlet_man_orifice_spacing = (
            self.upflow_l - 
            pipe.socket_depth(self.outlet_man_nd) - 
            pipe.cap_thickness(self.outlet_man_nd) - 
            self.outlet_man_orifice_d
            ) / ((self.q_tank / self.outlet_man_orifice_q) - 1)
        return outlet_man_orifice_spacing

    @property
    def outlet_man_orifice_n(self):
        outlet_orifice_n = math.floor(
            (
                self.upflow_l - 
                pipe.socket_depth(self.outlet_man_nd) - 
                pipe.cap_thickness(self.outlet_man_nd) - 
                self.outlet_man_orifice_d
            ) / self.outlet_man_orifice_spacing
        ) + 1 
        return outlet_orifice_n

    @property
    def outlet_orifice_hl(self):
        outlet_orifice_hl = pc.head_orifice(
            self.outlet_man_nd, 
            con.VC_ORIFICE_RATIO,
            self.q_tank / self.outlet_man_orifice_n
            )
        return outlet_orifice_hl.to(u.mm)

    @property
    def side_slopes_w(self):
        side_slopes_w = (
            self.w_inner - 
            pipe.ID_SDR(self.JET_REVERSER_ND, self.jet_reverser_sdr)
            ) / 2
        return side_slopes_w.to(u.m)

    @property
    def side_slopes_h(self):
        side_slopes_h = np.tan(self.slope_angle) * self.side_slopes_w
        return side_slopes_h.to(u.m)

    @property
    def weir_floc_z(self):
        pass
        
    @property
    def hopper_bottom_z(self):
        pass

    @property
    def hopper_slope_front_h(self):
        # hopper_slope_front_h = self.weir_floc_z - self.hopper_bottom_z
        # return hopper_slope_front_h
        pass

    @property
    def hopper_drain_nd(self):
        pass

    @property
    def hopper_slope_front_back_angle(self):
        pass

    @property
    def hopper_pipe_drain_l(self):
        # hopper_pipe_drain_l = (
        #     self.hopper_slope_front_h /
        #      np.tan(self.hopper_slope_front_back_angle)
        #      ) + self.WALL_THICKNESS + pipe.socket_depth(self.hopper_drain_nd)
        # return hopper_pipe_drain_l
        pass

    @property
    def hopper_l(self):
        if self.q > 60. * u.L / u.s: 
            hopper_l = self.sed_chan_w_outer
        else:
            hopper_l = max(
                self.hopper_l_min,
                self.plate_l * np.cos(self.plate_settler_angle) - \
                    self.sed_chan_weir_thickness
            )
        return hopper_l