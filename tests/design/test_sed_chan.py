from aguaclara.design.sed_chan import SedimentationChannel
from aguaclara.core.units import unit_registry as u

import pytest


sed_chan_20 = SedimentationChannel(q = 20.0 * u.L / u.s)
sed_chan_60 = SedimentationChannel(q = 60.0 * u.L / u.s)

@pytest.mark.parametrize('actual, expected', [
	(sed_chan_20.l, 1),
	(sed_chan_60.l, 1),

	(sed_chan_20.weir_exit_hl, 1),
	(sed_chan_60.weir_exit_hl, 1),

	(sed_chan_20.inlet_w_pre_weir, 1),
	(sed_chan_60.inlet_w_pre_weir, 1),

	(sed_chan_20.inlet_depth_plumbing_min, 1),
	(sed_chan_60.inlet_depth_plumbing_min, 1),

	
])
def test_sed_chan(actual, expected):
    assert actual == expected

    
