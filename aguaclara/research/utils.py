"""
General purpose utility library..
"""

import math


class Constants(object):
    """
    Constants.
    """

    class Earth(object):
        """
        Earth constants.
        """
        GRAVITY = 9.80665

    class Mars(object):
        """
        Mars constants.
        """
        GRAVITY = 9


def orbital_speed(planet, planatary_radius, altitude):
    """
    Calculate the orbital speed of an object.

    v = R*sqrt(g/(R+h))

    >>> from math import *
    >>> round(orbital_speed(Constants.Earth, 600000, 70), 3)
    2425.552
    """
    total_altitude = planatary_radius + altitude
    speed = planatary_radius * \
        math.sqrt(planet.GRAVITY / total_altitude)
    return speed


def circumference(radius):
    """
    Calculate the circumference of an object.

    2*pi*r

    >>> from math import *
    >>> round(circumference(600000), 3)
    3769911.184
    """
    distance = 2 * math.pi * radius

    return distance


def orbital_period(planet, planatary_radius, altitude):
    """
    Calculate the orbital period of an object.

    d = v*t

    >>> from math import *
    >>> round(orbital_period(Constants.Earth, 600000, 70), 3)
    1554.43
    """
    cir = circumference(planatary_radius + altitude)

    return cir / orbital_speed(planet, planatary_radius, altitude)
