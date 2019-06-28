"""This module allows plant component classes to

#. specify expert inputs and their defaults automatically without the need for an ``__init__()`` function
#. propogate plant-wide design inputs throughout all of its subcomponents.

Example:
    from aguaclara.design.component import Component
    
    class SubComponent(Component):
        h = 3 * u.m

    class MainComponent(Component):
        l = 2 * u.m
        sub = SubComponent()
        subcomponents = [sub]
"""
from aguaclara.core.units import unit_registry as u
import aguaclara.core.utility as ut

import numpy as np
import json
from pprint import pprint

        
class Component(object):
    """An abstract class that should be extended by other component classes.

    This class provides the ability to record and propogate a configuration of
    plant design variables for a component and all of its subcomponents.

    Args:
        - ``q (float * u.L / u.s)``: Flow rate (recommended, defaults to 20L/s)
        - ``temp (float * u.degC)``: Water temperature (recommended, defaults to
          20°C)
    """
    q = 20 * u.L / u.s
    temp = 20 * u.degC
    subcomponents = []

    def __init__(self, **kwargs):
        # Update the Component object with new expert inputs, if any were given.
        self.__dict__.update(kwargs)
        
        # Send plant-wide inputs to all subcomponents
        for subcomp in self.subcomponents:
            subcomp.q = self.q
            subcomp.temp = self.temp
        
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
