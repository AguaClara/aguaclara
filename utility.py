"""
Created on Sun Jun 11

@author: Monroe Weber-Shirk

Last modified: Wed Jul 5 2017 
By: Sage Weber-Shirk
"""
# units allows us to include units in all of our calculations
import math

from AguaClara_design.units import unit_registry as u

import numpy as np

#We need to fix the formatting so that it doesn't display trailing zeroes
#that are not significant.

def sig(x,n):
    """Return the 1st input reduced to a number of significant digits.
    
    x is a number that may include units. n is the number of significant 
    digits to display.
    """
# Check to see if the quantity x includes units so we can strip the
# units and then reattach them at the end.
    if type(x) == type(1 * u.m):
        xunit = x.units
        xmag = float(x.magnitude)
    else:
        xmag = x
    if xmag == 0.:
        return "0." + "0" * (n-1)
    if n == 1:
        return math.floor(xmag)

    out = []
    if xmag < 0:
        out.append("-")
        xmag = -xmag
    e = int(math.log10(xmag))
    tens = math.pow(10, e - n + 1)
    y = math.floor(xmag / tens)
    if y < math.pow(10, n - 1):
        e = e -1
        tens = math.pow(10, e - n+1)
        y = math.floor(xmag / tens)
    if abs((y + 1.) * tens - xmag) <= abs(y * tens -xmag):
        y = y + 1
    if y >= math.pow(10,n):
        y = y / 10.
        e = e + 1

    m = "%.*g" % (n, y)
    if e < -2 or e >= n:
        out.append(m[0])
        if n > 1:
            out.append(".")
            out.extend(m[1 : n])
        out.append('e')
        if e > 0:
            out.append("+")
        out.append(str(e))
    elif e == (n - 1):
        out.append(m)
    elif e >= 0:
        out.append(m[:e + 1])
        if e+1 < len(m):
            out.append(".")
            out.extend(m[e + 1:])
    else:
        out.append("0.")
        out.extend(["0"] * -(e + 1))
        out.append(m)
    
    if type(x) == type(1 * u.m):
        req = "".join(out)
        return '{:~P}'.format(u.Quantity(req,xunit))
    else:
        return "".join(out)

def stepceil_with_units(param, step, unit):
    """This function returns the smallest multiple of 'step' greater than or
    equal to 'param' and outputs the result in Pint units. 
    This function is unit-aware and functions without requiring translation
    so long as 'param' and 'unit' are of the same dimensionality.
    """
    counter = 0 * unit
    while counter < param.to(unit):
        counter += step * unit
    return counter
# Take the values of the array, compare to x, find the index of the first value less than or equal to x
def floor_nearest(x,array):
    myindex = np.argmax(array <= x)
    return array[myindex]

# Take the values of the array, compare to x, find the index of the first value greater or equal to x
def ceil_nearest(x,array):
    myindex = np.argmax(array >= x)
    return array[myindex]
