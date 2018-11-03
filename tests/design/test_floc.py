from pytest import approx

from aguaclara.design.floc import Flocculator
from aguaclara.core.units import unit_registry as u


def test_all_functions():
    floc = Flocculator(q=(20 * (u.L/u.s)), temp=(25 * u.degC))
    assert floc.vel_gradient_avg() == approx(118.715 / u.s, 0.001)
    assert floc.vol() == approx(6.233 * (u.m**3), 0.001)
    assert floc.w_min_h_s_ratio() == approx(0.1074 * u.cm, 0.0001)
    assert floc.w_min() == approx(45 * u.cm, 1)
    assert floc.num_channel() == 2
    assert floc.d_exp_max() == approx(0.375 * u.m, 0.001)
    assert floc.baffles_s() == approx(0.063 * u.m, 0.001)
    assert floc.baffles_n() == approx(31, 1)
