from aide_design.shared.units import unit_registry as u
from aide_render.builder_classes import DP, HP


class MainFlocBaffleSupport:
    """This is a main flocculator and baffle support class. The baffle module
    supports each individual baffle and obstacle in the entrance tank and
    flocculator.

    """

    def __init__(self, baffle_thickness, num_baffles_chan_1, num_baffles_chan_n):

        """This is where the "instantiation" occurs. Think of this as "rendering the
        template" or "using the cookie-cutter to make the cookie". Here is where
        we call all the methods that determine design qualities of the specific
        flocculator we are building.

        Parameters
        ----------

        baffle_thickness : float
            Thickness of a baffle

        num_baffles_chan_1 : int
            Number of baffles in the first channel

        num_baffles_chan_n : int
            Number of baffles in every channel but the first

        """

        self.bafflethickness = DP(baffle_thickness.magnitude,
                                  baffle_thickness.units)
        self.numberbaffles = DP(num_baffles_chan_n.magnitude)
        self.numberentbaffles = DP(num_baffles_chan_1.magnitude)
