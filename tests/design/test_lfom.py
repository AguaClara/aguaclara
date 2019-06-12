from aguaclara.design.lfom import LFOM
from aguaclara.core.units import unit_registry as u

import pytest


@pytest.fixture()
def lfom():
    return LFOM(
        q = 1 * u.L / u.s,
        hl = 30 * u.cm
    )

def test_stout_w_per_flow(lfom):
    assert lfom.stout_w_per_flow(10 * u.cm) ==
           2.4051545209289267 * u.s / u.m ** 2

def test_n_rows(lfom):
    assert lfom.n_rows == 10

def test_b_rows(lfom):
    assert lfom.b_rows.to(u.m) == 0.03*u.m

def test_vel_critical(lfom):
    assert lfom.vel_critical.to(u.m/u.s) == 1.0294963872061624 * u.m/u.s

def test_area_pipe_min(lfom):
    assert lfom.area_pipe_min.to(u.m**2) == 0.001457023082976217 * u.m**2

def test_nom_diam_pipe(lfom):
    assert lfom.nom_diam_pipe.to(u.inch) == 2 * u.inch

def test_area_top_orifice(lfom):
    assert lfom.area_top_orifice.to(u.m**2) == 4.274071743928371e-05*u.m**2

def test_d_orifice_max(lfom):
    assert lfom.d_orifice_max.to(u.m) == 0.00737693510978969 * u.m

def test_orifice_diameter(lfom):
    assert lfom.orifice_diameter.to(u.m) == 0.00635*u.m

def test_drillbit_area(lfom):
    assert lfom.drillbit_area.to(u.m**2) == 3.1669217443593606e-05*u.m**2.

def test_n_orifices_per_row_max(lfom):
    assert lfom.n_orifices_per_row_max == 15

def test_flow_ramp(lfom):
    assert lfom.flow_ramp[5] == 0.6 * u.L/u.s

def test_flow_actual(lfom):
    assert lfom.flow_actual(2, [4, 3, 2]) == 0.0001962543726011661 * u.m**3/u.s

def test_n_orifices_per_row(lfom):
    assert lfom.n_orifices_per_row[0] == 7

def test_error_per_row(lfom):
    assert -0.01 < (np.average(lfom.error_per_row) - 0.005194582036259183) < 0.01
