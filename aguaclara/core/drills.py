# -*- coding: utf-8 -*-
""""""
from aguaclara.core.units import unit_registry as u

import numpy as np

DRILL_D_IMPERIAL = [0.03125 * u.inch, 0.0625 * u.inch, 0.09375 * u.inch, 0.125 * u.inch, 0.15625 * u.inch, 0.1875 * u.inch, 0.21875 * u.inch,
                    0.25 * u.inch, 0.375 * u.inch, 0.5 * u.inch, 0.625 * u.inch, 0.75 * u.inch, 0.875 * u.inch,
                    1 * u.inch, 1.25 * u.inch, 1.5 * u.inch, 1.75 * u.inch, 2 * u.inch]

DRILL_D_METRIC = [0.5 * u.mm, 0.6 * u.mm, 0.7 * u.mm, 0.8 * u.mm, 0.9 * u.mm,
                  1 * u.mm, 1.1 * u.mm, 1.2 * u.mm, 1.3 * u.mm, 1.4 * u.mm,
                  1.5 * u.mm, 1.6 * u.mm, 1.7 * u.mm, 1.8 * u.mm, 1.9 * u.mm,
                  2 * u.mm, 2.1 * u.mm, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3.,
                   3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 4., 4.1, 4.2, 4.3,
                   4.4, 4.5, 4.6, 4.7, 4.8, 4.9
                  ]

# counter = 0
# these drill series should have been created using arange.

# while DRILL_D_METRIC[counter] <= 4.98*u.mm:
#     counter+=1
#     DRILL_D_METRIC.append(DRILL_D_METRIC[counter - 1] + 0.1 * u.mm)
#
# while DRILL_D_METRIC[counter] < 20*u.mm:
#     counter+=1
#     DRILL_D_METRIC.append(DRILL_D_METRIC[counter - 1] + 1 * u.mm)
#
# while DRILL_D_METRIC[counter] < 50*u.mm:
#     counter+=1
#     DRILL_D_METRIC.append(DRILL_D_METRIC[counter - 1] + 2 * u.mm)


def get_drill_bit_diameters_imperial():
    drill_bit_diameters = np.append([], [np.arange(0.03125, 0.25, 0.03125),
                                         np.arange(0.25, 0.125, 1),
                                         np.arange(1, 2, 0.25)])
    for drill_bit in drill_bit_diameters:
        drill_bit = drill_bit * u.inch

    return drill_bit_diameters

print(str(get_drill_bit_diameters_imperial()))