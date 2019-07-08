"""This file provides basic utility functions such as significant figures which
can be used throughout the plant design.

"""
from aguaclara.core.units import unit_registry as u
import functools

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
def floor_nearest(x, array):
    myindex = np.argmax(array >= x) - 1
    return array[myindex]


# Take the values of the array, compare to x, find the index of the first value greater or equal to x
def ceil_nearest(x, array):
    myindex = np.argmax(array >= x)
    return array[myindex]


def list_handler(HandlerResult="nparray"):
    """Wraps a function to handle list inputs.

    For each argument passed to the function as a sequence (list, tuple, or
    Numpy array), this wrapper will recursively evaluate the function with the
    sequence replaced by each of its elements and return the results in a
    sequence.

    For a function "f" of one argument, f([x_1, ..., x_n]) would be evaluated to
    [f(x_1), ..., f(x_n)]. For a function passed multiple sequences of
    dimensions d_1, ..., d_n (from left to right), the result would be a
    d_1 x ... x d_n dimensional array.

    :param HandlerResult: output type. Defaults to Numpy arrays.
    """
    def decorate(func):
        @functools.wraps(func) # For Sphinx documentation of decorated functions
        def wrapper(*args, **kwargs):
            """Run through the wrapped function once for each array element.
            """
            # Loop through the positional arguments (args), identify those that
            # are sequences, and add their index locations to the list
            # "argSequences". Pint units must be ignored in order to recognize
            # sequences with units as sequences instead of Pint Quantities.
            argsSequences = []
            for num, arg in enumerate(args):
                if isinstance(arg, u.Quantity):
                    arg = arg.to_base_units().magnitude
                if isinstance(arg, (list, tuple, np.ndarray)):
                    argsSequences.append(num)

            # Repeat the above for keyword arguments (kwargs), but access them
            # as a dictionary whose keys are keywords/argument names and values
            # are corresponding argument values.
            kwargsSequences = []
            for keyword, arg in kwargs.items():
                if isinstance(arg, u.Quantity):
                    arg = arg.to_base_units().magnitude
                if isinstance(arg, (list, tuple, np.ndarray)):
                    kwargsSequences.append(keyword)

            # If there are no sequences to iterate through, simply return
            # the function evaluated with the given arguments.
            if len(argsSequences) == 0 and len(kwargsSequences) == 0:
                return func(*args, **kwargs)

            # If there are sequences, iterate through them from left to right.
            # This means beginning with positional arguments.
            if len(argsSequences) != 0:
                result = []
                argsList = list(args)
                # For each element of the leftmost sequence, evaluate
                # the function using the original arguments, except with the
                # sequence replaced by the single element. Store the results of
                # all the elements in a list (result).
                for arg in argsList[argsSequences[0]]:
                    # We can safely redefine the entire list argument because
                    # the new definition remains within this namespace; it does
                    # alter the loop or penetrate further up the function.
                    argsList[argsSequences[0]] = arg
                    # Here we dive down the rabbit hole. This recursive call
                    # creates a multi-dimensional array.
                    result.append(wrapper(*argsList, **kwargs))

            # If there are no sequences in the positional arguments, we can
            # begin iterating through those in the keyword arguments. The
            # process is the same as for positional arguments.
            else:
                result = []
                for arg in kwargs[kwargsSequences[0]]:
                    kwargs[kwargsSequences[0]] = arg
                    result.append(wrapper(*args, **kwargs))

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
