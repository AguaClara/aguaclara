from aguaclara.design.sed import Sedimentor
from aguaclara.core.units import unit_registry as u

import pytest


sed_20 = Sedimentor(q = 20.0 * u.L / u.s)
sed_60 = Sedimentor(q = 60.0 * u.L / u.s)

@pytest.mark.parametrize('actual, expected', [
	(sed_20.tank_n, 4),
	(sed_60.tank_n, 10),

	(sed_20.hopper_l, 50 * u.cm),
	(sed_60.hopper_l, 50 * u.cm)
])
def test_sed(actual, expected):
    assert actual == expected

    
