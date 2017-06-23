"""
Created on Sun Jun 11

@author: Monroe Weber-Shirk

Last modified: Fri Jun 23 2017 
By: Sage Weber-Shirk
"""
# units allows us to include units in all of our calculations
import math

from units import unit_registry as u

#We need to fix the formatting so that it doesn't display trailing zeroes
#that are not significant.

def sig(x,n):
    """x is a number that may include units. n is the number of significant
digits to display."""
# Check to see if the quantity x includes units so we can strip the
# units and then reattach them at the end.
    if type(x) == type(1*u.m):
        xmag=float(x.magnitude)
        xunit=x.units
        if n==1:
            return math.floor(xmag)
        if xmag!=0:
           xmag=round(xmag, n-1-int(math.floor(math.log10(abs(xmag)))))
           return '{:~P}'.format(u.Quantity(xmag,xunit))
    else:
        xmag=x
        if n==1:
            return math.floor(xmag)
        if xmag!=0:
           xmag=round(xmag, n-1-int(math.floor(math.log10(abs(xmag)))))
           return xmag


def stepceil_with_units(param, step, unit):
    """This function returns the smallest multiple of 'step' greater than or
equal to 'param' and outputs the result in Pint units. 
This function is unit-aware and functions without requiring translation
so long as 'param' and 'unit' are of the same diemnsionality.
"""
    counter = 0 * unit
    while counter < param.to(unit):
        counter += step * u.inch
    return counter