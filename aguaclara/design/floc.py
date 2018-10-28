import math

import aguaclara.core.constants as con
import aguaclara.core.physchem as pc
from aguaclara.design import ent_tank as et
import aguaclara.design.human_access as ha
from aguaclara.core.units import unit_registry as u

# TODO: PLACEHOLDER constant for 'opt.L_sed'
# We don't know what this constant actually is, and would like to find out.
# 'opt' is alias for 'aguaclara.core.optional_inputs', which has been removed.
# 'L_sed' was never in 'optional_inputs'.
L_SED = 1 * u.m

FREEBOARD = 10 * u.cm
# vertical height of floc blanket from peak of slope to weir
BLANKET_HEIGHT = 0.25 * u.m

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
BAFFLE_K_MINOR = 2.5

BAFFLE_SET_BACK_PLASTIC_S = 2 * u.cm

# Target flocculator collision potential basis of design
COLL_POT_BOD = 75 * u.m**(2/3)

# Minimum width of flocculator channel required for constructability based
# on the width of the human hip
W_MIN = ha.HUMAN_W_MIN

# Minimum and maximum distance between expansions to baffle spacing ratio for
# flocculator geometry that will provide optimal efficiency.
HS_RATIO_MIN = 3
HS_RATIO_MAX = 6

# Ratio of the width of the gap between the baffle and the wall and the
# spacing between the baffles.
BAFFLE_RATIO = 1

# Max energy dissipation rate in the flocculator, basis of design.
ENERGY_DIS_FLOC_BOD = 10 * u.mW/u.kg

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


