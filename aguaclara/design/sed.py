"""This module contains all the functions needed to design a sedimentation tank
for an AguaClara plant.
"""
from aguaclara.core.units import unit_registry as u
from aguaclara.design.sed_tank_bay import SedimentationTankBay
from aguaclara.design.component import Component
import aguaclara.core.constants as con
import aguaclara.core.pipes as pipe
import aguaclara.core.physchem as pc
import aguaclara.core.drills as drills
import aguaclara.core.utility as ut

import numpy as np
import math

PLANT_FLOOR_THICKNESS = 0.2 * u.m  # plant floor slab thickness
WALL_THICKNESS = 0.15 * u.m  # thickness of sed tank dividing wall
HL_OUTLET_MAN = 4 * u.cm  # head loss through the outlet manifold

BOD_UP_VEL = 1 * u.mm / u.s

##Plate settler
CONC_BOD_VEL = 0.12 * u.mm / u.s  # capture velocity

PLATE_ANGLE = 60 * u.deg

PLATE_S = 2.5 * u.cm

MODULE_PLATES_N_MIN = 8

# This is moved to template because SED_PLATE_THICKNESS is in materials.yaml
# CENTER_SED_PLATE_DIST = PLATE_S + SED_PLATE_THICKNESS

# Bottom of channel
SLOPE_ANGLE = 50 * u.deg

##This slope needs to be verified for functionality in the field.
# A steeper slope may be required in the floc hopper.
HOPPER_SLOPE_ANGLE = 45 * u.deg

WATER_H_EST = 2 * u.m

GATE_VALVE_URL = "https://confluence.cornell.edu/download/attachments/173604905/Sed-Scaled-Gate-Valve-Threaded.dwg"

SUPPORT_BOLT_URL = "https://confluence.cornell.edu/download/attachments/173604905/PlateSettlerSupportBolt.dwg"

##Inlet channel
WEIR_HL_MAX = 5 * u.cm

##Height of the inlet channel overflow weir above the normal water level
# in the inlet channel so that the far side of the overflow weir does not
# fill with water under normal operating conditions. This means the water
# level in the inlet channel will increase when the inlet overflow weir
# is in use.
INLET_WEIR_FREE_BOARD_H = 2 * u.cm

WEIR_THICKNESS = 5*u.cm

INLET_HL_MAX = 1 * u.cm

# ratio of the height to the width of the sedimentation tank inlet channel.
INLET_H_W_RATIO = 0.95

##Exit launder
##Target headloss through the launder orifices
LAUNDER_BOD_HL = 4 * u.cm

##Acceptable ratio of min to max flow through the launder orifices
FLOW_LAUNDER_ORIFICES_RATIO = 0.80

##Center to center spacing of orifices in the launder
CENTER_LAUNDER_EST_DIST = 10 * u.cm

##The additional length needed in the launder cap pipe that is to be
# inserted into the launder coupling
LAUNDER_CAP_EXCESS_L = 3 * u.cm

##Space between the top of the plate settlers and the bottom of the
# launder pipe
LAMELLA_TO_LAUNDER_H = 5 * u.cm

##The additional length needed in the launder cap pipe that is to be
# inserted into the launder coupling

##Diameter of the pipe used to hold the plate settlers together
MOD_ND = 0.5 * u.inch

##Diameter of the pipe used to create spacers. The spacers slide over the
# 1/2" pipe and are between the plates
MOD_SPACER_ND = 0.75 * u.inch

MOD_SPACER_SDR = 17

##This is the vertical thickness of the lip where the lamella support sits. mrf222
LAMELLA_LEDGE_THICKNESS = 8 * u.cm

LAMELLA_PIPE_EDGE_S = 5 * u.cm

##Approximate x-dimension spacing between cross pipes in the plate settler
# support frame.
CENTER_PLATE_FRAME_CROSS_DIST_EST = 0.8 * u.m

##Estimated plate length used to get an initial estimate of sedimentation
# tank active length.
PLATE_L_EST = 60 * u.cm

##Pipe size of the support frame that holds up the plate settler modules
PLATE_FRAME_ND = 1.5 * u.inch

##Floc weir

