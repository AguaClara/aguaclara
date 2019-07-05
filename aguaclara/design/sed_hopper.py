from aguaclara.design.component import Component
from aguaclara.core.units import unit_registry as u
import aguaclara.core.pipes as pipe
import aguaclara.core.materials as mat


class SedTankHopper(Component):
    WALL_THICKNESS = 0.15 * u.m
    DRAIN_ND = 1.0 * u.inch

    l_min = 50.0 * u.cm    

    @property
    def l(self):
        """The length of the hopper."""
        if self.q > 60. * u.L / u.s: 
            l = self.sed_chan_w_outer
        else:
            l = max(
                self.l_min,
                self.plate_l * np.cos(self.plate_settler_angle) - \
                    self.sed_chan_weir_thickness
            )
        return l
		
    @property
    def floc_weir_z(self):
        floc_weir_z = max(
            self.sed_tank_inlet_man_pipe_z + pipe.od(self.sed_tank_inlet_manifold_nd) + mat.CONCRETE_THICKNESS_MIN,
            self.sed_tank_side_slopes_z
        )

    @property
    def bottom_z(self):
        bottom_z = self.sed_tank_inlet_manifold_pipe + \
        (
            (
                pipe.fitting_od(self.sed_tank_inlet_manifold_nd) + \
                    self.fitting_s
            ) / 2
        )
        if self.q > 60. * u.L /u.s:
            bottom_z = self.floc_weir_z - (self.sed_tank_w - \
                (
                    3 * self.fitting_s + 
                    pipe.fitting_od(self.sed_channel_drain_nd) - 
                    pipe.od(self.DRAIN_ND)
                ))*np.tan(self.slope_north_angle)
        return bottom_z
	
    @property
    def slope_front_h(self):
        slope_front_h = self.floc_weir_z - self.bottom_z
        return slope_front_h

    @property
    def slope_front_back_angle(self):
        return np.arctan(self.slope_front_h / self.l / 2)

    @property
    def pipe_drain_l(self):
        pipe_drain_l = (
            self.slope_front_h /
             np.tan(self.slope_front_back_angle)
             ) + self.WALL_THICKNESS + pipe.socket_depth(self.DRAIN_ND)
        return pipe_drain_l

    