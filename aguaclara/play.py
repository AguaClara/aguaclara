"""``aguaclara`` package playground setup

Provide easy setup for using the ``aguaclara`` package and all of its modules,
classes, and functions.

Note: this module should not be used for development. Instead, individually
import only necessary modules.

Example:
    >>> from aguaclara.play import *
"""

import math  # noqa: F401
import numpy as np  # noqa: F401
import pandas as pd  # noqa: F401
import matplotlib
import matplotlib.style
import matplotlib.pyplot as plt  # noqa: F401

import aguaclara.core.constants as con  # noqa: F401
from aguaclara.core import drills  # noqa: F401
import aguaclara.core.head_loss as k  # noqa: F401
import aguaclara.core.materials as mat  # noqa: F401
from aguaclara.core import physchem as pc  # noqa: F401
import aguaclara.core.pipes as pipe  # noqa: F401
from aguaclara.core.units import u  # noqa: F401
import aguaclara.core.utility as ut  # noqa: F401
import aguaclara.core.onshape_parser as par  # noqa: F401

from aguaclara.design.cdc import CDC  # noqa: F401
from aguaclara.design.component import Component  # noqa: F401
from aguaclara.design.ent_floc import EntTankFloc  # noqa: F401
from aguaclara.design.ent import EntranceTank  # noqa: F401
from aguaclara.design.filter import Filter  # noqa: F401
from aguaclara.design.floc import Flocculator  # noqa: F401
import aguaclara.design.human_access as ha  # noqa: F401
from aguaclara.design.lfom import LFOM  # noqa: F401
from aguaclara.design.plant import Plant  # noqa: F401
from aguaclara.design.sed_chan import SedimentationChannel  # noqa: F401
from aguaclara.design.sed_tank import SedimentationTank  # noqa: F401
from aguaclara.design.sed import Sedimentor  # noqa: F401

import aguaclara.research.environmental_processes_analysis as epa  # noqa: F401
import aguaclara.research.floc_model as fm  # noqa: F401
import aguaclara.research.procoda_parser as procoda_parser  # noqa: F401
import aguaclara.research.peristaltic_pump as peristaltic_pump  # noqa: F401
import aguaclara.research.stock_qc as stock_qc  # noqa: F401

import aguaclara as ac  # noqa: F401


def set_sig_figs(n=4):
    """Set the number of significant figures used to print Pint, Pandas, and
    NumPy quantities.

    Args:
        n (int): Number of significant figures to display.
    """
    u.default_format = "." + str(n) + "g"
    pd.options.display.float_format = ("{:,." + str(n) + "}").format


set_sig_figs()
matplotlib.style.use("ggplot")
