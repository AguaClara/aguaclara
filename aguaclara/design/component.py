"""Component design for AguaClara drinking water treatment plants

This module provides common functionality that can be used to write plant
component design classes, such as:

#. specifing expert inputs and their defaults automatically
#. propogating plant-wide design inputs (like flow rate and water temperature)
   throughout all of its subcomponents.

See :ref:`how_to_write_design_code` for full instructions on how to use this
module.
"""
from aguaclara.core.units import u
import aguaclara.core.utility as ut

import numpy as np
import json
from pprint import pprint
from abc import ABC


class Component(ABC):
    """An abstract class that represents a component in an AguaClara drinking
    water treatment plant.

    This class provides the ability to record and propogate a configuration of
    plant design variables for a component and all of its subcomponents.
    """
    Q_DEFAULT = 20 * u.L / u.s
    TEMP_DEFAULT = 20 * u.degC

    def __init__(self, **kwargs):
        self.q = self.Q_DEFAULT
        self.temp = self.TEMP_DEFAULT

        # Update the Component object with new expert inputs, if any were given
        self.__dict__.update(**kwargs)

    def set_subcomponents(self):
        """Set the plant-wide design inputs of all subcomponents.

        This function processes each of the subcomponents listed in
        ``self.subcomponents``. If the user did not configure custom plant-wide
        inputs for a subcomponent, the subcomponent's plant-wide design inputs
        are changed to match that of this component.
        """
        for subcomp in getattr(self, 'subcomponents'):
            
            if subcomp.q == self.Q_DEFAULT:
                subcomp.q = self.q
            if subcomp.temp == self.TEMP_DEFAULT:
                subcomp.temp = self.temp

            # Recursively set sub-subcomponents
            if hasattr(subcomp, 'subcomponents'):
                subcomp.set_subcomponents()
        
    def serialize_properties(self):
        """Serialize the properties (fields and ``@property`` functions) of a 
        component as a dictionary.
        """
        properties = {}
        ignored_properties = [
            '__dict__',
            '__doc__',
            '__module__',
            '__weakref__',
            'subcomponents',
            '__abstractmethods__',
            '_abc_cache',
            '_abc_negative_cache',
            '_abc_negative_cache_version',
            '_abc_registry'
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
    
    def write_properties_to_file(self):
        """Append the properties of a component to a file. If it does not exist,
        then the file is created.
        
        Args:
            ``filename (str)``: The name of the file
        """
        filename = "props.json"
        json.dump(self.serialize_properties(), open(filename, mode='w'),
            indent = 4)
        print("Properties of component can be found in file props.json")
