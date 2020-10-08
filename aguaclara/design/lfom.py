"""The Linear Flow Orifice Meter (LFOM) of an AguaClara water treatment plant
imitates a sutro weir and produces a linear relation between flow rate and
water level within the entrance tank.

Example:
    >>> from aguaclara.core.units import u
    >>> from aguaclara.design.lfom import LFOM
    >>> lfom = LFOM(q=20 * u.L / u.s, hl=20 * u.cm)
    >>> lfom.row_n
    6
"""
import aguaclara.core.constants as con
import aguaclara.core.physchem as pc
import aguaclara.core.pipes as pipe
import aguaclara.core.utility as ut
import aguaclara.core.drills as drills
from aguaclara.core.units import u
from aguaclara.design.component import Component

import numpy as np
import math


class LFOM(Component):
    """Design and AguaClara plant's LFOM.

    Design Inputs:
        - ``q (float * u.L/u.s)``: Flow rate (recommended, defaults to 20L/s)
        - ``temp (float * u.degC)``: Water temperature (recommended, defaults to
          20°C)
        - ``hl (float * u.cm)``: Head loss (optional, defaults to 20cm)
        - ``safety_factor (float)``: Safety factor (optional, defaults to 1.5)
        - ``sdr (float)``: Standard dimension ratio (optional, defaults to 26)
        - ``drill_bits (float * u.inch array)``: List of drill bits
          (optional)
        - ``orifice_s (float * u.cm)``: The spacing between orifices (optional,
          defaults to 0.5cm)
        - ``min_row_n (int)``: Minimum number of rows of orifices (optional,
          defaults to 4)
        - ``max_row_n (int)``: Maximum number of rows of orifices (optional,
          defaults to 10)
    """
    def __init__(self, **kwargs):
        self.hl = 20.0 * u.cm
        self.safety_factor = 1.5
        self.sdr = 26.0
        self.drill_bits = drills.DRILL_BITS_D_IMPERIAL
        self.orifice_s = 0.5 * u.cm
        self.min_row_n = 4
        self.max_row_n = 10

        super().__init__(**kwargs)

    def stout_w_per_flow(self, h):
        """The width of a stout weir at a given elevation.

        Args:
            - ``h (float * u.m)``: Elevation height
        """
        w_per_flow = 2 / ((2 * u.gravity * h) ** (1 / 2) *
                          con.VC_ORIFICE_RATIO * np.pi * self.hl)
        return w_per_flow.to_base_units()

    @property
    def row_n(self):
        """ The number of rows."""
        N_estimated = (self.hl * np.pi / (2 * self.stout_w_per_flow(self.hl) * \
             self.q)).to(u.dimensionless)
        row_n = min(self.max_row_n,
                    max(self.min_row_n, math.trunc(N_estimated.magnitude)))
        return row_n

    @property
    def row_b(self):
        """The distance center to center between each row of orifices."""
        return self.hl / self.row_n

    @property
    def vel_critical(self):
        """The average vertical velocity of the water inside the LFOM pipe
        at the bottom of the orfices."""
        return (4 / (3 * math.pi) * (2 * u.gravity * self.hl) ** \
            (1 / 2)).to(u.m/u.s)

    @property
    def pipe_a_min(self):
        """The minimum cross-sectional area of the LFOM pipe assuring
        a safety factor."""
        return (self.safety_factor * self.q / self.vel_critical).to(u.cm**2)

    @property
    def pipe_nd(self):
        """The nominal diameter of the LFOM pipe"""
        ID = pc.diam_circle(self.pipe_a_min)
        return pipe.ND_SDR_available(ID, self.sdr)

    @property
    def top_row_orifice_a(self):
        """The orifice area corresponding to the top row of orifices."""
        z = self.hl - 0.5 * self.row_b
        return self.stout_w_per_flow(z) * self.q * self.row_b

    @property
    def orifice_d_max(self):
        """The maximum orifice diameter."""
        return pc.diam_circle(self.top_row_orifice_a)

    @property
    def orifice_d(self):
        """The actual orifice diameter."""
        maxdrill = min(self.row_b, self.orifice_d_max)
        return ut.floor_nearest(maxdrill, self.drill_bits)

    @property
    def drill_bit_a(self):
        """The area of the actual drill bit."""
        return pc.area_circle(self.orifice_d)

    @property
    def orifice_n_max_per_row(self):
        """The max number of orifices allowed in each row."""
        c = math.pi * pipe.ID_SDR(self.pipe_nd, self.sdr)
        b = self.orifice_d + self.orifice_s

        return math.floor(c/b)

    @property
    def q_per_row(self):
        """An array of flow at each row."""
        return np.linspace(1 / self.row_n, 1, self.row_n)*self.q

    @property
    def orifice_h_per_row(self):
        """The height of the center of each row of orifices."""
        height_orifices = (np.linspace(0, self.row_n - 1, self.row_n)) * \
            self.row_b + 0.5 * self.orifice_d
        return height_orifices

    def q_submerged(self, row_n, orifice_n_per_row):
        """The flow rate through some number of submerged rows.

        Args:
            - ``row_n``: Number of submerged rows
        """
        flow = 0 * u.L / u.s
        for i in range(row_n):
            flow = flow + (orifice_n_per_row[i] * (
               pc.flow_orifice_vert(self.orifice_d,
                                    self.row_b*(row_n + 1)
                                    - self.orifice_h_per_row[i],
                                    con.VC_ORIFICE_RATIO)))
        return flow.to(u.L / u.s)

    @property
    def orifice_n_per_row(self):
        """The number of orifices at each level."""
        h = self.row_b - 0.5*self.orifice_d
        flow_per_orifice = pc.flow_orifice_vert(self.orifice_d, h,
         con.VC_ORIFICE_RATIO)
        n = np.zeros(self.row_n)
        for i in range(self.row_n):
            flow_needed = self.q_per_row[i] - self.q_submerged(i, n)
            n_orifices_real = (flow_needed / \
                flow_per_orifice).to(u.dimensionless)
            n[i] = min((max(0, round(n_orifices_real))),
             self.orifice_n_max_per_row)
        return n

    @property
    def error_per_row(self):
        """The error of the design based off the predicted flow rate and
        the actual flow rate."""
        q_error = np.zeros(self.row_n)
        for i in range(self.row_n):
            actual_flow = self.q_submerged(i, self.orifice_n_per_row)
            q_error[i] = (((actual_flow - self.q_per_row[i]) / \
                 self.q_per_row[i]).to(u.dimensionless)).magnitude
        return q_error
