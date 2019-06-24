from aguaclara.design.lfom import LFOM
from aguaclara.core.units import unit_registry as u

import pytest
import numpy as np

lfom_20 = LFOM(20.0 * u.L / u.s)
lfom_60 = LFOM(60.0 * u.L / u.s)


@pytest.mark.parametrize('actual, expected', [
    (lfom_20.stout_w_per_flow(10 * u.cm) , 3.6077317813933907 * u.s / u.m ** 2),  # 0
    (lfom_60.stout_w_per_flow(10 * u.cm) , 3.6077317813933907 * u.s / u.m ** 2),

    (lfom_20.row_n, 6),
    (lfom_60.row_n, 4),

    (lfom_20.row_b.to(u.m), 0.03333333333333333 * u.m),
    (lfom_60.row_b.to(u.m), 0.05 * u.m),  # 5
    
    (lfom_20.vel_critical.to(u.m/u.s), 0.8405802802312778 * u.m/u.s),
    (lfom_60.vel_critical.to(u.m/u.s), 0.8405802802312778 * u.m/u.s),

    (lfom_20.pipe_a_min.to(u.m**2), 0.035689630967485675 * u.m**2),
    (lfom_60.pipe_a_min.to(u.m**2), 0.10706889290245702 * u.m**2),

    (lfom_20.pipe_nd.to(u.inch), 10.0 * u.inch),  # 10
    (lfom_60.pipe_nd.to(u.inch), 16.0 * u.inch),
    
    (lfom_20.top_row_orifice_a.to(u.m**2), 0.0017763243361009463 * u.m ** 2),
    (lfom_60.top_row_orifice_a.to(u.m**2), 0.00818156664907796 * u.m ** 2),

    (lfom_20.orifice_d_max.to(u.m), 0.047557190718114956 * u.m),
    (lfom_60.orifice_d_max.to(u.m), 0.10206416704942245 * u.m),  # 15
    
    (lfom_20.orifice_d.to(u.m), 0.03175 * u.m),
    (lfom_60.orifice_d.to(u.m), 0.044449999999999996 * u.m),

    (lfom_20.drill_bit_a.to(u.m**2), 0.0007917304360898403 * u.m ** 2),
    (lfom_60.drill_bit_a.to(u.m**2), 0.0015517916547360866 * u.m ** 2),

    (lfom_20.orifice_n_max_per_row, 21),  # 20
    (lfom_60.orifice_n_max_per_row, 23),

    (lfom_20.q_per_row[5], 20.0 * u.L / u.s),
    (lfom_60.q_per_row[3], 60.0 * u.L / u.s),

    (lfom_20.q_submerged(3, [4, 3, 2]), 5.939085475350429 * u.L / u.s),
    (lfom_60.q_submerged(3, [4, 3, 2]), 14.34566338987966 * u.L / u.s),  # 25
    
    (lfom_20.orifice_n_per_row[0], 12),
    (lfom_60.orifice_n_per_row[0], 21)
])
def test_lfom(actual, expected):
    assert actual == expected

def test_error_per_row():
    assert np.abs(np.average(lfom_20.error_per_row) + 0.22311742777836815) / \
        0.22311742777836815 < 0.01
    assert np.abs(np.average(lfom_60.error_per_row) + 0.32716087383055126) / \
        0.32716087383055126 < 0.01
