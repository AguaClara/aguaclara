import aguaclara.core.constants as con
import aguaclara.core.head_loss as hl
import aguaclara.core.materials as mat
import aguaclara.core.physchem as pc
import aguaclara.core.pipes as pipe
from aguaclara.core.units import u
import aguaclara.core.utility as ut

from aguaclara.design.component import Component
from aguaclara.design.pipeline import Manifold

import numpy as np

class FilterBox(Component):

	def __init__(self, **kwargs):
		
		self.ratio_qp_min = 0.85
		self.datum_z=0*u.m
		self.trunk_nd_max=8 * u.inch
		self.layer_h_min=20*u.cm
		self.sand_d60=0.8 * u.mm
		self.trunk_bw_hl_max = 50 * u.cm
		self.filter_w = 2* u.m
	
		self.temp_max = 30 * u.degC
		self.backwash_v = 11 * u.mm/u.s
		self.layer_n = 6

		self.trunk_s_min = 3 * u.cm
		
		self.sand_density = 2650 * u.kg/u.m**3
		self.filter_max_hl = 80 * u.cm 
		self.filter_n_min = 2
		self.filter_n = 5
		self.siphon_vent_t = 15* u.s
		
		self.sand_porosity = 0.4

		self.orifice_s = 5 * u.cm
		self.trunk_spec = 'sdr26'
		self.branch_spec = 'sdr26'
		self.branch_filter_size = 1 * u.inch
		self.branch_bw_size = 1.5 * u.inch
		self.branch_s = 10 * u.cm
		self.trunk_l = 6 * u.m
		self.trunk_size = 6 * u.inch
		
		self.siphon_orifice_s = 1 * u.cm
		self.freeboard = 10 * u.cm
		self.trunk_bw_hl_max = 50 * u.cm
		self.sand_clean_hl = 3.848 * u.cm
		self.layer_h = 20 * u.cm
		self.siphon_l = 10.0 * u.m

		super().__init__(**kwargs)
		self._set_trunk_pipe()
	
	def _set_trunk_pipe(self):
		self.trunk_pipe = Manifold(
			spec = self.trunk_spec,
			l = self.trunk_l, 
			size = self.trunk_size
			)

	@property
	def trunk_inner_k_e(self):
		return 1 + hl.EL90_K_MINOR
		
	@property
	def trunk_outer_k_e(self):
		return 4 * self.trunk_inner_k_e
	
	@property
	def trunk_outlet_k_e(self):
		return 1 + 3*hl.EL90_K_MINOR
	
	@property
	def branch_k_e(self):
		return hl.PIPE_ENTRANCE_K_MINOR
		
	@property
	def siphon_k_e(self):
		siphon_k_e = hl.PIPE_ENTRANCE_K_MINOR + 3*hl.EL90_K_MINOR + \
			hl.TEE_FLOW_BR_K_MINOR + hl.PIPE_EXIT_K_MINOR
		return siphon_k_e
	
	@property
	def branch_s(self):
		branch_s = self.layer_h_min / 2
		return branch_s

	@property
	def siphon_orifice_d(self):
		a = np.pi/4
		b = -a * self.siphon_manifold.id**2/self.filter_w
		c = b*self.siphon_orifice_s 
		x = (-b+np.sqrt(b**2 - (4*a*c)))/(4*a)
		return x.to(u.cm)
	
	@property
	def filter_v(self):
		return self.backwash_v/self.layer_n 

	@property
	def filter_q(self):
		return self.q /self.filter_n

	@property
	def trunk_inner_q(self):
		return (2 * self.filter_q) / self.layer_n
	
	@property
	def trunk_outer_q(self):
		return self.filter_q / self.layer_n
	
	@property
	def filter_active_a(self):
		filter_active_a = self.filter_q / self.backwash_v
		return filter_active_a.to(u.m**2)
	
	@property
	def trunk_w(self):
		trunk_w = pc.area_circle(self.trunk_pipe.od) / self.layer_n
		return trunk_w

	@property
	def filter_active_w(self):
		return self.filter_w - self.trunk_w

	@property
	def filter_l(self):
		return self.filter_active_a / self.filter_active_w


	@property
	def branch_layer_n(self):
		return 2 * self.filter_l / self.branch_s

	@property
	def branch_bw_q(self):
		return self.filter_q / self.branch_layer_n
	@property
	def branch_l(self):
		return self.filter_w / 2
	@property
	def trunk_outer_bw_v(self):
		return self.filter_q / pc.area_circle(self.trunk_pipe.id)
	@property
	def orifice_contracted_v(self):
		return self.trunk_outer_bw_v * \
			 np.sqrt((self.ratio_qp_min**2 - 1) / (2 * (1- self.ratio_qp_min**2)))
	@property
	def orifice_bw_hl(self):
		orifice_bw_hl = self.orifice_contracted_v**2 / (2* u.gravity)
		return orifice_bw_hl.to(u.cm)
		
	@property 
	def orifice_fi_hl (self):
			orifice_fi_hl = (1/self.layer_n)**2 * self.orifice_bw_hl
			return orifice_fi_hl
	@property
	def _set_branch_bw(self):
		self.branch_bw_manifold = Manifold(
			q = self.branch_bw_q, 
			port_h_e = self.orifice_bw_hl,
			port_h_l_series=0*u.cm,
			ratio_qp_min=self.ratio_qp_min, 
			port_s=self.orifice_s, 
			port_vena_contracta=con.VC_ORIFICE_RATIO,
			spec = self.branch_spec,
			l=self.branch_l, 
			next_type='stopper', 
			k_minor=self.branch_k_e, 
			size_max=self.branch_bw_size
    	)
      
  	@property
  	def branch_fi_q(self):
		return (2 * self.branch_bw_manifold.q) / self.layer_n
		
 	@property
 	def _set_branch_fi_manifold(self):
		self.branch_fi_manifold = Manifold(
      		q=self.branch_fi_q, 
      		port_h_e=self.orifice_fi_hl, 
      		port_h_l_series=self.sand_clean_hl, 
      		ratio_qp_min=self.ratio_qp_min, 
      		port_s=self.orifice_s, 
      		port_vena_contracta=con.VC_ORIFICE_RATIO, 
      		spec=self.branch_spec, 
      		l=self.branch_l, 
      		next_type = 'stopper', 
      		k_minor =self.branch_k_e
      	)

  	@property
  	def trunk_inlet_fi_hl(self): 
		return pc.headloss_exp(
			self.trunk_outer_q, 
			self.trunk_pipe.id, 
			self.trunk_outer_k_e
			)
    	
	
	@property
	def trunk_bw_hl(self): 
		return pc.headloss_exp(
			self.filter_q, 
			self.trunk_pipe.id, 
			self.trunk_outer_k_e
			)
	
	@property
	def trunk_outlet_hl(self):
		return pc.headloss_exp(
			self.trunk_inner_q,
			self.trunk_pipe.id, 
			self.trunk_outlet_k_e)
	
	@property
	def inlet_fi_h_e(self):
		return pc.headloss_exp(self.trunk_outer_q, 
		self.trunk_pipe.id, 
		self.trunk_outer_k_e
		)

	@property
	def fluidize_sand_hl(self):
		fluidize_sand_hl = self.layer_h * (1 - self.sand_porosity) * \
			(self.sand_density / pc.density_water(self.temp)-1)
		
		return fluidize_sand_hl.to(u.m)
		
	@property
	def post_backwash_fill_h(self): 
		return (self.fluidize_sand_hl + self.trunk_bw_hl_max + 2*self.trunk_inlet_fi_hl + \
		self.orifice_fi_hl + 2*self.freeboard + self.sand_clean_hl +\
		self.trunk_inlet_fi_hl +self.orifice_fi_hl + self.trunk_outlet_hl)

	@property
	def filter_a(self):
		return self.filter_l * self.filter_w
		
	@property
	def post_backwash_fill_vol(self):
		return (self.post_backwash_fill_h * self.filter_a)
	
	@property
	def pre_backwash_flush_h(self):
		return (self.post_backwash_fill_h + (self.filter_max_hl - \
				self.sand_clean_hl))
		
	@property
	def pre_backwash_flush_vol(self):
		return (self.pre_backwash_flush_h * self.filter_a)
	
	@property
	def post_backwash_fill_t(self):
		return (self.post_backwash_fill_vol / self.filter_q).to(u.s)

	def _set_siphon_manifold(self):
		q = 2*(self.post_backwash_fill_vol/self.siphon_drain_t+self.filter_q)
		size = pc.diam_pipe(q, self.pre_backwash_flush_h, self.siphon_l, pc.viscosity_kinematic(self.temp), mat.PVC_PIPE_ROUGH, self.siphon_k_e)
	
		self.siphon_manifold = Manifold(q = q, l = self.siphon_l, spec = self.trunk_spec, size = size)

	@property
	def siphon_drain_t(self):
		return (self.post_backwash_fill_t)
	
	@property
	def siphon_orifice_n(self):
		return (ut.floor(self.filter_w/(self.siphon_orifice_d + \
			self.siphon_orifice_s)))
	
	@property
	def inlet_weir_w(self):
		return 0.5*self.filter_w
	
	@property
	def inlet_weir_h(self):
		return pc.headloss_weir(self.filter_q,self.inlet_weir_w)
	
	@property
	def inlet_weir_z(self):
		return self.datum_z - self.inlet_weir_h