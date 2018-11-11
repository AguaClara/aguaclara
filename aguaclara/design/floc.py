import math

import numpy as np

import aguaclara.core.constants as con
import aguaclara.core.physchem as pc
import aguaclara.design.human_access as ha
from aguaclara.core.units import unit_registry as u


HS_RATIO_MIN = 3
HS_RATIO_MAX = 6

# Unused constants - START \/

FREEBOARD = 10 * u.cm

# From slope peak to weir
FLOC_BLANKET_H = 0.25 * u.m

# Distance that the rapid mix coupling extends into the first floc channel
# so that the RM orifice place can be fixed in place.
COUPLING_EXT_L = 5 * u.cm

# The minor loss coefficient is 2. According to measurements at Agalteca
# and according to
# https://confluence.cornell.edu/display/AGUACLARA/PAHO+Water+Treatment+Publications
# (page 100 in chapter on flocculation)
OPTION_H = 0

# Increased both to provide a safety margin on flocculator head loss and
# to simultaneously scale back on the actual collision potential we are
# trying to achieve.
BAFFLE_MINOR_LOSS = 2.5

BAFFLE_SET_BACK_PLASTIC_S = 2 * u.cm

# Target flocculator collision potential basis of design

# Minimum width of flocculator channel required for constructability based
# on the width of the human hip
W_MIN = ha.HUMAN_W_MIN
BOD_GT = 75 * u.m ** (2 / 3)

# Ratio of the width of the gap between the baffle and the wall and the
# spacing between the baffles.
BAFFLE_RATIO = 1

# Max energy dissipation rate in the flocculator, basis of design.
BOD_ENERGY_DISSIPATION_MAX = 10 * u.mW / u.kg

DRAIN_TIME = 15 * u.min

MOD_ND = 0.5 * u.inch

SPACER_ND = 0.75 * u.inch

MOD_EDGE_LAST_PIPE_S = 10 * u.cm

RM_RESTRAINER_ND = 0.5 * u.inch

# Height that the drain stub extends above the top of the flocculator wall
DRAIN_STUB_EXT_H = 20 * u.cm

MOD_PIPE_EDGE_S = 10 * u.cm

BAFFLE_THICKNESS = 2 * u.mm

BAFFLE_RIGID_H_THICKNESS = 15*u.cm  # Is this a height or a thickness?

# The piping size for the main part of the floc modules
MODULES_MAIN_ND = (1/2)*u.inch

# The diameter of the oversized cap used to assemble the floc modules
MODULES_LARGE_ND = 1.5*u.inch

# Unused constants - END /\


