from aguaclara.core.units import unit_registry as u
from core.units import unit_registry as u

HL = 0.4 * u.m
COLL_POT = 37000  # collision potential, also referred to as Gt
FREEBOARD = 10 * u.cm
BLANKET_HEIGHT = 0.25 * u.m  # vertical height of floc blanket from peak of slope to weir

# Distance that the rapid mix coupling extends into the first floc channel
# so that the RM orifice place can be fixed in place.
FLOC_COUPLING_EXT_L = 5 * u.cm

##The minor loss coefficient is 2. According to measurements at Agalteca
# and according to
# https://confluence.cornell.edu/display/AGUACLARA/PAHO+Water+Treatment+Publications
# (page 100 in chapter on flocculation)
FLOC_OPTION_H = 0

##Increased both to provide a safety margin on flocculator head loss and
# to simultaneously scale back on the actual collision potential we are
# trying to achieve.
FLOC_BAFFLE_K_MINOR = 2.5

SPACE_FLOC_BAFFLE_SET_BACK_PLASTIC= 2 * u.cm

###Target flocculator collision potential basis of design
COLL_POT_FLOC_BOD = 75 * u.m**(2/3)

##Minimum width of flocculator channel required for constructability based
# on the width of the human hip
FLOC_W_MIN_CONST = 45 * u.cm

##Minimum and maximum distance between expansions to baffle spacing ratio for
#flocculator geometry that will provide optimal efficiency.
HS_RATIO_MIN = 3
HS_RATIO_MAX = 6

##Ratio of the width of the gap between the baffle and the wall and the
# spacing between the baffles.
FLOC_BAFFLE_RATIO = 1

##Max energy dissipation rate in the flocculator, basis of design.
ENERGY_DIS_FLOC_BOD = 10* u.mW/u.kg

FLOC_DRAIN_TIME = 15 * u.min

FLOC_MOD_ND = 0.5 * u.inch

FLOC_SPACER_ND = 0.75 * u.inch

SPACE_FLOC_MOD_EDGE_TO_LAST_PIPE = 10 * u.cm

FLOC_RM_RESTRAINER_ND = 0.5 * u.inch

###Height that the drain stub extends above the top of the flocculator wall
FLOC_DRAIN_STUB_EXT_L = 20 * u.cm

SPACE_FLOC_MOD_PIPE_TO_EDGE = 10 * u.cm

FLOC_BAFFLE_THICKNESS = 2 * u.mm