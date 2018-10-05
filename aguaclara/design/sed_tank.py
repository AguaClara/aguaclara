from aguaclara.core.units import unit_registry as u

PLANT_FLOOR_THICKNESS = 0.2 * u.m  # plant floor slab thickness
WALL_THICKNESS = 0.15 * u.m  # thickness of sed tank dividing wall
HL_OUTLET_MAN = 4 * u.cm  # head loss through the outlet manifold

VEL_SED_UP_BOD = 1 * u.mm/u.s

##Plate settler
VEL_SED_CONC_BOD = 0.12 * u.mm/u.s  # capture velocity

SED_PLATE_ANGLE = 60 * u.deg

SPACE_SED_PLATE = 2.5*u.cm

N_SED_MODULE_PLATES_MIN = 8

# This is moved to template because SED_PLATE_THICKNESS is in materials.yaml
# CENTER_SED_PLATE_DIST = SPACE_SED_PLATE + SED_PLATE_THICKNESS

# Bottom of channel
SED_SLOPE_ANGLE = 50 * u.deg

##This slope needs to be verified for functionality in the field.
# A steeper slope may be required in the floc hopper.
SED_HOPPER_SLOPE_ANGLE = 45 * u.deg

WATER_SED_EST_H = 2 * u.m

SED_GATE_VALVE_URL = "https://confluence.cornell.edu/download/attachments/173604905/Sed-Scaled-Gate-Valve-Threaded.dwg"

SUPPORT_BOLT_URL = "https://confluence.cornell.edu/download/attachments/173604905/PlateSettlerSupportBolt.dwg"

##Inlet channel
HEADLOSS_SED_WEIR_MAX = 5 * u.cm

##Height of the inlet channel overflow weir above the normal water level
# in the inlet channel so that the far side of the overflow weir does not
# fill with water under normal operating conditions. This means the water
# level in the inlet channel will increase when the inlet overflow weir
# is in use.
SED_INLET_WEIR_FREE_BOARD_H = 2 * u.cm

SED_WEIR_THICKNESS = 5*u.cm

HL_SED_INLET_MAX = 1 * u.cm

# ratio of the height to the width of the sedimentation tank inlet channel.
HW_SED_INLET_RATIO = 0.95

##Exit launder
##Target headloss through the launder orifices
HEADLOSS_SED_LAUNDER_BOD = 4 * u.cm

##Acceptable ratio of min to max flow through the launder orifices
FLOW_LAUNDER_ORIFICES_RATIO = 0.80

##Center to center spacing of orifices in the launder
CENTER_SED_LAUNDER_EST_DIST = 10 * u.cm

##The additional length needed in the launder cap pipe that is to be
# inserted into the launder coupling
SED_LAUNDER_CAP_EXCESS_L = 3 * u.cm

##Space between the top of the plate settlers and the bottom of the
# launder pipe
LAMELLA_TO_LAUNDER_H = 5 * u.cm

##The additional length needed in the launder cap pipe that is to be
# inserted into the launder coupling

##Diameter of the pipe used to hold the plate settlers together
NDETER_SED_MOD = 0.5 * u.inch

##Diameter of the pipe used to create spacers. The spacers slide over the
# 1/2" pipe and are between the plates
NDETER_SED_MOD_SPACER = 0.75 * u.inch

SDR_SED_MOD_SPACER = 17

##This is the vertical thickness of the lip where the lamella support sits. mrf222
SED_LAMELLA_LEDGE_THICKNESS = 8 * u.cm

SPACE_SED_LAMELLA_PIPE_TO_EDGE = 5 * u.cm

##Approximate x-dimension spacing between cross pipes in the plate settler
# support frame.
CENTER_SED_PLATE_FRAME_CROSS_EST_DIST = 0.8 * u.m

##Estimated plate length used to get an initial estimate of sedimentation
# tank active length.
SED_PLATE_EST_L = 60 * u.cm

##Pipe size of the support frame that holds up the plate settler modules
NDETER_SED_PLATE_FRAME = 1.5 * u.inch

##Floc weir

#Vertical distance from the top of the floc weir to the bottom of the pipe
# frame that holds up the plate settler modules
FLOC_WEIR_TO_PLATE_FRAME_H = 10 * u.cm

