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
from aide_design.play import*

# again we will change this to an important statment from the URL of  aide_template repo
sed_dict = {
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

@u.wraps(None, [None], False)
def n_sed_plates_max(sed_inputs=sed_dict):
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
    B_plate = sed_inputs['plate_settlers']['S'] + sed_inputs['plate_settlers']['thickness']
    return math.floor((sed_inputs['plate_settlers']['L_cantilevered'].magnitude / B_plate.magnitude
                      * np.tan(sed_inputs['plate_settlers']['angle'].to(u.rad).magnitude)) + 1)

@u.wraps(u.inch, [None], False)
def w_diffuser_inner_min(sed_inputs=sed_dict):
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
    return ((sed_inputs['tank']['vel_up'].to(u.inch/u.s).magnitude /
             sed_inputs['manifold']['diffuser']['vel_max'].to(u.inch/u.s).magnitude)
             * sed_inputs['tank']['W'])

@u.wraps(u.m, [None], False)
def w_diffuser_inner(sed_inputs=sed_dict):
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
    return ut.ceil_nearest(w_diffuser_inner_min(sed_inputs).magnitude,
                           (np.arange(1/16,1/4,1/16)*u.inch).magnitude)

@u.wraps(u.m, [None], False)
def w_diffuser_outer(sed_inputs=sed_dict):
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
    return (w_diffuser_inner_min(sed_inputs['tank']['W']) +
            (2 * sed_inputs['manifold']['diffuser']['thickness_wall'])).to(u.m).magnitude

@u.wraps(u.m, [None], False)
def L_diffuser_outer(sed_inputs=sed_dict):
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
    return ((sed_inputs['manifold']['diffuser']['A'] /
           (2 * sed_inputs['manifold']['diffuser']['thickness_wall']))
           - w_diffuser_inner(sed_inputs).to(u.inch)).to(u.m).magnitude

@u.wraps(u.m, [None], False)
def L_diffuser_inner(sed_inputs=sed_dict):
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
    return L_diffuser_outer(sed_inputs['tank']['W']) -
            (2 * (sed_inputs['manifold']['diffuser']['thickness_wall']).to(u.m)).magnitude)

@u.wraps(u.m**3/u.s, [None], False)
def q_diffuser(sed_inputs=sed_dict):
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
    return (sed_inputs['tank']['vel_up'].to(u.m/u.s) *
             sed_inputs['tank']['W'].to(u.m) *
             L_diffuser_outer(sed_inputs)).magnitude

@u.wraps(u.m/u.s, [None], False)
def vel_sed_diffuser(sed_inputs=sed_dict):
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
    return (q_diffuser(sed_inputs).magnitude
            / (w_diffuser_inner(w_tank) * L_diffuser_inner(w_tank)).magnitude)

@u.wraps(u.m**3/u.s, [None], False)
def q_tank(sed_inputs=sed_dict):
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
    return (sed_inputs['tank']['L'] * sed_inputs['tank']['vel_up'].to(u.m/u.s) *
            sed_inputs['tank']['W'].to(u.m)).magnitude

@u.wraps(u.m/u.s, [None], False)
def vel_inlet_man_max(sed_inputs=sed_dict):
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
    vel_manifold_max = (sed_inputs['diffuser']['vel_max'].to(u.m/u.s).magnitude *
        sqrt(2*((1-(sed_inputs['manifold']['ratio_Q_man_orifice'])**2)) /
        (((sed_inputs['manifold']['ratio_Q_man_orifice'])**2)+1)))
    return vel_manifold_max

@u.wraps(None, [u.m**3/u.s, None], False)
def n_tanks(Q_plant, sed_inputs=sed_dict):
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
    q = q_tank(sed_inputs).magnitude
    return (int(np.ceil(Q_plant / q)))

@u.wraps(u.m, [u.m**3/u.s, None], False)
def L_channel(Q_plant, sed_inputs=sed_dict):
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
    return ((n_tanks * sed_inputs['tank']['W']) + sed_inputs['thickness_wall'] +
            ((n_tanks-1) * sed_inputs['thickness_wall']))

@u.wraps(u.m, [u.m**3/u.s, u.degK, None], False)
@ut.list_handler
def ID_exit_man(Q_plant, temp, sed_inputs=sed_dict):
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
    nu = pc.viscosity_dynamic(temp)
    hl = sed_input['manifold']['exit_man']['hl_orifice'].to(u.m)
    L = sed_ipnut['manifold']['tank']['L']
    N_orifices = sed_inputs['manifold']['exit_man']['N_orifices']
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
                    / (1 - sed_inputs['manifold']['ratio_Q_orifice']**2)))**0.25
            err = abs(D_prev - D) / ((D + D_prev) / 2)
    return D

@u.wraps(u.m, [u.m**3/u.s, u.inch, None], False)
def D_exit_man_orifice(Q_plant, drill_bits, sed_inputs=sed_dict):
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
    Q_orifice = Q_plant/sed_input['exit_man']['N_orifices']
    D_orifice = np.sqrt(Q_orifice**4)/(np.pi * con.RATIO_VC_ORIFICE * np.sqrt(2 * pc.GRAVITY.magnitude * sed_input['exit_man']['hl_orifice'].magnitude))
    return ut.ceil_nearest(D_orifice, drill_bits)


@u.wraps(u.m, [u.m**3/u.s, u.inch, None], False)
def L_sed_plate(sed_inputs=sed_dict):
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
    L_sed_plate = ((sed_input['plate_settlers']['S'] * ((sed_input['tank']['vel_up']/sed_input['plate_settlers']['vel_capture'])-1)
                  + sed_input['plate_settlers']['thickness'] * (sed_input['tank']['vel_up']/sed_input['plate_settlers']['vel_capture']))
                 / (np.sin(sed_input['plate_settlers']['angle']) * np.cos(sed_input['plate_settlers']['angle']))
                 ).to(u.m)
    return L_sed_plate