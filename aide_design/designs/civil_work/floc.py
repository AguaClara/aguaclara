from aide_design.shared.units import unit_registry as u
from aide_design.designs.civil_work.floc_classes import *
from aide_render.builder_classes import DP, HP


class Flocculator:
    """This is a flocculator class. It already has a lot of features built in,
    such as constants that go in the class attribute section (defaults), and methods.
    As well as an instantiation process that can be used to set custom values.

    The design algorithm is as follows:
    - the planview area of the entrance tank is calculated
    - the planview area of the entrance tank and the flocculator is calculated
    - the total width of the flocculator and entrance tank is calculated
    - the number of channels and their widths are calculated
    - the height of the channel is calculated
    - the number of baffles, their spacing, and heights are calculated
    - the presence of obstacles is determined

    Attributes
    ----------
    These are the default values for a flocculator. To overwrite, pass these
    into the bod (Basis Of Design) variable into the constructor.

        temp : float
            Design temperature

        L_ent_tank_max : float
            The maximum length of the entrance tank

        L_sed : float
            The length of the sedimentation unit process, including channels

        hl : float
            Headloss through the flocculator

        coll_pot : int
            Desired collision potential in the flocculator

        freeboard: float
            The height between the water and top of the flocculator channels

        ratio_HS_min : int
            Minimum allowable ratio between the water depth and edge to edge distance
            between baffles

        ratio_HS_max : int
            Maximum allowable ratio between the water depth and edge to edge distance
            between baffles

        W_min_construct : float
            Minimum width of a flocculator channel based on the width of the human hip

        baffle_thickness : float
            Thickness of a baffle

    These are the values calculated when an instance of the class is initialized.

        num_chan : int
            Number of channels for the entrance tank and flocculator

        W_chan : float
            Width of the channels for the entrance tank and flocculator

        H_chan : float
            Height of the channels for the entrance tank and flocculator

        baffle_spacing_ : float
            Spacing between baffles in the flocculator

        num_baffles_chan_1 : int
            Number of baffles in the first channel of the flocculator (the channel
            which includes the entrance tank and the start to the flocculator)

        num_baffles_chan_n : int
            Number of baffles in the channels of the flocculator (excluding the
            first channel)

        L_top_baffle : float
            The vertical length of the baffles attached to the top of the flocculator

        L_bottom_baffle : float
            The vertical length of the baffles attached to the bottom of the flocculator

        obstacles_bool : int
            1 if there are obstacles in the flocculator, 0 otherwise

    The following are dictionaries created to follow the hierarchy of Fusion
    assemblies for plant design.

        BottomBaffles_Assembly : dict
            Dictionary of parameters required to assemble the bottom baffles

        ConcreteChannels : dict
            Dictionary of parameters required to create the channels themselves

        EntFlocBaffleSupport : dict
            Dictionary of parameters required to assemble the baffle supports
            in the first channel of the flocculator

        MainFlocBaffleSupport : dict
            Dictionary of parameters required to assemble the baffle supports
            in all but the first channel of the flocculator

        Obstacles_Assembly : dict
            Dictionary of parameters required to assemble the obstacles

        TopBaffles_Assembly : dict
            Dictionary of parameters required to assemble the top baffles

    Methods
    -------
    All these methods are just imported from the aide_design flocculator.

    area_ent_tank(Q_plant, temp, depth_end, hl, coll_pot, ratio_HS_min=3,
                  W_min_construct=45*u.cm, L_sed=7.35*u.m, L_ent_tank_max=2.2*u.m)
        Return the planview area of the entrance tank given plant flow rate,
        headloss, target collision potential, design temperature, and depth of
        water at the end of the flocculator

    vol_floc(Q_plant, temp, hl, coll_pot)
        Return the total volume of the flocculator using plant flow rate, head
        loss, collision potential and temperature

    width_floc_min(Q_plant, temp, depth_end, hl, coll_pot, ratio_HS_min=3,
                   W_min_construct=45*u.cm)
        Return the minimum channel width required

    num_channel(Q_plant, temp, depth_end, hl, coll_pot, W_tot, ratio_HS_min=3,
                W_min_construct=45*u.cm)
        Return the number of channels in the entrance tank/flocculator (ETF)

    baffle_spacing(Q_plant, temp, W_chan, hl, coll_pot, ratio_HS_max=6)
        Return the spacing between baffles based on the target velocity gradient

    num_baffles(Q_plant, temp, W_chan, L, hl, coll_pot, ratio_HS_max=6,
                baffle_thickness=2*u.mm)
        Return the number of baffles that would fit in the channel given the
        channel length and spacing between baffles

    TODO: The stringified YAML below is throwing a ValueError because the indentation is inconsistent. Suggestion to pass it as a pure stringified dictionary by deleting \n's and spaces, and using {}'s to group subdictionaries. -Oliver
    Examples
    --------

    >>> my_floc = Flocculator(HP(20, u.L/u.s), HP(15, u.degC), HP(2, u.m))
    >>> from aide_render.builder import extract_types
    >>> floc_design_dict = extract_types(my_floc, [DP], [dict])
    >>> from aide_render.yaml import load, dump
    >>> dump(floc_design_dict)
    "BottomBaffles_Assembly:\n    BottomBaffle: {Height: !DP '1.728 meter', Thickness: !DP '2 millimeter', Width: !DP '0.3134 meter'}\n    EntTank_Length: !DP '2.2 meter'\n  Length: !DP '7.35 meter'\n  Num_Exit: !DP '18 '\n  Num_Inlet: !DP '26 '\n  Spacing: !DP '0.272 meter'\n  Thickness: !DP '2 millimeter'\n  TotalNum: !DP '2 '\n  WallThickness: !DP '0.15 meter'\n  Width: !DP '0.3134 meter'\nConcreteChannels:\n  Channel: {EntTank_Length: !DP '2.2 meter', FirstLength: !DP '5.786 meter', FloorThickness: !DP '0.2\n      meter', Height: !DP '2.5 meter', Length: !DP '7.35 meter', TotalNum: !DP '2 ',\n    WallThickness: !DP '0.15 meter', Width: !DP '0.3134 meter'}\n  EntTank_Length: !DP '2.2 meter'\n  EvenWall: {EntTank_Length: !DP '2.2 meter', FirstLength: !DP '5.786 meter', FloorThickness: !DP '0.2\n      meter', Height: !DP '2.5 meter', Length: !DP '7.35 meter', TotalNum: !DP '2 ',\n    WallThickness: !DP '0.15 meter', Width: !DP '0.3134 meter'}\n  FirstChannel: {EntTank_Length: !DP '2.2 meter', FirstLength: !DP '5.786 meter',\n    FloorThickness: !DP '0.2 meter', Height: !DP '2.5 meter', Length: !DP '7.35 meter',\n    TotalNum: !DP '2 ', WallThickness: !DP '0.15 meter', Width: !DP '0.3134 meter'}\n  FirstLength: !DP '5.786 meter'\n  FloorThickness: !DP '0.2 meter'\n  Height: !DP '2.5 meter'\n  LastChannel: {EntTank_Length: !DP '2.2 meter', FirstLength: !DP '5.786 meter', FloorThickness: !DP '0.2\n      meter', Height: !DP '2.5 meter', Length: !DP '7.35 meter', TotalNum: !DP '2 ',\n    WallThickness: !DP '0.15 meter', Width: !DP '0.3134 meter'}\n  Length: !DP '7.35 meter'\n  OddWall: {EntTank_Length: !DP '2.2 meter', FirstLength: !DP '5.786 meter', FloorThickness: !DP '0.2\n      meter', Height: !DP '2.5 meter', Length: !DP '7.35 meter', TotalNum: !DP '2 ',\n    WallThickness: !DP '0.15 meter', Width: !DP '0.3134 meter'}\n  TotalNum: !DP '2 '\n  WallThickness: !DP '0.15 meter'\n  Width: !DP '0.3134 meter'\nEntFlocBaffleSupport:\n  BottomBaffle: {Height: !DP '1.728 meter', Thickness: !DP '2 millimeter', Width: !DP '0.3134\n      meter'}\n  TopBaffle: {Height: !DP '2.228 meter', Thickness: !DP '2 millimeter', Width: !DP '0.3134\n      meter'}\n  bafflethickness: !DP '2 millimeter'\n  numberbaffles: !DP '18 '\n  numberentbaffles: !DP '26 '\nMainFlocBaffleSupport: {bafflethickness: !DP '2 millimeter', numberbaffles: !DP '18 ',\n  numberentbaffles: !DP '26 '}\nObstacles_Assembly:\n  Num_Exit: !DP '26 '\n  Num_Inlet: !DP '18 '\n  Obstacle: {Width: !DP '0.3134 meter'}\n  Spacing: !DP '0.272 meter'\n  Thickness: !DP '2 millimeter'\n  TotalNum: !DP '2 '\n  WallThickness: !DP '0.15 meter'\n  Width: !DP '0.3134 meter'\nTopBaffles_Assembly:\n  EntTank_Length: !DP '2.2 meter'\n  Length: !DP '7.35 meter'\n  Spacing: !DP '0.272 meter'\n  Thickness: !DP '2 millimeter'\n  TopBaffle: {Height: !DP '2.228 meter', Thickness: !DP '2 millimeter', Width: !DP '0.3134\n      meter'}\n  TotalNum: !DP '2 '\n  WallThickness: !DP '0.15 meter'\n  Width: !DP '0.3134 meter'\nnumberrows: !DP '1 '\n"

    >>> #stream = open('floc_update_fusion.yaml', 'w+')
    >>> #floc_design_dict = {'Flocculator': floc_design_dict}
    >>> #dump(floc_design_dict, stream, default_flow_style=False)
    >>> #stream.close()
    """

    #ent_tank: dict = aide_render.render.("ent_tank.yaml")
    #sed: dict = aide_render.yaml.load("sed.yaml")
    #materials: dict = aide_render.yaml.load("materials.yaml")

    ############## ATTRIBUTES ################
    hl = HP(40, u.cm)
    coll_pot = DP(37000)
    freeboard = HP(10, u.cm)
    ratio_HS_min = HP(3)
    ratio_HS_max = HP(6)
    W_min_construct = HP(45, u.cm)
    #L_ent_tank_max = DP(ent_tank['L'])
    #L_sed = DP(sed['L'])
    #baffle_thickness = DP(materials['thickness_plate'])
    #temp = DP(plant['temp'])
    #wall_thickness = DP(plant['wall_thickness'])
    #floor_thickness = DP(plant['floor_thickness'])

    # will take these out later when we get the imports from other classes to work
    L_ent_tank_max = HP(2.2, u.m)
    L_sed = HP(7.35, u.m)
    baffle_thickness = HP(2, u.mm)
    wall_thickness = HP(0.15, u.m)
    floor_thickness = HP(0.2, u.m)
    ent_tank_overhang_length = HP(0.6363, u.m)

    ############### METHODS #################
    from aide_design.functions.floc import (
        area_ent_tank,
        vol_floc,
        width_floc_min,
        num_channel,
        baffle_spacing,
        num_baffles,
    )

    area_ent_tank = staticmethod(area_ent_tank)
    vol_floc = staticmethod(vol_floc)
    width_floc_min = staticmethod(width_floc_min)
    num_channel = staticmethod(num_channel)
    baffle_spacing = staticmethod(baffle_spacing)
    num_baffles = staticmethod(num_baffles)

    def __init__(self, q, temp, depth_end, bod=None):
        """
        This is where the "instantiation" occurs. Think of this as "rendering the
        template" or "using the cookie-cutter to make the cookie". Here is where we
        call all the methods that determine design qualities of the specific
        flocculator we are building.

        Parameters
        ----------
        bod (Basis of Design) : dict: optional
            A dict of values that will override or add any attributes of the Floc
            component.
        q : float
            The flow rate through the flocculator
        temp : float
            The design temperature
        depth_end : float
            The depth of water at the end of the flocculator
        """

        # add bod as instance fields:
        if bod:
            for k, v in bod.items():
                setattr(self, k, v)

        while True:
            # calculate planview area of the entrance tank
            A_ET_PV = self.area_ent_tank(q, self.temp, depth_end, self.hl, self.coll_pot,
                                         self.ratio_HS_min, self.W_min_construct,
                                         self.L_sed, self.L_ent_tank_max)

            # now calculate planview area of entrance tank + flocculator combined
            volume_floc = self.vol_floc(q, self.temp, self.hl, self.coll_pot)
            A_floc_PV = volume_floc/(depth_end + self.hl/2)
            A_ETF_PV = (A_ET_PV + A_floc_PV).to(u.m**2)

            # calculate width of the flocculator channels and entrance tank
            W_min = self.width_floc_min(q, self.temp, depth_end, self.hl, self.coll_pot,
                                        self.ratio_HS_min, self.W_min_construct).to(u.m)
            W_tot = A_ETF_PV/self.L_sed

            if W_tot.to(u.m).magnitude > (2*self.W_min_construct).to(u.m).magnitude:
                break

            self.coll_pot += 500

        self.num_chan = HP(self.num_channel(q, self.temp, depth_end, self.hl,
                                            self.coll_pot, W_tot,
                                            self.ratio_HS_min, self.W_min_construct))
        self.W_chan = HP((W_tot/self.num_chan).to(u.m).magnitude, u.m)

        # calculate the height of the channel using depth at the end of the
        # flocculator, headloss, and freeboard
        self.H_chan = HP((depth_end + self.hl + self.freeboard).to(u.m).magnitude, u.m)

        # calculate baffle spacing and number of baffles in the flocculator
        self.baffle_spacing_ = HP(self.baffle_spacing(q, self.temp, self.W_chan, self.hl,
                                              self.coll_pot, self.ratio_HS_max).magnitude, u.m)
        self.num_baffles_chan_n = HP(self.num_baffles(q, self.temp, self.W_chan, self.L_sed,
                                                   self.hl, self.coll_pot,
                                                   self.ratio_HS_max, self.baffle_thickness))
        self.num_baffles_chan_1 = HP(self.num_baffles(q, self.temp, self.W_chan,
                                                   self.L_sed - self.L_ent_tank_max,
                                                   self.hl, self.coll_pot,
                                                   self.ratio_HS_max, self.baffle_thickness))

        # calculate the length of the baffles. The top baffle is set to the top of the
        # channel wall and the bottom baffle is set to the bottom of the channel.
        # The distance between baffles is the same as the vertical distance between
        # the top baffle and the bottom of the channel, which is the same vertical
        # distance as the bottom baffle and the free surface at the end of the flocculator
        self.L_top_baffle = HP((self.H_chan - self.baffle_spacing_).to(u.m).magnitude, u.m)
        self.L_bottom_baffle = HP((depth_end - self.baffle_spacing_).to(u.m).magnitude, u.m)

        # determine if there are obstacles in the flocculator
        if q.to(u.m**3/u.s).magnitude > 0.05:
            self.obstacles_bool = HP(0)
        else:
            self.obstacles_bool = HP(1)

        self.BottomBaffles_Assembly = dict(vars(bottom_baffle_assembly.BottomBaffles_Assembly(self.L_ent_tank_max,
            self.L_sed, self.L_bottom_baffle, self.baffle_thickness, self.W_chan,
            self.num_chan, self.num_baffles_chan_1, self.num_baffles_chan_n,
            self.baffle_spacing_, self.wall_thickness)))

        self.ConcreteChannels = dict(vars(floc_concrete_chan.ConcreteChannels(self.num_chan, self.L_ent_tank_max,
            self.H_chan, self.L_sed, self.W_chan, self.ent_tank_overhang_length,
            self.wall_thickness, self.floor_thickness)))

        self.EntFlocBaffleSupport = dict(vars(ent_floc_baffle_support.EntFlocBaffleSupport(self.L_bottom_baffle,
            self.L_top_baffle, self.baffle_thickness, self.W_chan,
            self.num_baffles_chan_1, self.num_baffles_chan_n)))

        self.MainFlocBaffleSupport = dict(vars(main_floc_baffle_support.MainFlocBaffleSupport(self.baffle_thickness,
            self.num_baffles_chan_1, self.num_baffles_chan_n)))

        self.Obstacles_Assembly = dict(vars(obstacle_assembly.Obstacles_Assembly(self.obstacles_bool,
            self.baffle_thickness, self.W_chan, self.num_chan, self.num_baffles_chan_1,
            self.num_baffles_chan_n, self.baffle_spacing_, self.wall_thickness)))

        self.TopBaffles_Assembly = dict(vars(top_baffle_assembly.TopBaffles_Assembly(self.L_ent_tank_max,
            self.L_sed, self.L_top_baffle, self.baffle_thickness, self.W_chan,
            self.num_chan, self.baffle_spacing_, self.wall_thickness)))

        self.numberrows = DP(self.num_chan.magnitude - 1)
