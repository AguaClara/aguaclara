from aguaclara.core.units import unit_registry as u
import aguaclara.core.utility as ut

class SedimentationTankBay:
    """Calculates necessary dimensions and values for SedimentationTankBay.
    """

    def __init__(self,
                 q=20*u.L/u.s,
                 tank_l_inner=58*u.m,
                 tank_vel_up = 1 *u.mm/ u.s,
                 tank_w=42*u.inch,
                 plate_settlers_angle = 60*u.deg,
                 plate_settlers_s = 2.5*u.cm,
                 plate_settlers_thickness=2*u.mm,
                 plate_settlers_l_cantilevered=20*u.cm,
                 plate_settlers_vel_capture=0.12*u.mm/u.s,
                 manifold_diffuser_vel_max = 442.9 * u.mm / u.s,
                 diffuser_n = 108,
                 manifold_exit_man_hl_orifice = 4 * u.cm,
                 manifold_exit_man_n_orifices = 58,
                 manifold_ratio_q_man_orifice = 0.8,
                 manifold_diffuser_thickness_wall = 1.17 *u.inch):
        """Instantiates a SedimentationTankBay with specified values.
        Args:
            q (float): Flow rate
            tank_l_inner (float): Inner length of the tank
            tank_vel_up (float): Upflow velocity through a sedimentation tank
            tank_w (float): Width of the tank
            plate_settlers_angle (int): Angle of plate settlers from horizontal
            plate_settlers_s (float): Perpendicular distance between plates, not the horizontal distance between plates
            plate_settlers_thickness (float): Thickness of the plate settlers
            plate_settlers_l_cantilevered (float): Maximum length of sed plate sticking out past module pipes without any
            additional support
            plate_settlers_vel_capture (float): Velocity capture of plate settlers
            manifold_diffuser_vel_max (float):  Maximum velocity through a diffuser
            diffuser_n (int): number of diffusers per sed tank
            manifold_exit_man_hl_orifice (float): Headloss through an orifice in the exit manifold
            manifold_exit_man_n_orifices (int): Number of orifices in the exit manifold
            manifold_ratio_q_man_orifice (float): flow distribution from the inlet manifold
            manifold_diffuser_thickness_wall (float): wall thickness of diffuser


        Returns:
             An instantiated object of SedimentationTankBay class

        """
        self.q = q
        self.tank_l_inner = tank_l_inner
        self.tank_vel_up = tank_vel_up
        self.tank_w = tank_w
        self.plate_settlers_angle = plate_settlers_angle
        self.plate_settlers_s = plate_settlers_s
        self.plate_settlers_thickness = plate_settlers_thickness
        self.plate_settlers_l_cantilevered = plate_settlers_l_cantilevered
        self.plate_settlers_vel_capture = plate_settlers_vel_capture
        self.manifold_diffuser_vel_max = manifold_diffuser_vel_max
        self.diffuser_n = diffuser_n
        self.manifold_exit_man_hl_orifice = manifold_exit_man_hl_orifice
        self.manifold_exit_man_n_orifices = manifold_exit_man_n_orifices
        self.manifold_ratio_q_man_orifice = manifold_ratio_q_man_orifice
        self.manifold_diffuser_thickness_wall = manifold_diffuser_thickness_wall

    @property
    def q_bay(self):
        """Return the maximum flow through one sedimentation tank.

        Returns:
            Maximum flow through one sedimentation tank (float).
        """
        return (self.tank_l_inner * self.tank_vel_up.to(u.m/u.s) *
                self.tank_w.to(u.m)).to(u.L / u.s)
        #rename to q_bay, use to determine how many bays are needed

    @property
    def n(self):
        """Return the number of sedimentation tanks required for a given flow rate.

        Returns:
            Number of sedimentation tanks required for a given flow rate (int).
        """
        # q = self.q_tank.magnitude
        return int(np.ceil(self.q / self.q_tank))
        # Part of logic at the sed_tank level


    @property
    def w_diffuser_inner_min(self):
        """Return the minimum inner width of each diffuser in the sedimentation tank.

        Returns:
            Minimum inner width of each diffuser in the sedimentation tank (float).
        """
        return ((self.tank_vel_up.to(u.inch/u.s).magnitude /
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
                            math.sqrt(2 * ((1 - (self.manifold_ratio_q_man_orifice) ** 2)) /
                                      (((self.manifold_ratio_q_man_orifice) ** 2) + 1)))
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
        D_orifice = np.sqrt(Q_orifice**4)/(np.pi * con.RATIO_VC_ORIFICE * np.sqrt(2 * pc.GRAVITY.magnitude * self.manifold_exit_man_hl_orifice.magnitude))
        return ut.ceil_nearest(D_orifice, drills.DRILL_BITS_D_METRIC)


    @property
    def L_sed_plate(self):
        """Return the length of a single plate in the plate settler module based on
        achieving the desired capture velocity

        Returns:
            Length of a single plate (float).
        """
        L_sed_plate = ((self.plate_settlers_s * ((self.tank_vel_up/self.plate_settlers_vel_capture)-1)
                      + self.plate_settlers_thickness * (self.tank_vel_up/self.plate_settlers_vel_capture))
                     / (np.sin(self.plate_settlers_angle) * np.cos(self.plate_settlers_angle))
                     ).to(u.m)
        return L_sed_plates

    @property
    def diffuser_a(self):
        """
        Calculates manifold diffuser area from flow rate.
        """
        diffuser_a = self.q_bay / (self.manifold_diffuser_vel_max * self.diffuser_n)
        return diffuser_a
