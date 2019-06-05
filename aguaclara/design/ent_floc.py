"""The entrance tank/flocculator assembly of an AguaClara water treatment plant
contains the entrance tank, chemical dose controller (CDC), linear flow orifice
meter (LFOM), and flocculator. It adds the initial dose of coagulant and
chlorine to the influent water, then causes flocs (accumulated coagulant and
primary particles) to aggregate.

Example:
    >>> from aguaclara.design.ent_floc import *
    >>> etf = EntTankFloc(20 * u.L / u.s, floc_hl = 35 * u.cm,...)
    >>> etf.ent.l
    1.403 meter
"""
from aguaclara.core.units import unit_registry as u
import aguaclara.core.physchem as pc
import aguaclara.core.constants as con
import aguaclara.core.materials as mat
import aguaclara.core.pipes as pipe
import aguaclara.core.head_loss as hl
from aguaclara.core import drills

from aguaclara.design.ent import EntranceTank
from aguaclara.design.lfom import LFOM
from aguaclara.design.floc import Flocculator

import numpy as np

class EntTankFloc:
    """Design an AguaClara plant's entrance tank/flocculator assembly.

    The designs of the LFOM, entrance tank, and flocculator in an AguaClara
    water treatment plant are interdependent. Use this class instead of the
    classes of the individual components to design all three at once.

    Design Inputs:
        - ``q (float * u.L / u.s)``: Flow rate (required)
        - ``temp (float * u.degC)``: Water temperature (optional,
          defaults to 20 degrees celsius) 
        - ``ent_l (float * u.m)``: Entrance tank length
          (optional, defaults to 1.5m)
        - ``ent_sdr (float)``: Standard demension ratio (optional,
          defaults to 41)
        - ``ent_plate_s (float * u.cm)``: The spacing between plates in a plate
          settler (optional, defaults to 2.5cm)
        - ``ent_plate_thickness (float * u.deg)``: The thickness of a plate in a 
          plate settler (optional, defaults to 2mm)
        - ``ent_plate_angle (float * u.deg)``: The angle of the plate settler 
          (optional, defaults to 60 degrees)
        - ``ent_plate_capture_vel (float * u.mm / u.s)``: The capture velocity of the 
          plate settler (optional, defaults to 8m/s)
        - ``ent_fab_space (float * u.cm)``: The space needed for a person to remove 
          the drain pipe (optional, defaults to 5cm)
        - ``lfom_hl (float * u.cm)``: The LFOM's head loss (optional, defaults
          to 20cm)
        - ``lfom_sdr (float)``: The LFOM's standard dimension ratio (optional,
          defaults to 26)
        - ``lfom_orifice_s (float * u.cm)``: The LFOM's orifice spacing
          (optional, defaults to 0.5cm)
        - ``floc_l_max (float * u.m)``: Maximum length (optional, defaults to 6m)
        - ``floc_gt (float)``: Collision potential (optional, defaults to 37000)
        - ``floc_hl (float * u.cm)``: The flocculator's head loss (optional,
          defaults to 40cm)
        - ``floc_chan_w_max (float * u.inch)``: Maximum width (optional, defaults to
          42")
        - ``floc_chan_w (float * u.inch)``: The flocculator's channel width
          (optional, defaults to 42")
        - ``floc_drain_t (float * u.min)``: Drain time (optional, 
          defaults to 30 mins)
        - ``floc_end_water_depth (float * u.m)``: Depth at the end 
          (optional, defaults to 2m)
        - ``safety_factor (float)``: Safety factor (optional, defaults to 1.5)
        - ``drill_bits (float * u.cm list)``: List of standard drill bit sizes
          (optional)

    Attributes:
        - ``lfom (LFOM)``: the LFOM designed for the given inputs
        - ``ent (EntranceTank)``: the entrance tank designed for the given
          inputs
        - ``floc (Flocculator)``: the flocculator designed for the given inputs
    """
    def __init__(self, q,
                 temp=20. * u.degC,
                 ent_l=1.5 * u.m,
                 ent_sdr=41.,
                 ent_plate_s = 2.5 * u.cm,
                 ent_plate_thickness=2.0 * u.mm,
                 ent_plate_angle = 60.0 * u.deg,
                 ent_plate_capture_vel = 8.0 * u.mm / u.s,
                 ent_fab_space=5.0 * u.cm,
                 lfom_hl=20 * u.cm,
                 lfom_sdr=26,
                 lfom_orifice_s=0.5*u.cm,
                 floc_l_max=6 * u.m,
                 floc_gt=37000,
                 floc_hl = 40 * u.cm,
                 floc_chan_w_max=42 * u.inch,
                 floc_chan_w=42. * u.inch,
                 floc_drain_t=30 * u.min,
                 floc_end_water_depth = 2 * u.m,
                 safety_factor=1.5,
                 drill_bits=drills.DRILL_BITS_D_IMPERIAL):

        # Initial design estimates for all subcomponents
        self.lfom = LFOM(q,
                        lfom_hl,
                        safety_factor,
                        lfom_sdr,
                        drill_bits,
                        lfom_orifice_s)
        self.ent = EntranceTank(q,
                                self.lfom.nom_diam_pipe,
                                floc_chan_w,
                                floc_end_water_depth,
                                ent_plate_s,
                                ent_plate_thickness,
                                ent_plate_angle,
                                ent_plate_capture_vel,
                                ent_fab_space,
                                temp,
                                ent_sdr)
        self.floc = Flocculator(q,
                                ent_l,
                                floc_chan_w_max,
                                temp,
                                floc_l_max,
                                floc_gt,
                                floc_hl,
                                floc_end_water_depth,
                                floc_drain_t)
        
        # Design the entrance tank and flocculator in tandem
        self._design_ent_floc(self.floc.ent_l) 

    def _design_ent_floc(self, ent_l):
        """Design the entrance tank and flocculator in tandem.

        Each subcomponent is redesigned until the expected length of the
        entrance tank (used to design the flocculator) is close enough to the
        actual length of the entrance tank (which should accomodate the
        flocculator's channel width).
        
        Args:
            - ``ent_l (float * u.m)``: The initial guess for the entrance tank's
              length, used to design the first iteration of the flocculator.
        """
        # Design the flocculator using a guess of the entrance tank's length.
        self.floc = Flocculator(self.floc.q,
                                ent_l,
                                self.floc.chan_w_max,
                                self.floc.temp,
                                self.floc.l_max,
                                self.floc.gt,
                                self.floc.hl,
                                self.floc.end_water_depth,
                                self.floc.drain_t)
        
        # Design the entrance tank using the flocculator's channel width.
        self.ent = EntranceTank(self.ent.q,
                                self.ent.lfom_id,
                                self.floc.chan_w,
                                self.ent.floc_end_depth,
                                self.ent.plate_s,
                                self.ent.plate_thickness,
                                self.ent.plate_angle,
                                self.ent.plate_capture_vel,
                                self.ent.fab_space,
                                self.ent.temp,
                                self.ent.sdr)

        # Recalculate if the actual length of the entrance tank is not close
        # enough.
        if np.abs(self.ent.l.to(u.m) - ent_l) / self.ent.l > 0.01:
            self._design_ent_floc(self.ent.l)
