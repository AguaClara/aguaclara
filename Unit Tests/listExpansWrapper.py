# -*- coding: utf-8 -*-
"""
Created on Wed Aug  2 15:04:59 2017

@author: Sage Weber-Shirk
"""
import numpy as np
import functools

from AguaClara_design.units import unit_registry as u

def list_handler(func):
    """Wraps a function to handle list inputs."""
    @functools.wraps(func)
    def wrapper(*args, HandlerResult=None, **kwargs):
        """Run through the wrapped function once for each array element.
        
        :param HandlerResult: output type. Defaults to lists.
        """
        sequences = []
        enumsUnitCheck = enumerate(args)
        argsList = list(args)
        for num, arg in enumsUnitCheck:
            if type(arg) == type(1 * u.m):
                argsList[num] = arg.to_base_units().magnitude
        enumsUnitless = enumerate(argsList)
        for num, arg in enumsUnitless:
            if isinstance(arg, (list, tuple, np.ndarray)):
                sequences.append(num)
        if len(sequences) == 0:
            result = func(*args, **kwargs)
        else:
            limiter = len(argsList[sequences[0]])
            iterant = 0
            result = []
            for num in sequences:
                for arg in argsList[num]:
                    if iterant >= limiter:
                        break
                    argsList[num] = arg
                    result.append(wrapper(*argsList, 
                                          HandlerResult=HandlerResult, **kwargs))
                    iterant += 1
            if not HandlerResult:
                pass
            elif HandlerResult == "nparray":
                result = np.array(result)
            elif HandlerResult == "tuple":
                result = tuple(result)
            elif HandlerResult == "list":
                result == list(result)
        return result
    return wrapper

@list_handler
def foo(param):
    return param + 2

@list_handler
def bar(param):
    return param % 2 == 0

@u.wraps(None, None, False)
@list_handler
def foobar(one, two):
    return one + two

#print("singles:")
#
#print(foo(7), foo(10), bar(7), bar(10), foobar(7, 10))
#
#print("lists:")
#
#print(foo([7, 10]), foo((7, 10)), bar([7, 10]), bar((7, 10)))
#
#print("foobar:", foobar([1, 2], 3))
#print("foobar:", foobar(4, [5, 6]))
#
#print("compound:")
print("foobar:", foobar([1,3], [4,8]))
#
@list_handler
def threeadd(one, two, three):
    return one + two + three
#
#print("threeadd single:", threeadd(1, 2, 3))
#print("threeadd one list:", threeadd([1, 2], 3, 4))
#print("threeadd compound:", threeadd([1,2,3],[5,7],[10,13]))

pintlist = [1, 2, 3] * u.m
pintarray = np.array(pintlist)
pintone = 1 * u.m

print("pintlist type:", type(pintlist))
#print("pintlist:", pintlist)
print("pintarray type:", type(pintarray))
#print("pintone:", pintone)

print("list:", foobar(pintlist, [4,5]))
print("array:", foobar(pintarray, [4,5]))
print("typeorder test:", foobar(pintlist, [4,5], HandlerResult="nparray"))