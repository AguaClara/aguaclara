.. _design-component_make:

***********************
How to Make a Component
***********************
This section will show you how to design your own water treatment plant 
component. A component is any component of the plant, and for coding them these 
classes will extend the Component class. These classes must extend the Component
class as it will allow the sharing of certain properties such as flow rate, 
temperature with the subcomponents of those classes. For example, when making a
whole plant, the flow rate should be constant between every single subcomponent. 
For the rest of this section, we will learn how to make the Monroe Component 
``class Monroe(Component):``. Also make sure to import the neccesary classes and 
packages for your component, this includes importing the Component class.

Class Variables
===============

.. code-block:: python
	
	BEAN_DENSITY = 4.0 * u.g / u.L

``BEANS_DENSITY`` is a class variable (unlike the instance variables defined
in ``__init__``) and should remain constant. The all-caps indicates that it
shouldn't be changed.
- To access it from within the class, use ``self.BEANS_DENSITY``.
- To access it from outside of the class, import the class and use
``Monroe.BEANS_DENSITY``.

Init Functions
==============

.. code-block:: python
	
	def __init__(self, q = 20.0 * u.L/u.s, temp = 20.0 * u.degC,
			rice_and_beans_eaten = 5.0 * u.L,
			pc = PressureCooker()):

The ``__init__`` function is what is used to create an object. The args for this 
function are the design inputs of the object. In the example above, notice 
how the inputs that have an = attached to them. These inputs are expert inputs, 
as the values attached are default values. To make a default Monroe is as simple 
as writing ``Monroe()``. If an expert would like to change his flow rate you 
just add that design input ``Monroe(q = 1 * u.L/u.s)``. Notice the pc arg, 
it's default value is a class call as this Monroe's subcomponent, his trusty 
pressure cooker. When figuring out how to name your design inputs, refer to :ref:`coding-conventions`.  

The Init body
-------------

.. code-block:: python

	# Part 1
	super().__init__(q = q, temp = temp)
	# Part 2
	self.rice_and_beans_eaten = rice_and_beans_eaten
	self.pc = pc
	# Part 3
	super().propogate_config([self.pc])

The purpose of the ``__init__`` body is to assign all of the design inputs into 
instance variables of the object.  

Part 1: Assigning Plant-Wide Properties
"""""""""""""""""""""""""""""""""""""""
.. code-block:: python
	
	super().__init__(q = q, temp = temp)

The design inputs flow rate and water temperature are plant-wide properties, as 
they are constant throughout the whole plant. By using the init function from 
the Component Class, it not only instantiates these properties to the component 
but also allows the component's subcomponents to utilize the same q and temp. 

In later functions, you can use the q and temp by writing 
``self.q`` and ``self.temp``.

Part 2: Assigning Component-Wide Properties
"""""""""""""""""""""""""""""""""""""""""""
.. code-block:: python
	
	self.rice_and_beans_eaten = rice_and_beans_eaten
	self.pc = pc

The other design inputs for this component are component-wide properties, and 
aren't used in other areas unless it's a subcomponent. The lines above assign 
the design inputs, apart from q and temp, to now be properties of the component 
(in this case Monroe).

In later functions, you can use these properties by writing ``self.<property name>``.

Part 3: Propogating Configurations
""""""""""""""""""""""""""""""""""
.. code-block:: python

	super().propogate_config([self.pc])

By utilizing the propogate_config function from the Component class, all of the 
plant-wide properties of a component will be the plant wide properties for all 
of it's subcomponents. The line above gives the Monroe's plant-wide properties 
to his subcomponent, his pressure cooker. Therefore in this example Monroe's 
pressure cooker should have the same q and temp as Monroe. 


Property Functions 
==================

.. code-block:: python

	@property
    def h(self):
		"""The height."""
		h = self.q * (0.06414368184 * u.s / u.m ** 2) * self.pc.rice_and_beans_ratio
		return h.to(u.ft)

For a component, they're some properties that don't stem from design inputs, and 
could rely on some calculation. These properties can then be made through a 
property function. Property functions have no extra args, and allow for the 
calling of a property function to be the same as a normal property. Using the 
above example, you can use self.h to call on the h function (no parentheses 
needed). This is done by writing ``@property`` above your function. For these 
functions remember to follow :ref:`coding-conventions`.

How to Make a Subcomponent
==========================

.. code-block:: python

	class PressureCooker(Component):
		def __init__(self, q = 20.0 * u.L/u.s, temp = 20.0 * u.degC,
					 rice_and_beans_ratio = 0.5):
			super().__init__(q = q, temp = temp)
			self.rice_and_beans_ratio = rice_and_beans_ratio

		def rb_per_person(self, people_n, time_to_eat):
			rb_per_person = self.q * self.rice_and_beans_ratio * time_to_eat / people_n
			return rb_per_person

The code block above is the code for Monroe's subcomponent, his pressure cooker. 
The things to note here is a subcomponent is exactly the same as a normal 
component. To make a subcomponent, you have to affect the main component.

In order to make a component a subcomponent:

#. Add the subcomponent as a design input
#. Propogate the configs using super().propogate_config.


Ex: Making PressureCooker a Subcomponent of Monroe
--------------------------------------------------


.. code-block:: python

	def __init__(self, q = 20.0 * u.L/u.s, temp = 20.0 * u.degC,
                 rice_and_beans_eaten = 5.0 * u.L,
                 pc = PressureCooker()): # Step 1: Add pc as design input

		super().__init__(q = q, temp = temp)

		self.rice_and_beans_eaten = rice_and_beans_eaten
		self.pc = pc

		super().propogate_config([self.pc]) # Step 2: Propogate the config onto pc