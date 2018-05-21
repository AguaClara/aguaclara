from aide_design.shared.units import unit_registry as u
from aide_render.builder_classes import DP, HP


class BottomBaffle:
    """This is a bottom baffle class. It's called by the bottom baffles assembly
    class so that the hierarchy of objects in Python is the same as in Fusion.

    """

    def __init__(self, L_bottom_baffle, baffle_thickness, W_chan):
        """This is where the "instantiation" occurs. Think of this as "rendering the
        template" or "using the cookie-cutter to make the cookie". Here is where we
        call all the methods that determine design qualities of the specific
        flocculator we are building.

        Parameters
        ----------

        L_bottom_baffle : float
            Length of the baffles on the bottom of the flocculator

        baffle_thickness : float
            Thickness of a baffle

        W_chan : float
            Width of each flocculator channel

        """

        self.Height = DP(L_bottom_baffle.magnitude, L_bottom_baffle.units)
        self.Thickness = DP(baffle_thickness.magnitude, baffle_thickness.units)
        self.Width = DP(W_chan.magnitude, W_chan.units)
