"""This file contains all the functions needed to design a sedimentation tank
for an AguaClara plant.

"""
import numpy as np
import math
from aide_design.shared.units import unit_registry as u
import aide_design.shared.utility as ut
import aide_design.shared.physchem as pc
import aide_design.shared.constants as con
import aide_design.shared.materials_database as mat
import aide_design.shared.pipedatabase as pipe


@u.wraps(None, [], False)
def n_sed_plates_max(S_plate=2.5*u.cm, thickness_plate=2*u.mm,
                     angle_plate=60*u.deg, L_plate_cantilevered=20*u.cm):
    """Return the maximum possible number of plate settlers in a module given
    plate spacing, thickness, angle, and unsupported length of plate settler.

    Parameters
    ----------
    S_plate : float
        Edge to edge distance between plate settlers

    thickness_plate : float
        Thickness of PVC sheet used to make plate settlers

    L_plate_cantilevered : float
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
    >>> from aide_design.play import *
    >>> n_sed_plates_max()
    13
    """
    angle_plate = angle_plate.to(u.rad).magnitude
    S_plate = S_plate.to(u.cm).magnitude
    L_plate_cantilevered = L_plate_cantilevered.to(u.cm).magnitude
    thickness_plate = thickness_plate.to(u.cm).magnitude

    B_plate = S_plate + thickness_plate
    return math.floor(((L_plate_cantilevered / B_plate)
                      * np.tan(angle_plate)) + 1)

@u.wraps(u.inch, [], False)
def w_diffuser_inner_min(vel_up=1*u.mm/u.s, vel_max_diffuser=442.9*u.mm/u.s,
                         W_tank=42*u.inch):
    """Return the minimum inner width of each diffuser in the sedimentation tank.

    Parameters
    ----------
    vel_up : float
        Upflow velocity through a sedimentation tank used as basis of design

    vel_max_diffuser : float
        Maximum velocity through a diffuser

    W_tank : float
        Width of the sedimentation tank. Based off of the width of the PVC
        sheet used to make plate settlers

    Returns
    -------
    float
        Minimum inner width of each diffuser in the sedimentation tank

    Examples
    --------
    >>> from aide_design.play import *
    >>> w_diffuser_inner_min()
    0.09482953262587492 inch
    """
    return ((vel_up.to(u.inch/u.s).magnitude /
             vel_max_diffuser.to(u.inch/u.s).magnitude)
            * W_tank.to(u.inch).magnitude)

@u.wraps(u.m, [], False)
def w_diffuser_inner(vel_up=1*u.mm/u.s, vel_max_diffuser=442.9*u.mm/u.s,
                     W_tank=42*u.inch):
    """Return the inner width of each diffuser in the sedimentation tank.

    Parameters
    ----------
    vel_up : float
        Upflow velocity through a sedimentation tank used as basis of design

    vel_max_diffuser : float
        Maximum velocity through a diffuser

    W_tank : float
        Width of the sedimentation tank. Based off of the width of the PVC
        sheet used to make plate settlers

    Returns
    -------
    float
        Inner width of each diffuser in the sedimentation tank

    Examples
    --------
    >>> from aide_design.play import *
    >>> w_diffuser_inner()
    0.003175 meter
    """
    return ut.ceil_nearest(w_diffuser_inner_min(vel_up, vel_max_diffuser,
                                                W_tank),
                           (np.arange(1/16,1/4,1/16)*u.inch)).to(u.m).magnitude

