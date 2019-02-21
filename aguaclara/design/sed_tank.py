from aguaclara.core.units import unit_registry as u
import aguaclara.core.constants as con
import aguaclara.core.pipes as pipe

import numpy as np

PLANT_FLOOR_THICKNESS = 0.2 * u.m  # plant floor slab thickness
WALL_THICKNESS = 0.15 * u.m  # thickness of sed tank dividing wall
HL_OUTLET_MAN = 4 * u.cm  # head loss through the outlet manifold

BOD_UP_VEL = 1 * u.mm / u.s

##Plate settler
CONC_BOD_VEL = 0.12 * u.mm / u.s  # capture velocity

PLATE_ANGLE = 60 * u.deg

PLATE_S = 2.5 * u.cm

MODULE_PLATES_N_MIN = 8

# This is moved to template because SED_PLATE_THICKNESS is in materials.yaml
# CENTER_SED_PLATE_DIST = PLATE_S + SED_PLATE_THICKNESS

# Bottom of channel
SLOPE_ANGLE = 50 * u.deg

##This slope needs to be verified for functionality in the field.
# A steeper slope may be required in the floc hopper.
HOPPER_SLOPE_ANGLE = 45 * u.deg

WATER_H_EST = 2 * u.m

GATE_VALVE_URL = "https://confluence.cornell.edu/download/attachments/173604905/Sed-Scaled-Gate-Valve-Threaded.dwg"

SUPPORT_BOLT_URL = "https://confluence.cornell.edu/download/attachments/173604905/PlateSettlerSupportBolt.dwg"

##Inlet channel
WEIR_HL_MAX = 5 * u.cm

##Height of the inlet channel overflow weir above the normal water level
# in the inlet channel so that the far side of the overflow weir does not
# fill with water under normal operating conditions. This means the water
# level in the inlet channel will increase when the inlet overflow weir
# is in use.
INLET_WEIR_FREE_BOARD_H = 2 * u.cm

WEIR_THICKNESS = 5*u.cm

INLET_HL_MAX = 1 * u.cm

# ratio of the height to the width of the sedimentation tank inlet channel.
INLET_H_W_RATIO = 0.95

##Exit launder
##Target headloss through the launder orifices
LAUNDER_BOD_HL = 4 * u.cm

##Acceptable ratio of min to max flow through the launder orifices
FLOW_LAUNDER_ORIFICES_RATIO = 0.80

##Center to center spacing of orifices in the launder
CENTER_LAUNDER_EST_DIST = 10 * u.cm

##The additional length needed in the launder cap pipe that is to be
# inserted into the launder coupling
LAUNDER_CAP_EXCESS_L = 3 * u.cm

##Space between the top of the plate settlers and the bottom of the
# launder pipe
LAMELLA_TO_LAUNDER_H = 5 * u.cm

##The additional length needed in the launder cap pipe that is to be
# inserted into the launder coupling

##Diameter of the pipe used to hold the plate settlers together
MOD_ND = 0.5 * u.inch

##Diameter of the pipe used to create spacers. The spacers slide over the
# 1/2" pipe and are between the plates
MOD_SPACER_ND = 0.75 * u.inch

MOD_SPACER_SDR = 17

##This is the vertical thickness of the lip where the lamella support sits. mrf222
LAMELLA_LEDGE_THICKNESS = 8 * u.cm

LAMELLA_PIPE_EDGE_S = 5 * u.cm

##Approximate x-dimension spacing between cross pipes in the plate settler
# support frame.
CENTER_PLATE_FRAME_CROSS_DIST_EST = 0.8 * u.m

##Estimated plate length used to get an initial estimate of sedimentation
# tank active length.
PLATE_L_EST = 60 * u.cm

##Pipe size of the support frame that holds up the plate settler modules
PLATE_FRAME_ND = 1.5 * u.inch

##Floc weir

#Vertical distance from the top of the floc weir to the bottom of the pipe
# frame that holds up the plate settler modules
FLOC_WEIR_TO_PLATE_FRAME_H = 10 * u.cm

