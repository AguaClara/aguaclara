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
	(box_60.filter_active_a, 1.0909090909090908 * u.m**2),

	(box_20.sand_to_fluidize_h, 120 * u.cm),
	(box_60.sand_to_fluidize_h, 120 * u.cm),

	(box_20.trunk_w, 11.119853974881801 * u.cm),
	(box_60.trunk_w, 11.119853974881801 * u.cm),
	
	(box_20.filter_active_w, 1.388801460251182 * u.m),
	(box_60.filter_active_w, 1.388801460251182 * u.m),
	
	(box_20.filter_l, 0.26183466394872273 * u.m),
	(box_60.filter_l, 0.7855039918461681 * u.m),
	
	(box_20.filter_a, 0.3927519959230841 * (u.m ** 2)),
	(box_60.filter_a, 01.1782559877692522 * (u.m ** 2)),

	(box_20.sand_vol, 436.3636363636364 * u.l),
	(box_60.sand_vol, 1309.090909090909 * u.l),
	
	(box_20.sand_mass, 462.5454545454546 * u.kg),
	(box_60.sand_mass, 1387.6363636363635 * u.kg),

    (box_20.branch_layer_n, 5.2366932789744546),
    (box_60.branch_layer_n, 15.710079836923363),

    (box_20.branch_bw_q, 0.7638408031381501 * (u.L / u.s)),
    (box_60.branch_bw_q, 0.7638408031381502 * (u.L / u.s)),

    (box_20.branch_l, 0.75 * u.m),
    (box_60.branch_l, 0.75 * u.m),

    (box_20.trunk_outer_bw_v, 0.2573501279281694 * (u.m/u.s)),
    (box_60.trunk_outer_bw_v, 0.7720503837845082 * (u.m/u.s)),

    (box_20.orifice_contracted_v, 0.453374941135725 * (u.m/u.s)),
    (box_60.orifice_contracted_v, 1.3601248234071748 * (u.m/u.s)),

    (box_20.orifice_v, 0.28562621291550677 * (u.m/u.s)),
    (box_60.orifice_v, 0.8568786387465201 * (u.m/u.s)),

    (box_20.orifice_outer_a, 140.04316897844632 * (u.cm ** 2)),
    (box_60.orifice_outer_a, 140.04316897844635 * (u.cm ** 2)),

    (box_20.orifice_bw_hl, 1.0480074095120258 * u.cm),
    (box_60.orifice_bw_hl, 9.432066685608227 * u.cm),

    (box_20.orifice_fi_hl, 0.029111316930889603 * u.cm),
    (box_60.orifice_fi_hl, 0.2620018523780063 * u.cm),

    (box_20.branch_q, 0.25461360104605 * u.L/u.s),
    (box_60.branch_q, 0.2546136010460501 * u.L/u.s),

    (box_20.trunk_inlet_hl, 0.0007128681266443677 * u.m),
    (box_60.trunk_inlet_hl, 0.00641581313979931 * u.m),

    (box_20.trunk_bw_hl, 0.02566325255919724 * u.m),
    (box_60.trunk_bw_hl, 0.2309692730327752 * u.m),

    (box_20.trunk_outlet_hl, 0.00138821687820219 * u.m),
    (box_60.trunk_outlet_hl, 0.012493951903819708 * u.m),

    (box_20.inlet_fi_h_e, 0.0007128681266443677 * u.m),
    (box_60.inlet_fi_h_e, 0.00641581313979931 * u.m),

    (box_20.fluidize_sand_hl, 0.19857343217792028 * u.m),
    (box_60.fluidize_sand_hl, 0.19857343217792028 * u.m),

    (box_20.post_backwash_fill_h, 0.9411624797746733 * u.m),
    (box_60.post_backwash_fill_h, 0.974034860548698 * u.m),

    (box_20.post_backwash_fill_vol, 369.6434424194222 * u.L),
    (box_60.post_backwash_fill_vol, 1147.6624067374921 * u.L),

    (box_20.pre_backwash_flush_h, 1.7026824797746731 * u.m),
    (box_60.pre_backwash_flush_h, 1.7355548605486981 * u.m),

    (box_20.pre_backwash_flush_vol, 668.7319423547691 * u.L),
    (box_60.pre_backwash_flush_vol, 2044.927906543533 * u.L),

    (box_20.post_backwash_fill_t, 92.41086060485554 * u.s),
    (box_60.post_backwash_fill_t, 95.63853389479101 * u.s),

    (box_20.siphon_drain_t, 92.41086060485554 * u.s),
    (box_60.siphon_drain_t, 95.63853389479101 * u.s),

    (box_20.siphon_orifice_n, 75),
    # changed from 58 to 38
    (box_60.siphon_orifice_n, 38),

    (box_20.inlet_weir_w, 0.75 * u.m),
    (box_60.inlet_weir_w, 0.75 * u.m),
    
    (box_20.inlet_weir_h, 0.02018286125070386 * u.m),
    (box_60.inlet_weir_h, 0.041982043190490224 * u.m),

    (box_20.inlet_weir_z, -0.02018286125070386 * u.m),
    (box_60.inlet_weir_z, -0.041982043190490224 * u.m),

    (box_20.inlet_chan_v, 0.16595474719313838 * u.m/u.s),
    (box_60.inlet_chan_v, 0.23934816282977847 * u.m/u.s),

    (box_20.inlet_chan_a, 0.12051478091629383 * (u.m ** 2)),
    (box_60.inlet_chan_a, 0.25068084622262704 * (u.m ** 2))
	])

def test_filter_box(actual, expected):   
    assert actual == expected