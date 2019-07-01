from aguaclara.design.sed_chan import SedimentationChannel
from aguaclara.core.units import unit_registry as u

import pytest


sed_chan_20 = SedimentationChannel(q = 20.0 * u.L / u.s)
sed_chan_60 = SedimentationChannel(q = 60.0 * u.L / u.s)

@pytest.mark.parametrize('actual, expected', [
	(sed_chan_20.l, 1),
	(sed_chan_60.l, 1),

	(sed_chan_20.weir_exit_hl, 0.016962275713760088 * u.m),
	(sed_chan_60.weir_exit_hl, 0.035282955314338546 * u.m),

	(sed_chan_20.inlet_hl_max, 0.39087750000000016 * u.cm),
	(sed_chan_60.inlet_hl_max, 0.39087750000000016 * u.cm),

	(sed_chan_20.inlet_w_pre_weir, 41.811023622047244 * u.inch),
	(sed_chan_60.inlet_w_pre_weir, 41.811023622047244 * u.inch),

	(sed_chan_20.inlet_depth_plumbing_min, 107.90522757137602 * u.cm),
	(sed_chan_60.inlet_depth_plumbing_min, 109.73729553143386 * u.cm),

	(sed_chan_20.inlet_depth_hl, 0.08933041703807712 * u.m),
	(sed_chan_60.inlet_depth_hl, 0.22861065728970015 * u.m),

	(sed_chan_20.inlet_depth, 1),
	(sed_chan_60.inlet_depth, 1),

	(sed_chan_20.inlet_weir_hl, 1),
	(sed_chan_60.inlet_weir_hl, 1),

	(sed_chan_20.inlet_h, 1),
	(sed_chan_60.inlet_h, 1),

	(sed_chan_20.inlet_weir_h, 1),
	(sed_chan_60.inlet_weir_h, 1),
	
	(sed_chan_20.inlet_w_post_weir, 1),
	(sed_chan_60.inlet_w_post_weir, 1),

	(sed_chan_20.inlet_w, 1),
	(sed_chan_60.inlet_w, 1),

	(sed_chan_20.drain_nd, 1),
	(sed_chan_60.drain_nd, 1),

	(sed_chan_20.inlet_drain_box_w, 1),
	(sed_chan_60.inlet_drain_box_w, 1),

	(sed_chan_20.outlet_depth, 1),
	(sed_chan_60.outlet_depth, 1),

	(sed_chan_20.outlet_weir_depth, 1),
	(sed_chan_60.outlet_weir_depth, 1),

	(sed_chan_20.outlet_pre_weir_w, 1),
	(sed_chan_60.outlet_pre_weir_w, 1),

	# (sed_chan_20.outlet_post_weir_w, 1),
	# (sed_chan_60.outlet_post_weir_w, 1),

	(sed_chan_20.outlet_w, 1),
	(sed_chan_60.outlet_w, 1),

	# (sed_chan_20.outlet_drain_box_w, 1),
	# (sed_chan_60.outlet_drain_box_w, 1),

	# (sed_chan_20.outlet_weir_h, 1),
	# (sed_chan_60.outlet_weir_h, 1),

	# (sed_chan_20.w_outer, 1),
	# (sed_chan_60.w_outer, 1),

	(sed_chan_20.inlet_last_coupling_h, 1),
	(sed_chan_60.inlet_last_coupling_h, 1),

	(sed_chan_20.inlet_step_h, 1),
	(sed_chan_60.inlet_step_h, 1),

	(sed_chan_20.inlet_slope_l, 1),
	(sed_chan_60.inlet_slope_l, 1),
])
def test_sed_chan(actual, expected):
    assert actual == expected

    
