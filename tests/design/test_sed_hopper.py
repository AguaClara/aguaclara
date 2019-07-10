from aguaclara.design.sed_hopper import SedTankHopper
from aguaclara.core.units import unit_registry as u

import pytest


sed_hopper_20 = SedTankHopper(q = 20.0 * u.L / u.s)
sed_hopper_60 = SedTankHopper(q = 60.0 * u.L / u.s)

@pytest.mark.parametrize('actual, expected', [
	(sed_hopper_20.l_outer, 50.0 * u.cm),
	(sed_hopper_60.l_outer, 50.0 * u.cm),

	(sed_hopper_20.floc_weir_h, 0.64 * u.m),
	(sed_hopper_60.floc_weir_h, 0.64 * u.m),

	(sed_hopper_20.bottom_h_above_jet_reverser, 50.6 * u.cm),
	(sed_hopper_60.bottom_h_above_jet_reverser, 50.6 * u.cm),

	(sed_hopper_20.slope_h, 0.134 * u.m),
	(sed_hopper_60.slope_h, 0.134 * u.m),

	(sed_hopper_20.slope_front_back_angle, 1.1983978801181423 * u.radian),
	(sed_hopper_60.slope_front_back_angle, 1.1983978801181423 * u.radian),

	(sed_hopper_20.slope_vertical_angle, 1),
	(sed_hopper_60.slope_vertical_angle, 1),

    (sed_hopper_20.slope_l, 1),
    (sed_hopper_60.slope_l, 1),

    (sed_hopper_20.pipe_drain_l, 0.4127 * u.m),
    (sed_hopper_60.pipe_drain_l, 0.4127 * u.m)
])
def test_sed_hopper(actual, expected):
    assert actual == expected