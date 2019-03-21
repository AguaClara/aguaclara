from aguaclara.core.units import unit_registry as u

class SedimentationTankBay:
    TANK_L_INNER = 5.8 * u.m  # EI

    TANK_VEL_UP = 1 * u.mm / u.s  # EI

    TANK_W = 42 * u.inch  # EI

    PLATE_SETTLERS_ANGLE = 60 * u.deg  # EI

    PLATE_SETTLERS_S = 2.5 * u.cm  # EI

    PLATE_SETTLERS_THICKNESS = 2 * u.mm  # EI

    PLATE_SETTLERS_L_CANTILEVERED = 20 * u.cm  # EI

    PLATE_SETTLERS_VEL_CAPTURE = 0.12 * u.mm / u.s  # EI


    def __init__(self, q=20*u.L/u.s, tank_l_inner=58*u.m, tank_vel_up = 1 *u.mm/ u.s, tank_w=42*u.inch,
                 plate_settlers_angle = 60*u.deg, plate_settlers_s = 2.5*u.cm, plate_settlers_thickness=2*u.mm,
                 plate_settlers_l_cantilevered=20*u.cm, plate_settlers_vel_capture=0.12*u.mm/u.s):
        self.q = q
        self.tank_l_inner = tank_l_inner
        self.tank_vel_up = tank_vel_up
        self.tank_w = tank_w
        self.plate_settlers_angle = plate_settlers_angle
        self.plate_settlers_s = plate_settlers_s
        self.plate_settlers_thickness = plate_settlers_thickness
        self.plate_settlers_l_cantilevered = plate_settlers_l_cantilevered
        self.plate_settlers_vel_capture = plate_settlers_vel_capture

    @property
    def q_bay(self):
        """Return the maximum flow through one sedimentation tank.

        Returns:
            Maximum flow through one sedimentation tank (float).
        """
        return (self.TANK_L_INNER * self.TANK_VEL_UP.to(u.m/u.s) *
                self.TANK_W.to(u.m)).to(u.L / u.s)
        #rename to q_bay, use to determine how many bays are needed

    @property
    def n(self):
        """Return the number of sedimentation tanks required for a given flow rate.

        Args:
            Q_plant (float): the flow rate


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
        return ((self.TANK_VEL_UP.to(u.inch/u.s).magnitude /
                 self.MANIFOLD_DIFFUSER_VEL_MAX.to(u.inch/u.s).magnitude)
                 * self.TANK_W)

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
        vel_manifold_max = (self.MANIFOLD_DIFFUSER_VEL_MAX.to(u.m / u.s) *
                            math.sqrt(2 * ((1 - (self.MANIFOLD_RATIO_Q_MAN_ORIFICE) ** 2)) /
                                      (((self.MANIFOLD_RATIO_Q_MAN_ORIFICE) ** 2) + 1)))
        return vel_manifold_max

    @property
    @ut.list_handler
    def ID_exit_man(self):
        """Return the inner diameter of the exit manifold by guessing an initial
        diameter then iterating through pipe flow calculations until the answer
        converges within 1%% error

        Args:
            Q_plant (float): the flow rate
            temp (float): guess of initial diameter

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

        Args:
            Q_plant (float): the flow rate
            drill_bits =

        Returns:
            Diameter of the orifices in the exit manifold for the sedimentation tank (float).
        """
        Q_orifice = self.q/self.MANIFOLD_EXIT_MAN_N_ORIFICES
        D_orifice = np.sqrt(Q_orifice**4)/(np.pi * con.RATIO_VC_ORIFICE * np.sqrt(2 * pc.GRAVITY.magnitude * self.MANIFOLD_EXIT_MAN_HL_ORIFICE.magnitude))
        return ut.ceil_nearest(D_orifice, drills.DRILL_BITS_D_METRIC)


    @property
    def L_sed_plate(self):
        """Return the length of a single plate in the plate settler module based on
        achieving the desired capture velocity

        Returns:
            Length of a single plate (float).
        """
        L_sed_plate = ((self.PLATE_SETTLERS_S * ((self.TANK_VEL_UP/self.PLATE_SETTLERS_VEL_CAPTURE)-1)
                      + self.PLATE_SETTLERS_THICKNESS * (self.TANK_VEL_UP/self.PLATE_SETTLERS_VEL_CAPTURE))
                     / (np.sin(self.PLATE_SETTLERS_ANGLE) * np.cos(self.PLATE_ANGLE))
                     ).to(u.m)
        return L_sed_plates

    @property
    def diffuser_a(self):
        """
        Calculates manifold diffuser area from flow rate.
        """
        diffuser_a = self.q_bay / (self.MANIFOLD_DIFFUSER_VEL_MAX * self.DIFFUSER_N)
        return diffuser_a
