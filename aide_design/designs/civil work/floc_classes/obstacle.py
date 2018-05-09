from aide_design.units import unit_registry as u
from aide_render.builder_classes import DP, HP


class Obstacle:
    """This is the obstacle class. It's called by the obstacles assemby class
    so that the hierarchy of objects in Python is the same as in Fusion.

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
