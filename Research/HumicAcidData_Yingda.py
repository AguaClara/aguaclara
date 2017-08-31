# -*- coding: utf-8 -*-
"""
Created on Tue Aug 8 16:00:38 2017

@author: Sage Weber-Shirk

Last modified: Thu Aug 10 2016
By: Sage Weber-Shirk
"""

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from aide_design import floc_model as floc

from aide_design.units import unit_registry as u

import sys, os
GitPath = os.path.join('~', 'Documents', 'GitHub')
myGitHubdir=os.path.expanduser(GitPath)
sys.path.append(myGitHubdir)


k = 0.24
coag = np.array([0.53, 1.06, 1.59, 2.11, 2.56]) * u.mg/u.L
conc_humic_acid = np.array([0, 3, 6, 9, 12, 15] * u.mg/u.L)
# dataset[0] is the 50NTU, dataset[1] is the 100NTU.
# Within both subgroups, [0] is the pC.0, ranging evenly up to [5] which is the
# pC.15
dataset = np.array([[  # Dataset[0]: the 50NTU datasets
                     [0.634, 0.729, 0.891, 1.062, 1.205],
                     [0.563, 0.717, 0.903, 1.038, 1.193],
                     [0.136, 0.513, 0.793, 1.027, 1.095],
                     [0.109, 0.264, 0.749, 1.002, 1.089],
                     [0.084, 0.128, 0.647, 0.962, 1.057],
                     [0.061, 0.094, 0.308, 0.717, 0.928]
                     ],
                    [  # Dataset[1]: the 100NTU datasets
                     [0.746, 0.953, 1.191, 1.295, 1.414],
                     [0.563, 0.835, 1.085, 1.255, 1.403],
                     [0.185, 0.692, 0.971, 1.254, 1.390],
                     [0.105, 0.280, 0.956, 1.238, 1.361],
                     [0.097, 0.207, 0.740, 1.209, 1.316],
                     [0.084, 0.157, 0.566, 1.084, 1.314]
                     ]
                    ])
indexnames = ['{0} mg/L'.format(i) for i in np.arange(0,16,3)]
Data50NTU = pd.DataFrame(dataset[0], index=indexnames).T

Data100NTU = pd.DataFrame(dataset[1], index=indexnames).T
print(Data50NTU)
    
coagGraph = np.arange(1 * 10**-4, 25.1 * 10**-4, 1 * 10**-4) * u.kg/u.m**3
enerDis = 4.833 * u.mW/u.kg
temperature = 25 * u.degC
resTime = 302 * u.s
tubeDiam = 3/8 * u.inch
# Begin graphing the 50NTU datasets
plt.figure('50NTU', (6,6))
plt.title('50 NTU Graph')
plt.ylabel('pC*')
plt.xlabel('coagulant dosage (mg/L)')


plt.plot(coag, Data50NTU['0 mg/L'], 'r.', coag, Data50NTU['3 mg/L'], 'b.',
         coag, Data50NTU['6 mg/L'], 'g.', coag, Data50NTU['9 mg/L'], 'm.',
         coag, Data50NTU['12 mg/L'], 'c.', coag, Data50NTU['12 mg/L'], 'y.')

# I wish there was a cleaner way to assign these but I can't think
# of what it would be.
line0mg50 = floc.pc_viscous(enerDis, temperature, resTime, tubeDiam,
                            50 * u.NTU, coagGraph, 0 * u.mg/u.L, 
                            floc.HumicAcid, floc.PACl, floc.Clay,
                            k, floc.RATIO_HEIGHT_DIAM)
line3mg50 = floc.pc_viscous(enerDis, temperature, resTime, tubeDiam,
                            50 * u.NTU, coagGraph, 3 * u.mg/u.L, 
                            floc.HumicAcid, floc.PACl, floc.Clay,
                            k, floc.RATIO_HEIGHT_DIAM)
line6mg50 = floc.pc_viscous(enerDis, temperature, resTime, tubeDiam,
                            50 * u.NTU, coagGraph, 6 * u.mg/u.L, 
                            floc.HumicAcid, floc.PACl, floc.Clay,
                            k, floc.RATIO_HEIGHT_DIAM)
