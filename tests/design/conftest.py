import pytest
from numpy import vectorize


class Utils:
    @staticmethod
    def assert_unit_equality(expected, actual, precision=1e-12):
        """
        Tests equality of expected and actual, including unit equality, with
        specified precision.
        """
        converted = actual.to(expected.units)
        assert converted.magnitude == (
            pytest.approx(expected.magnitude, precision)
        )

    # vectorized version of assert_unit_equality
    vaue = vectorize(assert_unit_equality)


@pytest.fixture
def utils():
    return Utils
