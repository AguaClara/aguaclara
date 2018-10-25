import numpy
import aguaclara.core.constants as con
import aguaclara.core.physchem as pc
from aguaclara.core.units import unit_registry as u


FREEBOARD = 10 * u.cm
BLANKET_HEIGHT = 0.25 * u.m  # vertical height of floc blanket from peak of slope to weir

# Distance that the rapid mix coupling extends into the first floc channel
# so that the RM orifice place can be fixed in place.
COUPLING_EXT_L = 5 * u.cm

##The minor loss coefficient is 2. According to measurements at Agalteca
# and according to
# https://confluence.cornell.edu/display/AGUACLARA/PAHO+Water+Treatment+Publications
# (page 100 in chapter on flocculation)
OPTION_H = 0

##Increased both to provide a safety margin on flocculator head loss and
# to simultaneously scale back on the actual collision potential we are
# trying to achieve.
BAFFLE_K_MINOR = 2.5

BAFFLE_SET_BACK_PLASTIC_S = 2 * u.cm

###Target flocculator collision potential basis of design
COLL_POT_BOD = 75 * u.m**(2/3)

##Minimum width of flocculator channel required for constructability based
# on the width of the human hip
W_MIN = 45 * u.cm

##Minimum and maximum distance between expansions to baffle spacing ratio for
#flocculator geometry that will provide optimal efficiency.
HS_RATIO_MIN = 3
HS_RATIO_MAX = 6

##Ratio of the width of the gap between the baffle and the wall and the
# spacing between the baffles.
BAFFLE_RATIO = 1

##Max energy dissipation rate in the flocculator, basis of design.
ENERGY_DIS_FLOC_BOD = 10* u.mW/u.kg

DRAIN_TIME = 15 * u.min

MOD_ND = 0.5 * u.inch

SPACER_ND = 0.75 * u.inch

MOD_EDGE_LAST_PIPE_S = 10 * u.cm

RM_RESTRAINER_ND = 0.5 * u.inch

###Height that the drain stub extends above the top of the flocculator wall
DRAIN_STUB_EXT_H = 20 * u.cm

MOD_PIPE_EDGE_S = 10 * u.cm

BAFFLE_THICKNESS = 2 * u.mm

BAFFLE_RIGID_H_THICKNESS = 15*u.cm  # Is this a height or a thickness?

#The piping size for the main part of the floc modules
MODULES_MAIN_ND = (1/2)*u.inch

#The diameter of the oversized cap used to assemble the floc modules
MODULES_LARGE_ND = 1.5*u.inch


