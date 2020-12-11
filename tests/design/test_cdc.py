from aguaclara.design.cdc import CDC
from aguaclara.core.units import u

import pytest


cdc_20 = CDC(q = 20.0 * u.L / u.s)
cdc_60 = CDC(q = 60.0 * u.L / u.s)

@pytest.mark.parametrize('actual, expected', [
    (cdc_20.alum_nu(2 * u.g / u.L), 1.00357603e-06 * u.m**2 / u.s),
	(cdc_60.alum_nu(2 * u.g / u.L), 1.00357603e-06 * u.m**2 / u.s),

	(cdc_20.pacl_nu(2 * u.g / u.L), 1.00364398e-06 * u.m**2 / u.s),
	(cdc_60.pacl_nu(2 * u.g / u.L), 1.00364398e-06 * u.m**2 / u.s),

	(cdc_20.coag_nu(2 * u.g / u.L, "alum"), 1.00357603e-06 * u.m**2 / u.s),
	(cdc_20.coag_nu(2 * u.g / u.L, "PACl"), 1.00364398e-06 * u.m**2 / u.s)
])

def test_cdc(actual, expected):
	if (type(actual) == u.Quantity and type(expected) == u.Quantity):
		assert actual.units == expected.units
		assert actual.magnitude == pytest.approx(expected.magnitude)
	else:
		assert actual == pytest.approx(expected)
