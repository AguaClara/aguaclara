from aguaclara.design.ent import EntranceTank
from aguaclara.core.units import u

import pytest


ent_20 = EntranceTank(q = 20.0 * u.L / u.s)
ent_60 = EntranceTank(q = 60.0 * u.L / u.s)

@pytest.mark.parametrize("actual, expected", [
    (ent_20.drain_pipe.od, 4.5 * u.inch),  # 0
    (ent_60.drain_pipe.od, 8.625 * u.inch),

    (ent_20.plate_n, 11),
    (ent_60.plate_n, 19),

    (ent_20.l, 28.48536407603107 * u.inch),
    (ent_60.l, 45.198341479120394 * u.inch),  # 5
])

def test_ent(actual, expected):
    assert actual == expected
    