@u.wraps(u.m, [], False)
def w_diffuser_outer(vel_up=1*u.mm/u.s, vel_max_diffuser=442.9*u.mm/u.s,
                     W_tank=42*u.inch, thickness_diffuser_wall=1.17*u.inch):
    """Return the outer width of each diffuser in the sedimentation tank.

    Parameters
    ----------
    vel_up : float
        Upflow velocity through a sedimentation tank used as basis of design

    vel_max_diffuser : float
        Maximum velocity through a diffuser

    W_tank : float
        Width of the sedimentation tank. Based off of the width of the PVC
        sheet used to make plate settlers

    thickness_diffuser_wall : float
        Wall thickness of a diffuser

    Returns
    -------
    float
        Outer width of each diffuser in the sedimentation tank

    Examples
    --------
    >>> from aide_design.play import *
    >>> w_diffuser_outer()
    0.06184467012869722 meter
    """
    return (w_diffuser_inner_min(vel_up, vel_max_diffuser, W_tank).to(u.m).magnitude +
            (2 * thickness_diffuser_wall).to(u.m).magnitude)

@u.wraps(u.m, [], False)
def L_diffuser_outer(vel_up=1*u.mm/u.s, vel_max_diffuser=442.9*u.mm/u.s,
                     W_tank=42*u.inch, thickness_diffuser_wall=1.17*u.inch,
                     A_diffuser=0.419*u.inch**2):
    """Return the outer length of each diffuser in the sedimentation tank.

    Parameters
    ----------
    vel_up : float
        Upflow velocity through a sedimentation tank used as basis of design

    vel_max_diffuser : float
        Maximum velocity through a diffuser

    W_tank : float
        Width of the sedimentation tank. Based off of the width of the PVC
        sheet used to make plate settlers

    thickness_diffuser_wall : float
        Wall thickness of a diffuser

    A_diffuser : float
        Area of a diffuser when viewed down the length of the manifold

    Returns
    -------
    float
        Outer length of each diffuser in the sedimentation tank

    Examples
    --------
    >>> from aide_design.play import *
    >>> L_diffuser_outer()
    0.001373119658119658 meter
    """
    return ((A_diffuser / (2 * thickness_diffuser_wall))
            - w_diffuser_inner(vel_up, vel_max_diffuser,
                               W_tank).to(u.inch)).to(u.m).magnitude

@u.wraps(u.m, [], False)
def L_diffuser_inner(vel_up=1*u.mm/u.s, vel_max_diffuser=442.9*u.mm/u.s,
                     W_tank=42*u.inch, thickness_diffuser_wall=1.17*u.inch,
                     A_diffuser=0.419*u.inch**2):
    """Return the inner length of each diffuser in the sedimentation tank.

    Parameters
    ----------
    vel_up : float
        Upflow velocity through a sedimentation tank used as basis of design

    vel_max_diffuser : float
        Maximum velocity through a diffuser

    W_tank : float
        Width of the sedimentation tank. Based off of the width of the PVC
        sheet used to make plate settlers

    thickness_diffuser_wall : float
        Wall thickness of a diffuser

    A_diffuser : float
        Area of a diffuser when viewed down the length of the manifold

    Returns
    -------
    float
        Inner length of each diffuser in the sedimentation tank

    Examples
    --------
    >>> from aide_design.play import *
    >>> L_diffuser_inner()
    -0.17988788034188033 meter
    """
    return (L_diffuser_outer(vel_up, vel_max_diffuser, W_tank,
                             thickness_diffuser_wall, A_diffuser) -
                            (2 * (thickness_diffuser_wall).to(u.m))).magnitude

@u.wraps(u.m**3/u.s, [None], False)
def q_diffuser(vel_up=1*u.mm/u.s, vel_max_diffuser=442.9*u.mm/u.s,
                     W_tank=42*u.inch, thickness_diffuser_wall=1.17*u.inch,
                     A_diffuser=0.419*u.inch**2):
    """Return the flow through each diffuser.

    Parameters
    ----------
    vel_up : float
        Upflow velocity through a sedimentation tank used as basis of design

    vel_max_diffuser : float
        Maximum velocity through a diffuser

    W_tank : float
        Width of the sedimentation tank. Based off of the width of the PVC
        sheet used to make plate settlers

    thickness_diffuser_wall : float
        Wall thickness of a diffuser

    A_diffuser : float
        Area of a diffuser when viewed down the length of the manifold

    Returns
    -------
    float
        Flow through each diffuser in the sedimentation tank

    Examples
    --------
    >>> from aide_design.play import *
    >>> q_diffuser()
    1.4648440512820511e-06 meter3/second

    """
    return (vel_up.to(u.m/u.s) * W_tank.to(u.m) *
            L_diffuser_outer(vel_up, vel_max_diffuser, W_tank,
            thickness_diffuser_wall, A_diffuser).to(u.m)).magnitude

