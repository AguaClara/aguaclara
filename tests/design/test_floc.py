#TODO: Add testing for obstacle_pipe_od

from aguaclara.design.floc import Flocculator
from aguaclara.core.units import unit_registry as u

import pytest


@pytest.fixture()
def floc():
    return Flocculator()

def test_vel_grad_avg(floc):
    assert floc.vel_grad_avg == 118.71480891150067 * (u.s ** -1)

def test_retention_time(floc):
    assert floc.retention_time == 311.67130991705255 * u.s

def test_vol(floc):
    assert floc.vol == 6.233426198341051 * u.m**3

def test_channel_l(floc):
    assert floc.chan_l == 4.213014554633917 * u.m

def test_w_min_hs_ratio(floc):
    assert floc.w_min_hs_ratio == 11.026896890543643 * u.cm

def test_channel_n(floc):
    assert floc.chan_n == 2

def channel_w(floc):
    assert floc.chan_w == 0.45 * u.m 

def test_expansion_h_max(floc):
    assert floc.expansion_h_max == 1.1714751817536837 * u.m

def test_expansion_n(floc):
    assert floc.expansion_n == 2

def test_expansion_h(floc):
    assert floc.expansion_h == 100.0 * u.cm

def test_baffle_s(floc):
    assert floc.baffle_s == 20.58225112209816 * u.cm

def test_obstacle_n(floc):
    assert floc.obstacle_n == 1

