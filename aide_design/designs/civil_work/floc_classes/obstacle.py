from aide_design.shared.units import unit_registry as u
from aide_render.builder_classes import DP, HP


class Obstacle:
    """This is the obstacle class. Obstacles are half-pipes to contract the flow
    after the flow expands around one baffle and before it reaches the next
    baffle. The purpose of these obstacles is to provide extra head loss in
    between baffles. They generate head loss via minor losses, and one obstacle
    is designed to have the same minor loss as one baffle.

    """

    def __init__(self, W_chan):
        """This is where the "instantiation" occurs. Think of this as "rendering the
        template" or "using the cookie-cutter to make the cookie". Here is where
        we call all the methods that determine design qualities of the specific
        flocculator we are building.

        Parameters
        ----------

        W_chan : float
            Width of each flocculator channel

        """

        self.Width = DP(W_chan.magnitude, W_chan.units)
