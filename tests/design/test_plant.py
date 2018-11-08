from aguaclara.design.plant import Plant
from aguaclara.core.units import unit_registry as u


def test_plant(utils):
    plant = Plant()
    utils.assert_unit_equality(1*(u.m**2), plant.ent_tank_a, 0.001)
