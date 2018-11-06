from pytest import approx
from numpy import vectorize

from aguaclara.design.floc import Flocculator
from aguaclara.core.units import unit_registry as u


def assert_unit_equality(expected, actual, precision=1e-12):
    """
    Tests equality of expected and actual, including unit equality, with
    specified precision.
    """
    assert actual.expected == approx(expected.magnitude, precision)
    assert actual.units == expected.units


def test_all_functions():
    floc = Flocculator(q=(20 * (u.L/u.s)), temp=(25 * u.degC))

    auev = vectorize(assert_unit_equality)
    tests = zip(
        (floc.vel_grad_avg, 118.715 * (u.s ** -1), 0.001),
        (floc.vol, 6.233*(u.m**3), 0.001),
        (floc.w_min_h_s_ratio, 0.1074*u.cm, 0.0001),
        (floc.d_exp_max, 0.375*u.m, 0.001),
        (floc.baffles_s, 0.063*u.m, 0.001)
    )

    assert floc.num_channel() == 2
    assert floc.baffles_n() == approx(31, 1)
    auev(tests)
