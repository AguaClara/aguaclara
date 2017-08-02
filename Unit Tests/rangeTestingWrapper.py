# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 10:59:18 2017

@author: Sage Weber-Shirk

Last modified: Wed Aug 2 2017
By: Sage Weber-Shirk

NOTE: The wrapper in this file is currently broken and does not function as 
intended. It is based on an old version of the check_range function found in
'utility'. 
"""
import functools


def input_checker(*params):
    """Ensure that the values in the wrapped function are within valid ranges.
    
    Takes as inputs a number of sequence arguments equal to the number of
    input parameters the wrapped function has.
    Each sequence must either be mutable or a two-element tuple.
    The first element in each sequence is the range desired. Ranges this
    wrapper can understand are detailed in the knownChecks list, though
    this may become more robust in the future.
    The second element should be the name of the input, for debugging purposes
    if an error is raised. If no name is supplied and the input was a mutable
    sequence type, the name "Input" will be applied.
    """
    for param in params:
        #print("param:", param)
        if len(param) == 1:
            param.append("Input")
    paramsAsEnum = enumerate(params)
    def decorator(func):
        assigned = tuple(attr for attr in functools.WRAPPER_ASSIGNMENTS if hasattr(func, attr))
        updated = tuple(attr for attr in functools.WRAPPER_UPDATES if hasattr(func, attr))

        @functools.wraps(func, assigned=assigned, updated=updated)
        def input_wrapper(*args, **kwargs,):
            knownChecks = ('>0', '>=0', '0-1', 'int')
            argsList = list(args)
            #print("argsList:", argsList)
            newArgs = []
            for enum, (constraint, name) in paramsAsEnum:
                #This ensures that all whitespace is removed before checking 
                #if the request is understood
                constraint = "".join(constraint.split())
                
                if constraint not in knownChecks:
                    raise RuntimeError("Unknown parameter validation "
                                       "request: {0}.".format(constraint))
                elif constraint == ('>0') and argsList[enum] <= 0:
                    raise ValueError("{1} is {0} but must be greater "
                                     "than 0.".format(argsList[enum], name))
                elif constraint == ('>=0') and argsList[enum] <0:
                    raise ValueError("{1} is {0} but must not be "
                                     "negative.".format(argsList[enum], name))
                elif constraint == ('0-1') and not 0 <= argsList[enum] <= 1:
                    raise ValueError("{1} is {0} but must be between "
                                     "0 and 1.".format(argsList[enum], name))
                elif constraint == 'int' and int(argsList[enum]) != argsList[enum]:
                    raise TypeError("{1} is {0} but must evaluate to "
                                    "an integer.".format(argsList[enum], name))
        
                newArgs.append(argsList[enum])
            #print("newArgs:", newArgs)
            #print("unpacked:", *newArgs)
            result = func(*newArgs, **kwargs)
            return result
        #print("func:", func)
        #print("input_wrapper:", input_wrapper)
        return input_wrapper
    #print("decorator:", decorator)
    return decorator


@input_checker(['> 0', "foo"], ('> = 0', 'test2'), ['>=0', 'test3'], ['0-1', "Ratio"], ['0-1', 'Reynolds'], ['int', "number"])
def foo(*args):
    return [arg + 1 for arg in args]

@input_checker(['>0', 'tester'])
def bar(arg):
    return arg + 2
print("bar:", bar)

print("wrapper:", input_checker)

test2 = bar(6)
print("test2:", test2)

test1 = foo(7, 6, 0, 0.5, -0, 7.0, 2)
print("test1:", test1)

test4 = foo()
print("test4:", test4)

test3 = bar(1)
print("test3:", test3)