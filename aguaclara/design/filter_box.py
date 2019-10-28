"""The filter box of an AguaClara water treatment plant

#. Subcomponent of the filter component
#. Contains the sand used to filter the water

Example:
    >>> from aguaclara.design.filter_box import *
    >>> box = FilterBox(freeboard = 35 * u.cm)
    >>> box.branch_l
    <Quantity(1.0, 'meter')>
"""

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
	"""Design an AguaClara plant's filter box.

	A filter box's design relies on the filter's design in the same plant, but 
	assumed/default values may be used to design a filter box by itself. To 
	design these components in tandem, use 
	:class:`aguaclara.design.filter.Filter`.

	Design Inputs:
		- ``q (float * u.L / u.s)``: Flow rate (recommended, defaults to 20L/s)
        - ``temp (float * u.degC)``: Water temperature (recommended, defaults to
          20°C)
		- ``ratio_qp_min (float)``:Ratio of min port flow over max port flow 
		  (optional, defaults to 0.85)
		- ``ratio_q_filter_min (float)``: Ratio of min filter flow over max 
		  filter flow (optional, defaults to 0.95)
		- ``datum_z (int * u.m)``: Height of water under design flow in the 
		  filter inlet channel (optional, defaults to 0*u.m)
		- ``trunk_nd_max (int * u.inch)``: Maximum nominal diameter of trunk 
		  pipe (optional, defaults to 8 * u.inch)
		- ``layer_H_Min (int * u.cm)``: Miniumum height of layer (optional, 
		  defaults to 20*u.cm)
		- ``trunk_bw_hl_max(int*u.cm)``: Backwash headloss of trunk pipe 
		  (optional, defaults to 50 * u.cm)
		- ``filter_w (int * u.m)``: Width of filter (optional, defaults to 2m)
		- ``temp_max (int * u.degC)``: Max temperature (optional, defaults to 
		  30°C)
		- ``backwash_v (int * u.mm/u.s)``: Backwash velocity (optional, 
		  defaults to 11 mm/s)
		- ``layer_n (int)``: Number of layers (optional, defaults to 6)
		- ``branch_s (int*u.cm)``: Branch pipe spacing(optional, defaults to 
		  10cm)
		- ``trunk_s_min	 (int*u.cm)``: (optional, defaults to 3cm)
		- ``sand_density (int*u.cm)``: (optional, defaults to 3cm)2650 * 
		  u.kg/u.m**3
		- ``filter_max_hl (int*u.cm)``: (optional, defaults to 80cm)
		- ``sand_d60 (float * u.mm)``: (optional, defaults to 0.8)
		- ``filter_max_hl (int * u.cm)``: Maximum headloss of filter 
		  (optional, defaults to 80cm) 
		- ``filter_n_min (int)``: Minimum number of filters (optional, 
		  defaults to 2)
		- ``filter_n (int)``: Number of filters (optional, defaults to 5)
		- ``siphon_vent_t (int * u.s)``: Time for air to vent out of siphon pipe 
		  (optional, defaults to 15s)
		- ``sand_porosity (float): Porosity of sand (optional, defaults to 0.4)
		- ``orifice_s (int * u.cm)``: Size of orifice (optional, defualts to 5cm)
		- ``trunk_spec (string)``: Specifications of trunk 
		  (optional, defaults to 'sdr26')
		- ``branch_spec (string)``: Specifications of branch 
		  (optional, defaults to 'sdr26')
		- ``branch_filter_size (int * u.inch)``: Size of branch filter 
		  (optional, defaults to 1in.)
		- ``branch_bw_size (float * u.inch)``: Size of branch backwash 
		  (optional, defaults to 1.5in.)
		- ``trunk_l (int * u.m): Length of trunk (optional, defaults to 6m)
		- ``trunk_size (int * u.inch): Size of trunk (optional, defaults to 
		  6in.)
		- ``siphon_orifice_s (int * u.cm)``: Spacing of the siphon orifice 
		  (optional, defaults to 1cm)
		- ``freeboard (int * u.cm)``: The freeboard 
		  (optional, defaults to 10cm)
		- ``trunk_bw_hl_max (int * u.cm)``: Trunk backwash maximum headloss 
		  (optional, defaults to 50cm)
		- ``sand_clean_hl (float * u.cm)``: Sand clean headloss 
	  	  (optional, defaults to 3.848cm)
		- ``layer_h (int * u.cm)``: Height of layer (optional, defaults to 20cm)
		- ``siphon_l (float * u.m)``: Length of siphon (optional, defaults to 
		  10.0m)

	"""
	def __init__(self, **kwargs):
		
		self.ratio_qp_min = 0.85
		self.ratio_q_filter_min = 0.95
		self.datum_z=0*u.m
		self.trunk_nd_max=8 * u.inch
		self.layer_h_min=20*u.cm
		self.sand_d60=0.8 * u.mm
		self.trunk_bw_hl_max = 50 * u.cm
		self.filter_w = 1.5* u.m
	
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
		self._set_siphon_manifold()
		self._set_branch_bw()
		self._set_branch_manifold()
	

	def _set_branch_bw(self):
		"""This sets the branch backwash"""
		self.branch_bw_manifold = Manifold(
			q = self.branch_bw_q, 
			port_h_e = self.orifice_bw_hl,
			ratio_qp_min=self.ratio_qp_min, 
			port_s=self.orifice_s, 
			port_vena_contracta=con.VC_ORIFICE_RATIO,
			spec = self.branch_spec,
			l=self.branch_l, 
			k_minor=self.branch_k_e, 
			size_max=self.branch_bw_size
    	)
	def _set_trunk_pipe(self):
		"""Sets the trunk pipe."""
		self.trunk_pipe = Manifold(
			spec = self.trunk_spec,
			l = self.trunk_l, 
			size = self.trunk_size
			)

	def _set_siphon_manifold(self):
		"""This sets the siphon manifold"""
		q = 2*(self.post_backwash_fill_vol/self.siphon_drain_t+self.filter_q)
		size = pc.diam_pipe(
			q, 
			self.pre_backwash_flush_h, 
			self.siphon_l, 
			pc.viscosity_kinematic(self.temp), 
			mat.PVC_PIPE_ROUGH, 
			self.siphon_k_e)
	
		self.siphon_manifold = Manifold(
			q = q, 
			l = self.siphon_l, 
			spec = self.trunk_spec, 
			size = size)


	@property
	def trunk_inner_k_e(self):
		"""The minor loss coefficient expansion for the inner trunk."""
		return 1 + hl.EL90_K_MINOR
		
	@property
	def trunk_outer_k_e(self):
		"""The minor loss coefficient expansion for the outer trunk."""
		return 4 * self.trunk_inner_k_e
	
	@property
	def trunk_outlet_k_e(self):
		"""The minor loss coefficient expansion for the outlet of the trunk."""
		return 1 + 3*hl.EL90_K_MINOR
	
	@property
	def branch_k_e(self):
		"""The minor loss coefficient expansion for the branch."""
		return hl.PIPE_ENTRANCE_K_MINOR
		
	@property
	def siphon_k_e(self):
		"""The minor loss coefficient expansion for the siphon."""
		siphon_k_e = hl.PIPE_ENTRANCE_K_MINOR + 3*hl.EL90_K_MINOR + \
			hl.TEE_FLOW_BR_K_MINOR + hl.PIPE_EXIT_K_MINOR
		return siphon_k_e
	
	@property
	def branch_s(self):
		"""The spacing of the branch."""
		branch_s = self.layer_h_min / 2
		return branch_s

	@property
	def siphon_orifice_d(self):
		"""The diameter of the siphon orifice."""
		a = np.pi/4
		b = -a * self.siphon_manifold.id**2/self.filter_w
		c = b*self.siphon_orifice_s 
		x = (-b+np.sqrt(b**2 - (4*a*c)))/(4*a)
		return x.to(u.cm)
	
	@property
	def filter_v(self):
		"""The velocity of the backwash through the filter."""
		return self.backwash_v/self.layer_n 

	@property
	def filter_q(self):
		"""The flow rate through the filter."""
		return self.q /self.filter_n

	@property
	def trunk_inner_q(self):
		"""The flow rate through the inner trunk."""
		return (2 * self.filter_q) / self.layer_n
	
	@property
	def trunk_outer_q(self):
		"""The flow rate through the outer trunk."""
		return self.filter_q / self.layer_n
	
	@property
	def filter_active_a(self):
		"""The area of the filter that is active."""
		filter_active_a = self.filter_q / self.backwash_v
		return filter_active_a.to(u.m**2)

	@property
	def sand_to_fluidize_h(self):
		"""The height of the sand to the fluid."""
		return self.layer_h*self.layer_n
	
	@property
	def trunk_w(self):
		"""The width of the trunk."""
		trunk_w = pc.area_circle(self.trunk_pipe.od)/self.layer_h
		return trunk_w

	@property
	def filter_active_w(self):
		"""The width of the filter that is active."""
		return self.filter_w - self.trunk_w

	@property
	def filter_l(self):
		"""The length of the filter."""
		return self.filter_active_a / self.filter_active_w

	@property
	def filter_a(self):
		"""The area of the the filter."""
		return self.filter_l *self.filter_w

	@property
	def sand_volume(self):
		"""The volume of the sand."""
		return (self.filter_active_a*self.sand_to_fluidize_h).to(u.m**3)

	@property
	def sand_mass(self):
		"""The mass of the sand."""
		return (self.sand_volume*self.sand_density*self.sand_porosity).to(u.kg)

	@property
	def branch_layer_n(self):
		"""The branch of layer n"""
		return 2 * self.filter_l / self.branch_s

	@property
	def branch_bw_q(self):
		"""The flow rate of the branch backwash."""
		return self.filter_q / self.branch_layer_n
	
	@property
	def branch_l(self):
		"""The length of the branch"""
		return self.filter_w / 2
	
	@property
	def trunk_outer_bw_v(self):
		"""This is the outer backwash velocity of the truck pipe"""
		return self.filter_q / pc.area_circle(self.trunk_pipe.id)
	
	@property
	def orifice_contracted_v(self):
		"""This is the contracted velocity of the orifice"""
		return self.trunk_outer_bw_v * \
			 np.sqrt((self.ratio_qp_min**2 + 1) / (2 * (1- self.ratio_qp_min**2)))
	
	@property
	def orifice_v(self):
		"""This is the outer velocity of the orifice"""
		return con.VC_ORIFICE_RATIO * self.orifice_contracted_v
		
	@property
	def orifice_outer_a(self):
		"""This is the outer area of the orifice"""
		return self.filter_q / self.orifice_v

	@property
	def orifice_bw_hl(self):
		"""This is the backwash headloss of the orifice"""
		orifice_bw_hl = self.orifice_contracted_v**2 / (2* u.gravity)
		return orifice_bw_hl.to(u.cm)
		
	@property 
	def orifice_fi_hl (self):
		"""This is the headloss of the orifice"""
		orifice_fi_hl = (1/self.layer_n)**2 * self.orifice_bw_hl
		return orifice_fi_hl
	
    
	@property
	def branch_q(self):
		"""This is the flow rate of the branch"""
		return (2 * self.branch_bw_q) / self.layer_n
		
	def _set_branch_manifold(self):
		"""This sets the branch manifold"""
		self.branch_fi_manifold = Manifold(
      		q=self.branch_q, 
      		port_h_e=self.orifice_fi_hl, 
      		port_h_l_series=self.sand_clean_hl, 
      		ratio_qp_min=self.ratio_qp_min, 
      		port_s=self.orifice_s, 
      		port_vena_contracta=con.VC_ORIFICE_RATIO, 
      		spec=self.branch_spec, 
      		l=self.branch_l, 
      		k_minor =self.branch_k_e
      	)
	
	@property
	def trunk_inlet_hl(self): 
		"""This is the headloss of the trunk inlet pipe"""
		return pc.headloss_exp(
			self.trunk_outer_q, 
			self.trunk_pipe.id, 
			self.trunk_outer_k_e
			)
    	
	
	@property
	def trunk_bw_hl(self): 
		"""This is the backwash headloss of the trunk pipe"""
		return pc.headloss_exp(
			self.filter_q, 
			self.trunk_pipe.id, 
			self.trunk_outer_k_e
			)
	
	@property
	def trunk_outlet_hl(self):
		"""This is the headloss of the trunk outlet pipe"""
		return pc.headloss_exp(
			self.trunk_inner_q,
			self.trunk_pipe.id, 
			self.trunk_outlet_k_e)
	
	@property
	def inlet_fi_h_e(self):
		"""This is the height expansion of the inlet filter"""
		return pc.headloss_exp(self.trunk_outer_q, 
		self.trunk_pipe.id, 
		self.trunk_outer_k_e
		)

	@property
	def fluidize_sand_hl(self):
		"""This is the headloss of the fluidized sand"""
		fluidize_sand_hl = self.layer_h * (1 - self.sand_porosity) * \
			(self.sand_density / pc.density_water(self.temp)-1)
		
		return fluidize_sand_hl.to(u.m)
		
	@property
	def post_backwash_fill_h(self): 
		"""This is the height of the post backwash fill"""
		return (self.fluidize_sand_hl + self.trunk_bw_hl_max + 2*self.trunk_inlet_hl + \
		self.orifice_fi_hl + 2*self.freeboard + self.sand_clean_hl +\
		self.trunk_inlet_hl +self.orifice_fi_hl + self.trunk_outlet_hl)
		
	@property
	def post_backwash_fill_vol(self):
		"""This is the volume of the post backwash fill"""
		return (self.post_backwash_fill_h * self.filter_a)
	
	@property
	def pre_backwash_flush_h(self):
		"""This is the height of the pre backwash flush"""
		return (self.post_backwash_fill_h + (self.filter_max_hl - \
				self.sand_clean_hl))
		
	@property
	def pre_backwash_flush_vol(self):
		"""This is the volume of the pre backwash flush"""
		return (self.pre_backwash_flush_h * self.filter_a)
	
	@property
	def post_backwash_fill_t(self):
		"""This is the temperature of the post backwash fill"""
		return (self.post_backwash_fill_vol / self.filter_q).to(u.s)


	@property
	def siphon_drain_t(self):
		"""This is the thickness of the siphon drain"""
		return (self.post_backwash_fill_t)
	
	@property
	def siphon_orifice_n(self):
		"""This is the number of siphon orifices"""
		return (ut.floor(self.filter_w/(self.siphon_orifice_d + \
			self.siphon_orifice_s)))
	
	@property
	def inlet_weir_w(self):
		"""This is the width of the inlet weir"""
		return 0.5*self.filter_w
	
	@property
	def inlet_weir_h(self):
		"""This is the height of the inlet weir"""
		return pc.headloss_weir(self.filter_q,self.inlet_weir_w)
	
	@property
	def inlet_weir_z(self):
		"""This is the depth of the inlet weir"""
		return self.datum_z - self.inlet_weir_h

	@property
	def inlet_chan_v(self):
		"""This is the velocity of the inlet channel"""
		inlet_chan_v = 2 * np.sqrt(u.gravity * self.inlet_weir_h * (1 - self.ratio_q_filter_min**(2/3)) / (1*self.ratio_q_filter_min**(2/3)))
		return inlet_chan_v.to(u.m/u.s)
	
	@property
	def inlet_chan_a(self):
		"""This is the area of the inlet channel"""
		inlet_chan_a = self.q / self.inlet_chan_v
		return inlet_chan_a.to(u.m**2)