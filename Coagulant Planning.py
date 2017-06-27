# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 15:56:52 2017

@author: Sage Weber-Shirk
"""

class chemical(name, diameter, density, MW, ):
    #def DNC(): replaced completely by diameter object parameter
	# diameter of the input, not the precipitate!
	
    # The following two could be heavily reworked with the addition
    # of an object parameter, assuming the multiplier works in all 
    # the relevant equations
    ?def RhoAlNanCluster():
    ?def ConcPrecipitate():
    # These equations would still need to exist but could be simpler than
    # their MathCad counterparts.
    Above is Done!
	
    # The following functions can be rewritten: 
    def PhiFloc0(): #relies on ConcPrecipitate
        
    # The following functions will need to stay the same, remaining
    # functions and not methods:
    def ConcFloc(): #Is simply ConcPrecipitate + ConcClay(a constant)
    def NNC(): #Relies on diameter and RhoAlNanCluster
    def LambdaFloc(): #Relies on PhiFloc0
    def Phi(): #Relies on PhiFloc0
    def RhoFloc0(): #Relies on PhiFloc0 and ConcFloc
    def GammaCoag(): #Relies on PhiFloc0 and diameter
    def PCViscous(): # Relies on GammaCoag
    def RhoFloc(): #Relies on RhoFloc0
    def VelTerminal(): #Relies on RhoFloc0
    def DiamFuncVelTerminal(): #Relies on RhoFloc0
    def TimeCollisionLaminar(): #Relies on PhiFloc0 and GammaCoag
    def TimeCollisionTurbulent(): #Relies on PhiFloc0
    def DiamKolmogorov(): #Relies on PhiFloc0
    def DiamV(): #Relies on PhiFloc0
	
lambda = separation distance
Phi = vol frac occupied by particles
xFloc0 = initial x, xFloc = x of clay + coag
    