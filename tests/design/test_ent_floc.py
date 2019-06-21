from aguaclara.design.ent_floc import EntTankFloc
from aguaclara.core.units import unit_registry as u

import pytest

etf_20 = EntTankFloc()
etf_60 = EntTankFloc(q = 60.0 * u.L / u.s)

@pytest.mark.parametrize('actual, expected', [
    (etf_20.ent.l, 37.6732811402825 * u.inch),
	(etf_60.ent.l, 59.439445209113174 * u.inch),

	(etf_20.floc.chan_w, 0.45 * u.m),
    (etf_60.floc.chan_w, 0.4377982708968249 * u.m)
])
def test_etf(actual, expected):
    assert actual == expected