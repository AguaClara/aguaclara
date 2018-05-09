from aide_design.units import unit_registry as u
from top_baffle import *
from aide_render.builder_classes import DP, HP


class TopBaffles_Assembly:
    """This is a top baffle assembly class. It's called by the flocculator
    class so that the hierarchy of objects in Python is the same as in Fusion.

    """

    def __init__(self, L_ent_tank_max, L_sed, L_top_baffle, baffle_thickness,
                 W_chan, num_chan, baffle_spacing, wall_thickness):
        """This is where the "instantiation" occurs. Think of this as "rendering the
        template" or "using the cookie-cutter to make the cookie". Here is where we
        call all the methods that determine design qualities of the specific
        flocculator we are building.

        Parameters
        ----------

        L_ent_tank_max : float
            The maximum length of the entrance tank

        L_sed : float
            The length of the sedimentation unit process, including channels

        L_bottom_baffle : float
            Length of the baffles on the bottom of the flocculator

        baffle_thickness : float
            Thickness of a baffle

        W_chan : float
            Width of each flocculator channel

        num_chan : int
            Number of flocculator channels

        baffle_spacing : float
            The spacing between baffles

        wall_thickness : float
            Thickness of the walls in the flocculator

        """

        self.EntTank_Length = DP(L_ent_tank_max.magnitude, L_ent_tank_max.units)
        self.Length = DP(L_sed.magnitude, L_sed.units)
        self.Spacing = DP(baffle_spacing.magnitude, baffle_spacing.units)
        self.Thickness = DP(baffle_thickness.magnitude, baffle_thickness.units)
        self.TotalNum = DP(num_chan.magnitude)
        self.WallThickness = DP(wall_thickness.magnitude, wall_thickness.units)
        self.Width = DP(W_chan.magnitude, W_chan.units)

        self.TopBaffle = dict(vars(TopBaffle(L_top_baffle, baffle_thickness, W_chan)))
