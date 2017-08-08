# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 16:00:38 2017

@author: Sage Weber-Shirk
"""

import numpy as np
from matplotlib import pyplot as plt
try:
    from AguaClara_design.units import unit_registry as u
    from AguaClara_design import physchem as pc
except ModuleNotFoundError:
    from units import unit_registry as u
    import physchem as pc
    
    
coag = np.array([0.53, 1.06, 1.59, 2.11, 2.56] * u.mg/u.L)
conc_humic_acid = np.array([0, 3, 6, 9, 12, 15] * u.mg/u.L)
#dataset[0] is the 50NTU, dataset[1] is the 100NTU.
#Within both subgroups, [0] is the pC.0, ranging evenly up to [5] which is the 
# pC.15
dataset = np.array([[[0.634, 0.729, 0.891, 1.062, 1.205], 
                     [0.563, 0.717, 0.903, 1.038, 1.193], 
                     [0.136, 0.513, 0.793, 1.027, 1.095], 
                     [0.109, 0.264, 0.749, 1.002, 1.089], 
                     [0.084, 0.128, 0.647, 0.962, 1.057], 
                     [0.061, 0.094, 0.308, 0.717, 0.928]
                     ], 
                    [[0.746, 0.953, 1.191, 1.295, 1.414],
                     [0.563, 0.835, 1.085, 1.255, 1.403], 
                     [0.185, 0.692, 0.971, 1.254, 1.390], 
                     [0.105, 0.280, 0.956, 1.238, 1.361], 
                     [0.097, 0.207, 0.740, 1.209, 1.316],
                     [0.084, 0.157, 0.566, 1.084, 1.314]
                     ]
                    ])
x
