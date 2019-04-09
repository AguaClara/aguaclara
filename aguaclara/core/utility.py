"""This file provides basic utility functions such as significant figures which
can be used throughout the plant design.

"""
from aguaclara.core.units import unit_registry as u


import numpy as np
from math import log10, floor


def round_sf(number, digits):
    """Returns inputted value rounded to number of significant figures desired.

    :param number: Value to be rounded
    :type number: float
    :param digits: number of significant digits to be rounded to.
    :type digits: int
    """
    units = None
    try:
        num = number.magnitude
        units = number.units
    except AttributeError:
        num = number

    try:
        if (units != None):
            rounded_num = round(num, digits - int(floor(log10(abs(num)))) - 1) * units
        else:
            rounded_num = round(num, digits - int(floor(log10(abs(num)))) - 1)
        return rounded_num
    except ValueError:  # Prevents an error with log10(0)
        if (units != None):
            return 0 * units
        else:
            return 0


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


def list_handler(HandlerResult="nparray"):
    """Wraps a function to handle list inputs."""
    def decorate(func):
        def wrapper(*args, **kwargs):
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
    return decorate


def check_range(*args):
    """
    Check whether passed paramters fall within approved ranges.

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
