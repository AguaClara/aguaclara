"""
Created on Sun Jun 11

@author: Monroe Weber-Shirk

Last modified: Thu Jun 22 2017 
By: Sage Weber-Shirk
"""
# units allows us to include units in all of our calculations
import math

from AguaClara_design.units import unit_registry as u


# x is a number that may include units. n is the number of significant digits to display.

# We need to fix the formatting so that it doesn't display trailing zeroes that are not significant.
def sig(x,n):
    #Check to see if the quantity x includes units so we can strip the units and then reattach them at the end.
    if type(x) == type(1*u.m):
        xmag=float(x.magnitude)
        xunit=x.units
    else:
        xmag=x
        xunit=1
    if xmag!=0:
        xmag=round(xmag, n-1-int(math.floor(math.log10(abs(xmag)))))
    return '{:~P}'.format(u.Quantity(xmag,xunit))


def stepceil_with_units(param, step, unit):
    counter = 0 * unit
    while counter < param.to(unit):
        counter += step * u.inch
    return counter