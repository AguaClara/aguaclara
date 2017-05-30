# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import math
import pint
u = pint.UnitRegistry()
#defining one function
def Re(Q,D,nu):
    Re=(4*Q)/(math.pi*D*nu)
    return Re.to(u.dimensionless)
#The .to part forces Re to be dimensionless
