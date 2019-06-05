"""The flocculator of an AguaClara water treatment plant uses turbulence to
cause coagulant and other particles to accumulate, forming flocs.

Example:
    >>> from aguaclara.design.floc import * # See ent.py module docstring.
    >>> floc = Flocculator(q = 20 * u.L / u.s, hl = 40 * u.cm,...)
    >>> floc.chan_w
    42 inch
"""
import aguaclara.core.head_loss as hl
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
    """Design an AguaClara plant's flocculator.

    A flocculator's design relies on the entrance tank's design in the same
    plant, but assumed/default values may be used to design a flocculator by
    itself. To design these components in tandem, use the ``EntTankFloc`` class
    <add link>.

    Design Inputs:
        - ``q (float * u.L/u.s)``: Flow rate (required)
        - ``ent_l (float * u.m)``: Entrance tank length
          (recommmended, defaults to 1.5m)
        - ``chan_w_max (float * u.inch)``: Maximum width (optional, defaults to
          42")
        - ``l_max (float * u.m)``: Maximum length (optional, defaults to 6m)
        - ``end_water_depth (float * u.m)``: Depth at the end 
          (optional, defaults to 2m)
        - ``drain_t (float * u.min)``: Drain time (optional, 
          defaults to 30 mins)
        - ``gt (float)``: Collision potential (optional, defaults to 37000)
        - ``temp (float * u.degC)``: Water temperature (optional, defaults to
          20°C)
        - ``hl (float * u.cm)``: Head loss (optional, defaults to 40cm)
    """

    # Are the following constants necessary? -Oliver L., oal22, 5 Jun 2019

    # Increased both to provide a safety margin on flocculator head loss and
    # to simultaneously scale back on the actual collision potential we are
    # trying to achieve.
    # Originally calculated to be 2.3 from the equations:

    # K_MINOR_FLOC_BAFFLE = (1/VC_BAFFLE_RATIO - 1)**2
    BAFFLE_K = 2.5
    CHANNEL_N_MIN = 2
    HS_RATIO_MIN = 3.0
    RATIO_MAX_HS = 6.0
    SDR = 41.0 # This is an expert input in ent, should this be an expert
               # input as well? -Oliver L., oal22, 5 Jun 19

    def __init__(self, q,
                 ent_l=1.5 * u.m,
                 chan_w_max=42. * u.inch,
                 temp=25. * u.degC,
                 l_max=6. * u.m,
                 gt=37000.,
                 hl = 40. * u.cm,
                 end_water_depth = 2. * u.m,
                 drain_t=30. * u.min):
        self.q = q
        self.temp = temp
        self.l_max = l_max
        self.gt = gt
        self.hl = hl
        self.end_water_depth = end_water_depth
        self.ent_l = ent_l
        self.chan_w_max = chan_w_max
        self.drain_t = drain_t

    @property
    def vel_grad_avg(self):
        """The average velocity gradient of water."""
        vel_grad_avg = ((u.standard_gravity * self.hl) /
               (pc.viscosity_kinematic(self.temp) * self.gt)).to(u.s ** -1)
        return vel_grad_avg

    @property
    def retention_time(self):
        """The hydraulic retention time neglecting the volume 
        created by head loss.
        """
        retention_time = (self.gt / self.vel_grad_avg).to(u.s)
        return retention_time

    @property
    def vol(self):
        """The target volume (not counting the volume added by head loss)."""
        return (self.q * self.retention_time).to(u.m ** 3)

    @property
    def w_min_hs_ratio(self):
        """The minimum channel width."""
        w_min_hs_ratio = (
                (self.HS_RATIO_MIN * self.q / self.end_water_depth) *
                (
                    self.BAFFLE_K / (
                        2 * self.end_water_depth *
                        pc.viscosity_kinematic(self.temp) *
                        self.vel_grad_avg ** 2
                    )
                ) ** (1/3)
            ).to(u.cm)
        return w_min_hs_ratio

    @property
    def chan_n(self):
        """The minimum number of channels based on the maximum
        possible channel width and the maximum length of the channels.
        """
        hydraulic_w_min =np.amax(np.array([
                1, 
                (self.chan_w_max/self.w_min_hs_ratio).to(u.dimensionless)
            ])) * self.w_min_hs_ratio
        chan_n = 2 * np.ceil(
                (
                    (self.vol / 
                        (hydraulic_w_min * self.end_water_depth) + self.ent_l) /
                    (2 * self.l_max)
                ).to(u.dimensionless)
            )
        return chan_n

    @property
    def chan_w(self):
        """The minimum and hence optimal channel width."""
        chan_est_W = (
                self.vol / (
                    self.end_water_depth *
                    (self.chan_n * self.l_max - self.ent_l)
                )
            ).to(u.m)
        # The channel may need to wider than the width that would get the exact required volume.
        # In that case we will need to shorten the flocculator
        chan_W = np.amax(
                np.array([
                    1,
                    (ha.HUMAN_W_MIN/chan_est_W).to(u.dimensionless),
                    (self.w_min_hs_ratio/chan_est_W).to(u.dimensionless)
                ])
            ) * chan_est_W
        return chan_W

    @property
    def chan_l(self):
        """The channel length."""
        chan_l = (
                (
                    self.vol / (self.chan_w * self.end_water_depth) +
                    self.ent_l
                ) / self.chan_n
            ).to(u.m)
        return chan_l

    @property
    def expansion_h_max(self):
        """"The maximum distance between expansions for the largest
        allowable H/S ratio.
        """
        expansion_h_max = (
                (
                    (self.BAFFLE_K / 
                        (
                            2 * pc.viscosity_kinematic(self.temp) *
                            (self.vel_grad_avg ** 2)
                        )
                    ) *
                    (self.q * self.RATIO_MAX_HS / self.chan_w) ** 3
                ) ** (1/4)
            ).to(u.m)
        return expansion_h_max

    @property
    def expansion_n(self):
        """The minimum number of expansions per baffle space."""
        return np.ceil(self.end_water_depth / self.expansion_h_max)

    @property
    def expansion_h(self):
        """The height between flow expansions."""
        return (self.end_water_depth / self.expansion_n).to(u.cm)

    @property
    def baffle_s(self):
        """The spacing between baffles."""
        baffle_s = (
                (self.BAFFLE_K /
                    (
                        (2 * self.expansion_h * (self.vel_grad_avg ** 2) *
                        pc.viscosity_kinematic(self.temp))
                    ).to_base_units()
                ) ** (1/3) * 
                self.q / self.chan_w
            ).to(u.cm)
        return baffle_s

    @property
    def obstacle_n(self):
        """The number of obstacles per baffle."""
        return self.expansion_n - 1

    @property
    def drain_k(self):
        """The minor loss coefficient of the drain pipe."""
        drain_K = \
            hl.PIPE_ENTRANCE_K_MINOR + \
            hl.PIPE_ENTRANCE_K_MINOR + \
            hl.PIPE_EXIT_K_MINOR
        return drain_K

    @property
    def drain_d(self):
        """The depth of the drain pipe."""
        chan_pair_a = 2 * self.chan_l * self.chan_w
        drain_D = (
                np.sqrt(8 * chan_pair_a / (np.pi * self.drain_t) *
                    np.sqrt(
                        self.end_water_depth * self.drain_k /
                        (2 * u.standard_gravity)
                    )
                )
            ).to_base_units()
        return drain_D

    @property
    def drain_nd(self):
        """The diameter of the drain pipe."""
        drain_ND = pipes.ND_SDR_available(self.drain_d, self.SDR)
        return drain_ND

    @property
    def design(self):
        """The designed values."""
        floc_dict = {'channel_n': self.chan_n,
                     'channel_L': self.chan_l,
                     'channel_W': self.chan_w,
                     'baffle_S': self.baffle_s,
                     'obstacle_n': self.obstacle_n,
                     'G': self.vel_grad_avg,
                     't': self.retention_time,
                     'expansion_max_H': self.expansion_h_max,
                     'drain_ND': self.drain_nd}
        return floc_dict

    def draw(self):
        """Draw the Onshape flocculator model based off of this object."""
        from onshapepy import Part
        CAD = Part(
            'https://cad.onshape.com/documents/b4cfd328713460beeb3125ac/w/3928b5c91bb0a0be7858d99e/e/6f2eeada21e494cebb49515f'
        )
        CAD.params = {
            'channel_L': self.chan_l,
            'channel_W': self.chan_w,
            'channel_H': self.end_water_depth,
            'channel_pairs': self.chan_n/2,
            'baffle_S': self.baffle_s,
        }
