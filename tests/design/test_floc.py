from pytest import approx

from aguaclara.design.floc import Flocculator
from aguaclara.core.units import unit_registry as u


def test_all_functions():
    floc = Flocculator(q=(20 * (u.L/u.s)), temp=(25 * u.degC))
    assert floc.vel_gradient_avg == approx(118.715 / u.s, 0.001)
    assert floc.vol == approx(6.233 * (u.m**3), 0.001)
