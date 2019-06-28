from aguaclara.design.sed_tank import SedimentationTank
from aguaclara.core.units import unit_registry as u

import pytest


sed_tank_20 = SedimentationTank(q = 20.0 * u.L / u.s)
sed_tank_60 = SedimentationTank(q = 60.0 * u.L / u.s)

@pytest.mark.parametrize('actual, expected', [
	(sed_tank_20.q_tank, 1),
	(sed_tank_60.q_tank, 1),

	(sed_tank_20.diffuser_hl, 1),
	(sed_tank_60.diffuser_hl, 1),

    (sed_tank_20.diffuser_hl, 1),
    (sed_tank_60.diffuser_hl, 1),

    (sed_tank_20.diffuser_vel, 1),
	(sed_tank_60.diffuser_vel, 1),

    (sed_tank_20.diffuser_w_inner, 1),
	(sed_tank_60.diffuser_w_inner, 1),

    (sed_tank_20.diffuser_a, 1),
	(sed_tank_60.diffuser_a, 1),

    (sed_tank_20.inlet_man_v_max, 1),
	(sed_tank_60.inlet_man_v_max, 1),

    (sed_tank_20.inlet_man_nd, 1),
	(sed_tank_60.inlet_man_nd, 1),

    (sed_tank_20.q.outlet_man_nd, 1),
	(sed_tank_60.q.outlet_man_nd, 1),

    (sed_tank_20.exit_man_orifice_d, 1),
	(sed_tank_60.exit_man_orifice_d, 1),

    (sed_tank_20.plate_l, 1),
	(sed_tank_60.plate_l, 1),

    (sed_tank_20.outlet_orifice_n, 1),
	(sed_tank_60.outlet_orifice_n, 1),

    (sed_tank_20.outlet_nd, 1),
	(sed_tank_60.outlet_nd, 1),

    (sed_tank_20.outlet_major_hl, 1),
	(sed_tank_60.outlet_major_hl, 1),

    (sed_tank_20.outlet_orifice_hl, 1),
	(sed_tank_60.outlet_orifice_hl, 1),

    (sed_tank_20.outlet_hl, 1),
	(sed_tank_60.outlet_hl, 1),

    (sed_tank_20.side_slopes_w, 1),
	(sed_tank_60.side_slopes_w, 1),

    (sed_tank_20.side_slopes_h, 1),
	(sed_tank_60.side_slopes_h, 1),

    (sed_tank_20.weir_floc_z, 1),
	(sed_tank_60.weir_floc_z, 1),

    (sed_tank_20.hopper_slope_front_h, 1),
	(sed_tank_60.hopper_slope_front_h, 1),

    (sed_tank_20.hopper_pipe_drain_l, 1),
	(sed_tank_60.hopper_pipe_drain_l, 1),
])
def test_sed_tank(actual, expected):
    assert actual == expected

    
