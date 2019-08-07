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

TODO: update the below example with the complete Onshape design flow.

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
from onshape_client.client import Client
from onshape_client.onshape_url import ConfiguredOnshapeElement
from pprint import pprint
from abc import ABC

# I've placed Onshape authorization functionality in this module since it works
# with Component objects, while not being unique to a given Component object.
# Placing it within the Component class or in its own aguaclara.design.onshape
# module are potential alternatives. - Oliver Leung (oal22) 23 Jul '19

_client = None
"""onshape_client.client.Client: Store the initialized Client object to verify
that Onshape has been authorized.
"""

# TODO: verify that this function appears in the Sphinx-generated docs
def authorize_onshape(config_file_path="~/.onshape_client_config.yaml",
                      configuration=None):
    """Authorize use of the Onshape API
    
    TODO: explain getting access/secret keys and function params in depth.
    """
    global _client
    if _client:
        raise Exception('Onshape has already been authorized.')

    try:
        _client = Client(
                keys_file = config_file_path,
                configuration = configuration
            )
    except (FileNotFoundError, KeyError):
        raise Exception(
                'A configuration dictionary was not given, and the '
                'configuration file either doesn\'t exist or is invalid.'
            )


class Component(ABC):
    """An abstract class representing AguaClara plant components.
    
    This class provides subclasses with the ability to record and propogate a
    configuration of plant design variables (``q`` and ``temp``) for a component
    and all of its subcomponents.
    """
    Q_DEFAULT = 20 * u.L / u.s
    TEMP_DEFAULT = 20 * u.degC

    def __init__(self, **kwargs):
        self.q = self.Q_DEFAULT
        self.temp = self.TEMP_DEFAULT
        self.onshape_url = None
        self.element = None

        # Update the Component with new expert inputs, if any were given
        self.__dict__.update(**kwargs)

    # TODO: make this function private
    def set_subcomponents(self):
        """Set the plant-wide inputs of all subcomponents.

        Call this function at the end of a subclass's ``__init__()`` set ``q``
        and ``temp`` for subcomponents, except when a subcomponent specifies its
        own custom ``q`` and ``temp``.
        """
        for subcomp in getattr(self, 'subcomponents'):
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
            '_abc_registry'
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

    def configure_onshape(self):
        global _client
        if _client is None:
            raise Exception(
                'Onshape hasn\'t been authorized yet. Use the '
                'authorize_onshape() function.'
            )
        
        if self.onshape_url is None:
            raise AttributeError(
                'This Component object hasn\'t been connected '
                'to an Onshape Part Studio or Assembly.'
            )
        
        self.element = ConfiguredOnshapeElement(self.onshape_url)
        self.element.update_current_configuration(self.serialize_properties())
        self.element.get_url_with_configuration()
        
