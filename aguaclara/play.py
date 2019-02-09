"""
Provides easy setup for using the aguaclara package and all of its modules.

Usage:
    `from aguaclara.play import *`
"""

import math
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.style
import matplotlib.pyplot as plt
import warnings

import aguaclara
import aguaclara.core.pipes as pipe
from aguaclara.core.units import unit_registry as u
from aguaclara.core import physchem as pc
import aguaclara.core.constants as con
import aguaclara.core.materials as mat
import aguaclara.core.utility as ut
import aguaclara.core.head_loss as k
import aguaclara.core.pipeline as pipeline

# Temporarily disabled for release 0.0.15 to prevent problems with lacking
# Onshapepy setup. Re-enable when Onshapepy backend has been resolved.
# from aguaclara.design.lfom import LFOM


def set_sig_fig(n: int = 4):
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
        aguaclara.units.set_sig_figs(10)
        print('h after sigfig adjustment: ',h)
        print('e after sigfig adjustment: ',e)

        h before sigfig adjustment:  2.553 meter
        e before sigfig adjustment:  2.553e+16 meter
        h after sigfig adjustment:  2.553253252 meter
        e after sigfig adjustment:  2.553253252e+16 meter
    """
    u.default_format = '.' + str(n) + 'g'
    pd.options.display.float_format = ('{:,.' + str(n) + '}').format


set_sig_fig()
matplotlib.style.use('ggplot')
