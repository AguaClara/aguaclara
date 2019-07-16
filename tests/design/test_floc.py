from aguaclara.design.floc import Flocculator
from aguaclara.core.units import u

import pytest

floc_20 = Flocculator(q = 20 * u.L / u.s)
floc_60 = Flocculator(q = 60 * u.L / u.s)


@pytest.mark.parametrize("actual, expected", [
    (floc_20.vel_grad_avg, 105.64226282862514 * (u.s ** -1)), # 0
    (floc_60.vel_grad_avg, 105.64226282862514 * (u.s ** -1)),

    (floc_20.retention_time, 350.2386167174599 * u.s),
    (floc_60.retention_time, 350.2386167174599 * u.s),

    (floc_20.vol, 7.004772334349198 * u.m**3), 
    (floc_60.vol, 21.014317003047594 * u.m**3),   # 5
    
    (floc_20.chan_l, 3.8915401857495544 * u.m),
    (floc_60.chan_l, 6.0 * u.m),

    (floc_20.w_min_hs_ratio, 11.464163761790903 * u.cm),
    (floc_60.w_min_hs_ratio, 34.392491285372714 * u.cm), 
    
    (floc_20.chan_n, 2), # 10
    (floc_60.chan_n, 4),

    (floc_20.chan_w, 0.45 * u.m),
    (floc_60.chan_w, 0.4377982708968249 * u.m),

    (floc_20.expansion_h_max, 1.206146033516045 * u.m),
    (floc_60.expansion_h_max, 2.806691554748962 * u.m), # 15

    (floc_20.expansion_n, 2),
    (floc_60.expansion_n, 1),

    (floc_20.expansion_h, 1.0 * u.m),
    (floc_60.expansion_h, 2.0 * u.m), 
    
    (floc_20.baffle_s, 21.398431470996076 * u.cm), #20 
    (floc_60.baffle_s, 52.37190059388171 * u.cm),
    
    (floc_20.obstacle_n, 1),
    (floc_60.obstacle_n, 0),
    
    (floc_20.contraction_s, 12.839058882597646 * u.cm),
    (floc_60.contraction_s, 31.423140356329025 * u.cm),  # 25

    (floc_20.obstacle_pipe_od, 3.5 * u.inch),
    (floc_60.obstacle_pipe_od, 6.625 * u.inch)
])

def test_floc(actual, expected):   
    assert actual == expected
