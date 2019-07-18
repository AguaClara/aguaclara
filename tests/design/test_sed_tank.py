from aguaclara.design.sed_tank import SedimentationTank
from aguaclara.core.units import u

import pytest


sed_tank_20 = SedimentationTank(q = 20.0 * u.L / u.s)
sed_tank_60 = SedimentationTank(q = 60.0 * u.L / u.s)

@pytest.mark.parametrize('actual, expected', [
    (sed_tank_20.q_tank, 6.18744 * u.L / u.s),
    (sed_tank_60.q_tank, 6.18744 * u.L / u.s),

    (sed_tank_20.diffuser_hl, 0.009259259259259259 * u.cm),
    (sed_tank_60.diffuser_hl, 0.009259259259259259 * u.cm),

    (sed_tank_20.diffuser_hl, 0.009259259259259259 * u.cm),
    (sed_tank_60.diffuser_hl, 0.009259259259259259 * u.cm),

    (sed_tank_20.diffuser_vel, 42.615094700074245 * u.mm / u.s),
    (sed_tank_60.diffuser_vel, 42.615094700074245 * u.mm / u.s),

    (sed_tank_20.diffuser_w_inner, 2.5033383300169962 * u.cm),
    (sed_tank_60.diffuser_w_inner, 2.5033383300169962 * u.cm),

    (sed_tank_20.diffuser_a, 13.443853994535718 * u.cm ** 2),
    (sed_tank_60.diffuser_a, 13.443853994535718 * u.cm ** 2),

    (sed_tank_20.inlet_man_v_max, 0.02823629964931982 * u.m / u.s),
    (sed_tank_60.inlet_man_v_max, 0.02823629964931982 * u.m / u.s),

    (sed_tank_20.inlet_man_nd, 60.96 * u.cm),
    (sed_tank_60.inlet_man_nd, 60.96 * u.cm),

    (sed_tank_20.outlet_man_nd, 6. * u.inch),
    (sed_tank_60.outlet_man_nd, 6. * u.inch),

    (sed_tank_20.outlet_man_orifice_d, 16 * u.mm),
    (sed_tank_60.outlet_man_orifice_d, 16 * u.mm),

    (sed_tank_20.plate_l, 0.4618802153517006 * u.m),
    (sed_tank_60.plate_l, 0.4618802153517006 * u.m),

    (sed_tank_20.outlet_man_orifice_n, 55),
    (sed_tank_60.outlet_man_orifice_n, 55),

    (sed_tank_20.outlet_orifice_hl, 0.0048859072820359815 * u.mm),
    (sed_tank_60.outlet_orifice_hl, 0.0048859072820359815 * u.mm),

    (sed_tank_20.side_slopes_w, 0.4923692307692307 * u.m),
    (sed_tank_60.side_slopes_w, 0.4923692307692307 * u.m),

    (sed_tank_20.side_slopes_h, 0.5867827996520784 * u.m),
    (sed_tank_60.side_slopes_h, 0.5867827996520784 * u.m),

    (sed_tank_20.outlet_man_orifice_q, 0.11205446937244101 * u.L / u.s),
    (sed_tank_60.outlet_man_orifice_q, 0.11205446937244101 * u.L / u.s),

    (sed_tank_20.outlet_man_orifice_spacing, 0.1048062404520667 * u.m),
    (sed_tank_60.outlet_man_orifice_spacing, 0.1048062404520667 * u.m),
])
def test_sed_tank(actual, expected):
    assert actual == expected

    
