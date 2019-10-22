from aguaclara.design.filter import Filter
from aguaclara.core.units import u

import pytest

filter_20 = Filter(q = 20.0 * u.L / u.s)
filter_60 = Filter(q = 60.0 * u.L / u.s)


@pytest.mark.parametrize("actual, expected", [
	(filter_20.vel, 0),
	(filter_60.vel, 0),
  
	(filter_20.k_e, 0),
	(filter_60.k_e, 0),

	(filter_20.trunk_max_hl, 0),
	(filter_60.trunk_max_hl, 0),

	(filter_20.max_q, 0),
	(filter_60.max_q, 0),

	(filter_20.ratio_trunk_sand_hl, 0),
	(filter_60.ratio_trunk_sand_hl, 0),

	(filter_20.backwash_hl, 0),
	(filter_60.backwash_hl, 0),

	(filter_20.drain_d, 0),
	(filter_60.drain_d, 0)
	])

def test_floc(actual, expected):   
    assert actual == expected