#Vertical distance from the top of the floc weir to the bottom of the pipe
# frame that holds up the plate settler modules
FLOC_WEIR_TO_PLATE_FRAME_H = 10 * u.cm

##Minimum length (X dimension) of the floc hopper
HOPPER_MIN_L = 50 * u.cm

##Inlet manifold
##Max energy dissipation rate in the sed diffuser outletS
ENERGY_DIS_INT_MAX = 150 * u.mW/u.kg

##Ratio of min to max flow through the inlet manifold diffusers
INLET_Q_RATIO = 0.8

MAN_ND_MAX = 8 * u.inch

MAN_SDR = 41  # SDR of pipe for sed tank inlet manifold

##This is the minimum distance between the inlet manifold and the slope
# of the sed tank.
INLET_MAN_SLOPE_S = 10 * u.cm

##Length of exposed manifold stub coming out of the floc weir to which the
# free portion of the inlet manifold is attached with a flexible coupling.
MAN_CONNECTION_STUB_L = 4 * u.cm

##Space between the end of the manifold pipe and the edge of the first
# diffuser's hole, or the first manifold orifice.

MAN_FIRST_DIFFUSER_GAP_L = 3 * u.cm

##Vertical distance from the edge of the jet reverser half-pipe to the tip
# of the inlet manifold diffusers
JET_REVERSER_TO_DIFFUSERS_H = 3 * u.cm

##Gap between the end of the inlet manifold pipe and the end wall of the
# tank to be able to install the pipe
MAN_PIPE_FROM_TANK_END_L = 2  *u.cm

WALL_TO_DIFFUSER_GAP_L_MIN = 3 * u.cm

# Diameter of the holes drilled in the manifold so that the molded 1"
# diffuser pipes can fit tightly in place (normal OD of a 1" pipe is
# close to 1-5/16")
MAN_PORT_D = 1.25 * u.inch

# nominal diameter of pipe used for jet reverser in bottom of set tank
JET_REVERSER_ND = 3 * u.inch

SDR_REVERSER = 26  # SDR of jet reverser pipe

# Diffuser geometry
SDR_DIFFUSER = 26  # SDR of diffuser pipe

DIFFUSER_PIPE_ND = 4 * u.cm  # nominal diameter of pipe used to make diffusers

AREA_PVC_DIFFUSER = (
    (np.pi/4) * ((pipe.OD(DIFFUSER_PIPE_ND)**2)
    - (pipe.ID_SDR(DIFFUSER_PIPE_ND, SDR_DIFFUSER))**2)
)
# stretch factor applied to the diffuser PVC pipes as they are heated
# and molded
PVC_STRETCH_RATIO = 1.2

T_DIFFUSER = ((pipe.OD(DIFFUSER_PIPE_ND) -
                        pipe.ID_SDR(DIFFUSER_PIPE_ND, SDR_DIFFUSER))
                              / (2 * PVC_STRETCH_RATIO))

W_DIFFUSER_INNER = 0.3175 * u.cm  # opening width of diffusers

# Calculating using a minor loss equation with K = 1
V_SED_DIFFUSER_MAX = np.sqrt(2 * con.GRAVITY * INLET_HL_MAX).to(u.mm / u.s)

DIFFUSER_L = 15 * u.cm  # vertical length of diffuser

B_DIFFUSER = 5 * u.cm  # center to center spacing beteen diffusers

# Headloss through the diffusers to ensure uniform flow between sed tanks
DIFFUSER_HL = 0.001 * u.m

# Outlet to filter
# If the plant has two trains, the current design shows the exit channel
# continuing from one set of sed tanks into the filter inlet channel.
# The execution of this extended channel involves a few calculations.
FILTER_OUTLET_HL_MAX = 10 * u.cm

# Maximum length of sed plate sticking out past module pipes without any
# additional support. The goal is to prevent floppy modules that don't maintain
# constant distances between the plates

PLATE_CANTILEVERED_L = 20 * u.cm

HOPPER_DRAIN_ND = 1*u.inch

HOPPER_VIEWER_ND = 2*u.inch

HOPPER_SKIMMER_ND = 2*u.inch

# Diffusers/Jet Reverser

DIFFUSER_ND = 1*u.inch

JET_REVERSER_ND = 3*u.inch