class Flocculator:

    K = (1 / con.VC_ORIFICE_RATIO ** 2 - 1) ** 2
    HL = 40 * u.cm
    GT = 37000
    END_WATER_H = 2 * u.m
    L_MAX_SED = 6 * u.m
    CHANNEL_N_MIN = 2

    def __init__(self, q=20*u.L/u.s, temp=25*u.degC, l_sed_max=6*u.m):
        """Initializer function to set flow rate and temperature
        :param q: flow rate
        :param temp: temperature
        """
        self.q = q
        self.temp = temp
        self.l_sed_max = l_sed_max

    @property
    def vel_gradient_avg(self):
        """Return the average velocity gradient of a flocculator given head
        loss, collision potential and temperature.

        Examples
        --------
        >>> (40*u.cm, 37000, 25*u.degC)
        118.715 1/second
        """
        return ((pc.gravity * self.HL) /
                (self.GT * pc.nu(self.temp))).to(u.s ** -1)

    @property
    def retention_time(self):
        """Return the retention time of flocs in a flocculator."""
        return self.GT / self.vel_gradient_avg()

    @property
    def vol(self):
        """Return the total volume of the flocculator using plant flow rate, head loss,
        collision potential and temperature.

        Uses an estimation of flocculator retention time (ignoring the decrease
        in water depth caused by head loss in the flocculator). Volume does not
        take into account the extra volume that the flocculator will have due
        to changing water level caused by head loss.

        Examples
        --------
        vol(20*u.L/u.s, 40*u.cm, 37000, 25*u.degC)
        6.233 meter3

        """
        return (self.GT * self.q) / self.vel_gradient_avg

    @property
    def l_max_vol(self):
        """Return the maximum flocculator channel length that achieves the
        target volume, while still allowing human access.
        """
        return (
            self.vol
            / (self.CHANNEL_N_MIN * ha.HUMAN_W_MIN * self.END_WATER_HEIGHT)
        )

    @property
    def channel_l(self):
        """Return the length of the flocculator channel, as constrained by
        the length of the sedimentation tank (self.L_MAX_SED), and the target
        volume and human access width (self.l_max_vol_target).
        """
        return min(self.L_MAX_SED, self.l_max_vol)

    @property
    def w_min_h_s_ratio(self):
        """Return the minimum channel width required to achieve H/S > 3.

        The channel can be wider than this, but this is the absolute minimum
        width for a channel. The minimum width occurs when there is only one
        expansion per baffle and thus the distance between expansions is the
        same as the depth of water at the end of the flocculator.

        Examples
        --------
        width_HS_min(20*u.L/u.s, 40*u.cm, 37000, 25*u.degC, 2*u.m)
        0.1074 centimeter
        """
        return (
            HS_RATIO_MIN
            * (
                (
                    self.K_e
                    / (
                        2 * self.END_WATER_HEIGHT
                        * (self.vel_gradient_avg.magnitude ** 2)
                        * pc.nu(self.temp)
                    )
                ) ** (1/3)
            ) * self.q / self.END_WATER_HEIGHT
        )

    @property
    def w_min(self):
        """Return the minimum channel width required.

        This takes the maximum of the minimum required to achieve H/S > 3 and
        the minimum required for constructability based on the width of the
        human hip.

        Examples
        --------
        width_floc_min(20*u.L/u.s, 40*u.cm, 37000, 25*u.degC, 2*u.m)
        45 centimeter
        """
        return max(self.w_min_h_s_ratio, W_MIN).to(u.cm)

    @property
    def channel_n(self):
        """Return the number of channels in the entrance tank/flocculator (ETF).

        This takes the total width of the flocculator and divides it by the
        minimum channel width. A floor function is used to ensure that there
        are an even number of channels.

        Examples
        --------
        channel_n(20*u.L/u.s, 40*u.cm, 37000, 25*u.degC, 20*u.m, 2*u.m)
        2
        """
        num = self.w_total / self.w_min
        # floor function with step size 2
        num_floor = np.floor(num / 2) * 2
        return int(max(num_floor, 2))

    @property
    def w_total(self):
        """The total width of the flocculator."""
        return self.vol / (self.channel_l * self.END_WATER_HEIGHT)

    @property
    def channel_w(self):
        """
        The channel width of the flocculator.  See section 'Flocculation
        Design' of textbook'
        """
        return self.w_total / self.channel_n

    @property
    def expansion_h_max(self):
        """"Return the maximum distance between expansions for the largest
        allowable H/S ratio.

        Examples
        --------
        exp_dist_max(20*u.L/u.s, 40*u.cm, 37000, 25*u.degC, 2*u.m)
        0.375 meter
        """
        return ((self.K_e/(2*pc.nu(self.temp)*(self.vel_gradient_avg**2))) *
                (self.q*HS_RATIO_MAX/self.channel_w)**3) ** (1/4)

    @property
    def exp_n(self):
        """Return the minimum number of expansions per baffle space."""
        return math.ceil(self.END_WATER_HEIGHT / self.expansion_h_max)

    @property
    def expansions_h(self):
        """Returns the height between flow expansions."""
        return self.END_WATER_H / self.exp_n

    @property
    def baffles_s(self):
        """Return the spacing between baffles.

        Examples
        --------
        baffles_s(20*u.L/u.s, 40*u.cm, 37000, 25*u.degC, 2*u.m)
        0.063 meter
        """
        return (
            (
                self.K_e
                / (
                    2 * self.expansion_h_max
                    * (self.vel_gradient_avg ** 2)
                    * pc.nu(self.temp)
                )
            ) ** (1/3)
            * self.q / ha.HUMAN_W_MIN
        )

    @property
    def baffles_n(self):
        """Return the number of baffles a channel can contain.

        Examples
        --------
        baffles_n(20*u.L/u.s, 40*u.cm, 37000, 25*u.degC, 2*u.m, 2*u.m, 2*u.m)
        0
        baffles_n(20*u.L/u.s, 20*u.cm, 37000, 25*u.degC, 2*u.m, 2*u.m, 21*u.m)
        -1
        """
        return self.END_WATER_H / self.baffles_s - 1
