# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 16:50:46 2017

@author: Sage Weber-Shirk
"""

######################### Imports #########################
import math
import numpy as np
import scipy

from AguaClara_design.units import unit_registry as u

##################### Class Definition #####################

class Chemical:
    def __init__(self, diameter, density, molecWeight, multFactor):
        self.Diameter = diameter
        self.Density = density
        self.MolecWeight = molecWeight
        self.MultFactor = multFactor
        
    
PACl = Chemical(50 * u.nm, 1138 * u.kg/u.m**3, 1.039 * 10**3 * u.g/u.mole, 13)
AlOH3 = Chemical(70 * u.nm, 2420 * u.kg/u.m**3, 599.21 * u.g/u.mole, 1)