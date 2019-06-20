from aguaclara.design.ent import EntranceTank
from aguaclara.core.units import unit_registry as u

import pytest


ent_20 = EntranceTank(20 * u.L / u.s)
ent_60 = EntranceTank(60 * u.L / u.s)

@pytest.mark.parametrize("actual, expected", [
    (ent_20.drain_od, 4.5 * u.inch),  # 0
    (ent_60.drain_od, 6.625 * u.inch),

    (ent_20.plate_n, 11),
    (ent_60.plate_n, 19),

    (ent_20.l, 28.48536407603107 * u.inch),
    (ent_60.l, 43.198341479120394 * u.inch),  # 5
])

def test_l(actual, expected):
    assert actual == expected
    
