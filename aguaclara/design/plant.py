from aguaclara.core.units import unit_registry as u
from aguaclara.design.floc import Flocculator


class Plant:
    def __init__(self, q=20*u.L/u.s, temp=25*u.degC):
        """Initializes AguaClara plant parametrically given temp/flow rate

        :param q: flow rate
        :param temp: temperature
        """
        self.q = q
        self.temp = temp
        self.floc = Flocculator(q=q, temp=temp)

    @property
    def ent_tank_a(self):
        """Return the planview area of the entrance tank.

        Examples
        --------
        area_ent_tank(20*u.L/u.s, 40*u.cm, 37000, 25*u.degC, 2*u.m)
        1 meter ** 2
        """
        # first guess planview area
        a_new = 1 * u.m**2
        a_ratio = 0
        tolerance = 0.01
        while a_ratio > (1 + tolerance):
            a_et_pv = a_new
            a_floc_pv = (
                self.floc.vol() /
                (self.floc.END_WATER_HEIGHT + (self.floc.HL / 2))
            )
            a_etf_pv = a_et_pv + a_floc_pv

            w_tot = a_etf_pv / self.floc.l_sed_max
            w_chan = w_tot / self.floc.num_channel()

            a_new = self.floc.L_MAX * w_chan
            a_ratio = a_new / a_et_pv
        return a_new
