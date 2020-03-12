from aguaclara.design.filter import Filter
from aguaclara.core.units import u

import pytest

filter_20 = Filter(q = 20.0 * u.L / u.s)
filter_60 = Filter(q = 60.0 * u.L / u.s)


@pytest.mark.parametrize("actual, expected", [
	(filter_20.vel, 1.8333333333333333 * u.mm/u.s),
	(filter_60.vel, 1.8333333333333333 * u.mm/u.s),
  
	(filter_20.k_e, 3.2),
	(filter_60.k_e, 3.2),

	(filter_20.trunk_max_hl, 0.46802305239318925 * u.m),
	(filter_60.trunk_max_hl, 0.46802305239318925 * u.m),

	(filter_20.max_q, 140.67589670953868 * u.L / u.s),
	(filter_60.max_q, 140.67589670953868 * u.L / u.s),

	(filter_60.ratio_trunk_sand_hl, 0.07142857142857145),
	(filter_20.ratio_trunk_sand_hl, 0.07142857142857145),

	(filter_20.backwash_hl, 19.857343217792028 * u.cm),
	(filter_60.backwash_hl, 19.857343217792028 * u.cm),

	(filter_20.drain_d, 0.220199716489207 * u.m),
	(filter_60.drain_d, 0.220199716489207 * u.m)
	])

def test_filter(actual, expected):   
    assert actual == expected
