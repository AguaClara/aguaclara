"""The entrance tank of an AguaClara water treatment plant

#. removes large grit particles using plate settlers,
#. contains the LFOM <add link>, which maintains a linear relation between flow and water level, and
#. introduces chemical dosing through the CDC <add link> using the water level set by the LFOM <add link>.

Example:
    >>> from aguaclara.design.ent_tank import *
    >>> ent_tank = EntranceTank(q = 20 * u.L / u.s, floc_chan_w = 42.0 * u.inch,...)
    >>> ent_tank.plate_n
"""
from aguaclara.core.units import unit_registry as u
import aguaclara.core.physchem as pc
import aguaclara.core.constants as con
import aguaclara.core.materials as mat
import aguaclara.core.pipes as pipe
import aguaclara.core.head_loss as hl

import numpy as np
import math

L_MAX = 2.2 * u.m

# Angle of the sloped walls of the entrance tank hoppers
ENT_TANK_SLOPE_ANGLE = 45 * u.deg

# Extra space around the float (increase in effective diameter) to
# ensure that float has free travel
FLOAT_S = 5 * u.cm
HOPPER_PEAK_W = 3 * u.cm
MOD_ND = 0.5 * u.inch

# Distance from the front wall to the pipe stubs in the hopper drains so
# that an operator can easily reach them.
WALL_DRAIN_DIST_MAX = 40 * u.cm
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
FLOAT_ND = 8 * u.inch

# Are these next two variables supposed to be an expert input/calculated value?
# -Oliver (oal22), 4 Jun 19

# Minimum pipe size to handle grit and to ensure that the pipe can be
# easily unclogged
DRAIN_MIN_ND = 3 * u.inch
DRAIN_ND = 3 * u.inch  # This is constant for now

REMOVABLE_WALL_THICKNESS = 5*u.cm

# Parameters are arbitrary - need to be calculated
REMOVABLE_WALL_SUPPORT_H = 4 * u.cm
REMOVABLE_WALL_SUPPORT_THICKNESS = 5 * u.cm
HOPPER_LEDGE_THICKNESS = 15 * u.cm
WALKWAY_W = 1 * u.m
RAPID_MIX_ORIFICE_PLATE_THICKNESS = 2 * u.cm
RAPID_MIX_AIR_RELEASE_ND = 1 * u.inch

class EntranceTank(object): 
    """Design an AguaClara plant's entrance tank.
    
    An entrance tank's design relies on the LFOM's and flocculator's design in
    the same plant, but assumed/default values may be used to design an
    entrance tank by itself. To design these components in tandem, use the
    EntTankFloc class <add link>.

    Design Inputs:
        - ``q (float * u.L / u.s)``: Flow rate (required)
        - ``lfom_id (float * u.inch)``: The LFOM's inner diameter (recommended,
          defaults to 2")
        - ``floc_chan_w (float * u.inch)``: The flocculator's channel width
          (recommended, defaults to 42")
        - ``floc_chan_depth (float * u.m)``: The flocculator's channel depth
          (recommended, defaults to 2m)
        - ``plate_s (float * u.cm)``: The spacing between plates in a plate
          settler (optional, defaults to 2.5cm)
        - ``plate_thickness (float * u.deg)``: The thickness of a plate in a 
          plate settler (optional, defaults to 2mm)
        - ``plate_angle (float * u.deg)``: The angle of the plate settler 
          (optional, defaults to 60 degrees)
        - ``plate_capture_vel (float * u.mm / u.s)``: The capture velocity of the 
          plate settler (optional, defaults to 8m/s)
        - ``fab_space (float * u.cm)``: The space needed for a person to remove 
          the drain pipe (optional, defaults to 5cm) 
        - ``temp (float * u.degC)``: Water temperature (optional,
          defaults to 20 degrees celsius) 
        - ``sdr (float)``: Standard demension ratio (optional,
          defaults to 41)  
    """

    def __init__(self, q,
                 lfom_id=2.0 * u.inch, # May be innacurate, check with Monroe -Oliver L., oal22, 4 Jun '19 
                 floc_chan_w=42.0 * u.inch,
                 floc_end_depth=2.0 * u.m,
                 plate_s=2.5 * u.cm,
                 plate_thickness=2.0 * u.mm,
                 plate_angle = 60.0 * u.deg,
                 plate_capture_vel = 8.0 * u.mm / u.s,
                 fab_space=5.0 * u.cm,
                 temp=20.0 * u.degC,
                 sdr=41.0):
        self.q = q
        self.lfom_id = lfom_id
        self.floc_chan_w = floc_chan_w
        self.floc_end_depth = floc_end_depth
        self.plate_s = plate_s
        self.plate_thickness = plate_thickness
        self.plate_angle = plate_angle
        self.plate_capture_vel = plate_capture_vel
        self.fab_space = fab_space
        self.temp = temp
        self.sdr = sdr
    
    @property
    def drain_od(self):
        """The nominal diameter of the entrance tank drain pipe."""
        nu = pc.viscosity_kinematic(self.temp)
        k_minor = \
            hl.PIPE_ENTRANCE_K_MINOR + hl.PIPE_EXIT_K_MINOR + hl.EL90_K_MINOR
        drain_id = pc.diam_pipe(self.q,
                                self.floc_end_depth,
                                self.floc_end_depth,
                                nu,
                                mat.PVC_PIPE_ROUGH,
                                k_minor)
        drain_nd = pipe.ND_SDR_available(drain_id, self.sdr)
        return pipe.OD(drain_nd)
        
    @property
    def plate_n(self):
        """The number of plates in the plate settlers."""
        num_plates_as_float = \
            np.sqrt(
                (self.q / (
                    self.plate_s * self.floc_chan_w * self.plate_capture_vel *
                    np.sin(self.plate_angle.to(u.rad)).item()
                )).to(u.dimensionless)
            )
        num_plates_as_int = np.ceil(num_plates_as_float)
        return num_plates_as_int # This calculates to be too low. -Oliver

    @property
    def plate_l(self):
        """The length of the plates in the plate settlers."""
        plate_l = (
                self.q / (
                    self.plate_n * self.floc_chan_w * self.plate_capture_vel *
                    np.cos(self.plate_angle.to(u.rad))
                )
            ) - (self.plate_s * np.tan(self.plate_angle.to(u.rad)))
        return plate_l

    @property
    def l(self):
        """The length of the tank."""
        plate_array_thickness = \
            (self.plate_thickness * self.plate_n) + \
            (self.plate_s * (self.plate_n - 1))
            
        l = self.drain_od + (self.fab_space * 2) + \
            (
                plate_array_thickness * np.cos(((90 * u.deg) -
                self.plate_angle).to(u.rad))
            ) + \
            (self.plate_l * np.cos(self.plate_angle.to(u.rad))) + \
            (self.lfom_id * 2)
        return l
        