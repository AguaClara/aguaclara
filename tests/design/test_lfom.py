import pytest
import numpy as np

from aguaclara.design.lfom import LFOM
from aguaclara.core.units import unit_registry as u


@pytest.fixture()
def lfom():
    return LFOM(q=1*u.L/u.s, hl=30*u.cm)
    # return LFOM(q=30, hl=30)


def test_lfom(lfom):
    assert lfom.width_stout(10*u.cm).to(u.m) == 0.002405154520928927*u.m
    assert lfom.n_rows == 10
    assert lfom.b_rows.to(u.m) == 0.03*u.m
    assert lfom.vel_critical.to(u.m/u.s) == 1.0294963872061624 * u.m/u.s
    assert lfom.area_pipe_min.to(u.m**2) == 0.001457023082976217 * u.m**2
    assert lfom.nom_diam_pipe.to(u.inch) == 2 * u.inch
    assert lfom.area_top_orifice.to(u.m**2) == 4.274071743928371e-05*u.m**2
    assert lfom.d_orifice_max.to(u.m) == 0.00737693510978969 * u.m
    assert lfom.orifice_diameter.to(u.m) == 0.00635*u.m
    assert lfom.drillbit_area.to(u.m**2) == 3.1669217443593606e-05*u.m**2
    assert lfom.n_orifices_per_row_max == 10
    assert lfom.flow_ramp[5] == 0.6 * u.L/u.s
    assert lfom.flow_actual(2, [4, 3, 2]) == 0.0001962543726011661 * u.m**3/u.s
    assert lfom.n_orifices_per_row[0] == 8
    assert -0.001 < (np.average(lfom.error_per_row) - 0.005194582036259183) < 0.001
