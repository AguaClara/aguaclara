"""The flocculator of an AguaClara water treatment plant uses turbulence to
cause coagulant and other particles to accumulate, forming flocs.

Example:
    >>> from aguaclara.design.floc import *
    >>> floc = Flocculator(q = 20 * u.L / u.s, hl = 40 * u.cm)
    >>> floc.chan_w
    <Quantity(0.45, 'meter')>
"""
import aguaclara.core.head_loss as hl
import aguaclara.design.human_access as ha
import aguaclara.core.physchem as pc
import aguaclara.core.pipes as pipes
from aguaclara.core.units import unit_registry as u
from aguaclara.design.component import Component

import numpy as np

# TODO: check math with calculating number of channels

class Flocculator(Component):
    """Design an AguaClara plant's flocculator.

    A flocculator's design relies on the entrance tank's design in the same
    plant, but assumed/default values may be used to design a flocculator by
    itself. To design these components in tandem, use 
    :class:`aguaclara.design.ent_floc.EntTankFloc`.

    Attributes:
        - ``BAFFLE_K (float)``: Minor loss coefficient around a baffle edge
        - ``CHAN_N_MIN (int)``: Minimum channel number
        - ``HS_RATIO_MIN (float)``: Minimum H/S ratio
        - ``HS_RATIO_MAX (float)``: Maximum H/S ratio
        - ``SDR (float)``: Standard dimension ratio
        - ``OBSTACLE_OFFSET (bool)``: Whether the baffle obstacles are offset
          from each other 

    Design Inputs:
        - ``q (float * u.L/u.s)``: Flow rate (required)
        - ``temp (float * u.degC)``: Water temperature (optional, defaults to
          20°C)
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
        - ``hl (float * u.cm)``: Head loss (optional, defaults to 40cm)
    """
    # Should the following constants be expert inputs? -Oliver L., oal22, 5 Jun 2019

    # Increased both to provide a safety margin on flocculator head loss and
    # to simultaneously scale back on the actual collision potential we are
    # trying to achieve.
    # Originally calculated to be 2.3 from the equations:

    BAFFLE_K = 2.5
    CHAN_N_MIN = 2
    HS_RATIO_MIN = 3.0
    HS_RATIO_MAX = 6.0
    SDR = 41.0 # This is an expert input in ent, should this be an expert
               # input as well? -Oliver L., oal22, 5 Jun 19
    OBSTACLE_OFFSET = True

    def __init__(self, **kwargs):
        self.ent_l = 1.5 * u.m
        self.chan_w_max = 42.0 * u.inch
        self.l_max = 6.0 * u.m
        self.gt = 37000
        self.hl  =  40.0 * u.cm
        self.end_water_depth  =  2.0 * u.m
        self.drain_t = 30.0 * u.min

        super().__init__(**kwargs)

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
    def w_tot(self):
        return self.vol / (self.end_water_depth * self.chan_l)
    
    @property
    def w_min(self):
        return max(self.w_min_hs_ratio, ha.HUMAN_W_MIN)

    @property
    def chan_n(self):
        """The minimum number of channels based on the maximum
        possible channel width and the maximum length of the channels.
        """
        chan_n = self.w_tot / self.w_min
        return np.ceil(chan_n.to_base_units())
        
    @property
    def chan_w(self):
        """The minimum and hence optimal channel width."""
        # chan_est_W = (
        #         self.vol / (
        #             self.end_water_depth *
        #             (self.chan_n * self.l_max - self.ent_l)
        #         )
        #     ).to(u.m)

        # print("chan_est_W", chan_est_W)
        # # The channel may need to wider than the width that would get the exact required volume.
        # # In that case we will need to shorten the flocculator
        # chan_W = np.amax(
        #         np.array([
        #             1,
        #             (ha.HUMAN_W_MIN/chan_est_W).to(u.dimensionless),
        #             (self.w_min_hs_ratio/chan_est_W).to(u.dimensionless)
        #         ])
        #     ) * chan_est_W
        chan_w = self.w_tot / self.chan_n
        return chan_w

    @property
    def l_max_vol(self):
        l_max_vol = self.vol / \
            (self.CHAN_N_MIN * ha.HUMAN_W_MIN * self.end_water_depth)
        return l_max_vol

    @property
    def chan_l(self):
        """The channel length."""
        # chan_l = (
        #         (
        #             self.vol / (self.chan_w * self.end_water_depth) +
        #             self.ent_l
        #         ) / self.chan_n
        #     ).to(u.m)
        chan_l = min(self.l_max, self.l_max_vol)
        return chan_l.to_base_units()

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
                    (self.q * self.HS_RATIO_MAX / self.chan_w) ** 3
                ) ** (1/4)
            ).to(u.m)

        # expansion_h_max = (((self.BAFFLE_K/ (2 * pc.viscosity_kinematic(self.temp) * self.vel_grad_avg **2)) * \
        #      (((self.q * self.HS_RATIO_MAX)/ self.chan_w) ** 3)) ** (1/4)).to(u.m)
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
        return self.end_water_depth / self.expansion_h - 1

    @property
    def contraction_s(self):
        """The space in the baffle by which the flow contracts."""
        return self.baffle_s * 0.6

    @property
    def obstacle_pipe_od(self):
        """The outer diameter of an obstacle pipe. If the available pipe is 
        greater than 1.5 inches, the obstacle offset will become false."""
        pipe_od = pipes.od_available(self.contraction_s)

        if pipe_od > 1.5 * u.inch:
            self.OBSTACLE_OFFSET = False
            pipe_od = pipes.od_available(pipe_od / 2)

        return pipe_od

    @property
    def drain_k(self):
        """The minor loss coefficient of the drain pipe."""
        drain_K = \
            hl.PIPE_ENTRANCE_K_MINOR + \
            hl.PIPE_ENTRANCE_K_MINOR + \
            hl.PIPE_EXIT_K_MINOR
        return drain_K

    @property
    def drain_id(self):
        """The depth of the drain pipe."""
        chan_pair_a = 2 * self.chan_l * self.chan_w
        drain_id = (
                np.sqrt(8 * chan_pair_a / (np.pi * self.drain_t) *
                    np.sqrt(
                        self.end_water_depth * self.drain_k /
                        (2 * u.standard_gravity)
                    )
                )
            ).to_base_units()
        return drain_id

    @property
    def drain_nd(self):
        """The diameter of the drain pipe."""
        drain_ND = pipes.ND_SDR_available(self.drain_id, self.SDR)
        return drain_ND

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

