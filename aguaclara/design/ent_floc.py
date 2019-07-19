"""The entrance tank/flocculator assembly of an AguaClara water treatment plant
contains the entrance tank, chemical dose controller (CDC), linear flow orifice
meter (LFOM), and flocculator. It adds the initial dose of coagulant and
chlorine to the influent water, then causes flocs (accumulated coagulant and
primary particles) to aggregate.

Example:
    >>> from aguaclara.design.ent_floc import *
    >>> etf = EntTankFloc(q=20 * u.L / u.s, floc=Flocculator(hl=35 * u.cm))
    >>> etf.ent.l
    <Quantity(40.56720950298926, 'inch')>
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
    def __init__(self, **kwargs): 
        self.ent = EntranceTank()
        self.floc = Flocculator()
        self.lfom = LFOM()    
        self.subcomponents = [self.ent, self.floc, self.lfom]

        super().__init__(**kwargs)
        super().set_subcomponents()

        self._design_ent_floc(self.floc.ent_l)

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
        self.floc.ent_l = ent_l
        
        # Design the entrance tank using the flocculator's channel width.
        self.ent.floc_chan_w = self.floc.chan_w

        # Recalculate if the actual length of the entrance tank is not close
        # enough.
        if np.abs(self.ent.l.to(u.m) - ent_l) / self.ent.l > 0.01:
            self._design_ent_floc(self.ent.l)
