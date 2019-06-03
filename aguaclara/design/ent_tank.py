from aguaclara.core.units import unit_registry as u
import aguaclara.core.physchem as pc
import aguaclara.core.constants as con
import aguaclara.core.materials as mat
import aguaclara.core.pipes as pipe
import aguaclara.core.head_loss as hl

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

	def __init__(self, q=20. * u.L/u.s, temp=20. * u.degC, 
		floc_end_depth=2. * u.m, sdr=41.,floc_chan_w=42. * u.inch):
		self.q = q
		self.temp = temp
		self.floc_end_depth = floc_end_depth
		self.sdr = sdr
		self.floc_chan_w = floc_chan_w
	
@property
def drain_OD(self):
    """Return the nominal diameter of the entrance tank drain pipe. Depth at the
    end of the flocculator is used for headloss and length calculation inputs in
    the diam_pipe calculation.

    Parameters
    ----------
    q_plant: float
        Plant flow rate

    T: float
        Design temperature

    depth_end: float
        The depth of water at the end of the flocculator

    SDR: float
        Standard dimension ratio

    Returns
    -------
    float
        ?

    Examples
    --------
    >>> from aguaclara.play import*
    ??
    """
    nu = pc.viscosity_kinematic(self.t)
    K_minor = hl.PIPE_ENTRANCE_K_MINOR + hl.PIPE_EXIT_K_MINOR + hl.EL90_K_MINOR
    drain_ID = pc.diam_pipe(self.q, self.floc_end_depth, self.floc_end_depth, nu, mat.PVC_PIPE_ROUGH, K_minor)
    drain_ND = pipe.ND_SDR_available(drain_ID, self.sdr)
    return pipe.OD(drain_ND).magnitude



