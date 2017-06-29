"""
Created on Sun Jun 11

@author: Monroe Weber-Shirk

Last modified: Thu Jun 29 2017 
By: Sage Weber-Shirk
"""
# units allows us to include units in all of our calculations
import math
import numpy as np

from AguaClara_design.units import unit_registry as u

#We need to fix the formatting so that it doesn't display trailing zeroes
#that are not significant.

def sig(x,n):
    """x is a number that may include units. n is the number of significant
digits to display."""
# Check to see if the quantity x includes units so we can strip the
# units and then reattach them at the end.
    if type(x) == type(1*u.m):
        xunit=x.units
        xmag=float(x.magnitude)
    else:
        xmag=x
    
    if xmag == 0.:
        return "0." + "0"*(n-1)
    if n==1:
        return math.floor(xmag)

    out = []

    if xmag < 0:
        out.append("-")
        xmag = -xmag

    e = int(math.log10(xmag))
    tens = math.pow(10, e - n + 1)
    y = math.floor(xmag/tens)

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
            out.extend(m[1:n])
        out.append('e')
        if e > 0:
            out.append("+")
        out.append(str(e))
    elif e == (n -1):
        out.append(m)
    elif e >= 0:
        out.append(m[:e+1])
        if e+1 < len(m):
            out.append(".")
            out.extend(m[e+1:])
    else:
        out.append("0.")
        out.extend(["0"]*-(e+1))
        out.append(m)
    
    if type(x) == type(1*u.m):
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


####################### Unit Testing #######################
def has_units(*args, strict=True):
    """Return False if none of the passed parameters have pint units.
    
    By default, returns True only if every single parameter has units.
    If strict mode is deactivated, returns True if the majority (>=50%) 
    of the inputs have units.
    This distinction is important as some functions have parameters both with
    and without units (dimensionless ratios, etc.).
    
    Relies on the 'pint' module, which provides unit handling.
    """
    print('strict:', strict)
    print('type:', type(strict))
    if strict:
        for a in args:
            try:
                a.units
            except AttributeError:
                return False
        return True
    else:
        total = len(args)
        print('length:', total)
        num_units = 0
        for a in args:
            try:
                a.units
                num_units += 1
            except AttributeError:
                pass
        if (num_units / total) >= 0.5:
            return True
        else:
            return False


def unit_stripper(*args, mode='cursory', checkall=True):
    """Strip units from all input parameters.
    
    Parameters without units are simply passed along.
    
    By default, returns a NumPy array containing unit-stripped versions of
    all non-keyword input parameters in input order.
    
    In comprehensive mode, returns a similar NumPy array but with the first
    value a boolean indicator of whether or not the passed parameters contain
    units.
    By default, comprehensive mode 
    
    Values returned are in terms of pint's base units. AguaClara uses 'mks',
    or meters/kilograms/seconds. All magnitudes returned by this function
    will be in terms of those values or, in the case of temperature, Kelvin.
    
    Relies on the 'pint' module, which provides unit handling.
    """
    def single_strip(arg):
        try:
            arg.ito_base_units()
            return arg.magnitude
        except AttributeError: 
            return arg
    if mode == 'cursory':
        return np.array([single_strip(a) for a in args])
    elif mode == 'comprehensive':
        print('checkall:', checkall)
        print('type:', type(checkall))
        HasUnits = has_units(args, strict=checkall)
        print(args, HasUnits)
        return HasUnits, np.array([single_strip(a) for a in args])
    else:
        raise ValueError('Unknown argument for keyword \'mode\'')