class Flocculator:

    K_e = (1 / con.VC_ORIFICE_RATIO ** 2 - 1) ** 2

    HL = 40 * u.cm
    GT = 37000
    END_WATER_HEIGHT = 2 * u.m  # replaces depth_end
    L_MAX = 6 * u.m

    def __init__(self, q=20*u.L/u.s, temp=25*u.degC):
        """Initializer function to set flow rate and temperature
        :param q: flow rate
        :param temp: temperature
        """
        self.q = q
        self.temp = temp

    def vel_gradient_avg(self):
        """Return the average velocity gradient of a flocculator given head
        loss, collision potential and temperature.

        Examples
        --------
        >>> from aguaclara.play import*
        >>>G_avg(40*u.cm, 37000, 25*u.degC)
        118.715 1/second
        """
        return (pc.gravity.magnitude * self.HL) / \
               (self.GT * pc.viscosity_kinematic(self.temp).magnitude)

    def vol(self):
        """Return the total volume of the flocculator using plant flow rate, head
        loss, collision potential and temperature.

        Uses an estimation of flocculator residence time (ignoring the decrease
        in water depth caused by head loss in the flocculator.) Volume does not take
        into account the extra volume that the flocculator will have due to changing
        water level caused by head loss.

        Examples
        --------
        >>> from aguaclara.play import*
        >>>vol_floc(20*u.L/u.s, 40*u.cm, 37000, 25*u.degC)
        6.233 meter3
        """
        return (self.GT * self.q) / self.vel_gradient_avg

    @u.wraps(u.cm, [u.m**3/u.s, u.m, None, u.degK, u.m], False)
    def width_HS_min(q_plant, hl, Gt, T, depth_end):
        """Return the minimum channel width required to achieve H/S > 3.

        The channel can be wider than this, but this is the absolute minimum width
        for a channel. The minimum width occurs when there is only one expansion per
        baffle and thus the distance between expansions is the same as the depth of
        water at the end of the flocculator.

        Parameters
        ----------
        q_plant: float
            Plant flow rate

        hl: float
            Headloss through the flocculator

        Gt: float
            Target collision potential

        T: float
            Design temperature

        depth_end: float
            The depth of water at the end of the flocculator

        Returns
        -------
        float
            The minimum channel width required to achieve H/S > 3

        Examples
        --------
        >>> from aguaclara.play import*
        >>> width_HS_min(20*u.L/u.s, 40*u.cm, 37000, 25*u.degC, 2*u.m)
        0.1074 centimeter
        """
        nu = pc.viscosity_kinematic(T).magnitude

        w = con.HS_RATIO_MIN * ((K_e / (2 * depth_end * (G_avg(hl, Gt, T).magnitude ** 2)
                                        * nu)) ** (1/3)) * q_plant / depth_end
        return w

    @u.wraps(u.cm, [u.m**3/u.s, u.m, None, u.degK, u.m], False)
    def width_floc_min(q_plant, hl, Gt, T, depth_end):
        """Return the minimum channel width required.

        This takes the maximum of the minimum required to achieve H/S > 3 and the
        minimum required for constructability based on the width of the human hip.

        Parameters
        ----------
        q_plant: float
            Plant flow rate

        hl: float
            Headloss through the flocculator

        Gt: float
            Target collision potential

        T: float
            Design temperature

        depth_end: float
            The depth of water at the end of the flocculator

        Returns
        -------
        float
            The minimum channel width required to achieve H/S > 3

        Examples
        --------
        >>> from aguaclara.play import*
        >>> width_floc_min(20*u.L/u.s, 40*u.cm, 37000, 25*u.degC, 2*u.m)
        45 centimeter
        """
        return max(width_HS_min(q_plant, hl, Gt, T, depth_end).magnitude, con.FLOC_W_MIN_CONST.magnitude)

    @u.wraps(None, [u.m**3/u.s, u.m, None, u.degK, u.m, u.m], False)
    def num_channel(q_plant, hl, Gt, T, W_tot, depth_end):
        """Return the number of channels in the entrance tank/flocculator (ETF).

        This takes the total width of the flocculator and divides it by the minimum
        channel width. A floor function is used to ensure that there are an even
        number of channels.

        Parameters
        ----------
        q_plant: float
            Plant flow rate

        hl: float
            Headloss through the flocculator

        Gt: float
            Target collision potential

        T: float
            Design temperature

        W_tot: float
            Total width

        depth_end: float
            The depth of water at the end of the flocculator

        Returns
        -------
        ?

        Examples
        --------
        >>> from aguaclara.play import*
        >>> num_channel(20*u.L/u.s, 40*u.cm, 37000, 25*u.degC, 20*u.m, 2*u.m)
        2
        """
        num = W_tot/(width_floc_min(q_plant, hl, Gt, T, depth_end).magnitude)
        # floor function with step size 2
        num = np.floor(num/2)*2
        return int(max(num, 2))

    def a_ent_tank(self):
        """Return the planview area of the entrance tank given plant flow rate,
        headloss, target collision potential, design temperature, and depth of
        water at the end of the flocculator.

        Examples
        --------
        >>> from aguaclara.play import*
        >>> area_ent_tank(20*u.L/u.s, 40*u.cm, 37000, 25*u.degC, 2*u.m)
        1 meter ** 2
        """
        # first guess planview area
        a_new = 1 * u.m**2
        a_ratio = 0
        tolerance = 0.01
        while a_ratio > (1 + tolerance):
            a_et_pv = a_new
            a_floc_pv = self.vol / (self.END_WATER_HEIGHT + (self.hl/2))
            a_etf_pv = a_et_pv + a_floc_pv

            w_tot = a_etf_pv / L_SED
            w_chan = w_tot / self.num_channel

            a_new = et.L_MAX * w_chan
            a_ratio = a_new / a_et_pv
        return a_new

    def d_exp_max(self):
        """"Return the maximum distance between expansions for the largest
        allowable H/S ratio.
        TODO: unfinished!

        Examples
        --------
        >>> from aguaclara.play import*
        >>> exp_dist_max(20*u.L/u.s, 40*u.cm, 37000, 25*u.degC, 2*u.m)
        0.375 meter
        """
        g_avg = self.vel_gradient_avg
        nu = pc.viscosity_kinematic(self.temp).magnitude
        term1 = (self.K_e/(2 * (g_avg**2) * nu))**(1/4)
        term2 = (con.HS_RATIO_MAX * self.q / W_chan) ** (3 / 4)
        exp_dist_max = term1*term2
        return exp_dist_max

    def w_channel(self):
        """
        The channel width of the flocculator.  See section 'Flocculation
        Design' of textbook'
        TODO: Unfinished!
        """
        h = self.END_WATER_HEIGHT
        w_min_human = ha.HUMAN_W_MIN
        # perf_metric is (d between flow exp / baffle_spacing)
        w_min_perf_metric

        w_tot = self.vol / (
        n_chan=w_tot / w_min
        w_chan=w_tot / n_chan

    def exp_n(self):
        """Return the minimum number of expansions per baffle space."""
        return math.ceil(self.END_WATER_HEIGHT / self.exp_dist_max)

    def expansion_h(self):
        """Return the actual distance between expansions given the integer
        requirement for the number of expansions per flocculator depth.
        """
        return self.END_WATER_HEIGHT / self.num_expansions

    def baffle_space(self):
        """Return the spacing between baffles based on the target velocity gradient

        Examples
        --------
        >>> from aguaclara.play import*
        >>> baffle_spacing(20*u.L/u.s, 40*u.cm, 37000, 25*u.degC, 2*u.m)
        0.063 meter
        ."""
        nu=pc.viscosity_kinematic(self.temp)
        term1=(self.K_e / (2 * self.exp_dist_max *
                             (self.vel_gradient_avg() ** 2) * nu))**(1/3)
        return term1 * self.q / ha.HUMAN_W_MIN

    @u.wraps(None, [u.m**3/u.s, u.m, None, u.degK, u.m, u.m, u.m], False)
    def num_baffles(self, q_plant, hl, Gt, T, W_chan, L, baffle_thickness):
        """Return the number of baffles that would fit in the channel given the
        channel length and spacing between baffles.

        Parameters
        ----------
        q_plant: float
            Plant flow rate

        hl: float
            Headloss through the flocculator

        Gt: float
            Target collision potential

        T: float
            Design temperature

        W_chan: float
            Channel width

        L: float
            Length

        baffle_thickness: float
            Baffle thickness

        Returns
        -------
        ?

        Examples
        --------
        >>> from aguaclara.play import*
        >>> num_baffles(20*u.L/u.s, 40*u.cm, 37000, 25*u.degC, 2*u.m, 2*u.m, 2*u.m)
        0
        >>> num_baffles(20*u.L/u.s, 20*u.cm, 37000, 25*u.degC, 2*u.m, 2*u.m, 21*u.m)
        -1
        """
        num=round(L / self.baffle_space)
        # the one is subtracted because the equation for num gives the number of
        # baffle spaces and there is always one less baffle than baffle spaces due
        # to geometry
        return int(num) - 1
