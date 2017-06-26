# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 15:56:52 2017

@author: Sage Weber-Shirk
"""

class chemical(name, diameter, density, MW, ):
    
    
    #def DNC(): replaced completely by diameter object parameter 
    ?def EtaCoag(): #Can perhaps be erased altogether? Otherwise can be replaced
    # by an object parameter
    # The following two could be heavily reworked with the addition
    # of an object parameter, assuming the multiplier works in all 
    # the relevant equations
    ?def RhoAlNanCluster():
    ?def ConcPrecipitate():
    # These equations would still need to exist but could be simpler than
    # their MathCad counterparts.
    
    # The following functions can be rewritten: 
    def ThetaFloc0(): #relies on ConcPrecipitate
        
    # The following functions will need to stay the same, remaining
    # functions and not methods:
    def ConcFloc(): #Is simply ConcPrecipitate + ConcClay(a constant)
    def NNC(): #Relies on diameter and RhoAlNanCluster
    def LambdaFloc(): #Relies on ThetaFloc0
    def Phi(): #Relies on ThetaFloc0
    def RhoFloc0(): #Relies on ThetaFloc0 and ConcFloc
    def GammaCoag(): #Relies on ThetaFloc0 and diameter
    def PCViscous(): # Relies on GammaCoag
    def RhoFloc(): #Relies on RhoFloc0
    def VelTerminal(): #Relies on RhoFloc0
    def DiamFuncVelTerminal(): #Relies on RhoFloc0
    def TimeCollisionLaminar(): #Relies on ThetaFloc0 and GammaCoag
    def TimeCollisionTurbulent(): #Relies on ThetaFloc0
    def DiamKolmogorov(): #Relies on ThetaFloc0
    def DiamV(): #Relies on ThetaFloc0
    