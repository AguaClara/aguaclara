from aguaclara.design.component import Component

from aguaclara.design.ent_floc import EntTankFloc
from aguaclara.design.floc import Flocculator
from aguaclara.design.ent import EntranceTank
from aguaclara.design.lfom import LFOM

from aguaclara.design.sed import Sedimentor
from aguaclara.design.sed_tank import SedimentationTank
from aguaclara.design.sed_chan import SedimentationChannel

from aguaclara.core.units import u


class Plant(Component):
    """Functions for designing an AguaClara water treatment plant."""
    def __init__(self, **kwargs):
        self.etf = EntTankFloc()
        self.sed = Sedimentor()
        self.subcomponents = [self.etf, self.sed]

        super().__init__(**kwargs)
        super().set_subcomponents()

        self.design_floc()

    def design_floc(self):
        self.etf.floc.sed_chan_inlet_w_pre_weir = self.sed.chan.inlet_w_pre_weir