class Sedimentor(Component):
    """
    Calculates dimensions and values for Sedimentation Tank.

    Example:
        To create an object of SedimentationTank, use:
            >>> sed_tank = SedimentationTank()
    """


    # TODO: Specify schedule (SDR) of diffuser pipe for above


    def __init__(self,
                 q = 20 * u.L / u.s,
                 tank_l_inner = 58 * u.m,
                 tank_vel_up = 1 * u.mm / u.s,
                 tank_w = 42 * u.inch,
                 plate_settlers_angle = 60 * u.deg,
                 plate_settlers_s = 2.5 * u.cm,
                 plate_settlers_thickness = 2 * u.mm,
                 plate_settlers_l_cantilevered = 20 * u.cm,
                 plate_settlers_vel_capture = 0.12 * u.mm / u.s,
                 manifold_diffuser_vel_max = 442.9 * u.mm / u.s,
                 diffuser_n = 108,
                 manifold_exit_man_hl_orifice = 4 * u.cm,
                 manifold_exit_man_n_orifices = 58,
                 manifold_ratio_q_man_orifice = 0.8,
                 manifold_diffuser_thickness_wall = 1.17 * u.inch,
                 thickness_wall = 0.15 * u.m):
        """Instantiates a SedimentationTank with specified values.

        Args:
            q (float): Flow rate
            tank_l_inner (float): Inner length of the tank
            tank_vel_up (float): Upflow velocity through a sedimentation tank
            tank_w (float): Width of the tank
            plate_settlers_angle (int): Angle of plate settlers from horizontal
            plate_settlers_s (float): Perpendicular distance between plates, not the horizontal distance between plates
            plate_settlers_thickness (float): Thickness of the plate settlers
            plate_settlers_l_cantilevered (float): Maximum length of sed plate sticking out past module pipes without any
            additional support
            plate_settlers_vel_capture (float): Velocity capture of plate settlers
            thickness_wall (float): thickness of the wall

        Returns:
            An object of the SedimentationTank class
        """
        bay = SedimentationTankBay()

        self.num_bays = bay.n
        self.q = q
        self.tank_l_inner = tank_l_inner
        self.tank_vel_up = tank_vel_up
        self.tank_w = tank_w
        self.plate_settlers_angle = plate_settlers_angle
        self.plate_settlers_s = plate_settlers_s
        self.plate_settlers_thickness = plate_settlers_thickness
        self.plate_settlers_l_cantilevered = plate_settlers_l_cantilevered
        self.plate_settlers_vel_capture = plate_settlers_vel_capture
        self.manifold_diffuser_vel_max = manifold_diffuser_vel_max
        self.diffuser_n = diffuser_n
        self.manifold_exit_man_hl_orifice = manifold_exit_man_hl_orifice
        self.manifold_exit_man_n_orifices = manifold_exit_man_n_orifices
        self.manifold_ratio_q_man_orifice = manifold_ratio_q_man_orifice
        self.manifold_diffuser_thickness_wall = manifold_diffuser_thickness_wall
        self.thickness_wall = thickness_wall
        self.bay = SedimentationTankBay(self.q,
                                        self.tank_l_inner,
                                        self.tank_vel_up,
                                        self.tank_w,
                                        self.plate_settlers_angle,
                                        self.plate_settlers_s,
                                        self.plate_settlers_thickness,
                                        self.plate_settlers_l_cantilevered,
                                        self.plate_settlers_vel_capture,
                                        self.manifold_diffuser_vel_max,
                                        self.diffuser_n,
                                        self.manifold_exit_man_hl_orifice,
                                        self.manifold_exit_man_n_orifices,
                                        self.manifold_ratio_q_man_orifice,
                                        self.manifold_diffuser_thickness_wall)
        self.n_bays = self.bay.n()

    @property
    def L_channel(self):
        """Return the length of the inlet and exit channels for the sedimentation tank.

        Returns:
            Length of the inlet and exit channels for the sedimentation tank (float).
        """
        return ((self.n_bays * self.TANK_W) + self.THICKNESS_WALL +
                ((self.n_bays-1) * self.THICKNESS_WALL))

    # TODO: We need to specify a function for calculating the width of the channel.
