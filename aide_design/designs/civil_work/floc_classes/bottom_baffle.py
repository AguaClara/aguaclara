from aide_design.shared.units import unit_registry as u
from aide_render.builder_classes import DP, HP


class BottomBaffle:
    """This is a bottom baffle class. It includes information of length,
    thickness, and width of the baffles on the bottom of the flocculator. 
    Baffles are obstructions in the channel of a flocculator to force the 
    flow to switch directions by 180°. Baffles in AguaClara plants are 
    plastic sheets, and all of the baffles in one flocculator channel are 
    connected to form a baffle module.
   
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
