from aguaclara.design.floc import Flocculator
from aguaclara.core.units import unit_registry as u

import pytest

floc_20 = Flocculator()
floc_60 = Flocculator(q = 60 * u.L / u.s)
# @pytest.fixture()
# def floc_20():
#     return Flocculator()

# @pytest.fixture()
# def floc_60():
#     return Flocculator(q = 60 * u.L / u.s)
@pytest.mark.parametrize("actual, expected", [
    (floc_20.vel_grad_avg, 105.64226282862514 * (u.s ** -1)), # 0
    (floc_60.vel_grad_avg, 105.64226282862514 * (u.s ** -1)),

    (floc_20.retention_time, 350.2386167174599 * u.s),
    (floc_60.retention_time, 350.2386167174599 * u.s),

    (floc_20.vol, 7.004772334349198 * u.m**3), 
    (floc_60.vol, 21.014317003047594 * u.m**3),   # 5
    
    (floc_20.chan_l, 4.641540185749554 * u.m),
    (floc_60.chan_l, 6.000000000000001 * u.m),

    (floc_20.w_min_hs_ratio, 11.464163761790903 * u.cm),
    (floc_60.w_min_hs_ratio, 34.392491285372714 * u.cm), 
    
    (floc_20.chan_n, 2), # 10
    (floc_60.chan_n, 2),

    (floc_20.chan_w, 0.45 * u.m),
    (floc_60.chan_w, 0.45 * u.m),

    (floc_20.expansion_h_max, 1.206146033516045 * u.m),
    (floc_60.expansion_h_max, 1.509830627242024 * u.m), # 15

    (floc_20.expansion_n, 2),
    (floc_60.expansion_n, 2),

    (floc_20.expansion_h, 100.0 * u.cm),
    (floc_60.expansion_h, 100.0 * u.cm), 
    
    (floc_20.baffle_s, 21.398431470996076 * u.cm), #20 
    (floc_60.baffle_s, 28.8682012417896 * u.cm),
    
    (floc_20.obstacle_n, 1),
    (floc_60.obstacle_n, 1)
])
def test_floc(actual, expected):
    # assert floc_20.vel_grad_avg == 105.64226282862514 * (u.s ** -1)
    # assert floc_60.vel_grad_avg == 105.64226282862514 * (u.s ** -1)    
    assert actual == expected

# def test_retention_time(floc_20, floc_60):
#     assert floc_20.retention_time == 350.2386167174599 * u.s
#     assert floc_60.retention_time == 350.2386167174599 * u.s

# def test_vol(floc_20, floc_60):
#     assert floc_20.vol == 7.004772334349198 * u.m**3
#     assert floc_60.vol == 21.014317003047594 * u.m**3

# def test_channel_l(floc_20, floc_60):
#     assert floc_20.chan_l == 4.641540185749554 * u.m
#     assert floc_60.chan_l == 6.000000000000001 * u.m

# def test_w_min_hs_ratio(floc_20, floc_60):
#     assert floc_20.w_min_hs_ratio == 11.464163761790903 * u.cm
#     # assert floc_60.w_min_hs_ratio == 34.392491285372714 * u.cm

# def test_channel_n(floc_20, floc_60):
#     assert floc_20.chan_n == 2
#     assert floc_60.chan_n == 2

# def channel_w(floc_20, floc_60):
#     assert floc_20.chan_w == 0.45 * u.m 
#     assert floc_60.chan_w == 0.45 * u.m 

# def test_expansion_h_max(floc_20, floc_60):
#     assert floc_20.expansion_h_max == 1.206146033516045 * u.m
#     assert floc_60.expansion_h_max == 1.509830627242024 * u.m

# def test_expansion_n(floc_20, floc_60):
#     assert floc_20.expansion_n == 2
#     assert floc_60.expansion_n == 2

# def test_expansion_h(floc_20, floc_60):
#     assert floc_20.expansion_h == 100.0 * u.cm
#     assert floc_60.expansion_h == 100.0 * u.cm

# def test_baffle_s(floc_20, floc_60):
#     assert floc_20.baffle_s == 21.398431470996076 * u.cm
#     assert floc_60.baffle_s == 28.8682012417896 * u.cm

# def test_obstacle_n(floc_20, floc_60):
#     assert floc_20.obstacle_n == 1
#     assert floc_60.obstacle_n == 1
