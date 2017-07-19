"""
Created on Sun Jun 11

@author: Monroe Weber-Shirk

Last modified: Wed Jul 5 2017 
By: Sage Weber-Shirk
"""
# units allows us to include units in all of our calculations
import math

try:
    from AguaClara_design.units import unit_registry as u
except ModuleNotFoundError:
    from units import unit_registry as u

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
    myindex = np.argmax(array >= x) - 1
    return array[myindex]

# Take the values of the array, compare to x, find the index of the first value greater or equal to x
def ceil_nearest(x,array):
    myindex = np.argmax(array >= x)
    return array[myindex]


def check_range(*args):
    """Check whether passed paramters fall within approved ranges.
    
    Does not return anything, but will raise an error if a parameter falls
    outside of its defined range.
    
    Input should be passed as an array of sequences, with each sequence
    having three elements:
        [0] is the value being checked,
        [1] is the range parameter within which the value should fall, and
        [2] is the name of the parameter, for better error messages.
    If [2] is not supplied, "Input" will be appended as a generic name.
    
    Range requests that this function understands are listed in the
    knownChecks sequence.
    """
    knownChecks = ('>0', '>=0', '0-1', '<0', '<=0', 'int', 'boolean')
    for arg in args:
        #Converts arg to a mutable list
        arg = [*arg]
        if len(arg) == 1:
            #arg[1] details what range the parameter should fall within; if 
            #len(arg) is 1 that means a validity was not specified and the 
            #parameter should not have been passed in its current form
            raise TypeError("No range-validity parameter provided.")
        elif len(arg) == 2:
            #Appending 'Input" to the end allows us to give more descriptive
            #error messages that do not fail if no description was supplied.
            arg.append("Input")
        #This ensures that all whitespace is removed before checking if the
        #request is understood
        arg[1] = "".join(arg[1].lower().split())
            
        if arg[1] not in knownChecks:
            raise RuntimeError("Unknown parameter validation request: {0}.".format(arg[1]))
        elif arg[1] == '>0' and arg[0] <= 0:
            raise ValueError("{1} is {0} but must be greater than 0.".format(arg[0], arg[2]))
        elif arg[1] == '>=0' and arg[0] <0:
            raise ValueError("{1} is {0} but must be 0 or greater.".format(arg[0], arg[2]))
        elif arg[1] == '0-1' and not 0 <= arg[0] <= 1:
            raise ValueError("{1} is {0} but must be between 0 and 1.".format(arg[0], arg[2]))
        elif arg[1] == '<0' and arg[0] >= 0:
            raise ValueError("{1} is {0} but must be less than than 0.".format(arg[0], arg[2]))
        elif arg[1] == '<=0' and arg[0] >0:
            raise ValueError("{1} is {0} but must be 0 or less.".format(arg[0], arg[2]))
        elif arg[1] == 'int' and int(arg[0]) != arg[0]:
            raise TypeError("{1} is {0} but must be a numeric integer.".format(arg[0], arg[2]))
        elif arg[1] == 'boolean' and type(arg[0]) != bool:
            raise TypeError("{1} is {0} but must be a boolean.".format(arg[0], arg[2]))
