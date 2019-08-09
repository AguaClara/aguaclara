from aguaclara.design.floc import Flocculator
from aguaclara.core.units import u

import pytest

floc_20 = Flocculator(q = 20 * u.L / u.s)
floc_60 = Flocculator(q = 60 * u.L / u.s)


@pytest.mark.parametrize("actual, expected", [
    (floc_20.vel_grad_avg, 105.64226282862514 * (u.s ** -1)),
    (floc_60.vel_grad_avg, 105.64226282862514 * (u.s ** -1)),

    (floc_20.retention_time, 350.2386167174599 * u.s),
    (floc_60.retention_time, 350.2386167174599 * u.s),

    (floc_20.vol, 7.004772334349198 * u.m**3), 
    (floc_60.vol, 21.014317003047594 * u.m**3),
    
    (floc_20.chan_l, 6.0 * u.m),
    (floc_60.chan_l, 6.0 * u.m),

    (floc_20.chan_w_min_hs_ratio, 11.464163761790903 * u.cm),
    (floc_60.chan_w_min_hs_ratio, 34.392491285372714 * u.cm), 
    
    (floc_20.chan_w_min, 11.464163761790903 * u.cm),
    (floc_60.chan_w_min, 34.392491285372714 * u.cm),

    (floc_20.chan_n, 2),
    (floc_60.chan_n, 2),

    (floc_20.chan_w_min_gt, 33.35605873499618 * u.cm),
    (floc_60.chan_w_min_gt, 100.06817620498853 * u.cm),

    (floc_20.chan_w, 34 * u.cm),
    (floc_60.chan_w, 101.0 * u.cm),

    (floc_20.l_max_vol, 15.27536696068386 * u.m),
    (floc_60.l_max_vol, 15.27536696068386 * u.m),
    
    (floc_20.expansion_h_max, 1.4883329289986302 * u.m),
    (floc_60.expansion_h_max, 1.4993712841204838 * u.m), # 15

    (floc_20.expansion_n, 2),
    (floc_60.expansion_n, 2),

    (floc_20.expansion_h, 1.0 * u.m),
    (floc_60.expansion_h, 1.0 * u.m), 
    
    (floc_20.baffle_s, 28.32145341749481 * u.cm), #20 
    (floc_60.baffle_s, 28.601863847370996* u.cm),
    
    (floc_20.obstacle_n, 1),
    (floc_60.obstacle_n, 1),
    
    (floc_20.contraction_s, 16.992872050496885 * u.cm),
    (floc_60.contraction_s, 17.161118308422598 * u.cm),  # 25

    (floc_20.obstacle_pipe_od, 4.5 * u.inch),
    (floc_60.obstacle_pipe_od, 4.5 * u.inch),

    (floc_20.drain_pipe.k_minor, 2),
    (floc_60.drain_pipe.k_minor, 2),

    (floc_20.drain_pipe.id, 2.8536585365853657 * u.inch),
    (floc_60.drain_pipe.id, 3.8048780487804876 * u.inch),

    (floc_20.drain_pipe.size, 3 * u.inch),
    (floc_60.drain_pipe.size, 4 * u.inch)
])

def test_floc(actual, expected):   
    assert actual == expected
