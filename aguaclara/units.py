"""Module containing global `pint` unit registry.

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

import os
import pint
import pandas as pd

unit_registry = pint.UnitRegistry(system='mks', autoconvert_offset_to_baseunit=True)

# default formatting includes 4 significant digits. This can be overridden on a per-print basis
#  with print('{:.3f}'.format(3*ureg.m /9))
unit_registry.default_format = '.4g'
pd.options.display.float_format = '{:,.4g}'.format


def set_sig_fig(n: int):
    """Set the default number of significant figures used to print pint, pandas and numpy values
    quantities. Defaults to 4.

    Args:
        n: number of significant figures to display

    Example:
        import aguaclara
        from aguaclara.units import unit_registry as u
        h=2.5532532522352543*u.m
        e = 25532532522352543*u.m
        print('h before sigfig adjustment: ',h)
        print('e before sigfig adjustment: ',e)
        aguaclara.units.set_sig_fig(10)
        print('h after sigfig adjustment: ',h)
        print('e after sigfig adjustment: ',e)

        h before sigfig adjustment:  2.553 meter
        e before sigfig adjustment:  2.553e+16 meter
        h after sigfig adjustment:  2.553253252 meter
        e after sigfig adjustment:  2.553253252e+16 meter
    """
    unit_registry.default_format = '.' + str(n) + 'g'
    pd.options.display.float_format = ('{:,.' + str(n) + '}').format

unit_registry.load_definitions(os.path.join(os.path.dirname(__file__), "data/unit_definitions.txt"))
