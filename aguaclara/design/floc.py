"""Flocculator design.

This module provides all constants and functions necessary to design an
AguaClara flocculator. These constants and functions define both hydraulic
(head loss, retention time, etc.) and geometric (baffle spacing, channel length,
etc.) values that specify a flocculator design.
"""

import aguaclara.core.head_loss as minorloss
import aguaclara.design.human_access as ha
import aguaclara.core.physchem as pc
import aguaclara.core.pipes as pipes
from aguaclara.core.units import unit_registry as u

import numpy as np

# Ratio of the width of the gap between the baffle and the wall and the spacing
# between the baffles.
BAFFLE_RATIO = 1
DRAIN_TIME = 15 * u.min
MOD_ND = 0.5 * u.inch
SPACER_ND = 0.75 * u.inch
MOD_EDGE_LAST_PIPE_S = 10 * u.cm

# Height that the drain stub extends above the top of the flocculator wall
DRAIN_STUB_EXT_H = 0 * u.cm
MOD_PIPE_EDGE_S = 10 * u.cm
BAFFLE_THICKNESS = 2 * u.mm


class Flocculator:
    """Calculates physical dimensions of an AguaClara flocculator.
    Constant instance attributes
    ----------------------------
    - BAFFLE_K (K or K_{baffle}): float
        - The minor loss coefficient of the flocculator baffles.
    - CHANNEL_N_MIN (N_{channel}: int
        - The minimum number of flocculator channels.
    - HS_RATIO_MIN (\Pi_{HS}): float
        - The minimum ratio between expansion height and baffle spacing
    - RATIO_MAX_HS (\Pi_{HS}): float
        - The maximum ratio between expansion height and baffle spacing
    - SDR (sdr): float
        - The standard dimension ratio.
    """

    # Increased both to provide a safety margin on flocculator head loss and
    # to simultaneously scale back on the actual collision potential we are
    # trying to achieve.
    # Originally calculated to be 2.3 from the equations:

    # K_MINOR_FLOC_BAFFLE = (1/VC_BAFFLE_RATIO - 1)**2
    BAFFLE_K = 2.5
    CHANNEL_N_MIN = 2
    HS_RATIO_MIN = 3.0
    RATIO_MAX_HS = 6.0
    SDR = 41.0

    def __init__(
            self,
            Q=20 * u.L/u.s,
            temp=25 * u.degC,
            max_L=6 * u.m,
            Gt=37000,
            HL = 40 * u.cm,
            downstream_H = 2 * u.m,
            ent_tank_L=1.5 * u.m,
            max_W=42 * u.inch,
            drain_t=30 * u.min
    ):
        """Instantiate a Flocculator object, representing a real flocculator
        component.
        :param Q: Flow rate of water through the flocculator.
        :type Q: float * u.L/u.s
        :param temp: Water temperature of the flocculator.
        :type temp: float * u.degC
        :param max_L: Desired maximum length of the flocculator tank. Often equal to the sed tank length.
        :type max_L: float * u.m
        :param Gt: Desired total fluid deformation (collision potential).
        :type Gt: float * u.dimensionless
        :param HL: Desired head loss in the flocculator.
        :type HL: float * u.m
        :param  downstream_H: Desired depth at the downstream end.
        :type  downstream_H: float * u.m
        :param  ent_tank_L: Estimated length of entrance tank.
        :type  ent_tank_L: float * u.m
        :param  max_W: Maximum width of flocculator based on baffle sheet width.
        :type  max_W: float * u.m
        :returns: object
        :rtype: Flocculator
        """
        self.Q = Q
        self.temp = temp
        self.max_L = max_L
        self.Gt = Gt
        self.HL = HL
        self.downstream_H = downstream_H
        self.ent_tank_L = ent_tank_L
        self.max_W = max_W
        self.drain_t = drain_t

    @property
    def vel_grad_avg(self):
        """Calculate the average velocity gradient (G-bar) of water flowing
        through the flocculator.
        :returns: Average velocity gradient (G-bar)
        :rtype: float * 1 / second
        """
        return ((u.standard_gravity * self.HL) /
               (pc.viscosity_kinematic(self.temp) * self.Gt)).to(u.s ** -1)

    @property
    def retention_time(self):
        """Calculates the hydraulic retention time neglecting the volume created by head loss in the flocculator.
        :returns: Hydraulic retention time (:math:`\theta`)
        :rtype: float * second
        """
        return (self.Gt / self.vel_grad_avg).to(u.s)

    @property
    def vol(self):
        """Calculate the target volume (not counting the volume added by head loss) of the flocculator.
        :returns: Target volume
        :rtype: float * meter ** 3
        """
        return (self.Q * self.retention_time).to(u.m ** 3)

    @property
    def W_min_HS_ratio(self):
        """Calculate the minimum flocculator channel width, given the minimum
        ratio between expansion height (H) and baffle spacing (S).
        :returns: Minimum channel width given H_e/S
        :rtype: float * centimeter
        """
        return ((self.HS_RATIO_MIN * self.Q / self.downstream_H) *
               (self.BAFFLE_K /
                (2 * self.downstream_H * pc.viscosity_kinematic(self.temp) * self.vel_grad_avg ** 2)) ** (1/3)
               ).to(u.cm)

    @property
    def channel_n(self):
        """Calculate the minimum number of channels based on the maximum
        possible channel width and the maximum length of the channels.
        Round up to the next even number (factor of 2 shows up twice in equation)
        The channel width must be greater than the hydraulic width that ensure baffle overlap.
        Based on the equation for the flocculator volume
        volume = ([max_L*channel_n] - entrancetank_L)*max_W * downstream_H
        :returns: number of channels
        :rtype: float * dimensionless
        """
        min_hydraulic_W =\
            np.amax(np.array([1, (self.max_W/self.W_min_HS_ratio).to(u.dimensionless)])) * self.W_min_HS_ratio
        return 2*np.ceil(((self.vol / (min_hydraulic_W * self.downstream_H) +
                           self.ent_tank_L) / (2 * self.max_L)).to(u.dimensionless))

    @property
    def channel_W(self):
        """
        The minimum and hence optimal channel width of the flocculator.
        This
        The channel must be
        - wide enough to meet the volume requirement (channel_est_W)
        - wider than human access for construction
        - wider than hydraulic requirement to meet H/S ratio
        Create a dimensionless array of the 3 requirements and then get the maximum

        :returns: Channel width
        :rtype: float * meter
        """
        channel_est_W = (self.vol / (self.downstream_H * (self.channel_n * self.max_L - self.ent_tank_L))).to(u.m)
        # The channel may need to wider than the width that would get the exact required volume.
        # In that case we will need to shorten the flocculator
        channel_W = np.amax(np.array([1, (ha.HUMAN_W_MIN/channel_est_W).to(u.dimensionless),
                                      (self.W_min_HS_ratio/channel_est_W).to(u.dimensionless)])) * channel_est_W
        return channel_W

    @property
    def channel_L(self):
        """
        The channel length of the flocculator. If ha.HUMAN_W_MIN or W_min_HS_ratio
        is the defining constraint for the flocculator width, then the flocculator
        volume will be greater than necessary. Bring the volume back to the design
        volume by shortening the flocculator in this case. This design approach
        will produce flocculators that are the same length as the max_L that was
        specified in many cases. The flocculator will be less than the specified
        length especially for cases with only one or two sed tanks.
        channel_L = (vol/(channel_W * downstream_H) + entrancetank_L)/channel_n
        :returns: Channel length
        :rtype: float * meter
        """
        channel_L = ((self.vol / (self.channel_W * self.downstream_H) + self.ent_tank_L) / self.channel_n).to(u.m)
        return channel_L

    @property
    def expansion_max_H(self):
        """"Return the maximum distance between expansions for the largest
        allowable H/S ratio.
        :returns: Maximum expansion distance
        :rtype: float * meter
        Examples
        --------
        exp_dist_max(20*u.L/u.s, 40*u.cm, 37000, 25*u.degC, 2*u.m)
        0.375 meter
        """
        return (((self.BAFFLE_K / (2 * pc.viscosity_kinematic(self.temp) * (self.vel_grad_avg ** 2))) *
                (self.Q * self.RATIO_MAX_HS / self.channel_W) ** 3) ** (1/4)).to(u.m)

    @property
    def expansion_n(self):
        """Return the minimum number of expansions per baffle space.
        :returns: Minimum number of expansions/baffle space
        :rtype: int
        """
        return np.ceil(self.downstream_H / self.expansion_max_H)

    @property
    def expansion_H(self):
        """Returns the height between flow expansions.
        :returns: Height between flow expansions
        :rtype: float * centimeter
        """
        return (self.downstream_H / self.expansion_n).to(u.cm)

    @property
    def baffle_S(self):
        """Return the spacing between baffles.
        :returns: Spacing between baffles
        :rtype: int
        """
        return ((self.BAFFLE_K /
                ((2 * self.expansion_H * (self.vel_grad_avg ** 2) *
                 pc.viscosity_kinematic(self.temp))).to_base_units()) ** (1/3) *
               self.Q / self.channel_W).to(u.cm)

    @property
    def obstacle_n(self):
        """Return the number of obstacles per baffle.
        :returns: Number of obstacles per baffle
        :rtype: int
        """
        return self.expansion_n - 1

    @property
    def drain_K(self):
        """ Return the minor loss coefficient of the drain pipe.
        :returns: Minor Loss Coefficient
        :return: float
        """
        drain_K = minorloss.PIPE_ENTRANCE_K_MINOR + minorloss.PIPE_ENTRANCE_K_MINOR + minorloss.PIPE_EXIT_K_MINOR
        return drain_K

    @property
    def drain_D(self):
        """ Returns depth of drain pipe.
        :returns: Depth
        :return: float
        """
        tank_A = 2 * self.channel_L * self.channel_W
        drain_D = (np.sqrt(8 * tank_A / (np.pi * self.drain_t) * np.sqrt(
           self.downstream_H * self.drain_K / (2 * u.standard_gravity)))).to_base_units()
        return drain_D

    @property
    def drain_ND(self):
        """Returns the diameter of the drain pipe.
        Each drain pipe will drain two channels because channels are connected by
        a port at the far end and the first channel can't have a drain because
        of the entrance tank. Need to review the design to see if this is a good
        assumption.
        D_{Pipe} = \sqrt{ \frac{8 A_{Tank}}{\pi t_{Drain}} \sqrt{ \frac{h_0 \sum K}{2g} } }
        :returns: list of designed values
        :rtype: float * centimeter
        """
        drain_ND = pipes.ND_SDR_available(self.drain_D, self.SDR)
        return drain_ND

    @property
    def design(self):
        """Returns the designed values.
        :returns: list of designed values (G, t, channel_W, obstacle_n)
        :rtype: int
        """
        floc_dict = {'channel_n': self.channel_n,
                     'channel_L': self.channel_L,
                     'channel_W': self.channel_W,
                     'baffle_S': self.baffle_S,
                     'obstacle_n': self.obstacle_n,
                     'G': self.vel_grad_avg,
                     't': self.retention_time,
                     'expansion_max_H': self.expansion_max_H,
                     'drain_ND': self.drain_ND}
        return floc_dict

    def draw(self):
        """Draw the Onshape flocculator model based off of this object."""
        from onshapepy import Part
        CAD = Part(
            'https://cad.onshape.com/documents/b4cfd328713460beeb3125ac/w/3928b5c91bb0a0be7858d99e/e/6f2eeada21e494cebb49515f'
        )
        CAD.params = {
            'channel_L': self.channel_L,
            'channel_W': self.channel_W,
            'channel_H': self.downstream_H,
            'channel_pairs': self.channel_n/2,
            'baffle_S': self.baffle_S,
        }
