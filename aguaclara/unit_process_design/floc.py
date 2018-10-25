"""This file contains all the functions needed to design a flocculator for
an AguaClara plant.

"""
from aguaclara.design.floc import baffle_spacing
from aguaclara.play import*

# expansion minor loss coefficient for 180 degree bend


### Baffle calculations

baffle_spacing(20 * u.L / u.s, 40 * u.cm, 37000, 25 * u.degC, 2 * u.m)

