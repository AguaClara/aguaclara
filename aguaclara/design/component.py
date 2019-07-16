"""This module allows plant component classes to

#. specify expert inputs and their defaults automatically
#. propogate plant-wide design inputs throughout all of its subcomponents.

Example:

.. code-block:: python

    from aguaclara.design.component import Component
    
    class SubComponent(Component):
        def __init__(self, **kwargs):
            self.h = 3 * u.m
            
            super().__init__(**kwargs)

    class MainComponent(Component):
        def __init__(self, **kwargs):
            self.l = 2 * u.m
            self.sub = SubComponent()
            self.subcomponents = [self.sub]

            super().__init__(**kwargs)
            super().propogate_config()
"""
from aguaclara.core.units import u
import aguaclara.core.utility as ut

import numpy as np
import json
from pprint import pprint


class Component(object):
    """An abstract class that should be extended by other component classes.

    This class provides the ability to record and propogate a configuration of
    plant design variables for a component and all of its subcomponents.
    """
    Q_DEFAULT = 20 * u.L / u.s
    TEMP_DEFAULT = 20 * u.degC

    def __init__(self, **kwargs):
        if type(self) is Component:
            raise Exception(
                'The Component class should not be instantiated. Instead, '
                'instantiate a class that extends Component.'
            )

        self.q = self.Q_DEFAULT
        self.temp = self.TEMP_DEFAULT

        # Update the Component object with new expert inputs, if any were given
        self.__dict__.update(**kwargs)

    def set_subcomponents(self):
        """Set the plant-wide inputs of all subcomponents.

        When a Component-type object is instantiated (the supercomponent), this
        function will set ``q`` and ``temp`` of all subcomponents in
        ``self.subcomponents`` to match the supercomponent. However, if the
        supercomponent is instantiated with a subcomponent as an argument, and
        the subcomponent is instantiated with its own ``q``/``temp``, then the
        subcomponent's ``q``/``temp`` is used.
        """
        for subcomp in getattr(self, 'subcomponents'):

            if subcomp.q == self.Q_DEFAULT:
                subcomp.q = self.q
            if subcomp.temp == self.TEMP_DEFAULT:
                subcomp.temp = self.temp

            if hasattr(subcomp, 'subcomponents'):
                subcomp.set_subcomponents()
        
    def serialize_properties(self):
        """Convert the properties (fields and ``@property`` functions) of a 
        component into a dictionary string.
        """
        properties = {}
        ignored_properties = [
            '__dict__',
            '__doc__',
            '__module__',
            '__weakref__',
            'subcomponents'
        ]
        # Get all of the object's fields
        for var_name in dir(self):
            value = getattr(self, var_name)

            # Serialize subcomponents
            if isinstance(value, Component):
                properties[var_name] = value.serialize_properties()

            # Serialize non-component properties
            elif not callable(value) and var_name not in ignored_properties:

                # Serialize lists or arrays
                try: 
                    if type(value.magnitude) is np.ndarray:
                        properties[var_name] = ut.array_qtys_to_strs(value)
                    else:
                        properties[var_name] = str(value)
                
                # Serialize non-iterable properties
                except: 
                    properties[var_name] = str(value)
    
        return properties

    def print_properties(self):
        """Print the serialized properties with pretty indentation."""
        pprint(self.serialize_properties())
    
    def write_properties_to_file(self, filename):
        """Append the properties of a component to a file. If it does not exist,
        then the file is created.
        
        Args:
            - ``filename (str)``: The name of the file
        """
        json.dump(self.serialize_properties(), open(filename, mode='a'),
            indent = 4)
