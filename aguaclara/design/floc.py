"""The flocculator of an AguaClara water treatment plant uses turbulence to
cause coagulant and other particles to accumulate, forming flocs.

Example:
    >>> from aguaclara.design.floc import *
    >>> floc = Flocculator(q = 20 * u.L / u.s, hl = 40 * u.cm)
    >>> floc.chan_w
    <Quantity(34.0, 'centimeter')>
"""
import aguaclara.core.head_loss as hl
import aguaclara.design.human_access as ha
import aguaclara.core.physchem as pc
import aguaclara.core.pipes as pipes
import aguaclara.core.utility as ut
from aguaclara.core.units import u
from aguaclara.design.component import Component

import numpy as np


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
        - ``gt (float)``: Collision potential (optional, defaults to 37000)
        - ``hl (float * u.cm)``: Head loss (optional, defaults to 40cm)
        - ``end_water_depth (float * u.m)``: Depth at the end 
          (optional, defaults to 2m)
        - ``drain_t (float * u.min)``: Drain time (optional, 
          defaults to 30 mins)
        - ``polycarb_sheet_w (float * u.inch)``: Width of polycarbonate sheets
          used to construct baffles (optional, defaults to 42 in)
        - ``sed_chan_inlet_w_pre_weir (float * u.inch)``: Width of the inlet
          sedimentation channel pre-weir (optional, defaults to 42 in)
        - ``dividing_wall_thickness (float * u.cm)``: Thickness of dividing
          walls between each flocculator channel (optional, defaults to 15 cm)
        - ``chan_n_parity (str)``: Parity of the number of channels. Can be
          \'even\', \'odd\', or \'any\' (optional, defaults to \'even\')
    """
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
        self.polycarb_sheet_w = 42.0 * u.inch
        self.sed_chan_inlet_w_pre_weir = 42.0 * u.inch
        self.dividing_wall_thickness = 15.0 * u.cm
        self.chan_n_parity = 'even'

        super().__init__(**kwargs)

        if self.chan_n_parity not in ('even', 'odd', 'any'):
            raise AttributeError(
                'chan_n_parity must be set to \'even\', \'odd\', or \'any\'.'
            )

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
    def chan_w_min_hs_ratio(self):
        """The minimum channel width."""
        chan_w_min_hs_ratio = (
                (self.HS_RATIO_MIN * self.q / self.end_water_depth) *
                (
                    self.BAFFLE_K / (
                        2 * self.end_water_depth *
                        pc.viscosity_kinematic(self.temp) *
                        self.vel_grad_avg ** 2
                    )
                ) ** (1/3)
            ).to(u.cm)
        return chan_w_min_hs_ratio

    @property
    def chan_w_min(self):
        """The minimum channel width."""
        return ut.min(self.chan_w_min_hs_ratio, self.polycarb_sheet_w).to(u.cm)
        
    @property
    def chan_n(self):
        """The minimum number of channels based on the maximum
        possible channel width and the maximum length of the channels.
        """
        if self.q < 16 * u.L / u.s:
            return 1
        else:
            chan_n = ((
                    (self.vol /
                        (self.polycarb_sheet_w * self.end_water_depth)
                    ) + self.ent_l
                ) / self.chan_l).to_base_units()

            if self.chan_n_parity is 'even':
                return ut.ceil_step(chan_n, step = 2)
            elif self.chan_n_parity is 'odd':
                return ut.ceil_step(chan_n, step = 2) - 1
            elif self.chan_n_parity is 'any':
                return ut.ceil_step(chan_n, step = 1)

    @property
    def chan_w_min_gt(self):
        """The channel width minimum regarding the collision potential."""
        chan_w_min_gt = self.vol / (
                self.end_water_depth * (self.chan_n * self.chan_l - self.ent_l)
            )
        return chan_w_min_gt.to(u.cm)

    @property
    def chan_w(self):
        """The channel width."""
        chan_w = ut.ceil_step(
            ut.max(self.chan_w_min_gt, self.chan_w_min),
            step = 1 * u.cm
            )
        return chan_w

    @property
    def l_max_vol(self):
        """The maximum length depeneding on the volume."""
        l_max_vol = self.vol / \
            (self.CHAN_N_MIN * self.chan_w_min * self.end_water_depth)
        return l_max_vol.to(u.m)

    @property
    def chan_l(self):
        """The channel length."""
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
        return drain_id.to(u.inch)

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


def print_vals():
    # myF = floc.Flocculator(q=flow,ent_l=0*u.m,temp=Temperature,hl=50*u.cm,)
    n = 50
    mytemp = 15*u.degC
    GraphQ = np.linspace(0,1,n)*200*u.L/u.s
    myFs =np.empty(n, dtype=type(Flocculator))
    residencetimes = np.empty(n)*u.s
    gradients = np.empty(n)*u.Hz
    bafflespacing = np.empty(n)*u.cm
    channels = np.empty(n)
    channel_w = np.empty(n)*u.cm
    for i in range(1,n):
        myFs[i] = Flocculator(q=GraphQ[i],temp = mytemp)
        residencetimes[i] = myFs[i].retention_time
        gradients[i] = myFs[i].vel_grad_avg
        bafflespacing[i] = myFs[i].baffle_s
        channels[i] = myFs[i].chan_n
        channel_w[i] = myFs[i].chan_w

    print(channels)
    for w in channel_w:
        print(w)