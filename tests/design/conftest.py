import pytest
from aguaclara.design.lfom import LFOM
from aguaclara.core.units import unit_registry as u



@pytest.fixture()
def lfom():
    return LFOM(q=30*u.L/u.s, hl=30*u.cm)
    # return LFOM(q=30, hl=30)