@u.wraps(u.m/u.s, [], False)
def vel_sed_diffuser(vel_up=1*u.mm/u.s, vel_max_diffuser=442.9*u.mm/u.s,
                     W_tank=42*u.inch, thickness_diffuser_wall=1.17*u.inch,
                     A_diffuser=0.419*u.inch**2):
    """Return the velocity through each diffuser.

    Parameters
    ----------
    vel_up : float
        Upflow velocity through a sedimentation tank used as basis of design

    vel_max_diffuser : float
        Maximum velocity through a diffuser

    W_tank : float
        Width of the sedimentation tank. Based off of the width of the PVC
        sheet used to make plate settlers

    thickness_diffuser_wall : float
        Wall thickness of a diffuser

    A_diffuser : float
        Area of a diffuser when viewed down the length of the manifold

    Returns
    -------
    float
        Flow through each diffuser in the sedimentation tank

    Examples
    --------
    >>> from aide_design.play import *
    >>> vel_sed_diffuser()
    0.005714584693732781 meter/second

    """
    return (q_diffuser(vel_up, W_tank).to(u.m**3/u.s).magnitude /
            (w_diffuser_inner(vel_up, vel_max_diffuser, W_tank).to(u.m) *
            L_diffuser_inner(vel_up, vel_max_diffuser, W_tank,
                             thickness_diffuser_wall, A_diffuser).to(u.m)).magnitude)

@u.wraps(u.m**3/u.s, [], False)
def q_tank(vel_up=1*u.mm/u.s, W_tank=42*u.inch, L_tank=5.8*u.m):
    """Return the maximum flow through one sedimentation tank.

    Parameters
    ----------
    vel_up : float
        Upflow velocity through a sedimentation tank used as basis of design

    W_tank : float
        Width of the sedimentation tank. Based off of the width of the PVC
        sheet used to make plate settlers

    L_tank : float
        Length of the sedimentation tank. Based off of the length of a manifold
        pipe

    Returns
    -------
    float
        Maximum flow through one sedimentation tank

    Examples
    --------
    >>> from aide_design.play import *
    >>> q_tank()
    0.00618744 meter3/second

    """
    return (L_tank.to(u.m) * vel_up.to(u.m/u.s) * W_tank.to(u.m)).magnitude

@u.wraps(u.m/u.s, [], False)
def vel_inlet_man_max(vel_max_diffuser=442.9*u.mm/u.s, ratio_Q_man_orifice=0.8):
    """Return the maximum velocity through the manifold.

    Parameters
    ----------
    vel_max_diffuser : float
        Maximum velocity through a diffuser

    ratio_Q_man_orifice : float
        Acceptable ratio of min to max flow through the manifold orifices

    Returns
    -------
    float
        Maximum velocity through the manifold.

    Examples
    --------
    >>> from aide_design.play import*
    >>> vel_inlet_man_max()
    0.29346073739129713 meter/second

    """
    vel_manifold_max = (vel_max_diffuser.to(u.m/u.s).magnitude *
                        np.sqrt(2*((1-(ratio_Q_man_orifice)**2)) /
                        (((ratio_Q_man_orifice)**2)+1)))
    return vel_manifold_max

