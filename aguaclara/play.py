"""``aguaclara`` package playground setup

Provide easy setup for using the ``aguaclara`` package and all of its modules,
classes, and functions.

Note: this module should not be used for development. Instead, individually
import only necessary modules.

Example:
    >>> from aguaclara.play import *
"""

import math
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.style
import matplotlib.pyplot as plt
import warnings

import aguaclara.core.constants as con
from aguaclara.core import drills
import aguaclara.core.head_loss as k
import aguaclara.core.materials as mat
from aguaclara.core import physchem as pc
from aguaclara.core import pipeline
import aguaclara.core.pipes as pipe
from aguaclara.core.units import unit_registry as u
import aguaclara.core.utility as ut

# Temporarily disabled for release 0.0.15 to prevent problems with lacking
# Onshapepy setup. Re-enable when Onshapepy backend has been resolved.
# from aguaclara.design.lfom import LFOM
# from aguaclara.design.floc import Flocculator
import aguaclara.design.human_access as ha

import aguaclara.research.environmental_processes_analysis as epa
import aguaclara.research.floc_model as fm
import aguaclara.research.procoda_parser as procoda_parser
import aguaclara.research.peristaltic_pump as peristaltic_pump
import aguaclara.research.stock_qc as stock_qc

def set_sig_figs(n=4):
    """Set the number of significant figures used to print Pint, Pandas, and
    NumPy quantities.

    Args:
        n (int): Number of significant figures to display.
    """
    u.default_format = '.' + str(n) + 'g'
    pd.options.display.float_format = ('{:,.' + str(n) + '}').format


set_sig_figs()
matplotlib.style.use('ggplot')
