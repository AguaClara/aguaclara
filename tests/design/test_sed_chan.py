from aguaclara.design.sed_chan import SedimentationChannel
from aguaclara.core.units import unit_registry as u

import pytest


sed_chan_20 = SedimentationChannel(q = 20.0 * u.L / u.s)
sed_chan_60 = SedimentationChannel(q = 60.0 * u.L / u.s)

@pytest.mark.parametrize('actual, expected', [
	(sed_chan_20.l, 4.8671999999999995 * u.m),
	(sed_chan_60.l, 4.8671999999999995 * u.m),

	(sed_chan_20.outlet_weir_hl, 0.016962275713760088 * u.m),
	(sed_chan_60.outlet_weir_hl, 0.035282955314338546 * u.m),

	(sed_chan_20.inlet_hl_max, 0.39087750000000016 * u.cm),
	(sed_chan_60.inlet_hl_max, 0.39087750000000016 * u.cm),

	(sed_chan_20.inlet_w_pre_weir, 41.811023622047244 * u.inch),
	(sed_chan_60.inlet_w_pre_weir, 41.811023622047244 * u.inch),

	(sed_chan_20.inlet_depth, 96.90522757137602 * u.cm),
	(sed_chan_60.inlet_depth, 98.73729553143386 * u.cm),

	(sed_chan_20.inlet_weir_hl, 0.016962275713760088 * u.m),
	(sed_chan_60.inlet_weir_hl, 0.035282955314338546 * u.m),

	(sed_chan_20.inlet_h, 101.90522757137602 * u.cm),
	(sed_chan_60.inlet_h, 103.73729553143386 * u.cm),

	(sed_chan_20.inlet_weir_h, 98.90522757137602 * u.cm),
	(sed_chan_60.inlet_weir_h, 100.73729553143386 * u.cm),
	
	(sed_chan_20.inlet_w_post_weir, 30. * u.cm),
	(sed_chan_60.inlet_w_post_weir, 30. * u.cm),

	(sed_chan_20.inlet_w, 59.52755905511811 * u.inch),
	(sed_chan_60.inlet_w, 59.52755905511811 * u.inch),

	(sed_chan_20.drain_nd, 4.0 * u.inch),
	(sed_chan_60.drain_nd, 6.0 * u.inch),

	(sed_chan_20.inlet_drain_box_w, 46.8275 * u.cm),
	(sed_chan_60.inlet_drain_box_w, 51.9075 * u.cm),

	(sed_chan_20.outlet_depth, 92.89622757137602 * u.cm),
	(sed_chan_60.outlet_depth, 94.72829553143386 * u.cm),

	(sed_chan_20.outlet_weir_depth, 85.89622757137602 * u.cm),
	(sed_chan_60.outlet_weir_depth, 87.72829553143386 * u.cm),

	(sed_chan_20.outlet_w_pre_weir, 30.0 * u.cm),
	(sed_chan_60.outlet_w_pre_weir, 30.0 * u.cm),

    (sed_chan_20.outlet_pipe_l, 3.7119999999999997 * u.m),
	(sed_chan_60.outlet_pipe_l, 3.7119999999999997 * u.m),
    
    (sed_chan_20.outlet_pipe_q_max, 7.857105273561186 * u.L / u.s),
	(sed_chan_60.outlet_pipe_q_max, 7.857105273561186 * u.L / u.s),

	(sed_chan_20.outlet_pipe_n, 3),
	(sed_chan_60.outlet_pipe_n, 8),

	(sed_chan_20.outlet_pipe_q, 6.666666666666667 * u.L / u.s),
	(sed_chan_60.outlet_pipe_q, 7.5 * u.L / u.s),

	(sed_chan_20.outlet_pipe_nd, 8 * u.inch),
	(sed_chan_60.outlet_pipe_nd, 8 * u.inch),

	(sed_chan_20.outlet_post_weir_w, 42.305 * u.cm),
	(sed_chan_60.outlet_post_weir_w, 42.305 * u.cm),

	(sed_chan_20.outlet_w, 87.305 * u.cm),
	(sed_chan_60.outlet_w, 87.305 * u.cm),

	(sed_chan_20.outlet_drain_box_w, 42.305 * u.cm),
	(sed_chan_60.outlet_drain_box_w, 42.305 * u.cm),

	(sed_chan_20.outlet_weir_h, 87.89622757137602 * u.cm),
	(sed_chan_60.outlet_weir_h, 89.72829553143386 * u.cm),

	(sed_chan_20.w_outer, 283.505 * u.cm),
	(sed_chan_60.w_outer, 283.505 * u.cm),

	(sed_chan_20.inlet_last_coupling_h, 83.89622757137602 * u.cm),
	(sed_chan_60.inlet_last_coupling_h, 85.72829553143386 * u.cm),

	(sed_chan_20.inlet_step_h, 27.965409190458672 * u.cm),
	(sed_chan_60.inlet_step_h, 28.57609851047795 * u.cm),

	(sed_chan_20.inlet_slope_l, 4.1052 * u.m),
	(sed_chan_60.inlet_slope_l, 4.1052 * u.m),
])
def test_sed_chan(actual, expected):
    # TODO: switch to @ut.optional_units() once available
    actual *= u.dimensionless
    expected *= u.dimensionless
    assert actual.to(expected.units).magnitude == pytest.approx(expected.magnitude)
