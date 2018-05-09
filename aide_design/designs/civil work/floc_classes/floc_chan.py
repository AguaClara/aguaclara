from aide_design.units import unit_registry as u
from aide_render.builder_classes import DP, HP


class Channel:
    """This is a channel class. It's called by the flocculator class so
    that the hierarchy of objects in Python is the same as in Fusion.

    Attributes
    ----------
    These are the default values for a channel assembly. To overwrite, pass these
    into the bod (Basis Of Design) variable into the constructor.

    """

    def __init__(self, num_chan, L_ent_tank_max, h_chan, L_sed, W_chan,
                 ent_tank_overhang_length, wall_thickness, floor_thickness):
        """This is where the "instantiation" occurs. Think of this as "rendering the
        template" or "using the cookie-cutter to make the cookie". Here is where we
        call all the methods that determine design qualities of the specific
        flocculator we are building.

        Parameters
        ----------
        num_chan : int
            The number of channels in the entrance tank/flocculator (ETF)

        L_ent_tank_max : float
            The maximum length of the entrance tank

        h_chan : float
            The height of the flocculator channel

        L_sed : float
            The length of the sedimentation tank

        W_chan: float
            Channel width

        ent_tank_overhang_length : float
            The length of the entrance tank overhang

        wall_thickness : float
            Thickness of the plant wall

        floor_thickness : float
            Thickness of the plant floor

        """

        self.EntTank_Length = DP(L_ent_tank_max.magnitude, L_ent_tank_max.units)
        self.FirstLength = DP((L_sed - L_ent_tank_max + ent_tank_overhang_length).to(u.m).magnitude, u.m)
        self.Height = DP(h_chan.magnitude, h_chan.units)
        self.Length = DP(L_sed.magnitude, L_sed.units)
        self.TotalNum = DP(num_chan.magnitude, num_chan.units)
        self.Width = DP(W_chan.magnitude, W_chan.units)
        self.WallThickness = DP(wall_thickness.magnitude, wall_thickness.units)
        self.FloorThickness = DP(floor_thickness.magnitude, floor_thickness.units)
