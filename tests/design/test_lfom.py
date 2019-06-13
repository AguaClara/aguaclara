from aguaclara.design.lfom import LFOM
from aguaclara.core.units import unit_registry as u

import pytest
import numpy as np

lfom_20 = LFOM(20.0 * u.L / u.s)
lfom_60 = LFOM(60.0 * u.L / u.s)


@pytest.mark.parametrize('actual, expected', [
    (lfom_20.stout_w_per_flow(10 * u.cm) , 3.6077317813933907 * u.s / u.m ** 2),  # 0
    (lfom_60.stout_w_per_flow(10 * u.cm) , 3.6077317813933907 * u.s / u.m ** 2),

    (lfom_20.n_rows, 6),
    (lfom_60.n_rows, 4),

    (lfom_20.b_rows.to(u.m), 0.03333333333333333 * u.m),
    (lfom_60.b_rows.to(u.m), 0.05 * u.m),  # 5
    
    (lfom_20.vel_critical.to(u.m/u.s), 0.8405802802312778 * u.m/u.s),
    (lfom_60.vel_critical.to(u.m/u.s), 0.8405802802312778 * u.m/u.s),

    (lfom_20.area_pipe_min.to(u.m**2), 0.035689630967485675 * u.m**2),
    (lfom_60.area_pipe_min.to(u.m**2), 0.10706889290245702 * u.m**2),

    (lfom_20.nom_diam_pipe.to(u.inch), 10.0 * u.inch),  # 10
    (lfom_60.nom_diam_pipe.to(u.inch), 16.0 * u.inch),
    
    (lfom_20.area_top_orifice.to(u.m**2), 0.0017763243361009463 * u.m ** 2),
    (lfom_60.area_top_orifice.to(u.m**2), 0.00818156664907796 * u.m ** 2),

    (lfom_20.d_orifice_max.to(u.m), 0.047557190718114956 * u.m),
    (lfom_60.d_orifice_max.to(u.m), 0.10206416704942245 * u.m),  # 15
    
    (lfom_20.orifice_diameter.to(u.m), 0.03175 * u.m),
    (lfom_60.orifice_diameter.to(u.m), 0.044449999999999996 * u.m),

    (lfom_20.drillbit_area.to(u.m**2), 0.0007917304360898403 * u.m ** 2),
    (lfom_60.drillbit_area.to(u.m**2), 0.0015517916547360866 * u.m ** 2),

    (lfom_20.n_orifices_per_row_max, 21),  # 20
    (lfom_60.n_orifices_per_row_max, 23),

    (lfom_20.flow_ramp[5], 20.0 * u.L/u.s),
    (lfom_60.flow_ramp[3], 60.0 * u.L/u.s),

    (lfom_20.flow_actual(2, [4, 3, 2]), 0.004614633640055867 * u.m ** 3 / u.s),
    (lfom_60.flow_actual(2, [4, 3, 2]), 0.011208187699888418 * u.m ** 3 / u.s),  # 25

    (lfom_20.n_orifices_per_row[0], 12),
    (lfom_60.n_orifices_per_row[0], 21)
])
def test_lfom(actual, expected):
    assert actual == expected

def test_error_per_row():
    assert -0.01 < (np.average(lfom_20.error_per_row) - 0.005194582036259183) < 0.01
    assert -0.01 < (np.average(lfom_60.error_per_row) - 0.005194582036259183) < 0.01
