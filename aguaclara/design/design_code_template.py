"""Welcome to the design code template. This file is meant to teach you how to 
write AIDE Design Code.

Table of Contents: 
copy the title name and use find (ctrl+f) to jump to that section 
	- How to Import
	- How to name things
	- How to make a Component
		- Class Variables
		- Init functions
			- init args
			- super().__init__ purpose
			- giving fields to object
			- propogating configurations
		- property functions
		- normal functions
	- How to make a Subcomponent
"""
# How to Import
# These are the imports from other files or python packages that you would want 
# to use in the file.

from aguaclara.core.units import unit_registry as u #Gives python units
from aguaclara.design.component import Component 	#Allows for the objects to 
												 	#share q and temp

# How to name things
# To name a variable or a function, for example minimum area of a pipe, you 
# shorten the main words using (min a of a pipe), and make it in a directory 
# format with underscores (pipe_a_min). 

# How to make a subcomponent
# Just make a normal component, and in your main component make sure you 
# propogate the configs
class PressureCooker(Component):
	"""Design Monroe's pressure cooker.

	In order for Monroe to cook his favorite food, he must use his trusty 
	flow rate pressure cooker!

	Design Inputs:
	- ``q (float * u.L / u.s)``: Flow rate (recommended, defaults to 20L/s).
	- ``<name of input> (<type>)``: <Description> (<default>)
	"""
	def __init__(self, q = 20.0 * u.L/u.s, temp = 20.0 * u.degC,
				 rice_and_beans_ratio = 0.5):
		
		super().__init__(q = q, temp = temp)

		self.rice_and_beans_ratio = rice_and_beans_ratio

	def rb_per_person(self, people_n, time_to_eat):
		"""The rice and beans per person.
		
		Args:
			- ``people_n (float)``
			- ``time_to_eat (float * u.s)``
		"""
		rb_per_person = self.q * self.rice_and_beans_ratio * time_to_eat / \
			people_n
		return rb_per_person


# How to make a Component
# A component is  any component of the plant and extends the component class to 
# use those functions and abilities. The class Monroe is an example of a 
# component, PressureCooker is a subcomponent to Monroe, but can still be its own 
# component.
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
	# Class Variables
    # BEANS_DENSITY is a class variable (unlike the instance variables defined
    # in __init__) and should remain constant. The all-caps indicates that it
    # shouldn't be changed.
    # - To access it from within the class, use self.BEANS_DENSITY.
    # - To access it from outside of the class, import the class and use
    #   Monroe.BEANS_DENSITY.
    BEAN_DENSITY = 4.0 * u.g / u.L
	# Init functions - Used to create an object 
	# init args - (These args are used to create a Monroe object. All of the 
	# inputs below are expert inputs, which means that a user doesn't have to 
	# specify them as they have their own default value.
    def __init__(self, q = 20.0 * u.L/u.s, temp = 20.0 * u.degC,
                 rice_and_beans_eaten = 5.0 * u.L,
                 pc = PressureCooker()):

		# super().__init__ purpose
		# Using the init function from the Component Class, 
		# this will allow the subcomponents of this component to utilize the 
		# same q and temp. In later functions, you can use the q and temp by 
		# writing self.q and self.temp.
		super().__init__(q = q, temp = temp)

		# giving fields to object
		# The lines below instantiates a property to a Monroe object. In later 
		# functions, you can use the rice_and_beans_eaten and pc, by writing 
		# self.<property name>.
		self.rice_and_beans_eaten = rice_and_beans_eaten
		self.pc = pc

		# propogating configurations
		# If your component has a subcomponent (self.pc for our case, as it's default 
		# value is an object), the line below propogates the configurations to 
		# all of the classes subcomponents (monroe's pc will have the same 
		# q and temp). You must however put these subcomponents in a list, 
		# even if it's one subcomponent 
		super().propogate_config([self.pc])

	# property functions
	# Many properties of a component need some calculation, this is too much to 
	# put in an __init__ function. So we make functions with only the self 
	# parameter(you can't add more) and type @property. This is essentially a 
	# normal class function except it is called as if it was a property. 
	# For example, to call h, it is self.h. Use @property functions whenever 
	# you can.
	# The format for writing methods:
	# Use spaces around operators, minimal parentheses, keep lines under 80 
	# characters (use \ if necessary),as well as refrain from having the whole
	# body being wrapped in a return. Also, uses very straight to the point
	# documentation in the same form as the one below.
    @property
    def h(self):
		"""The height."""
		h = self.q * (0.06414368184 * u.s / u.m ** 2) * self.pc.rice_and_beans_ratio
		return h.to(u.ft)

	# normal functions
	# The format for writing methods:
	# Use spaces around operators, minimal parentheses, keep lines under 80 
	# characters (use \ if necessary),as well as refrain from having the whole
	# body being wrapped in a return. Also, uses very straight to the point
	# documentation in the same form as the one below.
    def love_for_sustainable_design(self, love_factor):
		"""His love for sustainable design."""
		love_for_sustainable_design = self.BEAN_DENSITY * \
			self.rice_and_beans_eaten + love_factor
		return love_for_sustainable_design.to(u.kg)