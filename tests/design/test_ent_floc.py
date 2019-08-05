from aguaclara.design.ent_floc import EntTankFloc
from aguaclara.core.units import u
import aguaclara.core.utility as ut

import pytest

etf_20 = EntTankFloc(q = 20.0 * u.L / u.s)
etf_60 = EntTankFloc(q = 60.0 * u.L / u.s)

@pytest.mark.parametrize('actual, expected', [
    (etf_20.ent.l, 37.6732811402825 * u.inch),
    (etf_60.ent.l, 57.820577185244304 * u.inch),

    (etf_20.floc.chan_w, 33.0 * u.cm),
    (etf_60.floc.chan_w, 97.0 * u.cm),

    (etf_20.floc.chan_n, 2),
    (etf_60.floc.chan_n, 2),
    
    (etf_20.floc.chan_w_min_gt, 32.02195253008654 * u.cm),
    (etf_60.floc.chan_w_min_gt, 96.72610238074294 * u.cm),

    (etf_20.ent.plate_l, 56 * u.cm),
    (etf_60.ent.plate_l, 58 * u.cm),

    (etf_20.ent.plate_n, 20),
    (etf_20.ent.plate_n, 20),

    (etf_20.ent.drain_pipe.id, 8.58005296821503 * u.cm),
    (etf_60.ent.drain_pipe.id, 14.517056850247537 * u.cm),
])
def test_etf(actual, expected):
    assert actual == expected