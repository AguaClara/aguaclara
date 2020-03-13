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
    #Changed from 1.550839228816135 to 3.068610955986001
	(box_60.siphon_orifice_d, 3.068610955986001 * u.cm),
	
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

    #Changed from 11.119853974881801 to 18.847143031118645
	(box_20.trunk_w, 18.847143031118645 * u.cm),
    #Changed from 11.119853974881801 to 18.847143031118645
	(box_60.trunk_w, 18.847143031118645 * u.cm),
	
    #Changed from 1.388801460251182 to 1.3115285696888135
	(box_20.filter_active_w, 1.3115285696888135 * u.m),
    #Changed from 1.388801460251182 to 1.3115285696888135
	(box_60.filter_active_w, 1.3115285696888135 * u.m),
	
    #Changed from 0.26183466394872273 to 0.2772614886480465
	(box_20.filter_l, 0.2772614886480465 * u.m),
    #Changed from 0.7855039918461681 to 0.8317844659441395
	(box_60.filter_l, 0.8317844659441395 * u.m),
	
    #Changed from 0.3927519959230841 to 0.4158922329720698
	(box_20.filter_a, 0.4158922329720698 * (u.m ** 2)),
    #Changed from 1.1782559877692522 to 1.2476766989162091
	(box_60.filter_a, 1.2476766989162091 * (u.m ** 2)),

	(box_20.sand_vol, 436.3636363636364 * u.l),
	(box_60.sand_vol, 1309.090909090909 * u.l),
	
	(box_20.sand_mass, 462.5454545454546 * u.kg),
	(box_60.sand_mass, 1387.6363636363635 * u.kg),

    #Changed from 5.236693278974455 to 5.54522977296093
    (box_20.branch_layer_n, 5.54522977296093),
    #Changed from 15.710079836923363 to 16.63568931888279
    (box_60.branch_layer_n, 16.63568931888279),

    #Changed from 0.7638408031381501 to 0.7213407133288474
    (box_20.branch_bw_q, 0.7213407133288474 * (u.L / u.s)),
    #Changed from 0.7638408031381501 to 0.7213407133288474
    (box_60.branch_bw_q, 0.7213407133288474 * (u.L / u.s)),

    (box_20.branch_l, 0.75 * u.m),
    (box_60.branch_l, 0.75 * u.m),

    #Changed from 0.2573501279281694 to 0.14475944695959525
    (box_20.trunk_outer_bw_v, 0.14475944695959525 * (u.m/u.s)),
    #Changed from 0.7720503837845082 to 0.43427834087878575
    (box_60.trunk_outer_bw_v, 0.43427834087878575 * (u.m/u.s)),

    #Changed from 0.453374941135725 to 0.25502340438884524
    (box_20.orifice_contracted_v, 0.25502340438884524 * (u.m/u.s)),
    #Changed from 1.3601248234071748 to 0.7650702131665357
    (box_60.orifice_contracted_v, 0.7650702131665357 * (u.m/u.s)),

    #Changed from 0.28562621291550677 to 0.1606647447649725
    (box_20.orifice_v, 0.1606647447649725 * (u.m/u.s)),
    #Changed from 0.8568786387465201 to 0.4819942342949175
    (box_60.orifice_v, 0.4819942342949175 * (u.m/u.s)),

    #Changed from 140.04316897844632 to 248.9656337394602
    (box_20.orifice_outer_a, 248.9656337394602 * (u.cm ** 2)),
    #Changed from 140.04316897844632 to 248.9656337394602
    (box_60.orifice_outer_a, 248.9656337394602* (u.cm ** 2)),

    #1.0480074095120258
    (box_20.orifice_bw_hl, 0.33159609441591414 * u.cm),
    #9.432066685608227
    (box_60.orifice_bw_hl, 2.984364849743227 * u.cm),

    #0.029111316930889603
    (box_20.orifice_fi_hl, 0.00921100262266428 * u.cm),
    #0.2620018523780063
    (box_60.orifice_fi_hl, 0.08289902360397852 * u.cm),

    #0.25461360104605
    (box_20.branch_q, 0.24044690444294914 * u.L/u.s),
    #0.2546136010460501
    (box_60.branch_q, 0.24044690444294914 * u.L/u.s),

    #0.0007128681266443677
    (box_20.trunk_inlet_hl, 0.0002255559306960694 * u.m),
    #0.00641581313979931
    (box_60.trunk_inlet_hl, 0.0020300033762646248 * u.m),

    #0.02566325255919724
    (box_20.trunk_bw_hl, 0.008120013505058499 * u.m),
    #0.2309692730327752
    (box_60.trunk_bw_hl, 0.0730801215455265 * u.m),

    #0.00138821687820219
    (box_20.trunk_outlet_hl, 0.0004392404966186615 * u.m),
    #0.012493951903819708
    (box_60.trunk_outlet_hl, 0.0039531644695679526 * u.m),

    #0.0007128681266443677
    (box_20.inlet_fi_h_e, 0.0002255559306960694 * u.m),
    #0.00641581313979931
    (box_60.inlet_fi_h_e, 0.0020300033762646248 * u.m),

    (box_20.fluidize_sand_hl, 0.19857343217792028 * u.m),
    (box_60.fluidize_sand_hl, 0.19857343217792028 * u.m),

    #0.9411624797746733
    (box_20.post_backwash_fill_h, 0.9383535605190805 * u.m),
    #0.974034860548698
    (box_60.post_backwash_fill_h, 0.9487545872483615 * u.m),

    #369.6434424194222
    (box_20.post_backwash_fill_vol, 390.2539576015726 * u.L),
    #1147.6624067374921
    (box_60.post_backwash_fill_vol, 1183.738991499646 * u.L),

    #1.7026824797746731
    (box_20.pre_backwash_flush_h, 1.6998735605190805 * u.m),
    #1.7355548605486981
    (box_60.pre_backwash_flush_h, 1.7102745872483616 * u.m),

    #668.7319423547691
    (box_20.pre_backwash_flush_vol, 706.9642108544632 * u.L),
    #2044.927906543533
    (box_60.pre_backwash_flush_vol, 2133.869751258318 * u.L),

    #92.41086060485554
    (box_20.post_backwash_fill_t, 97.56348940039315 * u.s),
    #95.63853389479101
    (box_60.post_backwash_fill_t, 98.64491595830384 * u.s),

    #92.41086060485554
    (box_20.siphon_drain_t, 97.56348940039315 * u.s),
    #95.63853389479101
    (box_60.siphon_drain_t, 98.64491595830384 * u.s),

    (box_20.siphon_orifice_n, 75),
    # changed from 58 to 38
    (box_60.siphon_orifice_n, 36),

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