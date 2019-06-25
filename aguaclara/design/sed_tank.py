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
import aguaclara.core.materials as mat

import numpy as np


class SedimentationTank(Component):
    """Calculates necessary dimensions and values for SedimentationTankBay.

    Example:
        >>> sed_tank_bay = SedimentationTankBay()
    """
    INLET_MAN_Q_RATIO = 0.8
    OUTLET_MAN_HL = 4 * u.cm

    def __init__(self, q=20.0 * u.L / u.s, temp=20.0 * u.degC,
                 vel_upflow=1.0 * u.mm / u.s,
                 l_inner=5.8 * u.m,
                 w_inner=42.0 * u.inch,
                 diffuser_vel_max=44.29 * u.cm / u.s,
                 diffuser_n=108,
                 diffuser_wall_thickness=1.17 * u.inch,
                 diffuser_sdr=41,
                 inlet_hl=1 * u.cm,
                 inlet_man_sdr = 41,
                 plate_settler_angle=60.0 * u.deg,
                 plate_settler_s=2.5 * u.cm,
                 plate_settler_thickness=2.0 * u.mm,
                 plate_settler_cantilever_l_max=20.0 * u.cm,
                 plate_settler_vel_capture=0.12 * u.mm / u.s,
                 exit_man_orifice_hl=4.0 * u.cm,
                 exit_man_orifice_n=58,
                 exit_man_orifice_q_ratio_max=0.8,
                 outlet_man_sdr=41,
                 
                 w=41.0 * u.inch):
        """Instantiates a SedimentationTankBay with the specified values.

        All args are optional, and default to values that are optimized for a 20
        L/s plant if not specified.

        Args:
            plant_q (float * u.L / u.s): Flow rate.
            vel_upflow (float * u.mm / u.s): Upflow velocity.
            l_inner (float * u.m): Inner length.
            w_inner (float * u.inch): Inner width.
            diffuser_vel_max (float * u.mm / u.s):  Maximum velocity through a
                diffuser.
            diffuser_n (int): Number of diffusers.
            diffuser_wall_thickness (float * u.inch): Diffuser wall thickness.
            plate_settler_angle (float * u.deg): Angle of plate settlers from
                horizontal.
            plate_settler_s (float * u.cm): Perpendicular space between plate
                settlers.
            plate_settler_thickness (float * u.mm): Plate settler thickness.
            plate_settler_cantilever_l_max (float * u.cm): Maximum length of
                plate settler protruding past the support pipes.
            plate_settler_vel_capture (float * u.mm / u.s): Capture velocity of
                plate settlers.
            exit_man_orifice_hl (float * u.cm): Head loss through an orifice in
                the exit manifold.
            exit_man_orifice_n (int): Number of orifices in the exit manifold
            exit_man_orifice_q_ratio_max (float): Maximum ratio of flow rate
                between any given orifice in the exit manifold.


        Returns:
             SedimentationTankBay object.
        """
        super().__init__(q = q, temp = temp)
        self.vel_upflow = vel_upflow
        self.l_inner = l_inner
        self.w_inner = w_inner
        self.plate_settler_angle = plate_settler_angle
        self.plate_settler_s = plate_settler_s
        self.plate_settler_thickness = plate_settler_thickness
        self.plate_settler_cantilever_l_max = plate_settler_cantilever_l_max
        self.plate_settler_vel_capture = plate_settler_vel_capture
        self.diffuser_vel_max = diffuser_vel_max
        self.diffuser_n = diffuser_n
        self.exit_man_orifice_hl = exit_man_orifice_hl
        self.exit_man_orifice_n = exit_man_orifice_n
        self.exit_man_orifice_q_ratio_max = exit_man_orifice_q_ratio_max
        self.diffuser_wall_thickness = diffuser_wall_thickness

        self.w = w
        self.inlet_hl = inlet_hl
        self.inlet_man_sdr = inlet_man_sdr
        self.outlet_man_sdr = outlet_man_sdr
        
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
        return self.inlet_hl / self.diffuser_n
    
    @property
    def diffuser_vel(self):
        diffuser_vel = np.sqrt(2 * con.GRAVITY * self.diffuser_hl)
        return diffuser_vel.to(u.mm / u.s)
        
    @property
    def diffuser_w_inner(self):
        diffuser_w_inner = self.w * self.vel_upflow / self.diffuser_vel
        return diffuser_w_inner.to(u.cm)

    @property
    def diffuser_a(self):
        """
        Calculates manifold diffuser area from flow rate.
        """
        diffuser_a = self.q / (self.diffuser_vel * self.diffuser_n)
        return diffuser_a

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
        outlet_man_id = pc.diam_pipe(
                self.q_tank,
                self.exit_man_orifice_hl.to(u.m),
                self.l_inner, 
                pc.viscosity_dynamic(self.temp), 
                mat.PVC_PIPE_ROUGH.to(u.m), 
                self.OUTLET_MAN_HL
            )
        outlet_man_nd = pipe.ND_SDR_available(
                outlet_man_id, 
                self.outlet_man_sdr
            )
        return outlet_man_nd

    @property
    def exit_man_orifice_d(self):
        """Return the diameter of the orifices in the exit manifold for the sedimentation tank.

        Returns:
            Diameter of the orifices in the exit manifold for the sedimentation tank (float).
        """
        Q_orifice = self.q/self.exit_man_orifice_n
        D_orifice = np.sqrt(Q_orifice**4)/(np.pi * con.VC_ORIFICE_RATIO * np.sqrt(2 * con.GRAVITY.magnitude * self.exit_man_orifice_hl.magnitude))
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
