"""Welcome to the design code template. This file is meant to teach you how to 
write AIDE Design Code.

These are the imports from other files or python packages that you would want to use in the file
"""
import aguaclara.core.constants as con
import aguaclara.core.drills as drill
import aguaclara.core.head_loss as hl
import aguaclara.core.materials as mat
import aguaclara.core.physchem as pc
import aguaclara.core.pipes as pipe
from aguaclara.core.units import unit_registry as u
import aguaclara.core.utility as ut

from aguaclara.design.component import Component

import numpy as np


class PressureCooker(Component):
	"""Design Monroe's pressure cooker.

	In order for Monroe to cook his favorite food, he must use his trusty 
	flow rate pressure cooker!
	
	(The inputs that can be used to create the pressure cooker object. All of the
	inputs below are expert inputs which means that a user doesn't have to input
	them as these inputs have their own default value)
	Design Inputs:
	- ``q (float * u.L / u.s)``: Flow rate (recommended, defaults to 20L/s).
	- ``temp (float * u.degC)``: Water Temperature (recommended, defaults to 
	20 degrees celsius).
	- ``rice_and_beans_ratio (float)``: The Monratio (optional, defaults to 
	20L/s).
	- ``<name of input> (<type>)``: <Description> (<default>)
	"""
	def __init__(self, q = 20.0 * u.L/u.s, temp = 20.0 * u.degC,
				 rice_and_beans_ratio = 0.5):
		
		# Using the init function from the Component Class, 
		# this will allow the subcomponents of this component to utilize the 
		# same q and temp. In later functions, you can use the q and temp by 
		# writing self.q and self.temp.
		super().__init__(q = q, temp = temp)
		
		self.rice_and_beans_ratio = rice_and_beans_ratio

	def rb_per_person(self, people_n, time_to_eat):
		rb_per_person = self.q * self.rice_and_beans_ratio * time_to_eat/ people_n
		return rb_per_person

# Like other component classes, the Monroe class must extend the Component class
# in order to use its functions and abilities.
class Monroe(Component): 
    """Design a Monroe. (This first line should be a short description of the
    class)

    Monroe's favorite food is rice and beans, but he can't make them without his
    trusty pressure cooker! (This part should be a longer description of the
    component class, what it generally calculates, and what its subcomponents
    are.)

    (The Attributes section describes the class variables that are defined
    in the class, but outside of __init__. Be sure to document the variable
    name, its type, and a plain language description of what it stores.)
    Attributes:
        - ``BEAN_DENSITY (float * u.g / u.L)``: Bean density

	(The Design Inputs section describes inputs that can be used to create a
    Monroe object. All of the inputs below are expert inputs, which means that a
    user doesn't have to specify them as they have their own default value.)
    Design Inputs:
        - ``q (float * u.L / u.s)``: Flow rate (recommended, defaults to 20L/s)
        - ``temp (float * u.degC)``: Water temperature (recommended, defaults to
          20°C)
    """
    # BEANS_DENSITY is a class variable (unlike the instance variables defined
    # in __init__) and should remain constant. The all-caps indicates that it
    # shouldn't be changed.
    # - To access it from within the class, use self.BEANS_DENSITY.
    # - To access it from outside of the class, import the class and use
    #   Monroe.BEANS_DENSITY.
    BEAN_DENSITY = 4.0 * u.g / u.L

    def __init__(self, q = 20.0 * u.L/u.s, temp = 20.0 * u.degC,
                 rice_and_beans_eaten = 5.0 * u.L,
                 pc = PressureCooker()):

		# Using the init function from the Component Class, 
		# this will allow the subcomponents of this component to utilize the 
		# same q and temp. In later functions, you can use the q and temp by 
		# writing self.q and self.temp.
		super().__init__(q = q, temp = temp)

		
		self.rice_and_beans_eaten = rice_and_beans_eaten
		self.pc = pc

		super().propogate_config([self.pc])

    @property
    def h(self):
		h = self.q * (0.06414368184 * u.s / u.m ** 2)
		return h.to(u.ft)
	
    @property
    def love_for_sustainable_design(self):
        love_for_sustainable_design = self.BEAN_DENSITY * \
            self.rice_and_beans_eaten
        return love_for_sustainable_design.to(u.kg)