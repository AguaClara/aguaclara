from aguaclara.core.units import unit_registry as u
from core.units import unit_registry as u

L_MAX = 2.2 * u.m

# Angle of the sloped walls of the entrance tank hoppers
ENT_TANK_SLOPE_ANGLE = 45 * u.deg

# Extra space around the float (increase in effective diameter) to ensure
# that float has free travel
ENT_TANK_FLOAT_S = 5 * u.cm
ENT_TANK_HOPPER_PEAK_W = 3 * u.cm
ENT_TANK_PLATE_S = 2.5 * u.cm
ENT_TANK_PLATE_THICKNESS = 2 * u.mm
CENTER_ENT_TANK_PLATE_DIST = ENT_TANK_PLATE_S + ENT_TANK_PLATE_THICKNESS
ENT_TANK_MOD_ND = 0.5 * u.inch

# Distance from the front wall to the pipe stubs in the hopper drains so
# that an operator can easily reach them.
ENT_TANK_WALLTODRAIN_L_MAX = 40 * u.cm

# Entrance tank capture velocity
ENT_TANK_CAPTURE_BOD_VEL = 8 * u.mm / u.s
ENT_TANK_PLATE_ANGLE = 50 * u.deg
ENT_TANK_MOD_SPACER_ND = 0.75 * u.inch

# Thickness of the PVC disk used as the float for the chemical dose
# controller lever arm.
ENT_TANK_FLOAT_THICKNESS = 5 * u.cm
ENT_TANK_LAMINA_PIPETOEDGE_S = 5 * u.cm

# Nom diam of the pipes that are embedded in the entrance tank slope
# to support the plate settler module
ENT_TANK_PLATE_SUPPORT_ND = 3 * u.inch


# Increased to get better mixing (10/10/2015 by Monroe)
RAPID_MIX_EDR = 3 * u.W / u.kg

RAPID_MIX_PLATE_RESTRAINER_ND = 0.5 * u.inch