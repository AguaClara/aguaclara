"""Build an Linear Flow Orifice Meter"""
import aguaclara.core.constants as con
import aguaclara.core.physchem as pc
import aguaclara.core.pipes as pipe
import aguaclara.core.utility as ut
import aguaclara.core.drills as drills
from aguaclara.core.units import unit_registry as u
import numpy as np
import math


class LFOM:

    def __init__(self, q=20*u.L/u.s, hl=20*u.cm, safety_factor=1.5, sdr=26,
                 drill_bits=drills.DRILL_BITS_D_IMPERIAL, s_orifice=0.5*u.cm):

        self.q = q
        self.hl = hl
        self.safety_factor = safety_factor
        self.sdr = sdr
        self.drill_bits = drill_bits
        self.s_orifice = s_orifice

    def stout_w_per_flow(self, z):
        """Return the width of a Stout weir at elevation z. More info
        here. <https://confluence.cornell.edu/display/AGUACLARA/
        LFOM+sutro+weir+research>
        """
        w_per_flow = 2 / ((2 * pc.gravity * z) ** (1 / 2) *
                          con.VC_ORIFICE_RATIO * np.pi * self.hl)
        return w_per_flow.to_base_units()

    @property
    def n_rows(self):
        """This equation states that the open area corresponding to one row
        can be set equal to two orifices of diameter=row height. If there
        are more than two orifices per row at the top of the LFOM then there
        are more orifices than are convenient to drill and more than
        necessary for good accuracy. Thus this relationship can be used to
        increase the spacing between the rows and thus increase the diameter
        of the orifices. This spacing function also sets the lower depth on
        the high flow rate LFOM with no accurate flows below a depth equal
        to the first row height.
        But it might be better to always set then number of rows to 10.
        The challenge is to figure out a reasonable system of constraints that
        reliably returns a valid solution.
        """
        N_estimated = (self.hl * np.pi / (2 * self.stout_w_per_flow(self.hl) * self.q)).to(u.dimensionless)
        variablerow = min(10, max(4, math.trunc(N_estimated.magnitude)))
        return variablerow

    @property
    def b_rows(self):
        """The distance center to center between each row of orifices.
        Message how long it took to load everything (minus packages)"""
        return self.hl / self.n_rows

    @property
    def vel_critical(self):
        """The average vertical velocity of the water inside the LFOM pipe
        at the very bottom of the bottom row of orifices The speed of
        falling water is 0.841 m/s for all linear flow orifice meters of
        height 20 cm, independent of total plant flow rate. """
        return (4 / (3 * math.pi) * (2 * pc.gravity * self.hl) ** (1 / 2)).to(u.m/u.s)

    @property
    def area_pipe_min(self):
        """The minimum cross-sectional area of the LFOM pipe that assures
        a safety factor."""
        return (self.safety_factor * self.q / self.vel_critical).to(u.cm**2)

    @property
    def nom_diam_pipe(self):
        """The nominal diameter of the LFOM pipe"""
        ID = pc.diam_circle(self.area_pipe_min)
        return pipe.ND_SDR_available(ID, self.sdr)

    @property
    def area_top_orifice(self):
        """Estimate the orifice area corresponding to the top row of orifices.
        Another solution method is to use integration to solve this problem.
        Here we use the width of the stout weir in the center of the top row
        to estimate the area of the top orifice
        """
        # Calculate the center of the top row:
        z = self.hl - 0.5 * self.b_rows
        # Multiply the stout weir width by the height of one row.
        return self.stout_w_per_flow(z) * self.q * self.b_rows

    @property
    def d_orifice_max(self):
        """Determine the maximum orifice diameter."""
        return pc.diam_circle(self.area_top_orifice)

    @property
    def orifice_diameter(self):
        """The actual orifice diameter. We don't let the diameter extend
        beyond its row space. """
        maxdrill = min(self.b_rows, self.d_orifice_max)
        return ut.floor_nearest(maxdrill, self.drill_bits)

    @property
    def drillbit_area(self):
        """The area of the actual drill bit."""
        return pc.area_circle(self.orifice_diameter)

    @property
    def n_orifices_per_row_max(self):
        """A bound on the number of orifices allowed in each row.
        The distance between consecutive orifices must be enough to retain
        structural integrity of the pipe.
        """
        c = math.pi * pipe.ID_SDR(self.nom_diam_pipe, self.sdr)
        b = self.orifice_diameter + self.s_orifice

        return math.floor(c/b)

    @property
    def flow_ramp(self):
        """An equally spaced array representing flow at each row."""
        return np.linspace(1 / self.n_rows, 1, self.n_rows)*self.q

    @property
    def height_orifices(self):
        """Calculates the height of the center of each row of orifices.
        The bottom of the bottom row orifices is at the zero elevation
        point of the LFOM so that the flow goes to zero when the water height
        is at zero.
        """

        return (np.linspace(0, self.n_rows-1, self.n_rows))*self.b_rows + 0.5 * self.orifice_diameter

    def flow_actual(self, Row_Index_Submerged, N_LFOM_Orifices):
        """Calculates the flow for a given number of submerged rows of orifices
        harray is the distance from the water level to the center of the
        orifices when the water is at the max level.
        Parameters
        ----------
        Row_Index_Submerged: int
          The index of the submerged row. All rows below and including this
          index are submerged.
        N_LFOM_Orifices: [int]
          The number of orifices at each row.
        Returns
        --------
        The flow through all of the orifices that are submerged.
        """

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
        """Calculate number of orifices at each level given an orifice
        diameter.
        """
        # H is distance from the bottom of the next row of orifices to the
        # center of the current row of orifices
        H = self.b_rows - 0.5*self.orifice_diameter
        flow_per_orifice = pc.flow_orifice_vert(self.orifice_diameter, H, con.VC_ORIFICE_RATIO)
        n = np.zeros(self.n_rows)
        for i in range(self.n_rows):
            # calculate the ideal number of orifices at the current row without
            # constraining to an integer
            flow_needed = self.flow_ramp[i] - self.flow_actual(i, n)
            n_orifices_real = (flow_needed / flow_per_orifice).to(u.dimensionless)
            # constrain number of orifices to be less than the max per row and
            # greater or equal to 0
            n[i] = min((max(0, round(n_orifices_real))), self.n_orifices_per_row_max)
        return n

    @property
    def error_per_row(self):
        """This function calculates the error of the design based on the
        differences between the predicted flow rate
        and the actual flow rate through the LFOM."""
        FLOW_lfom_error = np.zeros(self.n_rows)
        for i in range(self.n_rows):
            actual_flow = self.flow_actual(i, self.n_orifices_per_row)
            FLOW_lfom_error[i] = (((actual_flow - self.flow_ramp[i]) / self.flow_ramp[i]).to(u.dimensionless)).magnitude
        return FLOW_lfom_error

    # def draw(self):
    #     """Draw the LFOM in CAD."""
    #     self.cad.params = {"dHoles": self.orifice_diameter, "nHolesPerRow": str(self.n_orifices_per_row),
    #                        "OD": self.nom_diam_pipe, "bRows": self.b_rows}
