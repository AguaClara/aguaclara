"""The Linear Flow Orifice Meter (LFOM) of an AguaClara water treatment plant
imitates a Sutro Weir and produces a linear relation between flow rate and
water level within the entrance tank.

Example:
    >>> from aguaclara.design.lfom import *
    >>> lfom = LFOM(q = 20 * u.L / u.s, hl = 20 * u.cm,...)
    >>> lfom.n_rows
    6
"""
import aguaclara.core.constants as con
import aguaclara.core.physchem as pc
import aguaclara.core.pipes as pipe
import aguaclara.core.utility as ut
import aguaclara.core.drills as drills
from aguaclara.core.units import unit_registry as u
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
        - ``s_orifice (float * u.cm)``: The spacing between orifices (optional, 
          defaults to 0.5cm)
    """
    def __init__(self, q=20.0 * u.L / u.s, temp=20.0 * u.degC,
                 hl=20.0 * u.cm,
                 safety_factor=1.5,
                 sdr=26.0,
                 drill_bits=drills.DRILL_BITS_D_IMPERIAL,
                 s_orifice=0.5 * u.cm):
        super().__init__(q = q, temp = temp)
        self.hl = hl
        self.safety_factor = safety_factor
        self.sdr = sdr
        self.drill_bits = drill_bits
        self.s_orifice = s_orifice

    def stout_w_per_flow(self, z):
        """The width of a stout weir at elevation z."""
        w_per_flow = 2 / ((2 * pc.gravity * z) ** (1 / 2) *
                          con.VC_ORIFICE_RATIO * np.pi * self.hl)
        return w_per_flow.to_base_units()

    @property
    def n_rows(self):
        """ The number of rows."""
        N_estimated = (self.hl * np.pi / (2 * self.stout_w_per_flow(self.hl) * \
             self.q)).to(u.dimensionless)
        variablerow = min(10, max(4, math.trunc(N_estimated.magnitude)))
        return variablerow

    @property
    def b_rows(self):
        """The distance center to center between each row of orifices."""
        return self.hl / self.n_rows

    @property
    def vel_critical(self):
        """The average vertical velocity of the water inside the LFOM pipe
        at the bottom of the orfices."""
        return (4 / (3 * math.pi) * (2 * pc.gravity * self.hl) ** \
            (1 / 2)).to(u.m/u.s)

    @property
    def area_pipe_min(self):
        """The minimum cross-sectional area of the LFOM pipe assuring
        a safety factor."""
        return (self.safety_factor * self.q / self.vel_critical).to(u.cm**2)

    @property
    def nom_diam_pipe(self):
        """The nominal diameter of the LFOM pipe"""
        ID = pc.diam_circle(self.area_pipe_min)
        return pipe.ND_SDR_available(ID, self.sdr)

    @property
    def area_top_orifice(self):
        """The orifice area corresponding to the top row of orifices."""
        # Calculate the center of the top row:
        z = self.hl - 0.5 * self.b_rows
        # Multiply the stout weir width by the height of one row.
        return self.stout_w_per_flow(z) * self.q * self.b_rows

    @property
    def d_orifice_max(self):
        """The maximum orifice diameter."""
        return pc.diam_circle(self.area_top_orifice)

    @property
    def orifice_diameter(self):
        """The actual orifice diameter."""
        maxdrill = min(self.b_rows, self.d_orifice_max)
        return ut.floor_nearest(maxdrill, self.drill_bits)

    @property
    def drillbit_area(self):
        """The area of the actual drill bit."""
        return pc.area_circle(self.orifice_diameter)

    @property
    def n_orifices_per_row_max(self):
        """The max number of orifices allowed in each row."""
        c = math.pi * pipe.ID_SDR(self.nom_diam_pipe, self.sdr)
        b = self.orifice_diameter + self.s_orifice

        return math.floor(c/b)

    @property
    def flow_ramp(self):
        """An array of flow at each row."""
        return np.linspace(1 / self.n_rows, 1, self.n_rows)*self.q

    @property
    def height_orifices(self):
        """The height of the center of each row of orifices."""
        height_orifices = (np.linspace(0, self.n_rows - 1, self.n_rows)) * \
            self.b_rows + 0.5 * self.orifice_diameter
        return height_orifices

    def flow_actual(self, Row_Index_Submerged, N_LFOM_Orifices):
        """The flow for a given number of submerged rows of orifices
        harray is the distance from the water level to the center of the
        orifices when the water is at the max level."""

        flow = 0
        for i in range(Row_Index_Submerged + 1):
            flow = flow + (N_LFOM_Orifices[i] * (
               pc.flow_orifice_vert(self.orifice_diameter,
                                    self.b_rows*(Row_Index_Submerged + 1)
                                    - self.height_orifices[i],
                                    con.VC_ORIFICE_RATIO)))
        return flow

    @property
    def n_orifices_per_row(self):
        """The number of orifices at each level."""
        # H is distance from the bottom of the next row of orifices to the
        # center of the current row of orifices
        H = self.b_rows - 0.5*self.orifice_diameter
        flow_per_orifice = pc.flow_orifice_vert(self.orifice_diameter, H,
         con.VC_ORIFICE_RATIO)
        n = np.zeros(self.n_rows)
        for i in range(self.n_rows):
            # calculate the ideal number of orifices at the current row without
            # constraining to an integer
            flow_needed = self.flow_ramp[i] - self.flow_actual(i, n)
            n_orifices_real = (flow_needed / \
                flow_per_orifice).to(u.dimensionless)
            # constrain number of orifices to be less than the max per row and
            # greater or equal to 0
            n[i] = min((max(0, round(n_orifices_real))),
             self.n_orifices_per_row_max)
        return n

    @property
    def error_per_row(self):
        """The error of the design based off the predicted flow rate and 
        the actual flow rate."""
        FLOW_lfom_error = np.zeros(self.n_rows)
        for i in range(self.n_rows):
            actual_flow = self.flow_actual(i, self.n_orifices_per_row)
            FLOW_lfom_error[i] = (((actual_flow - self.flow_ramp[i]) / \
                 self.flow_ramp[i]).to(u.dimensionless)).magnitude
        return FLOW_lfom_error
        