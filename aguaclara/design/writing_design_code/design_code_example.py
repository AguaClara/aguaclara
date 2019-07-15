"""Example design code for a component and subcomponent.

This module provides two example classes that demonstrate proper usage of the
:class:`aguaclara.design.component.Component` class for the design code of a
component and a subcomponent. The classes contain the various properties and
functions that can be used for design code.

Example:
    >>> from aguaclara.design.writing_design_code.design_code_example import *
    >>> monroe = Monroe()

"""
from aguaclara.core.units import unit_registry as u
from aguaclara.design.component import Component


class PressureCooker(Component):
    """Design Monroe's pressure cooker.

    In order for Monroe to cook his favorite food, he must use his trusty 
    flow rate pressure cooker!

    Design Inputs:
    - ``q (float * u.L / u.s)``: Flow rate (recommended, defaults to 20L/s).
    - ``temp (float * u.degC)``: Water temperature (recommended, defaults to
      20°C)
    - ``rice_and_beans_ratio (float)``: Ratio of rice to beans (optional,
      defaults to 0.5)
    """
    def __init__(self, **kwargs):
        self.q = 20.0 * u.L/u.s
        self.temp = 20.0 * u.degC
        self.rice_and_beans_ratio = 0.5
        
        super().__init__(**kwargs)

    def rb_per_person(self, people_n, time_to_eat):
        """The amount of rice and beans per person (L).
        
        Args:
            - ``people_n (float)``: The number of people eating
            - ``time_to_eat (float * u.s)``: The amount of time it takes to eat
        """
        rb_per_person = self.q * self.rice_and_beans_ratio * time_to_eat / \
            people_n
        return rb_per_person


class Monroe(Component): 
    """Design Monroe.

    Monroe's favorite food is rice and beans, but he can't make them without his
    trusty pressure cooker, one of Monroe's subcomponents!

    Attributes:
        - ``BEAN_DENSITY (float * u.g / u.L)``: Bean density

    Design Inputs:
        - ``q (float * u.L / u.s)``: Flow rate (recommended, defaults to 20L/s)
        - ``temp (float * u.degC)``: Water temperature (recommended, defaults to
          20°C)
        - ``rice_and_beans_eaten (float * u.L)``: Volume of rice and beans
          eaten (optional, defaults to 5L)
        - ``pc (PressureCooker)``: Pressure cooker (optional, see
          :class:`aguaclara.design.design_code_example.PressureCooker` for
          defaults)
    """
    BEAN_DENSITY = 4.0 * u.g / u.L

    def __init__(self, **kwargs):
        self.q = 20.0 * u.L/u.s
        self.temp = 20.0 * u.degC
        self.rice_and_beans_eaten = 5.0 * u.L
        self.pc = PressureCooker()
        self.subcomponents = [self.pc]

        super().__init__(**kwargs)
        super().set_subcomponents()

    @property
    def h(self):
        """His height (m)."""
        h = self.q * (200 * u.s / u.m ** 2) * \
            self.pc.rice_and_beans_ratio
        return h.to(u.m)

    def love_for_sustainable_design(self, love_factor):
        """His love for sustainable design (kg)."""
        love_for_sustainable_design = self.BEAN_DENSITY * \
            self.rice_and_beans_eaten * love_factor
        return love_for_sustainable_design.to(u.kg)