from aguaclara.design.sed import Sedimentor
from aguaclara.core.units import u

import pytest


sed_20 = Sedimentor(q=20.0 * u.L / u.s)
sed_60 = Sedimentor(q=60.0 * u.L / u.s)


@pytest.mark.parametrize(
    "actual, expected",
    [
        (sed_20.tank_n, 4),
        (sed_60.tank_n, 10),
    ],
)
def test_sed(actual, expected):
    assert actual == expected
