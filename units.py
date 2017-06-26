"""
Created on Thu Jun 8 2017

@author: Monroe Weber-Shirk

Last modified: Fri Jun 23 2017 
By: Sage Weber-Shirk


Module containing global `pint` unit registry.

The `pint` module supports arithmetic involving *physical quantities*
each of which has a magnitude and units, for example 1 cm or 3 kg.
The units of a quantity come from a `pint` *unit registry*, and it
appears that `pint` supports arithmetic operations only on quantities
whose units come from the same unit registry (an attempt to perform
an operation on quantities whose units come from different unit
registries raises an exception). This module contains a single global
unit registry `unit_registry` that can be used by any number of other
modules.
"""


import pint
from os import path


unit_registry = pint.UnitRegistry(system='mks')

unit_registry.load_definitions(path.expanduser('~\\Documents\\GitHub\\AguaClara_design\\unit_definitions.txt'))