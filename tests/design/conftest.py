import pytest
from numpy import vectorize


class Utils:
    @staticmethod
    def assert_unit_equality(expected, actual, precision=1e-12):
        """
        Tests equality of expected and actual, including unit equality, with
        specified precision.
        """
        assert actual.magnitude == pytest.approx(expected.magnitude, precision)
        assert actual.units == expected.units

    # vectorized version of assert_unit_equality
    vaue = vectorize(assert_unit_equality)


@pytest.fixture
def utils():
    return Utils
