"""This file provides basic utility functions such as significant figures which
can be used throughout the plant design.

"""

# units allows us to include units in all of our calculations
import math

try:
    from aguaclara.core.units import unit_registry as u
except ModuleNotFoundError:
    from aguaclara.core.units import unit_registry as u

import numpy as np
import functools

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
        if n==1 and xmag>=1:
             req = round(xmag)
             return '{:~P}'.format(u.Quantity(req,xunit))

    else:
        xmag = x
    if xmag == 0.:
        return "0." + "0" * (n-1)
    if n == 1 and type(x)!=type(1 * u.m):
        return round(xmag)

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


def list_handler(func):
    """Wraps a function to handle list inputs."""
    @functools.wraps(func)
    def wrapper(*args, HandlerResult="nparray", **kwargs):
        """Run through the wrapped function once for each array element.

        :param HandlerResult: output type. Defaults to numpy arrays.
        """
        sequences = []
        enumsUnitCheck = enumerate(args)
        argsList = list(args)
        #This for loop identifies pint unit objects and strips them
        #of their units.
        for num, arg in enumsUnitCheck:
            if type(arg) == type(1 * u.m):
                argsList[num] = arg.to_base_units().magnitude
        enumsUnitless = enumerate(argsList)
        #This for loop identifies arguments that are sequences and
        #adds their index location to the list 'sequences'.
        for num, arg in enumsUnitless:
            if isinstance(arg, (list, tuple, np.ndarray)):
                sequences.append(num)
        #If there are no sequences to iterate through, simply return
        #the function.
        if len(sequences) == 0:
            result = func(*args, **kwargs)
        else:
            #iterant keeps track of how many times we've iterated and
            #limiter stops the loop once we've iterated as many times
            #as there are list elements. Without this check, a few
            #erroneous runs will occur, appending the last couple values
            #to the end of the list multiple times.
            #
            #We only care about the length of sequences[0] because this
            #function is recursive, and sequences[0] is always the relevant
            #sequences for any given run.
            limiter = len(argsList[sequences[0]])
            iterant = 0
            result = []
            for num in sequences:
                for arg in argsList[num]:
                    if iterant >= limiter:
                        break
                    #We can safely replace the entire list argument
                    #with a single element from it because of the looping
                    #we're doing. We redefine the object, but that
                    #definition remains within this namespace and does
                    #not penetrate further up the function.
                    argsList[num] = arg
                    #Here we dive down the rabbit hole. This ends up
                    #creating a multi-dimensional array shaped by the
                    #sizes and shapes of the lists passed.
                    result.append(wrapper(*argsList,
                                          HandlerResult=HandlerResult, **kwargs))
                    iterant += 1
            #HandlerResult allows the user to specify what type to
            #return the generated sequence as. It defaults to numpy
            #arrays because functions tend to handle them better, but if
            #the user does not wish to import numpy the base Python options
            #are available to them.
            if HandlerResult == "nparray":
                result = np.array(result)
            elif HandlerResult == "tuple":
                result = tuple(result)
            elif HandlerResult == "list":
                result == list(result)
        return result
    return wrapper


def check_range(*args):
    """Check whether passed paramters fall within approved ranges.

    Does not return anything, but will raise an error if a parameter falls
    outside of its defined range.

    Input should be passed as an array of sequences, with each sequence
    having three elements:
        [0] is the value being checked,
        [1] is the range parameter(s) within which the value should fall, and
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
        #This block checks that each range request is understood.
        #If the request is a compound one, it must be separated into individual
        #requests for validity comprehension
        for i in arg[1].split(","):
            if i not in knownChecks:
                raise RuntimeError("Unknown parameter validation "
                                       "request: {0}.".format(i))
        if not isinstance(arg[0], (list, tuple, np.ndarray)):
            arg[0] = [arg[0]]
        for i in arg[0]:
            if '>0' in arg[1] and i <= 0:
                raise ValueError("{1} is {0} but must be greater than "
                                 "0.".format(i, arg[2]))
            if '>=0' in arg[1] and i <0:
                raise ValueError("{1} is {0} but must be 0 or "
                                 "greater.".format(i, arg[2]))
            if '0-1' in arg[1] and not 0 <= i <= 1:
                raise ValueError("{1} is {0} but must be between 0 and "
                                 "1.".format(i, arg[2]))
            if '<0' in arg[1] and i >= 0:
                raise ValueError("{1} is {0} but must be less than "
                                 "0.".format(i, arg[2]))
            if '<=0' in arg[1] and i >0:
                raise ValueError("{1} is {0} but must be 0 or "
                                 "less.".format(i, arg[2]))
            if 'int' in arg[1] and int(i) != i:
                raise TypeError("{1} is {0} but must be a numeric "
                                "integer.".format(i, arg[2]))
            if 'boolean' in arg[1] and type(i) != bool:
                raise TypeError("{1} is {0} but must be a "
                                "boolean.".format(i, arg[2]))
