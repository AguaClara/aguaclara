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

	# (box_20.trunk_w, 0),
	# (box_60.trunk_w, 0),
	
	# (box_20.filter_active_w, 0),
	# (box_60.filter_active_w, 0),
	
	# (box_20.filter_l, 0),
	# (box_60.filter_l, 0),
	
	# (box_20.filter_a, 0),
	# (box_60.filter_a, 0),

	# (box_20.sand_volume, 0),
	# (box_60.sand_volume, 0),
	
	# (box_20.sand_mass, 0),
	# (box_60.sand_mass, 0),

    # (box_20.branch_layer_n, 0),
    # (box_60.branch_layer_n, 0),

    # (box_20.branch_bw_q, 0),
    # (box_60.branch_bw_q, 0),

    # (box_20.branch_l, 0),
    # (box_60.branch_l, 0),

    # (box_20.trunk_outer_bw_v, 0),
    # (box_60.trunk_outer_bw_v, 0),

    # (box_20.orifice_contracted_v, 0),
    # (box_60.orifice_contracted_v, 0),

    # (box_20.orifice_v, 0),
    # (box_60.orifice_v, 0),

    # (box_20.orifice_outer_a, 0),
    # (box_60.orifice_outer_a, 0),

    # (box_20.orifice_bw_hl, 0),
    # (box_60.orifice_bw_hl, 0),

    # (box_20.orifice_fi_hl, 0),
    # (box_60.orifice_fi_hl, 0),

    # (box_20._set_branch_bw, 0),
    # (box_60._set_branch_bw, 0),

    # (box_20.branch_q, 0),
    # (box_60.branch_q, 0),

    # (box_20._set_branch_manifold, 0),
    # (box_60._set_branch_manifold, 0),

    # (box_20.trunk_inlet_hl, 0),
    # (box_60.trunk_inlet_hl, 0),

    # (box_20.trunk_bw_hl, 0),
    # (box_60.trunk_bw_hl, 0),

    # (box_20.trunk_outlet_hl, 0),
    # (box_60.trunk_outlet_hl, 0),

    # (box_20.inlet_fi_h_e, 0),
    # (box_60.inlet_fi_h_e, 0),

    # (box_20.fluidize_sand_hl, 0),
    # (box_60.fluidize_sand_hl, 0),

    # (box_20.post_backwash_fill_h, 0),
    # (box_60.post_backwash_fill_h, 0),

    # (box_20.post_backwash_fill_vol, 0),
    # (box_60.post_backwash_fill_vol, 0),

    # (box_20.pre_backwash_flush_h, 0),
    # (box_60.pre_backwash_flush_h, 0),

    # (box_20.pre_backwash_flush_vol, 0),
    # (box_60.pre_backwash_flush_vol, 0),

    # (box_20.post_backwash_fill_t, 0),
    # (box_60.post_backwash_fill_t, 0),

    # (box_20._set_siphon_manifold, 0),
    # (box_60._set_siphon_manifold, 0),

    # (box_20.siphon_drain_t, 0),
    # (box_60.siphon_drain_t, 0),

    # (box_20.siphon_orifice_n, 0),
    # (box_60.siphon_orifice_n, 0),

    # (box_20.inlet_weir_w, 0),
    # (box_60.inlet_weir_w, 0),
    
    # (box_20.inlet_weir_h, 0),
    # (box_60.inlet_weir_h, 0),

    # (box_20.inlet_weir_z, 0),
    # (box_60.inlet_weir_z, 0),

    # (box_20.inlet_chan_v, 0),
    # (box_60.inlet_chan_v, 0),

    # (box_20.inlet_chan_a, 0),
    # (box_60.inlet_chan_a, 0)
	])

def test_filter_box(actual, expected):   
    assert actual == expected