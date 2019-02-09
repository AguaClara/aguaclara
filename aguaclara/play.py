"""Provide easy setup for using the `aguaclara` package and all of its modules.

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


def set_sig_figs(n=4):
    """Set the number of significant figures used to print pint, pandas, and
    numpy quantities.

    Args:
        n: Number of significant figures to display
    """
    u.default_format = '.' + str(n) + 'g'
    pd.options.display.float_format = ('{:,.' + str(n) + '}').format


set_sig_figs()
matplotlib.style.use('ggplot')
