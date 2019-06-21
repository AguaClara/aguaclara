from aguaclara.design.ent_floc import *


class Plant(Component):
    """Functions for designing an AguaClara water treatment plant."""

    def __init__(self, q=20 * u.L/u.s, temp=25 * u.degC,
                 etf = EntTankFloc()):
        """Initialize a Plant object that represents a real AguaClara water
        treatment plant.

        :param q: Flow rate of water through the plant.
        :type q: float * u.L/u.s
        :param temp: Temperature of water through the plant.
        :type q: float * u.degC
        :returns: object
        :rtype: Plant
        """
        super().__init__(q = q, temp = temp)
        self.etf = etf

        super().propogate_config([self.etf])