@u.wraps(None, [u.m**3/u.s], False)
def n_tanks(Q_plant, vel_up=1*u.mm/u.s, W_tank=42*u.inch, L_tank=5.8*u.m):
    """Return the number of sedimentation tanks required for a given flow rate.

    Parameters
    ----------
    Q_plant : float
        Total plant flow rate

    vel_up : float
        Upflow velocity through a sedimentation tank used as basis of design

    W_tank : float
        Width of the sedimentation tank. Based off of the width of the PVC
        sheet used to make plate settlers

    L_tank : float
        Length of the sedimentation tank. Based off of the length of a manifold
        pipe

    Returns
    -------
    int
        Number of sedimentation tanks required for a given flow rate.

    Examples
    --------
    >>> from aide_design.play import *
    >>> n_tanks(20*u.L/u.s)
    4
    >>> n_tanks(60*u.L/u.s)
    10

    """
    q = q_tank(vel_up, W_tank, L_tank).magnitude
    return (int(np.ceil(Q_plant / q)))

@u.wraps(u.m, [u.m**3/u.s], False)
def L_channel(Q_plant, vel_up=1*u.mm/u.s, W_tank=42*u.inch, L_tank=5.8*u.m,
              thickness_wall = 0.15*u.m):
    """Return the length of the inlet and exit channels for the sedimentation tank.

    Parameters
    ----------
    Q_plant : float
        Total plant flow rate

    vel_up : float
        Upflow velocity through a sedimentation tank used as basis of design

    W_tank : float
        Width of the sedimentation tank. Based off of the width of the PVC
        sheet used to make plate settlers

    L_tank : float
        Length of the sedimentation tank. Based off of the length of a manifold
        pipe

    thickness_wall : float
        Thickness of walls in the sedimentation unit process

    Returns
    -------
    float
        Length of the inlet and exit channels for the sedimentation tank.

    Examples
    --------
    >>> from aide_design.play import *
    >>> L_channel(20*u.L/u.s)
    4.8672 meter
    >>> L_channel(60*u.L/u.s)
    12.168 meter

    """
    n_tank = n_tanks(Q_plant, vel_up=1*u.mm/u.s, W_tank=42*u.inch, L_tank=5.8*u.m)
    return ((n_tank * W_tank.to(u.m)) + thickness_wall.to(u.m) +
            ((n_tank-1) * thickness_wall.to(u.m))).magnitude

@u.wraps(u.m, [u.m**3/u.s, u.degK], False)
@ut.list_handler
def ID_exit_man(Q_plant, temp, hl_orifice_exit_man=4*u.cm, L_tank=5.8*u.m,
                N_orifices_exit_man=58, ratio_Q_man_orifice=0.8):
    """Return the inner diameter of the exit manifold by guessing an initial
    diameter then iterating through pipe flow calculations until the answer
    converges within 1%% error

    Parameters
    ----------
    Q_plant : float
        Total plant flow rate

    temp : float
        Design temperature

    hl_orifice_exit_man : float
        Headloss through an orifice in the exit manifold

    L_tank : float
        Length of the sedimentation tank. Based off of the length of a manifold
        pipe

    N_orifices_exit_man : int
        Number of orifices in the exit manifold

    ratio_Q_man_orifice : float
        Acceptable ratio of min to max flow through the manifold orifices

    Returns
    -------
    float
        Inner diameter of the exit manifold

    Examples
    --------
    >>> from aide_design.play import *
    >>> ID_exit_man(20*u.L/u.s, 20*u.degC)
    0.21247905143432252 meter
    """
    #Inputs do not need to be checked here because they are checked by
    #functions this function calls.
    nu = pc.viscosity_dynamic(temp)
    hl = hl_orifice_exit_man.to(u.m)
    L = L_tank.to(u.m)
    N_orifices = N_orifices_exit_man
    K_minor = con.K_MINOR_PIPE_EXIT
    pipe_rough = mat.PIPE_ROUGH_PVC.to(u.m)

    D = max(pc.diam_pipemajor(Q_plant, hl, L, nu, pipe_rough).magnitude,
                   pc.diam_pipeminor(Q_plant, hl, K_minor).magnitude)
    err = 1.00
    while err > 0.01:
            D_prev = D
            f = pc.fric(Q_plant, D_prev, nu, pipe_rough)
            D = ((8*Q_plant**2 / con.GRAVITY.magnitude * np.pi**2 * hl.magnitude) *
                    (1 + ((f*L.magnitude/D_prev + K_minor) *
                    (1/3 + 1/(2 * N_orifices) + 1/(6 * N_orifices**2)))
                    / (1 - ratio_Q_man_orifice**2)))**0.25
            err = abs(D_prev - D) / ((D + D_prev) / 2)
    return D