##Minimum length (X dimension) of the floc hopper
HOPPER_MIN_L = 50 * u.cm

##Inlet manifold
##Max energy dissipation rate in the sed diffuser outletS
ENERGY_DIS_INT_MAX = 150 * u.mW/u.kg

##Ratio of min to max flow through the inlet manifold diffusers
INLET_Q_RATIO = 0.8

MAN_ND_MAX = 8 * u.inch

MAN_SDR = 41  # SDR of pipe for sed tank inlet manifold

##This is the minimum distance between the inlet manifold and the slope
# of the sed tank.
INLET_MAN_SLOPE_S = 10 * u.cm

##Length of exposed manifold stub coming out of the floc weir to which the
# free portion of the inlet manifold is attached with a flexible coupling.
MAN_CONNECTION_STUB_L = 4 * u.cm

##Space between the end of the manifold pipe and the edge of the first
# diffuser's hole, or the first manifold orifice.

MAN_FIRST_DIFFUSER_GAP_L = 3 * u.cm

##Vertical distance from the edge of the jet reverser half-pipe to the tip
# of the inlet manifold diffusers
JET_REVERSER_TO_DIFFUSERS_H = 3 * u.cm

##Gap between the end of the inlet manifold pipe and the end wall of the
# tank to be able to install the pipe
MAN_PIPE_FROM_TANK_END_L = 2  *u.cm

WALL_TO_DIFFUSER_GAP_L_MIN = 3 * u.cm

# Diameter of the holes drilled in the manifold so that the molded 1"
# diffuser pipes can fit tightly in place (normal OD of a 1" pipe is
# close to 1-5/16")
MAN_PORT_D = 1.25 * u.inch

# nominal diameter of pipe used for jet reverser in bottom of set tank
JET_REVERSER_ND = 3 * u.inch

SDR_REVERSER = 26  # SDR of jet reverser pipe

# Diffuser geometry
SDR_DIFFUSER = 26  # SDR of diffuser pipe

DIFFUSER_PIPE_ND = 4 * u.cm  # nominal diameter of pipe used to make diffusers

AREA_PVC_DIFFUSER = (
    (np.pi/4) * ((pipe.OD(DIFFUSER_PIPE_ND)**2)
    - (pipe.ID_SDR(DIFFUSER_PIPE_ND, SDR_DIFFUSER))**2)
)
# stretch factor applied to the diffuser PVC pipes as they are heated
# and molded
PVC_STRETCH_RATIO = 1.2

T_DIFFUSER = ((pipe.OD(DIFFUSER_PIPE_ND) -
                        pipe.ID_SDR(DIFFUSER_PIPE_ND, SDR_DIFFUSER))
                              / (2 * PVC_STRETCH_RATIO))

W_DIFFUSER_INNER = 0.3175 * u.cm  # opening width of diffusers

# Calculating using a minor loss equation with K = 1
V_SED_DIFFUSER_MAX = np.sqrt(2 * con.GRAVITY * INLET_HL_MAX).to(u.mm / u.s)

DIFFUSER_L = 15 * u.cm  # vertical length of diffuser

B_DIFFUSER = 5 * u.cm  # center to center spacing beteen diffusers

# Headloss through the diffusers to ensure uniform flow between sed tanks
DIFFUSER_HL = 0.001 * u.m

# Outlet to filter
# If the plant has two trains, the current design shows the exit channel
# continuing from one set of sed tanks into the filter inlet channel.
# The execution of this extended channel involves a few calculations.
FILTER_OUTLET_HL_MAX = 10 * u.cm

# Maximum length of sed plate sticking out past module pipes without any
# additional support. The goal is to prevent floppy modules that don't maintain
# constant distances between the plates

PLATE_CANTILEVERED_L = 20 * u.cm

HOPPER_DRAIN_ND = 1*u.inch

HOPPER_VIEWER_ND = 2*u.inch

