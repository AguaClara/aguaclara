# -*- coding: utf-8 -*-
"""Lists of drill bit diameters."""
from aguaclara.core.units import u

import numpy as np


def get_drill_bits_d_imperial():
    """Return array of possible drill diameters in imperial."""
    step_32nd = np.arange(0.03125, 0.25, 0.03125)
    step_8th = np.arange(0.25, 1.0, 0.125)
    step_4th = np.arange(1.0, 2.0, 0.25)
    maximum = [2.0]

    return np.concatenate((step_32nd,
                           step_8th,
                           step_4th,
                           maximum)) * u.inch


def get_drill_bits_d_metric():
    """Return array of possible drill diameters in metric."""
    return np.concatenate((np.arange(1.0, 10.0, 0.1),
                           np.arange(10.0, 18.0, 0.5),
                           np.arange(18.0, 36.0, 1.0),
                           np.arange(40.0, 55.0, 5.0))) * u.mm


DRILL_BITS_D_IMPERIAL = get_drill_bits_d_imperial()
DRILL_BITS_D_METRIC = get_drill_bits_d_metric()
