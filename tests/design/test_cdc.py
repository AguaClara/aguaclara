from aguaclara.design.cdc import CDC
from aguaclara.core.units import u

import pytest

cdc_20 = CDC(q=20.0 * u.L / u.s)
cdc_60 = CDC(q=60.0 * u.L / u.s, coag_stock_conc=500 * u.g / u.L)


@pytest.mark.parametrize(
    "actual, expected",
    [
        (cdc_20.alum_nu(2 * u.g / u.L), 1.00357603e-06 * u.m ** 2 / u.s),
        (cdc_60.alum_nu(2 * u.g / u.L), 1.00357603e-06 * u.m ** 2 / u.s),
        (cdc_20.pacl_nu(2 * u.g / u.L), 1.00364398e-06 * u.m ** 2 / u.s),
        (cdc_60.pacl_nu(2 * u.g / u.L), 1.00364398e-06 * u.m ** 2 / u.s),
        (cdc_20.coag_nu(2 * u.g / u.L, "alum"), 1.00357603e-06 * u.m ** 2 / u.s),
        (cdc_20.coag_nu(2 * u.g / u.L, "PACl"), 1.00364398e-06 * u.m ** 2 / u.s),
        (cdc_20.coag_q_max, 0.01333333 * u.L / u.s),
        (cdc_60.coag_q_max, 0.012 * u.L / u.s),
        (cdc_20.coag_stock_vol, 2500 * u.L),
        (cdc_60.coag_stock_vol, 1100 * u.L),
        (cdc_20.coag_sack_n, 15),
        (cdc_60.coag_sack_n, 22),
        (cdc_20.coag_stock_time_min, 187500 * u.s),
        (cdc_60.coag_stock_time_min, 91666.66666667 * u.s),
        (cdc_20.coag_stock_nu, 1.31833437e-06 * u.m ** 2 / u.s),
        (cdc_60.coag_stock_nu, 4.0783455e-06 * u.m ** 2 / u.s),
        (cdc_20._coag_tube_q_max, 0.0035063291 * u.L / u.s),
        (cdc_60._coag_tube_q_max, 0.0035063291 * u.L / u.s),
        (cdc_20.coag_tubes_active_n, 4),
        (cdc_60.coag_tubes_active_n, 4),
        (cdc_20.coag_tubes_n, 5),
        (cdc_60.coag_tubes_n, 5),
        (cdc_20.coag_tube_operating_q_max, 0.003333333 * u.L / u.s),
        (cdc_60.coag_tube_operating_q_max, 0.003 * u.L / u.s),
        (cdc_20.coag_tube_l, 1.01256563 * u.m),
        (cdc_60.coag_tube_l, 0.370547757 * u.m),
        (cdc_20.coag_tank_r, 0.775 * u.m),
        (cdc_60.coag_tank_r, 0.55 * u.m),
        (cdc_20.coag_tank_h, 1.65 * u.m),
        (cdc_60.coag_tank_h, 1.39 * u.m),
    ],
)
def test_cdc(actual, expected):
    if type(actual) == u.Quantity and type(expected) == u.Quantity:
        assert actual.units == expected.units
        assert actual.magnitude == pytest.approx(expected.magnitude)
    else:
        assert actual == pytest.approx(expected)


@pytest.mark.parametrize(
    "warning, func",
    [
        (UserWarning, lambda: cdc_20._alum_nu(2 * u.g / u.L)),
        (UserWarning, lambda: cdc_20._pacl_nu(2 * u.g / u.L)),
        (UserWarning, lambda: cdc_20._coag_nu(2 * u.g / u.L, "alum")),
        (UserWarning, lambda: cdc_20.coag_q_max_est),
    ],
)
def test_cdc_warning(warning, func):
    pytest.warns(warning, func)
