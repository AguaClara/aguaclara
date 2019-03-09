class SedimentationTankBay:
    TANK_L_INNER = 5.8 * u.m  # EI

    TANK_VEL_UP = 1 * u.mm / u.s  # EI

    TANK_W = 42 * u.inch  # EI

    PLATE_SETTLERS_ANGLE = 60 * u.deg  # EI

    PLATE_SETTLERS_S = 2.5 * u.cm  # EI

    PLATE_SETTLERS_THICKNESS = 2 * u.mm  # EI

    PLATE_SETTLERS_L_CANTILEVERED = 20 * u.cm  # EI

    PLATE_SETTLERS_VEL_CAPTURE = 0.12 * u.mm / u.s  # EI

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