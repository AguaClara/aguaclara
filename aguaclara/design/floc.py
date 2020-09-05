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
from aguaclara.design.pipeline import Pipe

import numpy as np
from urllib.parse import quote_plus


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

    _onshape_url = (
        "https://cad.onshape.com/documents/c3a8ce032e33ebe875b9aab4/w/de9ad5474448b34f33fef097/e/08f41d8bdd9a9c90ab396f8a"
    )

    def __init__(self, **kwargs):
        self.ent_l = 1.5 * u.m
        self.chan_w_max = 42.0 * u.inch
        self.l_max = 6.0 * u.m
        self.gt = 37000
        self.hl = 40.0 * u.cm
        self.end_water_depth = 2.0 * u.m
        self.drain_t = 30.0 * u.min
        self.spec = 'sdr41'
        self.drain_pipe = Pipe()
        self.subcomponents = [self.drain_pipe]
        self.polycarb_sheet_w = 42.0 * u.inch
        self.sed_chan_inlet_w_pre_weir = 42.0 * u.inch
        self.dividing_wall_thickness = 15.0 * u.cm
        self.chan_n_parity = 'even'

        super().__init__(**kwargs)

        self._set_drain_pipe()
        super().set_subcomponents()

        if self.chan_n_parity not in ('even', 'odd', 'any'):
            raise AttributeError(
                'chan_n_parity must be set to \'even\', \'odd\', or \'any\'.'
            )

    @property
    def vel_grad_avg(self):
        """The average velocity gradient of water."""
        vel_grad_avg = ((u.standard_gravity * self.hl) /
                        (pc.viscosity_kinematic_water(self.temp) * self.gt)).to(u.s ** -1)
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
                    pc.viscosity_kinematic_water(self.temp) *
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
                return ut.ceil_step(chan_n, step=2)
            elif self.chan_n_parity is 'odd':
                return ut.ceil_step(chan_n, step=2) - 1
            elif self.chan_n_parity is 'any':
                return ut.ceil_step(chan_n, step=1)

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
            step=1 * u.cm
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
                            2 * pc.viscosity_kinematic_water(self.temp) *
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
                  pc.viscosity_kinematic_water(self.temp))
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

    def _set_drain_pipe(self):
        drain_k_minor = \
            hl.PIPE_ENTRANCE_K_MINOR + \
            hl.PIPE_ENTRANCE_K_MINOR + \
            hl.PIPE_EXIT_K_MINOR

        chan_pair_a = 2 * self.chan_l * self.chan_w
        drain_id = (
            np.sqrt(8 * chan_pair_a / (np.pi * self.drain_t) *
                    np.sqrt(
                self.end_water_depth * drain_k_minor /
                (2 * u.standard_gravity)
            )
            )
        ).to_base_units()

        self.drain_pipe = Pipe(
            id=drain_id,
            k_minor=drain_k_minor,
            spec=self.spec
        )

    @property
    def onshape_url_configured(self):
        # Make the configuration string for the flocculator concrete. {{ and }}
        # are used so that str.format() doesn't recognize them.
        concrete_config = (
            '{{"w_channel":"{}", "h_channel":"{}", "l_channel":"{}", "s_baffle"'
            ':"{}", "n_channel":{}, "t_wall":"{}"}}'.format(
                self.chan_w,
                self.end_water_depth,
                self.chan_l,
                self.baffle_s,
                self.chan_n,
                self.dividing_wall_thickness
            )
        )
        # concrete_config = quote_plus(concrete_config)
        encoded_config = '?configuration='

        encoded_config += quote_plus('Concrete_config=' + concrete_config + ';')
        encoded_config += quote_plus('Channel_L=' + str(self.chan_l) + ';')

        configured_url = self._onshape_url + encoded_config
        return configured_url
