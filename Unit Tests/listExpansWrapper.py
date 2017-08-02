# -*- coding: utf-8 -*-
"""
Created on Wed Aug  2 15:04:59 2017

@author: mw24
"""
import numpy as np

def list_handler(func):
    def wrapper(*args, **kwargs):
        sequences = []
        enums = enumerate(args)
        for num, arg in enums:
            if isinstance(arg, (list, tuple, np.ndarray)):
                sequences.append(num)
        if len(sequences) == 0:
            result = func(*args, **kwargs)
        else:
            argsList = list(args)
            result = []
            iterant = 0
            for num in sequences:
                #print("sequences:", sequences)
                print("argsList pre:", argsList)
                for arg in argsList[num]:
                    argsList[num] = arg
                    #print("argsList[num]:", argsList[num])
                    #print("iter:", iterant)
                    result.append(wrapper(*argsList, **kwargs))
                    iterant += 1
                    #print("res len:", len(result))
                print("argsList mid:", argsList)
            print("argsList post:", argsList)
            #print("iterant:", iterant)
            #print("seq len:", len(sequences))
            if iterant > len(sequences) + 1:
                #del result[len(sequences):]
                pass
        return result
    return wrapper

@list_handler
def foo(param):
    return param + 2

@list_handler
def bar(param):
    return param % 2 == 0

@list_handler
def foobar(one, two):
    return one + two

print("singles:")

print(foo(7), foo(10), bar(7), bar(10), foobar(7, 10))

print("lists:")

print(foo([7, 10]), foo((7, 10)), bar([7, 10]), bar((7, 10)))

print("foobar:", foobar([1, 2], 3))
print("foobar:", foobar(4, [5, 6]))

print("compound:")
print("foobar:", foobar([1,3], [4,8]))

@list_handler
def threeadd(one, two, three):
    return one + two + three

print("threeadd single:", threeadd(1, 2, 3))
print("threeadd one list:", threeadd([1, 2], 3, 4))
print("threeadd compound:", threeadd([1,2],[4,6],9))