"""Utility functions and features

This module provides functions and features for scientific calculations and 
complex function inputs.

Example:
    >>> import aguaclara.core.utility as ut
    >>> ut.round_sig_figs(1234567, 3)
    1230000
"""
from aguaclara.core.units import u

import numpy as np
from math import log10, floor, ceil
import warnings

def optional_units(arg_positions, keys):
    """Wrap a function so that arguments may optionally have units.
    
    This should be used as a function decorator; it will not do anything
    meaningful unless it is appended with a ``@`` before another function.

    Example:
        @optional_units([0, 1], ['num', 'step'])
        def stepper(num, step=10, func=round):
            step = step.to(num.units)
            num = func(num / step) * step
            return num

    Args:
        - ``arg_positions (int list)``: Position indices of positional and
          keyword arguments with optional units
        - ``keys (str list)``: Names of positional and keyword arguments with
          optional units
    """
    # func is the function that is being decorated, and *args/**kwargs are the 
    # arguments being passed to that function.
    def decorator(func):
        def wrapper(*args, **kwargs):
            args = list(args)
            for i in range(len(args)):
                if i in arg_positions:
                    args[i] *= u.dimensionless

            for key in list(kwargs.keys()):
                if key in keys:
                    kwargs[key] *= u.dimensionless

            result = func(*args, **kwargs)

            # Convert back to native Python number type, if possible
            if result.units == u.dimensionless:
                result = result.magnitude

            return result
        return wrapper
    return decorator

@optional_units([0], ['num'])
def round_sig_figs(num, figs=4):
    """Round a number to some amount of significant figures.

    Args:
        - ``num (float)``: Value to be rounded (optional units)
        - ``figs (int)``: Number of significant digits to be rounded to 
          (recommended, defaults to 4)
    """
    # Prevents undefined log10(0) if num is already 0
    if num.magnitude != 0:
        decimals = figs - int(floor(log10(abs(num.magnitude)))) - 1
        num = np.round(num.magnitude, decimals) * num.units

    return num

def round_sf(num, figs=4):
    """Round a number to some amount of significant figures.

    Args:
        - ``num (float)``: Value to be rounded (optional units)
        - ``figs (int)``: Number of significant digits to be rounded to 
          (recommended, defaults to 4)

    Note: This function will be deprecated after 21 Dec 2019. Use
    round_sig_figs instead.
    """
    warnings.warn(
        'round_sf will be deprecated after 21 Dec 2019. Use '
            'round_sig_figs instead.',
        FutureWarning
    )
    round_sig_figs(num, figs = figs)

@optional_units([0, 1], ['num', 'step'])
def _stepper(num, step=10, func=round):
    """Round a number to be a multiple of some step.
    
    Args:
        - ``num (float)``: Value to be rounded (optional units)
        - ``step (float)``: Factor to which ``num`` will be rounded (defaults
          to 10).
        - ``func (function)``: Rounding function to use (defaults to round())
    
    Note:
        ``step`` must have the same dimensionality as ``num``, but not
        necessarily the same units (e.g. ``num``: meters and ``step``:
        centimeters are acceptable).
    """
    step = step.to(num.units)
    num = func(num / step) * step
    return num

def round_step(num, step=10):
    """Round a number to be a multiple of some step.
    
    Args:
        - ``num (float)``: Value to be rounded (optional units)
        - ``step (float)``: Factor to which ``num`` will be rounded (defaults
          to 10).
    
    Note:
        ``step`` must have the same dimensionality as ``num``, but not
        necessarily the same units (e.g. ``num``: meters and ``step``:
        centimeters are acceptable).
    """
    return _stepper(num, step = step, func = round)

def ceil_step(num, step=10):
    """Like :func:`round_step`, but ``num`` is always rounded up."""
    return _stepper(num, step = step, func = ceil)

def floor_step(num, step=10):
    """Like :func:`round_step`, but ``num`` is always rounded down."""
    return _stepper(num, step = step, func = floor)

def stepceil_with_units(param, step, unit):
    """Round a number up to be a multiple of some step.
    
    Args:
        - ``param (float)``: Value to be rounded (optional units)
        - ``step (float)``: Factor to which ``param`` will be rounded
        - ``unit (Quantity)``: units of ``step``
    
    Note: this function will be deprecated after 21 Dec 2019. Use ceil_step
    instead.
    """
    warnings.warn(
        'stepceil_with_units will be deprecated after 21 Dec 2019. Use '
            'ceil_step instead.',
        FutureWarning
    )
    counter = 0 * unit
    while counter < param.to(unit):
        counter += step * unit
    return counter

def floor_nearest(x, array):
    """Get the nearest element of a NumPy array less than or equal to a value.

    Args:
        - ``x``: Value to compare
        - ``array (numpy.array)``: Array to search
    """
    i = np.argmax(array >= x) - 1
    return array[i]

def ceil_nearest(x, array):
    """Get the nearest element of a NumPy array less than or equal to a value.

    Args:
        - ``x``: Value to compare
        - ``array (numpy.array)``: Array to search
    """
    i = np.argmax(array >= x)
    return array[i]

def _minmax(*args, func=np.max):
    """Get the minuimum/maximum value of some Pint quantities with units.
    
    Args:
        - ``func (function)``: the min/max function being used.

    Note:
        - All quantities must have the same dimensionality, but can have
          different units.
        - The output will have the same units as the first argument.

    Example:
        >>> from aguaclara.play import *
        >>> ut.max(10 * u.m, 100 * u.cm, 32 * u.cm, 40 * u.inch, 40 * u.km)
        <Quantity(40000.0, 'meter')>
    """
    base_quantity = args[0]
    lst = []

    for arg in args:
        lst.append((arg / base_quantity))

    result = func(lst) * base_quantity
    return result

def max(*args):
    """Get the maximum value of some Pint quantities with units.
    
    Note:
        - All quantities must have the same dimensionality, but can have
          different units.
        - The output will have the same units as the first argument.

    Example:
        >>> from aguaclara.play import *
        >>> ut.max(10 * u.m, 100 * u.cm, 32 * u.cm, 40 * u.inch, 40 * u.km)
        <Quantity(40000.0, 'meter')>
    """
    return _minmax(*args, func = np.max)

def min(*args):
    """Like :func:`max`, but the minimum of the quantites."""
    return _minmax(*args, func = np.min)

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

def array_qtys_to_strs(lst):
    """Convert Pint quantities in a NumPy array to strings.
    
    Args:
        - ``lst (numpy.ndarray Quantity)``: a list of values that has a Pint
            unit attached to it
    """
    return [str(value) for value in lst]