HOPPER_SKIMMER_ND = 2*u.inch

# Diffusers/Jet Reverser

DIFFUSER_ND = 1*u.inch

JET_REVERSER_ND = 3*u.inch


"""This file contains all the functions needed to design a sedimentation tank
for an AguaClara plant.
Attributes
----------
thickness_wall : float
    Thickness of walls in the sedimentation unit process
plate_settlers : dict
    A dictionary containing variables relating to the plate settlers
    Attributes
    ----------
    angle : int
        Angle of plate settlers (relative to being completely horizontal)
    S : float
        Edge to edge distance between plates
    thickness : float
        Thickness of PVC sheet used to make plate settlers
    L_cantilevered : float
        Maximum length of sed plate sticking out past module pipes without any
        additional support. The goal is to prevent floppy modules that don't
        maintain constant distances between the plates
tank : dict
    A dictionary containing variables relating to the concrete portion of the
    sedimentation tank
    Attributes
    ----------
    W : float
        Width of the sedimentation tank. Based off of the width of the PVC
        sheet used to make plate settlers
    L : float
        Length of the sedimentation tank. Based off of the length of a manifold
        pipe
    vel_up : float
        Upflow velocity through a sedimentation tank used as basis of design
manifold : dict
    A dictionary containg variables relating to the inlet manifold,
    exit manifold, and diffusers
    Attributes
    ----------
    ratio_Q_orifice : float
        Acceptable ratio of min to max flow through the manifold orifices
    diffuser : dict
        A dictionary containing variables relating to the diffuser
        Attributes
        ----------
        thickness_wall : float
            Wall thickness of a diffuser
        vel_max : float
            Maximum velocity through a diffuser
        A : float
            Area of a diffuser when viewed down the length of the manifold
    exit_man : dict
        A dictionary containing variables relating to the exit manifold
        Attributes
        ----------
        hl_orifice : float
            Headloss through an orifice in the exit manifold
        N_orifices : int
            Number of orifices in the exit manifold
"""
from aguaclara.play import*

# again we will change this to an important statment from the URL of  aide_template repo
"""sed_dict = {
            'thickness_wall': 0.15*u.m,
            'plate_settlers': {
                'angle': 60*u.deg, 'S': 2.5*u.cm,
                'thickness': 2*u.mm, 'L_cantilevered': 20*u.cm,
                },
            'tank': {
                'W': 42*u.inch, 'L': 5.8*u.m, 'vel_up': 1*u.mm/u.s
            },
            'manifold': {
                'ratio_Q_man_orifice': 0.8,
                'diffuser': {
                    'thickness_wall': 1.17*u.inch, 'vel_max': 442.9*u.mm/u.s,
                    'A': 0.419*u.inch**2
                },
                'exit_man': {
                    'hl_orifice': 4*u.cm, 'N_orifices': 58
                }
            }
}
"""

