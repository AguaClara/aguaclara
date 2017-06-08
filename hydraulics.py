# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import math
import pint
u = pint.UnitRegistry(system='mks')

def Re_pipe(Q,D,nu):
    Re=(4*Q)/(math.pi*D*nu)
    return Re.to(u.dimensionless)
# The .to part forces Re to be dimensionless

Re_TRANSITION_PIPE=2100

# Returns the friction factor for pipe flow for both laminar and turbulent flows
def f(Q,D,nu,e):
    if Re_pipe(Q,D,nu)>=Re_TRANSITION_PIPE:
        f=0.25/(math.log10(e/(3.7*D)+5.74/Re_pipe(Q,D,nu)**0.9))**2
    else:
        f=64/Re_pipe(Q,D,nu)
    return f*u.dimensionless

# Returns the major pipe head loss (due to wall shear) for both laminar and turbulent flows.
def HLf(Q,D,L,nu,e):
    HLf=f(Q,D,nu,e)*8/(u.g_0*math.pi**2)*(L*Q**2)/D**5
    return HLf.to(u.m)

# Returns the minor head loss (due to expansions). This equation applies to both laminar and turbulent flows.
def HLe(Q,D,K):
    HLe=K*8/(u.g_0*math.pi**2)*(Q**2)/(D**4)
    return HLe.to(u.m)

# Returns the total head loss due to major and minor losses. This equation applies to both laminar and turbulent flows.
def HL(Q,D,L,nu,e,K):
    HL=HLf(Q,D,L,nu,e)+HLe(Q,D,K)
    return HL.to(u.m)