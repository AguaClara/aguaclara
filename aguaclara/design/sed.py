"""The sedimentor of an AguaClara water treatment plant receives flocculated
water from the flocculator, then settles the flocs out via upflow and an array
of plate settlers.

Example:
    >>> from aguaclara.design.sed import *
    >>> sed = Sedimentor(q = 20 * u.L / u.s, temp = 20 * u.degC)
    >>> sed.tank_n
    4
"""
from aguaclara.design.sed_tank import SedimentationTank
from aguaclara.design.sed_chan import SedimentationChannel
from aguaclara.design.component import Component
from aguaclara.core.units import u
import aguaclara.core.constants as con

import numpy as np


class Sedimentor(Component):
    """Design an AguaClara sedimentor.

    The ``Sedimentor`` class designs the sedimentation tank and channel in
    tandem. For more information on those classes, see
    :class:`aguaclara.design.sed_tank.SedimentationTank` and
    :class:`aguaclara.design.sed_chan.SedimentationChannel`.

    Design inputs:
        - ``q (float * u.L / u.s)``: Flow rate (recommended, defaults to 20L/s)
        - ``temp (float * u.degC)``: Water temperature (recommended, defaults to
          20°C)
        - ``wall_thickness (float * u.cm)``: Wall thickness (optional, defaults
          to 15 * u.cm)
        - ``tank (SedimentationTank)``: Sedimentation Tank
          (optional, see :class:`aguaclara.design.sed_tank.SedimentationTank`
          for defaults)
        - ``chan (SedimentationChannel)``: Sedimentation Channel
          (optional, see
          :class:`aguaclara.design.sed_chan.SedimentationChannel` for defaults)
    """
    def __init__(self, **kwargs):
        self.wall_thickness = 15.0 * u.cm
        
        self.tank = SedimentationTank()
        self.chan = SedimentationChannel()
        self.subcomponents = [self.tank, self.chan]

        super().__init__(**kwargs)
        super().set_subcomponents()

        self._design_chan()
        self._design_tank()

    @property
    def tank_n(self):
        """The number of sedimentation tanks."""
        tank_n = np.ceil(self.q / self.tank.q_tank)
        return int(tank_n)
    
    def _design_chan(self):
        """Design the sedimentation channel based off of the tank."""
        self.chan.sed_tank_n = self.tank_n
        self.chan.sed_tank_diffuser_hl = self.tank.diffuser_hl
        self.chan.sed_tank_inlet_man_nd = self.tank.inlet_man_nd
        self.chan.sed_tank_outlet_man_nd = self.tank.outlet_man_nd
        self.chan.sed_tank_outlet_man_hl = self.tank.outlet_man_orifice_hl
        self.chan.sed_tank_diffuser_hl = self.tank.diffuser_hl
        self.chan.w_inner = self.tank.w_inner
        self.chan.sed_tank_wall_thickness = self.tank.WALL_THICKNESS
        self.chan.sed_wall_thickness = self.wall_thickness

    def _design_tank(self):
        """Design the sedimentation tank based off of the channel"""
        self.tank.sed_chan_w_outer = self.chan.w_outer
        self.tank.sed_chan_weir_thickness = self.chan.weir_thickness
        
MODULE_PLATES_N_MIN = 8

WATER_H_EST = 2 * u.m

GATE_VALVE_URL = "https://confluence.cornell.edu/download/attachments/173604905/Sed-Scaled-Gate-Valve-Threaded.dwg"

SUPPORT_BOLT_URL = "https://confluence.cornell.edu/download/attachments/173604905/PlateSettlerSupportBolt.dwg"

# ratio of the height to the width of the sedimentation tank inlet channel.
INLET_H_W_RATIO = 0.95

##############
# Exit launder
##############

# Center to center spacing of orifices in the launder
CENTER_LAUNDER_EST_DIST = 10 * u.cm

# The additional length needed in the launder cap pipe that is to be
# inserted into the launder coupling
LAUNDER_CAP_EXCESS_L = 3 * u.cm

# Space between the top of the plate settlers and the bottom of the
# launder pipe
LAMELLA_TO_LAUNDER_H = 5 * u.cm

# The additional length needed in the launder cap pipe that is to be
# inserted into the launder coupling

# Diameter of the pipe used to hold the plate settlers together
MOD_ND = 0.5 * u.inch

# Diameter of the pipe used to create spacers. The spacers slide over the
# 1/2" pipe and are between the plates
MOD_SPACER_ND = 0.75 * u.inch

MOD_SPACER_SDR = 17

# This is the vertical thickness of the lip where the lamella support sits. mrf222
LAMELLA_LEDGE_THICKNESS = 8 * u.cm

LAMELLA_PIPE_EDGE_S = 5 * u.cm

# Approximate x-dimension spacing between cross pipes in the plate settler
# support frame.
CENTER_PLATE_FRAME_CROSS_DIST_EST = 0.8 * u.m

# Estimated plate length used to get an initial estimate of sedimentation
# tank active length.
PLATE_L_EST = 60 * u.cm

# Pipe size of the support frame that holds up the plate settler modules
PLATE_FRAME_ND = 1.5 * u.inch

################
# Inlet manifold
################

# Max energy dissipation rate in the sed diffuser outletS
ENERGY_DIS_INT_MAX = 150 * u.mW/u.kg

# Ratio of min to max flow through the inlet manifold diffusers
MAN_ND_MAX = 8 * u.inch

# This is the minimum distance between the inlet manifold and the slope
# of the sed tank.
INLET_MAN_SLOPE_S = 10 * u.cm

# Length of exposed manifold stub coming out of the floc weir to which the
# free portion of the inlet manifold is attached with a flexible coupling.
MAN_CONNECTION_STUB_L = 4 * u.cm

# Space between the end of the manifold pipe and the edge of the first
# diffuser's hole, or the first manifold orifice.

MAN_FIRST_DIFFUSER_GAP_L = 3 * u.cm

#Vertical distance from the edge of the jet reverser half-pipe to the tip
# of the inlet manifold diffusers
JET_REVERSER_TO_DIFFUSERS_H = 3 * u.cm

#Gap between the end of the inlet manifold pipe and the end wall of the
# tank to be able to install the pipe
MAN_PIPE_FROM_TANK_END_L = 2  *u.cm

WALL_TO_DIFFUSER_GAP_L_MIN = 3 * u.cm

# Diameter of the holes drilled in the manifold so that the molded 1"
# diffuser pipes can fit tightly in place (normal OD of a 1" pipe is
# close to 1-5/16")
MAN_PORT_D = 1.25 * u.inch

# nominal diameter of pipe used for jet reverser in bottom of set tank

SDR_REVERSER = 26  # SDR of jet reverser pipe

DIFFUSER_PIPE_ND = 4 * u.cm  # nominal diameter of pipe used to make diffusers


# stretch factor applied to the diffuser PVC pipes as they are heated
# and molded
PVC_STRETCH_RATIO = 1.2

W_DIFFUSER_INNER = 0.3175 * u.cm  # opening width of diffusers

B_DIFFUSER = 5 * u.cm  # center to center spacing beteen diffusers

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
