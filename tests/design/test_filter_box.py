from aguaclara.design.filter_box import FilterBox
from aguaclara.core.units import u

import pytest

box_20 = FilterBox(q = 20.0 * u.L / u.s)
box_60 = FilterBox(q = 60.0 * u.L / u.s)

@pytest.mark.parametrize("actual, expected", [
	(box_20.trunk_inner_k_e, 1.9),
	(box_60.trunk_inner_k_e, 1.9),

	(box_20.trunk_outer_k_e, 7.6),
	(box_60.trunk_outer_k_e, 7.6),

	(box_20.trunk_outlet_k_e, 3.7),
	(box_60.trunk_outlet_k_e, 3.7),
	
	(box_20.branch_k_e, 0.5),
	(box_60.branch_k_e, 0.5),

	(box_20.siphon_k_e, 6.0),
	(box_60.siphon_k_e, 6.0),

	(box_20.branch_s, 10. * u.cm),
	(box_60.branch_s, 10. * u.cm),
	
	(box_20.siphon_orifice_d, 0.9921196734469191 * u.cm),
	(box_60.siphon_orifice_d, 1.550839228816135 * u.cm),
	
    (box_20.filter_v, 1.8333333333333333 * u.mm/u.s),
	(box_60.filter_v, 1.8333333333333333 * u.mm / u.s),
	
	(box_20.filter_q, 4.0  * u.L/u.s),
	(box_60.filter_q, 12.0 * u.L/u.s),
	
	(box_20.trunk_inner_q, 1.3333333333333333 * u.L/u.s),
	(box_60.trunk_inner_q, 4.0 * u.L/u.s),

	(box_20.trunk_outer_q, 0.6666666666666666 * u.L / u.s),
	(box_60.trunk_outer_q, 2* u.L / u.s),

	(box_20.filter_active_a, 0.36363636363636365 * u.m**2),
	(box_60.filter_active_a, 1.0909090909090908 * (u.m)**2),

	(box_20.sand_to_fluidize_h, 120 * u.cm),
	(box_60.sand_to_fluidize_h, 120 * u.cm),

	(box_20.trunk_w, 0.0011119853974881802 * (u.m ** 2) / u.cm),
	(box_60.trunk_w, 0.0011119853974881802 * (u.m ** 2) / u.cm),
	
	(box_20.filter_active_w, 1.388801460251182 * u.m),
	(box_60.filter_active_w, 1.388801460251182 * u.m),
	
	(box_20.filter_l, 0.26183466394872273 * u.m),
	(box_60.filter_l, 0.7855039918461681 * u.m),
	
	(box_20.filter_a, 0.3927519959230841 * (u.m ** 2)),
	(box_60.filter_a, 01.1782559877692522 * (u.m ** 2)),

	(box_20.sand_volume, 0.4363636363636364 * (u.m ** 3)),
	(box_60.sand_volume, 1.309090909090909 * u.m**3),
	
	(box_20.sand_mass, 462.5454545454546 * u.kg),
	(box_60.sand_mass, 1387.6363636363637 * u.kg),

    (box_20.branch_layer_n, 0.052366932789744546 * (u.m/u.cm)),
    (box_60.branch_layer_n, 0.15710079836923363 * (u.m/u.cm)),

    (box_20.branch_bw_q, 76.384080313815 * (u.cm * u.L / u.m / u.s)),
    (box_60.branch_bw_q, 76.384080313815 * (u.cm * u.L / u.m / u.s)),

    (box_20.branch_l, 0.75 * u.m),
    (box_60.branch_l, 0.75 * u.m),

    (box_20.trunk_outer_bw_v, 257.3501279281694 * (u.L/(u.m ** 2)/u.s)),
    (box_60.trunk_outer_bw_v, 772.0503837845082 * (u.L/(u.m ** 2)/u.s)),

    (box_20.orifice_contracted_v, 453.37494113572495 * (u.L/(u.m ** 2)/u.s)),
    (box_60.orifice_contracted_v, 1360.124823407175 * (u.L/(u.m**2)/u.s)),

    (box_20.orifice_v, 285.6262129155067 * (u.L/(u.m ** 2)/u.s)),
    (box_60.orifice_v, 856.8786387465202 * (u.L/(u.m ** 2)/u.s)),

    (box_20.orifice_outer_a, 0.014004316897844635 * (u.m ** 2)),
    (box_60.orifice_outer_a, 0.014004316897844633 * (u.m ** 2)),

    (box_20.orifice_bw_hl, 1.04800740951202531 * u.cm),
    (box_60.orifice_bw_hl, 9.43206668560823 * u.cm),

    (box_20.orifice_fi_hl, 0.02911131693088959 * u.cm),
    (box_60.orifice_fi_hl, 0.2620018523780064 * u.cm),

    (box_20.branch_q, 0),
    (box_60.branch_q, 0),

    (box_20.trunk_inlet_hl, 0),
    (box_60.trunk_inlet_hl, 0),

    (box_20.trunk_bw_hl, 0),
    (box_60.trunk_bw_hl, 0),

    (box_20.trunk_outlet_hl, 0),
    (box_60.trunk_outlet_hl, 0),

    (box_20.inlet_fi_h_e, 0),
    (box_60.inlet_fi_h_e, 0),

    (box_20.fluidize_sand_hl, 0),
    (box_60.fluidize_sand_hl, 0),

    (box_20.post_backwash_fill_h, 0),
    (box_60.post_backwash_fill_h, 0),

    (box_20.post_backwash_fill_vol, 0),
    (box_60.post_backwash_fill_vol, 0),

    (box_20.pre_backwash_flush_h, 0),
    (box_60.pre_backwash_flush_h, 0),

    (box_20.pre_backwash_flush_vol, 0),
    (box_60.pre_backwash_flush_vol, 0),

    (box_20.post_backwash_fill_t, 0),
    (box_60.post_backwash_fill_t, 0),

    (box_20.siphon_drain_t, 0),
    (box_60.siphon_drain_t, 0),

    (box_20.siphon_orifice_n, 0),
    (box_60.siphon_orifice_n, 0),

    (box_20.inlet_weir_w, 0),
    (box_60.inlet_weir_w, 0),
    
    (box_20.inlet_weir_h, 0),
    (box_60.inlet_weir_h, 0),

    (box_20.inlet_weir_z, 0),
    (box_60.inlet_weir_z, 0),

    (box_20.inlet_chan_v, 0),
    (box_60.inlet_chan_v, 0),

    (box_20.inlet_chan_a, 0),
    (box_60.inlet_chan_a, 0)
	])

def test_filter_box(actual, expected):   
    assert actual == expected