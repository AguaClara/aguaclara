from aguaclara.design.ent_floc import *


class Plant(Component):
    """Functions for designing an AguaClara water treatment plant."""

    q=20 * u.L/u.s
    temp=25 * u.degC
    etf = EntTankFloc()
    subcomponents = [etf]
    """Initialize a Plant object that represents a real AguaClara water
    treatment plant.

    :param q: Flow rate of water through the plant.
    :type q: float * u.L/u.s
    :param temp: Temperature of water through the plant.
    :type q: float * u.degC
    :returns: object
    :rtype: Plant
    """