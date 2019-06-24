"""The entrance tank/flocculator assembly of an AguaClara water treatment plant
contains the entrance tank, chemical dose controller (CDC), linear flow orifice
meter (LFOM), and flocculator. It adds the initial dose of coagulant and
chlorine to the influent water, then causes flocs (accumulated coagulant and
primary particles) to aggregate.

Example:
    >>> from aguaclara.design.ent_floc import *
    >>> etf = EntTankFloc(q=20 * u.L / u.s, floc=Flocculator(hl=35 * u.cm))
    >>> etf.ent.l
    <Quantity(37.6732811402825, 'inch')>
"""
from aguaclara.design.ent import *
from aguaclara.design.lfom import *
from aguaclara.design.floc import *


class EntTankFloc(Component):
    """Design an AguaClara plant's entrance tank/flocculator assembly.

    The designs of the LFOM, entrance tank, and flocculator in an AguaClara
    water treatment plant are interdependent. Use this class instead of the
    classes of the individual components to design all three at once.

    Design Inputs:
        - ``q (float * u.L / u.s)``: Flow rate (recommended, 
          defaults to 20L/s)
        - ``temp (float * u.degC)``: Water temperature (recommended,
          defaults to 20°C)
        - ``ent (EntranceTank)``: Entrance Tank
          (optional, see :class:`aguaclara.design.ent.EntranceTank`
          for defaults)
        - ``floc (Flocculator)``: Flocculator
          (optional, see :class:`aguaclara.design.floc.Flocculator` for 
          defaults)
        - ``lfom (LFOM)``: Linear Flow Orifice Meter
          (optional, see :class:`aguaclara.design.lfom.LFOM` for defaults)
    """
    def __init__(self, q =20.0 * u.L/u.s, temp=20. * u.degC,
                 ent = EntranceTank(), floc = Flocculator(), lfom = LFOM()):
        super().__init__(q = q, temp = temp)
        self.lfom = lfom
        self.ent = ent
        self.floc = floc
        
        # Design the entrance tank and flocculator in tandem
        self._design_ent_floc(self.floc.ent_l)

        super().propogate_config([self.lfom, self.ent, self.floc])

    def _design_ent_floc(self, ent_l):
        """Design the entrance tank and flocculator in tandem.

        Each subcomponent is redesigned until the expected length of the
        entrance tank (used to design the flocculator) is close enough to the
        actual length of the entrance tank (which should accomodate the
        flocculator's channel width).
        
        Args:
            - ``ent_l (float * u.m)``: The initial guess for the entrance tank's
              length, used to design the first iteration of the flocculator.
        """
        # Design the flocculator using a guess of the entrance tank's length.
        self.floc = Flocculator(self.floc.q, self.floc.temp,
                                ent_l,
                                self.floc.chan_w_max,
                                self.floc.l_max,
                                self.floc.gt,
                                self.floc.hl,
                                self.floc.end_water_depth,
                                self.floc.drain_t)
        
        # Design the entrance tank using the flocculator's channel width.
        self.ent = EntranceTank(self.ent.q, self.ent.temp,
                                self.ent.lfom_nd,
                                self.floc.chan_w,
                                self.ent.floc_end_depth,
                                self.ent.plate_s,
                                self.ent.plate_thickness,
                                self.ent.plate_angle,
                                self.ent.plate_capture_vel,
                                self.ent.fab_s,
                                self.ent.sdr)

        # Recalculate if the actual length of the entrance tank is not close
        # enough.
        if np.abs(self.ent.l.to(u.m) - ent_l) / self.ent.l > 0.01:
            self._design_ent_floc(self.ent.l)
