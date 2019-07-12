from aguaclara.design.ent_floc import EntTankFloc
from aguaclara.design.sed import Sedimentor
from aguaclara.design.component import Component
from aguaclara.core.units import unit_registry as u

class Plant(Component):
    """Functions for designing an AguaClara water treatment plant."""
    def __init__(self, **kwargs):
        self.etf = EntTankFloc()
        self.sed = Sedimentor()

        super().__init__(subcomponents = ["etf", "sed"], **kwargs)

        

    