##Minimum length (X dimension) of the floc hopper
SED_HOPPER_MIN_L = 50 * u.cm

##Inlet manifold
##Max energy dissipation rate in the sed diffuser outletS
ENERGY_DIS_SED_INT_MAX = 150 * u.mW/u.kg

##Ratio of min to max flow through the inlet manifold diffusers
FLOW_SED_INLET_RATIO = 0.8

SED_MANIFOLD_ND_MAX = 8 * u.inch

SDR_SED_MANIFOLD = 41  # SDR of pipe for sed tank inlet manifold

##This is the minimum distance between the inlet manifold and the slope
# of the sed tank.
SPACE_SED_INLET_MAN_SLOPE = 10 * u.cm

##Length of exposed manifold stub coming out of the floc weir to which the
# free portion of the inlet manifold is attached with a flexible coupling.
SED_MAN_CONNECTION_STUB_L = 4 * u.cm

##Space between the end of the manifold pipe and the edge of the first
# diffuser's hole, or the first manifold orifice.

SED_MANIFOLD_FIRST_DIFFUSER_GAP_L = 3 * u.cm

##Vertical distance from the edge of the jet reverser half-pipe to the tip
# of the inlet manifold diffusers
JET_REVERSER_TO_DIFFUSERS_H = 3 * u.cm

##Gap between the end of the inlet manifold pipe and the end wall of the
# tank to be able to install the pipe
SED_MANIFOLD_PIPE_FROM_TANK_END_L = 2  *u.cm

SED_WALL_TO_DIFFUSER_GAP_MIN_L = 3 * u.cm

##Diameter of the holes drilled in the manifold so that the molded 1"
# diffuser pipes can fit tightly in place (normal OD of a 1" pipe is
# close to 1-5/16")
DIAM_SED_MANIFOLD_PORT = 1.25 * u.inch

JET_REVERSER_ND = 3 * u.inch  # nominal diameter of pipe used for jet reverser in bottom of set tank

SDR_REVERSER = 26  # SDR of jet reverser pipe

## Diffuser geometry
SDR_DIFFUSER = 26  # SDR of diffuser pipe

DIFFUSER_PIPE_ND = 4 * u.cm  # nominal diameter of pipe used to make diffusers

AREA_PVC_DIFFUSER = (np.pi/4) * ((pipe.OD(DIFFUSER_PIPE_ND)**2)
                                 - (pipe.ID_SDR(DIFFUSER_PIPE_ND, SDR_DIFFUSER))**2)

PVC_STRETCH_RATIO = 1.2  # stretch factor applied to the diffuser PVC pipes as they are heated and molded

T_DIFFUSER = ((pipe.OD(DIFFUSER_PIPE_ND) -
                        pipe.ID_SDR(DIFFUSER_PIPE_ND, SDR_DIFFUSER))
                              / (2 * PVC_STRETCH_RATIO))

W_DIFFUSER_INNER = 0.3175 * u.cm  # opening width of diffusers

# Calculating using a minor loss equation with K = 1
V_SED_DIFFUSER_MAX = np.sqrt(2 * GRAVITY * HL_SED_INLET_MAX).to(u.mm/u.s)

DIFFUSER_L = 15 * u.cm  # vertical length of diffuser

B_DIFFUSER = 5 * u.cm  # center to center spacing beteen diffusers

HEADLOSS_SED_DIFFUSER = 0.001 * u.m # Headloss through the diffusers to ensure uniform flow between sed tanks

##Outlet to filter
#If the plant has two trains, the current design shows the exit channel
# continuing from one set of sed tanks into the filter inlet channel.
#The execution of this extended channel involves a few calculations.
HEADLOSS_SED_TO_FILTER_PIPE_MAX = 10 * u.cm

#Maximum length of sed plate sticking out past module pipes without any
#additional support. The goal is to prevent floppy modules that don't maintain
# constant distances between the plates

LENGTH_SED_PLATE_CANTILEVERED = 20*u.cm

SED_HOPPER_DRAIN_ND = 1*u.inch

SED_HOPPER_VIEWER_ND = 2*u.inch

SED_HOPPER_SKIMMER_ND = 2*u.inch

##Diffusers/Jet Reverser

SED_DIFFUSER_ND = 1*u.inch

SED_JET_REVERSER_ND = 3*u.inch