line9mg50 = floc.pc_viscous(enerDis, temperature, resTime, tubeDiam,
                            50 * u.NTU, coagGraph, 9 * u.mg/u.L, 
                            floc.HumicAcid, floc.PACl, floc.Clay,
                            k, floc.RATIO_HEIGHT_DIAM)
line12mg50 = floc.pc_viscous(enerDis, temperature, resTime, tubeDiam,
                             50 * u.NTU, coagGraph, 12 * u.mg/u.L, 
                             floc.HumicAcid, floc.PACl, floc.Clay,
                             k, floc.RATIO_HEIGHT_DIAM)
line15mg50 = floc.pc_viscous(enerDis, temperature, resTime, tubeDiam,
                             50 * u.NTU, coagGraph, 15 * u.mg/u.L, 
                             floc.HumicAcid, floc.PACl, floc.Clay,
                             k, floc.RATIO_HEIGHT_DIAM)

x = coagGraph.to(u.mg/u.L)
plt.plot(x, line0mg50, 'r', x, line3mg50, 'b', x, line6mg50, 'g',
         x, line9mg50, 'm', x, line12mg50, 'c', x, line15mg50, 'y')


# Begin graphing the 100NTU datasets
plt.figure('100NTU', (6,6))
plt.title('100 NTU Graph')
plt.ylabel('pC*')
plt.xlabel('coagulant dosage (mg/L)')

plt.plot(coag, Data100NTU['0 mg/L'], 'r.', coag, Data100NTU['3 mg/L'], 'b.',
         coag, Data100NTU['6 mg/L'], 'g.', coag, Data100NTU['9 mg/L'], 'm.',
         coag, Data100NTU['12 mg/L'], 'c.', coag, Data100NTU['15 mg/L'], 'y.')

line0mg100 = floc.pc_viscous(enerDis, temperature, resTime, tubeDiam,
                             100 * u.NTU, coagGraph, 0 * u.mg/u.L, 
                             floc.HumicAcid, floc.PACl, floc.Clay,
                             k, floc.RATIO_HEIGHT_DIAM)
line3mg100 = floc.pc_viscous(enerDis, temperature, resTime, tubeDiam,
                             100 * u.NTU, coagGraph, 3 * u.mg/u.L, 
                             floc.HumicAcid, floc.PACl, floc.Clay,
                             k, floc.RATIO_HEIGHT_DIAM)
line6mg100 = floc.pc_viscous(enerDis, temperature, resTime, tubeDiam,
                             100 * u.NTU, coagGraph, 6 * u.mg/u.L, 
                             floc.HumicAcid, floc.PACl, floc.Clay,
                             k, floc.RATIO_HEIGHT_DIAM)
line9mg100 = floc.pc_viscous(enerDis, temperature, resTime, tubeDiam,
                             100 * u.NTU, coagGraph, 9 * u.mg/u.L, 
                             floc.HumicAcid, floc.PACl, floc.Clay,
                             k, floc.RATIO_HEIGHT_DIAM)
line12mg100 = floc.pc_viscous(enerDis, temperature, resTime, tubeDiam,
                              100 * u.NTU, coagGraph, 12 * u.mg/u.L, 
                              floc.HumicAcid, floc.PACl, floc.Clay,
                              k, floc.RATIO_HEIGHT_DIAM)
line15mg100 = floc.pc_viscous(enerDis, temperature, resTime, tubeDiam,
                              100 * u.NTU, coagGraph, 15 * u.mg/u.L, 
                              floc.HumicAcid, floc.PACl, floc.Clay,
                              k, floc.RATIO_HEIGHT_DIAM)

x = coagGraph.to(u.mg/u.L)
plt.plot(x, line0mg100, 'r', x, line3mg100, 'b', x, line6mg100, 'g',
         x, line9mg100, 'm', x, line12mg100, 'c', x, line15mg100, 'y')


# And now we display our graph!
plt.show()