class SedimentationTank:
    THICKNESS_WALL = 0.15 * u.m

    PLATE_SETTLERS_ANGLE = 60 * u.deg

    PLATE_SETTLERS_S = 2.5 * u.cm

    PLATE_SETTLERS_THICKNESS = 2 * u.mm

    PLATE_SETTLERS_L_CANTILEVERED = 20 * u.cm

    PLATE_SETTLERS_VEL_CAPTURE = 0.12 * u.mm / u.s

    TANK_W = 42 * u.inch

    TANK_L = 5.8 * u.m

    TANK_VEL_UP = 1 * u.mm / u.s

    MANIFOLD_RATIO_Q_MAN_ORIFICE = 0.8

    MANIFOLD_DIFFUSER_THICKNESS_WALL = 1.17 * u.inch

    MANIFOLD_DIFFUSER_VEL_MAX = 442.9 * u.mm / u.s

    MANIFOLD_DIFFUSER_A = 0.419 * u.inch ** 2

    MANIFOLD_EXIT_MAN_HL_ORIFICE = 4 * u.cm

    MANIFOLD_EXIT_MAN_N_ORIFICES = 58

    @property
    def n_sed_plates_max(self):
        """Return the maximum possible number of plate settlers in a module given
        plate spacing, thickness, angle, and unsupported length of plate settler.
        Parameters
        ----------
        S_plate : float
            Edge to edge distance between plate settlers
        thickness_plate : float
            Thickness of PVC sheet used to make plate settlers
        L_sed_plate_cantilevered : float
            Maximum length of sed plate sticking out past module pipes without any
            additional support. The goal is to prevent floppy modules that don't
            maintain constant distances between the plates
        angle_plate : float
            Angle of plate settlers
        Returns
        -------
        int
            Maximum number of plates
        Examples
        --------
        >>> from aide_design.play import*
        >>>
        """
        B_plate = self.PLATE_SETTLERS_S + self.PLATE_SETTLERS_THICKNESS
        return math.floor((self.PLATE_SETTLERS_L_CANTILEVERED.magnitude / B_plate.magnitude
                          * np.tan(self.PLATE_SETTLERS_ANGLE.to(u.rad).magnitude)) + 1)

    @property
    def w_diffuser_inner_min(self):
        """Return the minimum inner width of each diffuser in the sedimentation tank.
        Parameters
        ----------
        sed_inputs : dict
            A dictionary of all of the constant inputs needed for sedimentation tank
            calculations. Can be found in sed.yaml
        Returns
        -------
        float
            Minimum inner width of each diffuser in the sedimentation tank
        Examples
        --------
        >>> from aide_design.play import*
        >>>
        """
        return ((self.TANK_VEL_UP.to(u.inch/u.s).magnitude /
                 self.MANIFOLD_DIFFUSER_VEL_MAX.to(u.inch/u.s).magnitude)
                 * self.TANK_W)

    @property
    def w_diffuser_inner(self):
        """Return the inner width of each diffuser in the sedimentation tank.
        Parameters
        ----------
        sed_inputs : dict
            A dictionary of all of the constant inputs needed for sedimentation tank
            calculations can be found in sed.yaml
        Returns
        -------
        float
            Inner width of each diffuser in the sedimentation tank
        Examples
        --------
        >>> from aide_design.play import*
        >>>
        """
        return ut.ceil_nearest(self.w_diffuser_inner_min.magnitude,
                               (np.arange(1/16, 1/4, 1/16)*u.inch).magnitude)*u.inch

    @property
    def w_diffuser_outer(self):
        """Return the outer width of each diffuser in the sedimentation tank.
        Parameters
        ----------
        sed_inputs : dict
            A dictionary of all of the constant inputs needed for sedimentation tank
            calculations can be found in sed.yaml
        Returns
        -------
        float
            Outer width of each diffuser in the sedimentation tank
        Examples
        --------
        >>> from aide_design.play import*
        >>>
        """
        return (self.w_diffuser_inner_min +
                (2 * self.MANIFOLD_DIFFUSER_THICKNESS_WALL)).to(u.m).magnitude

    @property
    def L_diffuser_outer(self):
        """Return the outer length of each diffuser in the sedimentation tank.
        Parameters
        ----------
        sed_inputs : dict
            A dictionary of all of the constant inputs needed for sedimentation tank
            calculations can be found in sed.yaml
        Returns
        -------
        float
            Outer length of each diffuser in the sedimentation tank
        Examples
        --------
        >>> from aide_design.play import*
        >>>
        """
        return ((self.MANIFOLD_DIFFUSER_A /
               (2 * self.MANIFOLD_DIFFUSER_THICKNESS_WALL))
               - self.w_diffuser_inner.to(u.inch)).to(u.m).magnitude

    @property
    def L_diffuser_inner(self):
        """Return the inner length of each diffuser in the sedimentation tank.
        Parameters
        ----------
        sed_inputs : dict
            A dictionary of all of the constant inputs needed for sedimentation tank
            calculations can be found in sed.yaml
        Returns
        -------
        float
            Inner length of each diffuser in the sedimentation tank
        Examples
        --------
        >>> from aide_design.play import*
        >>>
        """
        return (self.L_diffuser_outer -
                (2 * (self.MANIFOLD_DIFFUSER_THICKNESS_WALL).to(u.m)).magnitude)

    @property
    def q_diffuser(self):
        """Return the flow through each diffuser.
        Parameters
        ----------
        sed_inputs : dict
            A dictionary of all of the constant inputs needed for sedimentation tank
            calculations can be found in sed.yaml
        Returns
        -------
        float
            Flow through each diffuser in the sedimentation tank
        Examples
        --------
        >>> from aide_design.play import*
        >>>
        """
        return (self.TANK_VEL_UP.to(u.m/u.s) *
                 self.TANK_W.to(u.m) *
                 self.L_diffuser_outer).magnitude

    @property
    def vel_sed_diffuser(self):
        """Return the velocity through each diffuser.
        Parameters
        ----------
        sed_inputs : dict
            A dictionary of all of the constant inputs needed for sedimentation tank
            calculations can be found in sed.yaml
        Returns
        -------
        float
            Flow through each diffuser in the sedimentation tank
        Examples
        --------
        >>> from aide_design.play import*
        >>>
        """
        return (q_diffuser().magnitude
                / (w_diffuser_inner(w_tank) * L_diffuser_inner(w_tank)).magnitude)

    @property
    def q_tank(self):
        """Return the maximum flow through one sedimentation tank.
        Parameters
        ----------
        sed_inputs : dict
            A dictionary of all of the constant inputs needed for sedimentation tank
            calculations can be found in sed.yaml
        Returns
        -------
        float
            Maximum flow through one sedimentation tank
        Examples
        --------
        >>> from aide_design.play import*
        >>>
        """
        return (self.TANK_L * self.TANK_VEL_UP.to(u.m/u.s) *
                self.TANK_W.to(u.m)).magnitude

    @property
    def vel_inlet_man_max(self):
        """Return the maximum velocity through the manifold.
        Parameters
        ----------
        sed_inputs : dict
            A dictionary of all of the constant inputs needed for sedimentation tank
            calculations can be found in sed.yaml
        Returns
        -------
        float
            Maximum velocity through the manifold.
        Examples
        --------
        >>> from aide_design.play import*
        >>>
        """
        vel_manifold_max = (self.MANIFOLD_DIFFUSER_VEL_MAX.to(u.m/u.s).magnitude *
            sqrt(2*((1-(self.MANIFOLD_RATIO_Q_MAN_ORIFICE)**2)) /
            (((MANIFOLD_RATIO_Q_MAN_ORIFICE)**2)+1)))
        return vel_manifold_max

    @property
    def n_tanks(self, Q_plant):
        """Return the number of sedimentation tanks required for a given flow rate.
        Parameters
        ----------
        Q_plant : float
            Total plant flow rate
        sed_inputs : dict
            A dictionary of all of the constant inputs needed for sedimentation tank
            calculations can be found in sed.yaml
        Returns
        -------
        int
            Number of sedimentation tanks required for a given flow rate.
        Examples
        --------
        >>> from aide_design.play import*
        >>>
        """
        q = q_tank().magnitude
        return (int(np.ceil(Q_plant / q)))

    @property
    def L_channel(self, Q_plant):
        """Return the length of the inlet and exit channels for the sedimentation tank.
        Parameters
        ----------
        Q_plant : float
            Total plant flow rate
        sed_inputs : dict
            A dictionary of all of the constant inputs needed for sedimentation tank
            calculations can be found in sed.yaml
        Returns
        -------
        float
            Length of the inlet and exit channels for the sedimentation tank.
        Examples
        --------
        >>> from aide_design.play import*
        >>>
        """
        n_tanks = n_tanks(Q_plant, sed_inputs)
        return ((n_tanks * self.TANK_W) + self.THICKNESS_WALL +
                ((n_tanks-1) * self.THICKNESS_WALL))

    ###@property
    ###@ut.list_handler
    ###def ID_exit_man(self, Q_plant, temp):
        """Return the inner diameter of the exit manifold by guessing an initial
        diameter then iterating through pipe flow calculations until the answer
        converges within 1%% error
        Parameters
        ----------
        Q_plant : float
            Total plant flow rate
        temp : float
            Design temperature
        sed_inputs : dict
            A dictionary of all of the constant inputs needed for sedimentation tank
            calculations can be found in sed.yaml
        Returns
        -------
        float
            Inner diameter of the exit manifold
        Examples
        --------
        >>> from aide_design.play import*
        >>>
        """
        #Inputs do not need to be checked here because they are checked by
        #functions this function calls.
        """nu = pc.viscosity_dynamic(temp)
        hl = self.MANIFOLD_EXIT_MAN_HL_ORIFICE.to(u.m)
        L = self.TANK_L
        N_orifices = self.MANIFOLD_EXIT_MAN_N_ORIFICES
        K_minor = con.K_MINOR_PIPE_EXIT
        pipe_rough = mat.PIPE_ROUGH_PVC.to(u.m)

        D = max(diam_pipemajor(Q_plant, hl, L, nu, pipe_rough).magnitude,
                       diam_pipeminor(Q_plant, hl, K_minor).magnitude)
        err = 1.00
        while err > 0.01:
                D_prev = D
                f = pc.fric(Q_plant, D_prev, nu, pipe_rough)
                D = ((8*Q_plant**2 / pc.GRAVITY.magnitude * np.pi**2 * hl) *
                        (((f*L/D_prev + K_minor) * (1/3 * 1/) *
                        (1/3 + 1/(2 * N_orifices) + 1/(6 * N_orifices**2)))
                        / (1 - self.MANIFOLD_RATIO_Q_MAN_ORIFICE**2)))**0.25
                err = abs(D_prev - D) / ((D + D_prev) / 2)
        return D """


    @property
    def D_exit_man_orifice(self, Q_plant, drill_bits):
        """Return the diameter of the orifices in the exit manifold for the sedimentation tank.
        Parameters
        ----------
        Q_plant : float
            Total plant flow rate
        drill_bits : list
            List of possible drill bit sizes
        sed_inputs : dict
            A dictionary of all of the constant inputs needed for sedimentation tank
            calculations can be found in sed.yaml
        Returns
        -------
        float
            Diameter of the orifices in the exit manifold for the sedimentation tank.
        Examples
        --------
        >>> from aide_design.play import*
        >>>
        """
        Q_orifice = Q_plant/self.MANIFOLD_EXIT_MAN_N_ORIFICES
        D_orifice = np.sqrt(Q_orifice**4)/(np.pi * con.RATIO_VC_ORIFICE * np.sqrt(2 * pc.GRAVITY.magnitude * self.MANIFOLD_EXIT_MAN_HL_ORIFICE.magnitude))
        return ut.ceil_nearest(D_orifice, drill_bits)


    @property
    def L_sed_plate(self):
        """Return the length of a single plate in the plate settler module based on
        achieving the desired capture velocity
        Parameters
        ----------
        sed_inputs : dict
            A dictionary of all of the constant inputs needed for sedimentation tank
            calculations can be found in sed.yaml
        Returns
        -------
        float
            Length of a single plate
        Examples
        --------
        >>> from aide_design.play import*
        >>>
        """
        L_sed_plate = ((self.PLATE_SETTLERS_S * ((self.TANK_VEL_UP/self.PLATE_SETTLERS_VEL_CAPTURE)-1)
                      + self.PLATE_SETTLERS_THICKNESS * (self.TANK_VEL_UP/self.PLATE_SETTLERS_VEL_CAPTURE))
                     / (np.sin(self.PLATE_SETTLERS_ANGLE) * np.cos(self.PLATE_ANGLE))
                     ).to(u.m)
        return L_sed_plates