@u.wraps(u.m, [u.m**3/u.s, u.inch], False)
def D_exit_man_orifice(Q_plant, drill_bits, N_orifices_exit_man=58,
                       hl_orifice_exit_man=4*u.cm):
    """Return the diameter of the orifices in the exit manifold for the sedimentation tank.

    Parameters
    ----------
    Q_plant : float
        Total plant flow rate

    drill_bits : list
        List of possible drill bit sizes

    N_orifices_exit_man : int
        Number of orifices in the exit manifold

    hl_orifice_exit_man : float
        Headloss through an orifice in the exit manifold

    Returns
    -------
    float
        Diameter of the orifices in the exit manifold for the sedimentation tank.

    Examples
    --------
    >>> from aide_design.play import*
    >>> D_exit_man_orifice(20*u.L/u.s, mat.DIAM_DRILL_ENG)
    0.03125 meter

    """
    Q_orifice = Q_plant/N_orifices_exit_man
    D_orifice = np.sqrt(Q_orifice**4)/(np.pi *
                con.RATIO_VC_ORIFICE * np.sqrt(2 * con.GRAVITY.magnitude *
                hl_orifice_exit_man.to(u.m).magnitude))
    return ut.ceil_nearest(D_orifice, drill_bits)

@u.wraps(u.m, [None], False)
def L_sed_plate(S_plate=2.5*u.cm, vel_up=1*u.mm/u.s, vel_capture=0.12*u.mm/u.s,
                thickness_plate=2*u.mm, angle_plate=60*u.deg):
    """Return the length of a single plate in the plate settler module based on
    achieving the desired capture velocity

    Parameters
    ----------
    S_plate : float
        Edge to edge distance between plate settlers

    vel_up : float
        Upflow velocity through a sedimentation tank used as basis of design

    vel_capture : float
        Capture velocity of the plate settlers. This is the velocity of the
        floc that is only barely settled-out, or "captured", during the
        sedimentation process

    thickness_plate : float
        Thickness of PVC sheet used to make plate settlers

    angle_plate : float
        Angle of plate settlers

    Returns
    -------
    float
        Length of a single plate

    Examples
    --------
    >>> from aide_design.play import*
    >>> L_sed_plate()
    0.4618802153517006 meter

    """
    return ((S_plate * ((vel_up/vel_capture)-1)
                 + thickness_plate * (vel_up/vel_capture))
                 / (np.sin(angle_plate.to(u.rad)) * np.cos(angle_plate.to(u.rad))
                 )).to(u.m).magnitude

