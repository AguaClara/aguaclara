from aguaclara.design.ent_floc import EntTankFloc
from aguaclara.design.sed import Sedimentor
from aguaclara.design.component import Component
from aguaclara.core.units import unit_registry as u

class Plant(Component):
    """Functions for designing an AguaClara water treatment plant."""

    q=20 * u.L/u.s
    temp=25 * u.degC
    etf = EntTankFloc()
    sed = Sedimentor()
    subcomponents = [etf, sed]
    