from aide_design.shared.units import unit_registry as u
from aide_design.designs.civil_work.floc_classes.bottom_baffle import *
from aide_design.designs.civil_work.floc_classes.top_baffle import *
from aide_design.designs.civil_work.floc_classes.obstacle import *
from aide_render.builder_classes import DP, HP


class EntFlocBaffleSupport:
    """This is a entrance tank, flocculator, and baffle support class.
    It's called by the flocculator class so that the hierarchy of
    objects in Python is the same as in Fusion.

    """

    def __init__(self, L_bottom_baffle, L_top_baffle, baffle_thickness, W_chan,
                 num_baffles_chan_1, num_baffles_chan_n):

        """This is where the "instantiation" occurs. Think of this as "rendering the
        template" or "using the cookie-cutter to make the cookie". Here is where
        we call all the methods that determine design qualities of the specific
        flocculator we are building.

        Parameters
        ----------

        L_bottom_baffle : float
            Length of the baffles on the bottom of the flocculator

        baffle_thickness : float
            Thickness of a baffle

        W_chan : float
            Width of each flocculator channel

        num_baffles_chan_1 : int
            Number of baffles in the first channel

        num_baffles_chan_n : int
            Number of baffles in every channel but the first

        """

        self.bafflethickness = DP(baffle_thickness.magnitude,
                                  baffle_thickness.units)
        self.numberbaffles = DP(num_baffles_chan_n.magnitude)
        self.numberentbaffles = DP(num_baffles_chan_1.magnitude)

        self.BottomBaffle = dict(vars(BottomBaffle(L_bottom_baffle,
                                                   baffle_thickness,
                                                   W_chan)))

        self.Obstacle = dict(vars(Obstacle(W_chan)))

        self.TopBaffle = dict(vars(TopBaffle(L_top_baffle,
                                             baffle_thickness, W_chan)))
