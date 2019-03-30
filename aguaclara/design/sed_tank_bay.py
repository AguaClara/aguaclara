"""Calculate hydraulic dimensions of a sedimentation tank bay.

Example:
    >>> from aguaclara.design.sed_tank_bay import SedimentationTankBay
"""

from aguaclara.core.units import unit_registry as u
import aguaclara.core.constants as con
import aguaclara.core.materials as mat
from aguaclara.core import drills
import aguaclara.core.utility as ut
import numpy as np
import math


class SedimentationTankBay:
    """Calculates necessary dimensions and values for SedimentationTankBay.

    Example:
        >>> sed_tank_bay = SedimentationTankBay()
    """

    def __init__(self,
                 q=20.0 * u.L / u.s,
                 vel_upflow=1.0 * u.mm / u.s,
                 l_inner=5.8 * u.m,
                 w_inner=42.0 * u.inch,
                 diffuser_vel_max=442.9 * u.mm / u.s,
                 diffuser_n=108,
                 diffuser_wall_thickness=1.17 * u.inch,
                 plate_settler_angle=60.0 * u.deg,
                 plate_settler_s=2.5 * u.cm,
                 plate_settler_thickness=2.0 * u.mm,
                 plate_settler_l_cantilever_max=20.0 * u.cm,
                 plate_settler_vel_capture=0.12 * u.mm / u.s,
                 exit_man_orifice_hl=4.0 * u.cm,
                 exit_man_orifice_n=58,
                 exit_man_orifice_q_ratio_max=0.8):
        """Instantiates a SedimentationTankBay with the specified values.

        All args are optional, and default to values that are optimized for 20
        L/s if not specified.

        Args:
            q (float * u.L / u.s): Flow rate.
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
            plate_settler_l_cantilever_max (float * u.cm): Maximum length of
                plate settler protruding past the support pipes.
            plate_settler_vel_capture (float * u.mm / u.s): Capture velocity of
                plate settlers.
            exit_man_orifice_hl (float * u.cm): Head loss through an orifice in
                the exit manifold.
            exit_man_orifice_n (int): Number of orifices in the exit manifold
            exit_man_orifice_q_ratio_max (float): Maximum ratio of flow rate
                between any given orifice in the exit manifold.


        Returns:
             An instantiated object of SedimentationTankBay class

        """
        self.q = q
        self.l_inner = l_inner
        self.vel_upflow = vel_upflow
        self.tank_w = w_inner
        self.plate_settlers_angle = plate_settler_angle
        self.plate_settlers_s = plate_settler_s
        self.plate_settlers_thickness = plate_settler_thickness
        self.plate_settlers_l_cantilevered = plate_settler_l_cantilever_max
        self.plate_settlers_vel_capture = plate_settler_vel_capture
        self.manifold_diffuser_vel_max = diffuser_vel_max
        self.diffuser_n = diffuser_n
        self.manifold_exit_man_hl_orifice = exit_man_orifice_hl
        self.manifold_exit_man_n_orifices = exit_man_orifice_n
        self.manifold_ratio_q_man_orifice = exit_man_orifice_q_ratio_max
        self.manifold_diffuser_thickness_wall = diffuser_wall_thickness

    @property
    def q_bay(self):
        """Return the maximum flow through one sedimentation tank.

        Returns:
            Maximum flow through one sedimentation tank (float).
        """
        return (self.l_inner * self.vel_upflow.to(u.m/u.s) *
                self.tank_w.to(u.m)).to(u.L / u.s)
        #rename to q_bay, use to determine how many bays are needed

    @property
    def n(self):
        """Return the number of sedimentation tanks required for a given flow rate.

        Returns:
            Number of sedimentation tanks required for a given flow rate (int).
        """
        return int(np.ceil(self.q / self.q_bay))

    @property
    def w_diffuser_inner_min(self):
        """Return the minimum inner width of each diffuser in the sedimentation tank.

        Returns:
            Minimum inner width of each diffuser in the sedimentation tank (float).
        """
        return ((self.vel_upflow.to(u.inch/u.s).magnitude /
                 self.manifold_diffuser_vel_max.to(u.inch/u.s).magnitude)
                 * self.tank_w)

    # Note: we need to specify in Onshape a 15% stretch difference between
    # the circumference of both diffuser ends' inner/outer circumferences.
    # We can model the aggregate diffuser jet as one continuous flow. Don't
    # correct for the thickness that separates each diffuser's effluent orifice.


    @property
    def vel_inlet_man_max(self):
        """Return the maximum velocity through the manifold.

        Returns:
            Maximum velocity through the manifold (float).
        """
        vel_manifold_max = (self.manifold_diffuser_vel_max.to(u.m / u.s) *
                            math.sqrt(2 * (1 - self.manifold_ratio_q_man_orifice ** 2) /
                                      (self.manifold_ratio_q_man_orifice ** 2 + 1)))
        return vel_manifold_max

    @property
    @ut.list_handler
    def ID_exit_man(self):
        """Return the inner diameter of the exit manifold by guessing an initial
        diameter then iterating through pipe flow calculations until the answer
        converges within 1%% error

        Returns:
            Inner diameter of the exit manifold (float).
        """
        #Inputs do not need to be checked here because they are checked by
        #functions this function calls.
        """
        nu = pc.viscosity_dynamic(temp)
        hl = self.MANIFOLD_EXIT_MAN_HL_ORIFICE.to(u.m)
        L = self.TANK_L
        N_orifices = self.MANIFOLD_EXIT_MAN_N_ORIFICES
        K_minor = con.K_MINOR_PIPE_EXIT
        pipe_rough = mat.PIPE_ROUGH_PVC.to(u.m)

        D = max(pc.diam_pipemajor(self.q, hl, L, nu, pipe_rough).magnitude,
                pc.diam_pipeminor(self.q, hl, K_minor).magnitude)
        err = 1.00
        while err > 0.01:
                D_prev = D
                f = pc.fric(self.q, D_prev, nu, pipe_rough)
                D = ((8*self.q**2 / pc.GRAVITY.magnitude * np.pi**2 * hl) *
                     (((f*L/D_prev + K_minor) * (1/3 + 1/(2 * N_orifices) + 1/(6 * N_orifices**2)))
                      / (1 - self.MANIFOLD_RATIO_Q_MAN_ORIFICE**2)))**0.25
                err = abs(D_prev - D) / ((D + D_prev) / 2)
        return D"""
        pipe_rough = mat.PVC_PIPE_ROUGH.to(u.m)
        id = ((self.q / (np.pi / 4 * ((2 * con.GRAVITY * pipe_rough) ** 1 / 2))) ** 1 / 2) * u.m
        return id



    @property
    def D_exit_man_orifice(self):
        """Return the diameter of the orifices in the exit manifold for the sedimentation tank.

        Returns:
            Diameter of the orifices in the exit manifold for the sedimentation tank (float).
        """
        Q_orifice = self.q/self.manifold_exit_man_n_orifices
        D_orifice = np.sqrt(Q_orifice**4)/(np.pi * con.VC_ORIFICE_RATIO * np.sqrt(2 * con.GRAVITY.magnitude * self.manifold_exit_man_hl_orifice.magnitude))
        return ut.ceil_nearest(D_orifice, drills.DRILL_BITS_D_METRIC)


    @property
    def L_sed_plate(self):
        """Return the length of a single plate in the plate settler module based on
        achieving the desired capture velocity

        Returns:
            Length of a single plate (float).
        """
        L_sed_plate = ((self.plate_settlers_s * ((self.vel_upflow/self.plate_settlers_vel_capture)-1)
                      + self.plate_settlers_thickness * (self.vel_upflow/self.plate_settlers_vel_capture))
                     / (np.sin(self.plate_settlers_angle) * np.cos(self.plate_settlers_angle))
                     ).to(u.m)
        return L_sed_plate

    @property
    def diffuser_a(self):
        """
        Calculates manifold diffuser area from flow rate.
        """
        diffuser_a = self.q_bay / (self.manifold_diffuser_vel_max * self.diffuser_n)
        return diffuser_a
