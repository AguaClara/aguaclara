from aguaclara.core.units import unit_registry as u
from aguaclara.design.floc import Flocculator


class Plant:
    """Functions for designing an AguaClara water treatment plant."""

    def __init__(self, q=20 * u.L/u.s, temp=25 * u.degC):
        """Initialize a Plant object that represents a real AguaClara water
        treatment plant.

        :param q: Flow rate of water through the plant.
        :type q: float * u.L/u.s
        :param temp: Temperature of water through the plant.
        :type q: float * u.degC
        :returns: object
        :rtype: Plant
        """
        self.q = q
        self.temp = temp
        self.floc = Flocculator(Q=q, temp=temp)

    @property
    def ent_tank_a(self):
        """Calculate the planview area of the entrance tank, given the volume of
        the flocculator.

        :returns: The planview area of the entrance tank.
        :rtype: float * u.m ** 2
        """
        # first guess planview area
        a_new = 1 * u.m**2
        a_ratio = 2  # set to >1+tolerance to start while loop
        tolerance = 0.01
        a_floc_pv = (
            self.floc.vol /
            (self.floc.downstream_H + (self.floc.HL / 2))
        )
        while a_ratio > (1 + tolerance):
            a_et_pv = a_new
            a_etf_pv = a_et_pv + a_floc_pv
            w_tot = a_etf_pv / self.floc.max_L
            w_chan = w_tot / self.floc.channel_n

            a_new = self.floc.max_L * w_chan
            a_ratio = a_new / a_et_pv
        return a_new
