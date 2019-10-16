"""Design abilities for AguaClara drinking water treatment plant components

This module allows plant component classes to

#. specify expert inputs and their defaults automatically
#. propogate plant-wide design inputs throughout all of its subcomponents
#. reconfigure Onshape Part Studios and Assemblies that represent plant
   components.

If a ``Component`` is instantiated with custom subcomponents, and the
subcomponents have their own ``q`` and/or ``temp`` specified:

.. code-block:: python

    plant = Plant(
            q = 40 * u.L / u.s,
            filter = Filter(q = 20 * u.L / u.s)
        )

then the subcomponets will preserve their ``q`` and ``temp``:

.. code-block:: python

    >>> plant.q
    40 liter / second
    >>> plant.filter.q
    20 liter / second

Otherwise, subcomponents will inherit the main component's ``q`` and ``temp``:

.. code-block:: python

    >>> plant = Plant(q = 40 * u.L / u.s)
    >>> plant.q
    40 liter / second
    >>> plant.filter.q
    40 liter / second

.. # TODO: update the a code example with the complete Onshape design flow.
"""
from aguaclara.core.units import u
import aguaclara.core.utility as ut

import numpy as np
import json
from pprint import pprint
from abc import ABC, abstractmethod
from urllib.parse import quote_plus


class Component(ABC):
    """An abstract class representing AguaClara plant components.
    
    This class provides subclasses with the ability to record and propogate a
    configuration of plant design variables (``q`` and ``temp``) for a component
    and all of its subcomponents.
    """
    Q_DEFAULT = 20 * u.L / u.s
    TEMP_DEFAULT = 20 * u.degC
    onshape_url_default = ''

    def __init__(self, **kwargs):
        self.q = self.Q_DEFAULT
        self.temp = self.TEMP_DEFAULT

        # Update the Component with new expert inputs, if any were given
        self.__dict__.update(**kwargs)

    def set_subcomponents(self):
        """Set the plant-wide inputs of all subcomponents.

        Call this function at the end of a subclass's ``__init__()`` set ``q``
        and ``temp`` for subcomponents, except when a subcomponent specifies its
        own custom ``q`` and ``temp``.
        """
        for subcomp in self.subcomponents:
            # Set the subcomponent's ``q`` and ``temp`` to match this component
            # unless they were changed during instantiation.
            if subcomp.q == self.Q_DEFAULT:
                subcomp.q = self.q
            if subcomp.temp == self.TEMP_DEFAULT:
                subcomp.temp = self.temp

            # Recursively set sub-subcomponents.
            if hasattr(subcomp, 'subcomponents'):
                subcomp.set_subcomponents()
        
    def serialize_properties(self):
        """Return the properties (fields and ``@property`` functions) of a 
        component as a dictionary string.
        """
        properties = {}
        ignored_properties = [
            '__dict__',
            '__doc__',
            '__module__',
            '__weakref__',
            'subcomponents',
            'Q_DEFAULT',
            'TEMP_DEFAULT',
            '__abstractmethods__',
            '_abc_cache',
            '_abc_negative_cache',
            '_abc_negative_cache_version',
            '_abc_registry',
            'onshape_config'
        ]
        # Get all of the object's fields
        for var_name in dir(self):
            value = getattr(self, var_name)

            # Serialize subcomponents to strings so that they are accessible by
            # Onshape's Super Derive feature
            if isinstance(value, Component):
                properties[var_name] = str(value.serialize_properties())

            # Serialize non-component properties
            elif not callable(value) and var_name not in ignored_properties:

                # Serialize lists or arrays
                try: 
                    if type(value.magnitude) is np.ndarray:
                        properties[var_name] = ut.array_qtys_to_strs(value)
                    else:
                        properties[var_name] = str(value)
                
                # Serialize non-iterable properties
                except AttributeError: 
                    properties[var_name] = str(value)
    
        return properties

    def print_properties(self):
        """Print the serialized properties with pretty indentation."""
        pprint(self.serialize_properties())
    
    def write_properties_to_file(self):
        """Append the properties of a component to a file. If it does not exist,
        then the file is created.
        
        Args:
            - ``filename (str)``: The name of the file
        """
        filename = "props.json"
        json.dump(self.serialize_properties(), open(filename, mode='w'),
            indent = 4)
        print("Properties of component can be found in file props.json")

    def _encode_onshape_config(self, config):
        encoding = ''
        for key, value in onshape_config.items():
            if type(value) is u.Quantity:
                value = str(value)
            elif type(value) is dict:
                value = _encode_onshape_config(value)
            encoding += key

    @property
    def onshape_url_configured(self):
        onshape_url_configured = (
            self.onshape_url_default + 
            '?configuration=' +
            self._encode_onshape_config(self.onshape_config)
        )
        return onshape_url_configured

# TODO: get the following to work in the general case when passing a simple
# nested dictionary to Onshape.

def nested_dict_to_str(dict_, level=0):
    for key, value in dict_.items():
        if type(value) is u.Quantity:
            dict_[key] = str(value)
        elif type(value) is dict:
            dict_[key] = nested_dict_to_str(value, level - 1)
    
    if level <= 0:
        dict_ = str(dict_)
    return dict_

def encode_onshape_config(config):
    encoding = ''
    for key, value in config.items():
        if type(value) in [u.Quantity, dict]:
            value = str(value)
        value = quote_plus(value)
        encoding += '{}={};'.format(key, value)

    return encoding

def onshape_url_configured(base_url, encoding):
    onshape_url_configured = (
        base_url + 
        '?configuration=' +
        quote_plus(encoding)
    )
    return onshape_url_configured