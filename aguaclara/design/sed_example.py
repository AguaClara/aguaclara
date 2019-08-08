"""Example design code for a minimal AguaClara sedimentor.

This module provides three example classes that demonstrate proper extension of
the :class:`aguaclara.design.component.Component` class. Note that they are
minimal examples of the :class:`aguaclara.design.sed.Sedimentor`,
:class:`aguaclara.design.sed_tank.SedimentationTank`, and
:class:`aguaclara.design.sed_chan.SedimentationChannel` classes, and should not
be used to design real plant components.

Example:
    >>> from aguaclara.design.sed_example import *
    >>> sed = Sedimentor()
    >>> sed.q
    <Quantity(20.0, 'liter / second')>
    >>> sed.tank.q
    <Quantity(5.0, 'liter / second')>
    >>> sed.tank_n
    4
    >>> sed.chan.l_inner
    <Quantity(5.0172, 'meter')>
"""
import aguaclara as ac
from aguaclara.core.units import u


class Sedimentor(ac.Component):
    """Design a minimal AguaClara sedimentor.

    The ``Sedimentor`` class designs the sedimentation tank and channel in
    tandem. For more information on those classes, see
    :class:`aguaclara.design.sed_example.SedimentationTank` and
    :class:`aguaclara.design.sed_example.SedimentationChannel`.

    Design inputs:
        - ``q (float * u.L / u.s)``: Flow rate (recommended, defaults to 20L/s)
        - ``temp (float * u.degC)``: Water temperature (recommended, defaults to
          20°C)
        - ``wall_thickness (float * u.cm)``: Wall thickness (optional, defaults
          to 15 * u.cm)
        - ``tank (SedimentationTank)``: Sedimentation Tank
          (optional, see :class:`aguaclara.design.sed_example.SedimentationTank`
          for defaults)
        - ``chan (SedimentationChannel)``: Sedimentation Channel
          (optional, see
          :class:`aguaclara.design.sed_example.SedimentationChannel` for
          defaults)
    """
    def __init__(self, **kwargs):
        self.wall_thickness = 15 * u.cm

        self.tank = SedimentationTank()
        self.chan = SedimentationChannel()
        self.subcomponents = [self.tank, self.chan]

        super().__init__(**kwargs)
        super().set_subcomponents()
        self._set_tank()
        self._set_chan()

    @property
    def tank_n(self):
        """The number of sedimentation tanks."""
        tank_n = ac.ceil_step((self.q / self.tank.q_ideal), 1)
        return int(tank_n)

    def _set_tank(self):
        """Set special inputs for self.tank."""
        self.tank.q = self.q / self.tank_n

    def _set_chan(self):
        """Set special inputs for self.chan."""
        self.chan.sed_tank_n = self.tank_n
        self.chan.sed_tank_w_inner = self.tank.w_inner
        self.chan.sed_wall_thickness = self.wall_thickness


class SedimentationChannel(ac.Component):
    """Design a minimal AguaClara sedimentation channel.
    
    The sedimentation channel relies on the number and dimensions of the
    sedimentation tanks in the same plant, but assumed/default values may be
    used to design a sedimentation channel by itself. To design these components
    in tandem, use :class:`aguaclara.design.sed.Sedimentor`.

    Design Inputs:
        - ``q (float * u.L / u.s)``: Flow rate (recommended, defaults to 20L/s)
        - ``temp (float * u.degC)``: Water temperature (recommended, defaults to
          20°C)
        - ``sed_tank_n (int)``: Number of sedimentation tanks (recommended,
          defaults to 4)
        - ``sed_tank_w_inner (float * u.inch)``: Inner width of the
          sedimentation tank (recommended, defaults to 42 in)
        - ``sed_wall_thickness (float * u.cm)``: Wall thickness of the
          sedimentor (recommended, defaults to 15 cm)
    """
    def __init__(self, **kwargs):
        self.sed_tank_n = 4
        self.sed_tank_w_inner = 42 * u.inch
        self.sed_wall_thickness = 15 * u.cm

        super().__init__(**kwargs)

    @property
    def l(self):
        """``(float * u.m)`` Length"""
        l = (
                self.sed_tank_n * 
                    (self.sed_tank_w_inner + self.sed_wall_thickness)
            ) + self.sed_wall_thickness
        return l.to(u.m)


class SedimentationTank(ac.Component):
    """Design a minimal AguaClara sedimentation tank.

    An sedimentation tank's design relies on the sedimentation channel's design 
    in the same plant, but assumed/default values may be used to design an
    sedimentation tank by itself. To design these components in tandem, use
    :class:`aguaclara.design.sed.Sedimentor`.

    Design Inputs:
        - ``q (float * u.L / u.s)``: Flow rate (recommended, defaults to 20L/s)
        - ``temp (float * u.degC)``: Water temperature (recommended, defaults to
          20°C)
        - ``vel_upflow (float * u.mm / u.s)``: Upflow velocity (optional,
          defaults to 1mm/s)
        - ``l_inner (float * u.m)``: The inner length (optional, defaults to
          5.8m)
        - ``w_inner (float * u.inch)``: The inner width (optional, defaults to
          42in.)
    """
    def __init__(self, **kwargs):
        self.vel_upflow = 1 * u.mm / u.s
        self.l_inner = 5.8 * u.m
        self.w_inner = 42 * u.inch

        super().__init__(**kwargs)

    @property
    def q_ideal(self):
        """``(float * u.L / u.s)`` Ideal flow rate given the upflow velocity"""
        q_ideal = self.l_inner * self.w_inner * self.vel_upflow
        return q_ideal.to(u.L / u.s)
