from aguaclara.core.units import unit_registry as u

from design.floc import Flocculator

L_MAX = 2.2 * u.m

# Angle of the sloped walls of the entrance tank hoppers
ENT_TANK_SLOPE_ANGLE = 45 * u.deg

# Extra space around the float (increase in effective diameter) to
# ensure that float has free travel
FLOAT_S = 5 * u.cm
HOPPER_PEAK_W = 3 * u.cm
PLATE_S = 2.5 * u.cm
PLATE_THICKNESS = 2 * u.mm
CENTER_PLATE_DIST = PLATE_S + PLATE_THICKNESS
MOD_ND = 0.5 * u.inch

# Distance from the front wall to the pipe stubs in the hopper drains so
# that an operator can easily reach them.
WALL_DRAIN_DIST_MAX = 40 * u.cm

# Entrance tank capture velocity
CAPTURE_BOD_VEL = 8 * u.mm / u.s
PLATE_ANGLE = 50 * u.deg
MOD_SPACER_ND = 0.75 * u.inch

# Thickness of the PVC disk used as the float for the chemical dose
# controller lever arm.
FLOAT_THICKNESS = 5 * u.cm
LAMINA_PIPE_EDGE_S = 5 * u.cm

# Nom diam of the pipes that are embedded in the entrance tank slope
# to support the plate settler module
PLATE_SUPPORT_ND = 3 * u.inch


# Increased to get better mixing (10/10/2015 by Monroe)
RAPID_MIX_EDR = 3 * u.W / u.kg

RAPID_MIX_PLATE_RESTRAINER_ND = 0.5 * u.inch

FLOAT_ND = 8*u.inch

# Minimum pipe size to handle grit and to ensure that the pipe can be
# easily unclogged
DRAIN_MIN_ND = 3*u.inch

DRAIN_ND = 3*u.inch  # This is constant for now

REMOVABLE_WALL_THICKNESS = 5*u.cm

# Parameters are arbitrary - need to be calculated
REMOVABLE_WALL_SUPPORT_H = 4 * u.cm

REMOVABLE_WALL_SUPPORT_THICKNESS = 5*u.cm

HOPPER_LEDGE_THICKNESS = 15*u.cm
WALKWAY_W = 1 * u.m
RAPID_MIX_ORIFICE_PLATE_THICKNESS = 2*u.cm
RAPID_MIX_AIR_RELEASE_ND = 1*u.inch


class EntranceTank:

    def __init__(self, floc=Flocculator()):
        self.floc = floc
        self.q = floc.q
        self.temp = floc.temp

    def a_ent_tank(self):
        """Return the planview area of the entrance tank given plant flow rate,
        headloss, target collision potential, design temperature, and depth of
        water at the end of the flocculator.

        Examples
        --------
        area_ent_tank(20*u.L/u.s, 40*u.cm, 37000, 25*u.degC, 2*u.m)
        1 meter ** 2
        """
        # first guess planview area
        a_new = 1 * u.m**2
        a_ratio = 0
        tolerance = 0.01
        while a_ratio > (1 + tolerance):
            a_et_pv = a_new
            a_floc_pv = self.floc.vol() / (self.floc.END_WATER_HEIGHT + (
                self.floc.HL / 2))
            a_etf_pv = a_et_pv + a_floc_pv

            w_tot = a_etf_pv / self.floc.l_sed_max
            w_chan = w_tot / self.floc.num_channel()

            a_new = L_MAX * w_chan
            a_ratio = a_new / a_et_pv
        return a_new
