"""Module containing global ``pint`` unit registry.

The ``pint`` package supports arithmetic involving **physical quantities**
each of which has a magnitude and units, for example 1 cm or 3 kg m/s^2.
The units of a quantity come from ``pint``'s **unit registry**. This module
contains a single global unit registry ``u`` that can be used by any
number of other modules. The ``aguaclara`` has also defined and added some of
its own units to the ``u``:

  * NTU = 1.47 * (mg / L)
  * dollar = [money] = USD
  * lempira = dollar * 0.0427 = HNL
  * equivalent = mole = eq
  * rev = revolution

:Examples:

>>> from aguaclara.core.units import u
>>> rpm = 10 * u.rev/u.min
>>> rpm
<Quantity(10.0, 'rev / minute')>
>>> rpm.magnitude
10.0
>>> rpm.units
<Unit('rev / minute')>
>>> rpm.to(u.rad/u.s)
<Quantity(1.0471975511965976, 'radian / second')>
"""

import os
import pint
import pandas as pd

# A global unit registry that can be used by any of other module.
unit_registry = pint.UnitRegistry(
    system='mks',
    autoconvert_offset_to_baseunit=True
)
u = unit_registry

# default formatting includes 4 significant digits.
# This can be overridden on a per-print basis with
# print('{:.3f}'.format(3 * ureg.m / 9)).
u.default_format = '.4g'
pd.options.display.float_format = '{:,.4g}'.format

u.load_definitions(os.path.join(os.path.dirname(__file__),
                                            "data", "unit_definitions.txt"))


def set_sig_figs(n):
    """Set the default number of significant figures used to print pint,
    pandas and numpy values quantities. Defaults to 4.

    :param n: number of significant figures to display
    :type n: int

    :Examples:

    >>> from aguaclara.core.units import set_sig_figs, u as u
    >>> h = 2.5532532522352543*u.m
    >>> e = 25532532522352543*u.m
    >>> print('h before sigfig adjustment:',h)
    h before sigfig adjustment: 2.553 meter
    >>> print('e before sigfig adjustment:',e)
    e before sigfig adjustment: 2.553e+16 meter
    >>> set_sig_figs(10)
    >>> print('h after sigfig adjustment:',h)
    h after sigfig adjustment: 2.553253252 meter
    >>> print('e after sigfig adjustment:',e)
    e after sigfig adjustment: 2.553253252e+16 meter
    """
    u.default_format = '.' + str(n) + 'g'
    pd.options.display.float_format = ('{:,.' + str(n) + '}').format