@u.wraps(u.m, [u.m**3/u.s, u.degK], False)
def depth_end_floc(Q_plant, temp, depth_above_exit_man=5*u.cm, sdr_exit_man=26,
                   plate_settler_to_exit_man=5*u.cm, angle_plate=60*u.deg,
                   floc_blanket_to_plate_settler=10*u.cm,
                   depth_floc_blanket=25*u.cm, angle_bottom_tank=50*u.deg,
                   W_tank=42*u.inch, L_tank=5.8*u.m, hl_orifice_exit_man=4*u.cm,
                   N_orifices_exit_man=58, ratio_Q_man_orifice=0.8, S_plate=2.5*u.cm,
                   vel_up=1*u.mm/u.s, vel_capture=0.12*u.mm/u.s, thickness_plate=2*u.mm,
                   sed_bottom_to_floc_bottom=0.194*u.m):
    """Return the depth of water at the exit of the flocculator.

    The depth of water at the end of flocculator is dictated by the depth of
    water in the sedimentation tank. To find the depth of water in the
    sedimentation tank, the following heights were summed from the bottom of
    the sedimentation tank to the top.
        - Vertical height of the sloped portion of the sedimentation
          tank bottom.
        - Vertical height of the floc blanket.
        - Vertical distance between the plate settlers and floc blanket.
        - Vertical height of plate settlers.
        - Vertical distance between the plate settlers and exit manifold.
        - Outer diameter of exit manifold.
        - Vertical depth of water above top of the exit manifold.

    After summing the heights in the sedimentation tank, a correction is applied
    to account for the difference in elevation between the bottom of the
    sedimentation tank and the bottom of the flocculator.

    Parameters
    ----------
    Q_plant : float
        Total plant flow rate

    temp : float
        Design temperature

    depth_above_exit_man : float
        Depth of water above the exit manifold in the sedimentation tank

    sdr_exit_man : float
        SDR (standard dimension ratio) of the exit manifold

    angle_plate : float
        Angle of plate settlers (relative to being completely horizontal)

    plate_settler_to_exit_man : float
        Vertical distance between the plate settler and exit manifold

    floc_blanket_to_plate_settler : float
        Vertical distance between the floc blanket and plate settler

    depth_floc_blanket : float
        Depth of the floc blanket

    angle_bottom_tank : float
        Angle of the sloped part of the sed tank

    W_tank : float
        Width of the sedimentation tank. Based off of the width of the PVC
        sheet used to make plate settlers

    L_tank : float
        Length of the sedimentation tank. Based off of the length of a manifold
        pipe

    hl_orifice_exit_man : float
        Headloss through an orifice in the exit manifold

    N_orifices_exit_man : int
        Number of orifices in the exit manifold

    ratio_Q_man_orifice : float
        Acceptable ratio of min to max flow through the manifold orifices

    S_plate : float
        Edge to edge distance between plate settlers

    vel_up : float
        Upflow velocity through a sedimentation tank used as basis of design

    vel_capture : float
        Capture velocity of the plate settlers. This is the velocity of the
        floc that is only barely settled-out, or "captured", during the
        sedimentation process

    thickness_plate : float
        Thickness of PVC sheet used to make plate settlers

    sed_bottom_to_floc_bottom : float
        Vertical distance from the bottom of the sedimentation tank to the
        bottom of the flocculator channel

    Returns
    -------
    float
        Depth of water at the end of the flocculator

    Examples
    --------
    >>> from aide_design.play import*
    >>> depth_end_floc(20*u.L/u.s, 15*u.degC)
    1.5647313662897513 meter

    """
    ID_exit_man_ = ID_exit_man(Q_plant, temp, hl_orifice_exit_man, L_tank,
                    N_orifices_exit_man, ratio_Q_man_orifice)
    OD_exit_man_ = pipe.OD(pipe.ND_SDR_available(ID_exit_man_, sdr_exit_man))
    L_sed_plate_ = L_sed_plate(S_plate, vel_up, vel_capture, thickness_plate,
                               angle_plate)
    depth_sed_tank = ((W_tank*np.tan(angle_bottom_tank.to(u.rad))/2) + depth_floc_blanket +
            floc_blanket_to_plate_settler + (L_sed_plate_*np.sin(angle_plate.to(u.rad))
            + plate_settler_to_exit_man + OD_exit_man_ + depth_above_exit_man)).to(u.m)
    return (depth_sed_tank - sed_bottom_to_floc_bottom).magnitude
