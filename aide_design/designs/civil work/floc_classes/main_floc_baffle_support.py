from aide_design.units import unit_registry as u
from aide_render.builder_classes import DP, HP


class MainFlocBaffleSupport:
    """This is the main flocculator baffle support class.
    It's called by the flocculator class so that the hierarchy of
    objects in Python is the same as in Fusion.

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
