# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 15:43:43 2017

@author: kn348
"""
import numpy as np
def wer(x,n):
    sgn=np.sign(x)
    x=abs(x)
    n=int(np.log10(x/10.)) # Here you overwrite input n!
    if x<1. :
            val=x/(10**(n-1))
    else:
        val=x/(10**n)
    return sgn*int(val)*10.**n

          