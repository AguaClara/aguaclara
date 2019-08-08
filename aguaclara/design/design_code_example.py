"""Example design code for a component and subcomponent.

"""
from aguaclara.core.units import unit_registry as u
import aguaclara.core.utility as ut
from aguaclara.design.component import Component


class Sedimentor(Component):
    def __init__(self, **kwargs):
        self.wall_thickness = 15 * u.cm

        self.tank = SedimentationTank()
        self.chan = SedimentationChannel()
        self.subcomponents = [self.tank, self.chan]

        super().__init__(**kwargs)
        super().set_subcomponents()
        self._set_tank()
        self._set_chan()

    @property
    def tank_n(self):
        """The number of sedimentation tanks."""
        tank_n = ut.ceil_step((self.q / self.tank.q_ideal), 1)
        return int(tank_n)

    def _set_tank(self):
        self.tank.q = self.q / self.tank_n

    def _set_chan(self):
        self.chan.sed_tank_n = self.tank_n
        self.chan.sed_tank_w_inner = self.tank.w_inner
        self.chan.sed_wall_thickness = self.wall_thickness


class SedimentationChannel(Component):
    def __init__(self, **kwargs):
        self.sed_tank_n = 4
        self.sed_tank_w_inner = 42 * u.inch
        self.sed_wall_thickness = 15 * u.cm

        super().__init__(**kwargs)

    @property
    def l_inner(self):
        l_inner = (
                self.sed_tank_n * 
                    (self.sed_tank_w_inner + self.sed_wall_thickness)
            ) + self.sed_wall_thickness
        return l_inner.to(u.m)


class SedimentationTank(Component):
    def __init__(self, **kwargs):
        self.vel_upflow = 1 * u.mm / u.s
        self.l_inner = 5.8 * u.m
        self.w_inner = 42 * u.inch

        super().__init__(**kwargs)

    @property
    def q_ideal(self):
        q_ideal = self.l_inner * self.w_inner * self.vel_upflow
        return q_ideal.to(u.L / u.s)
