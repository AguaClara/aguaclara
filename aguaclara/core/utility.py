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
import functools


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

# TODO: I'm not sure if these next two functions work for unsorted arrays, so it
# would be good to check in the future -Oliver Leung (oal22), 19 Jul '19

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

def get_sdr(spec):
    """Get the SDR of a string ``spec`` with the form \"sdrXX\".

    Args:
        - ``spec (str)``: The specification string to be parsed."""
    if spec[:3] != "sdr":
        raise ValueError('Not a valid SDR.')
    return int(spec[3:])

def list_handler():
    """Wraps a scalar function to output a NumPy array if passed one or more inputs
    as sequences (lists, tuples or NumPy arrays). For each sequence input, this
    wrapper will recursively evaluate the function with the sequence replaced
    by each of its elements and return the results in n-dimensional NumPy array,
    where n is the number of sequence inputs.

    For a function "f" of one argument, f([x_1, ..., x_n]) would be evaluated to
    [f(x_1), ..., f(x_n)]. For a function passed multiple sequences of
    dimensions d_1, ..., d_n (from left to right), the result would be a
    d_1 x ... x d_n array.
    """
    def decorate(func):
        @functools.wraps(func) # For Sphinx documentation of decorated functions
        def wrapper(*args, **kwargs):
            """Run through the wrapped function once for each array element.
            """
            # Identify the first positional argument that is a sequence.
            # Pint units must be ignored to include sequences with units.
            argsFirstSequence = None
            for num, arg in enumerate(args):  # args is a tuple
                if isinstance(arg, u.Quantity):
                    arg = arg.to_base_units().magnitude
                if isinstance(arg, (list, tuple, np.ndarray)):
                    argsFirstSequence = num
                    break
            # Identify the first keyword argument that is a sequence.
            kwargsFirstSequence = None
            for keyword, arg in kwargs.items():  # kwargs is a dictionary
                if isinstance(arg, u.Quantity):
                    arg = arg.to_base_units().magnitude
                if isinstance(arg, (list, tuple, np.ndarray)):
                    kwargsFirstSequence = keyword
                    break

            # If there are no sequences, evaluate the function.
            if argsFirstSequence is None and kwargsFirstSequence is None:
                return func(*args, **kwargs)
            # If there are sequences, iterate through them from left to right.
            # This means beginning with positional arguments.
            elif argsFirstSequence is not None:
                result = []
                argsList = list(args)
                # For each element of the leftmost sequence, evaluate the
                # function with the sequence replaced by the single element.
                # Store the results of all the elements in result.
                for arg in argsList[argsFirstSequence]:
                    # We can safely redefine the entire list argument because
                    # the new definition remains within this namespace; it does
                    # alter the loop or penetrate further up the function.
                    argsList[argsFirstSequence] = arg
                    # This recursive call creates a multi-dimensional array if
                    # there are multiple sequence arguments.
                    result.append(wrapper(*argsList, **kwargs))
            # If there are no sequences in the positional arguments, iterate
            # through those in the keyword arguments.
            else:
                result = []
                for arg in kwargs[kwargsFirstSequence]:
                    kwargs[kwargsFirstSequence] = arg
                    result.append(wrapper(*args, **kwargs))

            if isinstance(result[0], u.Quantity):
                units = result[0].units
                return np.array([r.magnitude for r in result]) * units
            else:
                return np.array(result)

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

def array_qtys_to_strs(lst):
    """Convert Pint quantities in a NumPy array to strings.

    Args:
        - ``lst (numpy.ndarray Quantity)``: a list of values that has a Pint
            unit attached to it
    """
    return [str(value) for value in lst]
