from aguaclara.design.component import Component
from aguaclara.core.units import unit_registry as u
import aguaclara.core.pipes as pipe
import aguaclara.core.materials as mat
import numpy as np

class SedTankHopper(Component):
    WALL_THICKNESS = 0.15 * u.m
    DRAIN_ND = 1.0 * u.inch

    l_min = 50.0 * u.cm
    sed_chan_w_outer = 283.505 * u.cm
    sed_tank_plate_l = 0.46 * u.m
    sed_tank_plate_angle = 60.0 * u.deg
    sed_chan_weir_thickness = 5 * u.cm
    sed_chan_drain_nd = 5 * u.inch
    sed_tank_side_slope_h = 0.59 * u.m
    sed_tank_side_slope_to_floc_weir_h_min = 5.0 * u.cm
    sed_tank_inlet_man_nd = 60.96 * u.cm
    sed_tank_inlet_man_h = 10 * u.cm
    fitting_s = 5.0 * u.cm
    
    @property
    def l_outer(self):
        """The length of the hopper."""
        if self.q > 60. * u.L / u.s: 
            l = self.sed_chan_w_outer
        else:
            l = max(
                self.l_min,
                self.sed_tank_plate_l * np.cos(self.sed_tank_plate_angle) - \
                    self.sed_chan_weir_thickness
            )
        return l
		
    @property
    def floc_weir_h(self):
        floc_weir_h = max(
            self.sed_tank_inlet_man_h + (pipe.OD(self.sed_tank_inlet_man_nd) / 2) + mat.CONCRETE_THICKNESS_MIN,
            self.sed_tank_side_slope_h + self.sed_tank_side_slope_to_floc_weir_h_min
        )
        return floc_weir_h
        
    @property
    def bottom_h_above_jet_reverser(self):
        if self.q > 60. * u.L /u.s:
            bottom_z = self.floc_weir_h - (self.sed_chan_w_outer - \
                (
                    3 * self.fitting_s + 
                    pipe.fitting_od(self.sed_chan_drain_nd) - 
                    pipe.OD(self.DRAIN_ND)
                ))*np.tan(self.slope_vertical_angle)
        else:
            bottom_z = self.sed_tank_inlet_man_h + \
            (
                (
                    pipe.fitting_od(self.sed_tank_inlet_man_nd) + \
                        self.fitting_s
                ) / 2
            )
        return bottom_z
	
    @property
    def slope_h(self):
        slope_h = self.floc_weir_h - self.bottom_h_above_jet_reverser
        return slope_h
        
    @property
    def slope_front_back_angle(self):
        return np.arctan(self.slope_h * 2 / self.l_outer).to(u.deg)

    @property
    def slope_vertical_angle(self):
        return (self.slope_front_back_angle / 2).to(u.deg)
        
    @property
    def slope_l(self):
        slope_l = self.slope_h * np.tan(self.slope_vertical_angle)
        return slope_l

    @property
    def pipe_drain_l(self):
        pipe_drain_l = (
            self.slope_h /
             np.tan(self.slope_front_back_angle)
             ) + self.WALL_THICKNESS + pipe.socket_depth(self.DRAIN_ND)
        return pipe_drain_l
