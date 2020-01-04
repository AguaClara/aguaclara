"""The entrance tank of an AguaClara water treatment plant

#. removes large grit particles using plate settlers,
#. contains the :ref:`design-lfom`, which maintains a linear relation between flow and water level, and
#. introduces chemical dosing through the CDC <add link> using the water level set by the :ref:`design-lfom`.

Example:
    >>> from aguaclara.design.ent import *
    >>> ent_tank = EntranceTank(q = 20 * u.L / u.s, floc_chan_w = 42.0 * u.inch)
    >>> ent_tank.plate_n
    <Quantity(11.0, 'dimensionless')>
"""
import aguaclara.core.constants as con
import aguaclara.core.head_loss as hl
import aguaclara.core.materials as mat
import aguaclara.core.physchem as pc
import aguaclara.core.pipes as pipe
from aguaclara.core.units import u
import aguaclara.core.utility as ut

from aguaclara.design.component import Component
from aguaclara.design.pipeline import Pipe

import numpy as np


class EntranceTank(Component):
    """Design an AguaClara plant's entrance tank.

    An entrance tank's design relies on the LFOM's and flocculator's design in
    the same plant, but assumed/default values may be used to design an
    entrance tank by itself. To design these components in tandem, use
    :class:`aguaclara.design.ent_floc.EntTankFloc`.

    Design Inputs:
        - ``q (float * u.L / u.s)``: Flow rate (recommended, defaults to 20L/s)
        - ``temp (float * u.degC)``: Water temperature (recommended, defaults to
          20°C)
        - ``lfom_nd (float * u.inch)``: The LFOM's nominal diameter (recommended,
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
        - ``fab_s(float * u.cm)``: The space needed for a person to remove
          the drain pipe (optional, defaults to 5cm)
        - ``sdr (float)``: Standard demension ratio (optional,
          defaults to 41)
    """
    def __init__(self, **kwargs):
        self.lfom_nd = 2.0 * u.inch # May be innacurate, check with Monroe -Oliver L., oal22, 4 Jun '19
        self.floc_chan_w = 42.0 * u.inch
        self.floc_end_depth = 2.0 * u.m
        self.plate_s = 2.5 * u.cm
        self.plate_thickness = 2.0 * u.mm
        self.plate_angle  =  50.0 * u.deg
        self.plate_capture_vel  =  8.0 * u.mm / u.s
        self.fab_s = 5.0 * u.cm
        self.spec = 'sdr41'

        self.drain_pipe = Pipe()
        self.subcomponents = [self.drain_pipe]

        super().__init__(**kwargs)
        self._set_drain_pipe()
        super().set_subcomponents()

    def _set_drain_pipe(self):
        """The inner diameter of the entrance tank drain pipe."""
        drain_pipe_k_minor = \
            hl.PIPE_ENTRANCE_K_MINOR + hl.PIPE_EXIT_K_MINOR + hl.EL90_K_MINOR

        nu = pc.viscosity_kinematic_water(self.temp)
        drain_id = pc.diam_pipe(self.q,
                                self.floc_end_depth,
                                self.floc_end_depth,
                                nu,
                                mat.PVC_PIPE_ROUGH,
                                drain_pipe_k_minor)

        self.drain_pipe = Pipe(
            id = drain_id,
            k_minor = drain_pipe_k_minor,
            spec = self.spec
        )

    @property
    def plate_n(self):
        """The number of plates in the plate settlers."""
        num_plates_as_float = \
            np.sqrt(
                (self.q / (
                    (self.plate_s + self.plate_thickness) * self.floc_chan_w *
                    self.plate_capture_vel *
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
        plate_l_rounded = ut.ceil_step(plate_l.to(u.cm), 1.0 * u.cm)
        return plate_l_rounded

    @property
    def l(self):
        """The length of the entrance tank."""
        plate_array_thickness = \
            (self.plate_thickness * self.plate_n) + \
            (self.plate_s * (self.plate_n - 1))

        l = self.drain_pipe.od + (self.fab_s * 2) + \
            (
                plate_array_thickness * np.cos(((90 * u.deg) -
                self.plate_angle).to(u.rad))
            ) + \
            (self.plate_l * np.cos(self.plate_angle.to(u.rad))) + \
            (self.lfom_nd * 2)
        return l