class Flocculator:

    K_e = (1 / con.VC_ORIFICE_RATIO ** 2 - 1) ** 2

    HL = 40 * u.cm
    GT = 37000
    END_WATER_HEIGHT = 2 * u.m
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


    @u.wraps(u.m**3, [u.m**3/u.s, u.m, None, u.degK], False)
    def vol_floc(q_plant, hl, Gt, T):
        """Return the total volume of the flocculator using plant flow rate, head
        loss, collision potential and temperature.

        Uses an estimation of flocculator residence time (ignoring the decrease
        in water depth caused by head loss in the flocculator.) Volume does not take
        into account the extra volume that the flocculator will have due to changing
        water level caused by head loss.

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

        Returns
        -------
        ?

        Examples
        --------
        >>> from aguaclara.play import*
        >>>vol_floc(20*u.L/u.s, 40*u.cm, 37000, 25*u.degC)
        6.233 meter3
        """
        vol = (Gt / G_avg(hl, Gt, T).magnitude)*q_plant
        return vol


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


    @u.wraps(u.m**2, [u.m**3/u.s, u.m, None, u.degK, u.m], False)
    def area_ent_tank(q_plant, hl, Gt, T, depth_end):
        """Return the planview area of the entrance tank given plant flow rate,
        headloss, target collision potential, design temperature, and depth of
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
            The planview area of the entrance tank

        Examples
        --------
        >>> from aguaclara.play import*
        >>> area_ent_tank(20*u.L/u.s, 40*u.cm, 37000, 25*u.degC, 2*u.m)
        1 meter ** 2
        """
        # guess the planview area before starting iteration
        A_new = 1*u.m**2
        A_ratio = 0

        while (A_ratio) > 1.01 and (A_ET_PV/A_new) < 0.99:
            A_ET_PV = A_new

            vol_floc = vol_floc(q_plant, hl, Gt, T)
            A_floc_PV = vol_floc/(depth_end + hl/2)
            A_ETF_PV = A_ET_PV + A_floc_PV

            W_min = width_floc_min(q_plant, hl, Gt, T, depth_end)

            W_tot = A_ETF_PV/opt.L_sed

            num_chan = num_channel(q_plant, hl, Gt, T, W_tot)
            W_chan = W_tot/num_chan

            A_new = opt.L_ET_max*W_chan

            A_ratio = A_new/A_ET_PV

        return A_new.to(u.m**2).magnitude


    @u.wraps(u.m, [u.m**3/u.s, u.m, None, u.degK, u.m], False)
    def exp_dist_max(q_plant, hl, Gt, T, W_chan):
        """"Return the maximum distance between expansions for the largest
        allowable H/S ratio.

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

        Returns
        -------
        ?

        Examples
        --------
        >>> from aguaclara.play import*
        >>> exp_dist_max(20*u.L/u.s, 40*u.cm, 37000, 25*u.degC, 2*u.m)
        0.375 meter
        """
        g_avg = G_avg(hl, Gt, T).magnitude
        nu = pc.viscosity_kinematic(T).magnitude
        term1 = (K_e/(2 * (g_avg**2) * nu))**(1/4)
        term2 = (con.HS_RATIO_MAX * q_plant / W_chan) ** (3 / 4)
        exp_dist_max = term1*term2
        return exp_dist_max


    @u.wraps(None, [u.m**3/u.s, u.m, None, u.degK, u.m], False)
    def num_expansions(q_plant, hl, Gt, T, depth_end):
        """"Return the minimum number of expansions per baffle space.

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
        ?

        Examples
        --------
        >>> from aguaclara.play import*
        ???
        """
        return int(np.ceil(depth_end/(exp_dist_max(q_plant, hl, Gt, T)).magnitude))


    @u.wraps(u.m, [u.m**3/u.s, u.m, None, u.degK, u.m], False)
    def height_exp(q_plant, hl, Gt, T, depth_end):
        """Return the actual distance between expansions given the integer
        requirement for the number of expansions per flocculator depth.

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
        ?

        Examples
        --------
        >>> from aguaclara.play import*
        ???
        """
        return depth_end/num_expansions(q_plant, hl, Gt, T)


    @u.wraps(u.m, [u.m**3/u.s, u.m, None, u.degK, u.m], False)
    def baffle_spacing(q_plant, hl, Gt, T, W_chan):
        """Return the spacing between baffles based on the target velocity gradient

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

        Returns
        -------
        ?

        Examples
        --------
        >>> from aguaclara.play import*
        >>> baffle_spacing(20*u.L/u.s, 40*u.cm, 37000, 25*u.degC, 2*u.m)
        0.063 meter
        ."""
        g_avg = G_avg(hl, Gt, T).magnitude
        nu = pc.viscosity_kinematic(T).magnitude
        term1 = (K_e/(2 * exp_dist_max(q_plant, hl, Gt, T, W_chan).magnitude * (g_avg**2) * nu))**(1/3)
        return term1 * q_plant/W_chan


    @u.wraps(None, [u.m**3/u.s, u.m, None, u.degK, u.m, u.m, u.m], False)
    def num_baffles(q_plant, hl, Gt, T, W_chan, L, baffle_thickness):
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
        num = round((L / (baffle_spacing(q_plant, hl, Gt, T, W_chan).magnitude + baffle_thickness)))
        # the one is subtracted because the equation for num gives the number of
        # baffle spaces and there is always one less baffle than baffle spaces due
        # to geometry
        return int(num) - 1