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

    vel_capture : float
        Capture velocity of the plate settlers. Capture velocity is the velocity
        of the floc that is only barely settled-out, or "captured", during the
        sedimentation process

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
                'vel_capture': 0.12*u.mm/u.s
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
    >>> from aide_design.play import*
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
    >>> from aide_design.play import*
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
    >>> from aide_design.play import*
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
    >>> from aide_design.play import*
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
    >>> from aide_design.play import*
    >>> L_diffuser_outer()
    0.001373119658119658 meter
    """
    return ((A_diffuser / (2 * thickness_diffuser_wall))
           - w_diffuser_inner(vel_up, vel_max_diffuser,
                              W_tank).to(u.inch)).to(u.m).magnitude

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
    >>> sed_dict = {
    ...         'thickness_wall': 0.15*u.m,
    ...         'plate_settlers': {
    ...             'angle': 60*u.deg, 'S': 2.5*u.cm,
    ...             'thickness': 2*u.mm, 'L_cantilevered': 20*u.cm,
    ...             'vel_capture': 0.12*u.mm/u.s
    ...             },
    ...         'tank': {
    ...             'W': 42*u.inch, 'L': 5.8*u.m, 'vel_up': 1*u.mm/u.s
    ...         },
    ...         'manifold': {
    ...             'ratio_Q_man_orifice': 0.8,
    ...             'diffuser': {
    ...                 'thickness_wall': 1.17*u.inch, 'vel_max': 442.9*u.mm/u.s,
    ...                 'A': 0.419*u.inch**2
    ...             },
    ...             'exit_man': {
    ...                 'hl_orifice': 4*u.cm, 'N_orifices': 58
    ...             }
    ...         }
    ... }
    >>> L_diffuser_inner()
    -0.17988788034188033 meter
    """
    return (L_diffuser_outer(sed_inputs) - \
    (2 * (sed_inputs['manifold']['diffuser']['thickness_wall']).to(u.m))).magnitude

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
    >>> sed_dict = {
    ...         'thickness_wall': 0.15*u.m,
    ...         'plate_settlers': {
    ...             'angle': 60*u.deg, 'S': 2.5*u.cm,
    ...             'thickness': 2*u.mm, 'L_cantilevered': 20*u.cm,
    ...             'vel_capture': 0.12*u.mm/u.s
    ...             },
    ...         'tank': {
    ...             'W': 42*u.inch, 'L': 5.8*u.m, 'vel_up': 1*u.mm/u.s
    ...         },
    ...         'manifold': {
    ...             'ratio_Q_man_orifice': 0.8,
    ...             'diffuser': {
    ...                 'thickness_wall': 1.17*u.inch, 'vel_max': 442.9*u.mm/u.s,
    ...                 'A': 0.419*u.inch**2
    ...             },
    ...             'exit_man': {
    ...                 'hl_orifice': 4*u.cm, 'N_orifices': 58
    ...             }
    ...         }
    ... }
    >>> q_diffuser()
    -0.00012849806594871792 meter3/second

    """
    return (sed_inputs['tank']['vel_up'].to(u.m/u.s) *
             sed_inputs['tank']['W'].to(u.m) *
             L_diffuser_outer(sed_inputs).to(u.m)).magnitude

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
    >>> sed_dict = {
    ...         'thickness_wall': 0.15*u.m,
    ...         'plate_settlers': {
    ...             'angle': 60*u.deg, 'S': 2.5*u.cm,
    ...             'thickness': 2*u.mm, 'L_cantilevered': 20*u.cm,
    ...             'vel_capture': 0.12*u.mm/u.s
    ...             },
    ...         'tank': {
    ...             'W': 42*u.inch, 'L': 5.8*u.m, 'vel_up': 1*u.mm/u.s
    ...         },
    ...         'manifold': {
    ...             'ratio_Q_man_orifice': 0.8,
    ...             'diffuser': {
    ...                 'thickness_wall': 1.17*u.inch, 'vel_max': 442.9*u.mm/u.s,
    ...                 'A': 0.419*u.inch**2
    ...             },
    ...             'exit_man': {
    ...                 'hl_orifice': 4*u.cm, 'N_orifices': 58
    ...             }
    ...         }
    ... }
    >>> vel_sed_diffuser()
    0.005714584693732781 meter/second

    """
    return (q_diffuser(sed_inputs).to(u.m**3/u.s).magnitude \
            / (w_diffuser_inner(sed_inputs).to(u.m) *
            L_diffuser_inner(sed_inputs).to(u.m)).magnitude)

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
    >>> sed_dict = {
    ...         'thickness_wall': 0.15*u.m,
    ...         'plate_settlers': {
    ...             'angle': 60*u.deg, 'S': 2.5*u.cm,
    ...             'thickness': 2*u.mm, 'L_cantilevered': 20*u.cm,
    ...             'vel_capture': 0.12*u.mm/u.s
    ...             },
    ...         'tank': {
    ...             'W': 42*u.inch, 'L': 5.8*u.m, 'vel_up': 1*u.mm/u.s
    ...         },
    ...         'manifold': {
    ...             'ratio_Q_man_orifice': 0.8,
    ...             'diffuser': {
    ...                 'thickness_wall': 1.17*u.inch, 'vel_max': 442.9*u.mm/u.s,
    ...                 'A': 0.419*u.inch**2
    ...             },
    ...             'exit_man': {
    ...                 'hl_orifice': 4*u.cm, 'N_orifices': 58
    ...             }
    ...         }
    ... }
    >>> q_tank()
    0.00618744 meter3/second

    """
    return (sed_inputs['tank']['L'] * sed_inputs['tank']['vel_up'].to(u.m/u.s) * \
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
    >>> sed_dict = {
    ...         'thickness_wall': 0.15*u.m,
    ...         'plate_settlers': {
    ...             'angle': 60*u.deg, 'S': 2.5*u.cm,
    ...             'thickness': 2*u.mm, 'L_cantilevered': 20*u.cm,
    ...             'vel_capture': 0.12*u.mm/u.s
    ...             },
    ...         'tank': {
    ...             'W': 42*u.inch, 'L': 5.8*u.m, 'vel_up': 1*u.mm/u.s
    ...         },
    ...         'manifold': {
    ...             'ratio_Q_man_orifice': 0.8,
    ...             'diffuser': {
    ...                 'thickness_wall': 1.17*u.inch, 'vel_max': 442.9*u.mm/u.s,
    ...                 'A': 0.419*u.inch**2
    ...             },
    ...             'exit_man': {
    ...                 'hl_orifice': 4*u.cm, 'N_orifices': 58
    ...             }
    ...         }
    ... }
    >>> vel_inlet_man_max()
    0.29346073739129713 meter/second

    """
    vel_manifold_max = (sed_inputs['manifold']['diffuser']['vel_max'].to(u.m/u.s).magnitude * \
        np.sqrt(2*((1-(sed_inputs['manifold']['ratio_Q_man_orifice'])**2)) / \
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
    >>> sed_dict = {
    ...         'thickness_wall': 0.15*u.m,
    ...         'plate_settlers': {
    ...             'angle': 60*u.deg, 'S': 2.5*u.cm,
    ...             'thickness': 2*u.mm, 'L_cantilevered': 20*u.cm,
    ...             'vel_capture': 0.12*u.mm/u.s
    ...             },
    ...         'tank': {
    ...             'W': 42*u.inch, 'L': 5.8*u.m, 'vel_up': 1*u.mm/u.s
    ...         },
    ...         'manifold': {
    ...             'ratio_Q_man_orifice': 0.8,
    ...             'diffuser': {
    ...                 'thickness_wall': 1.17*u.inch, 'vel_max': 442.9*u.mm/u.s,
    ...                 'A': 0.419*u.inch**2
    ...             },
    ...             'exit_man': {
    ...                 'hl_orifice': 4*u.cm, 'N_orifices': 58
    ...             }
    ...         }
    ... }
    >>> n_tanks(20*u.L/u.s)
    4
    >>> n_tanks(60*u.L/u.s)
    10

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
    >>> sed_dict = {
    ...         'thickness_wall': 0.15*u.m,
    ...         'plate_settlers': {
    ...             'angle': 60*u.deg, 'S': 2.5*u.cm,
    ...             'thickness': 2*u.mm, 'L_cantilevered': 20*u.cm,
    ...             'vel_capture': 0.12*u.mm/u.s
    ...             },
    ...         'tank': {
    ...             'W': 42*u.inch, 'L': 5.8*u.m, 'vel_up': 1*u.mm/u.s
    ...         },
    ...         'manifold': {
    ...             'ratio_Q_man_orifice': 0.8,
    ...             'diffuser': {
    ...                 'thickness_wall': 1.17*u.inch, 'vel_max': 442.9*u.mm/u.s,
    ...                 'A': 0.419*u.inch**2
    ...             },
    ...             'exit_man': {
    ...                 'hl_orifice': 4*u.cm, 'N_orifices': 58
    ...             }
    ...         }
    ... }
    >>> L_channel(20*u.L/u.s)
    4.8672 meter
    >>> L_channel(60*u.L/u.s)
    12.168 meter

    """
    n_tank = n_tanks(Q_plant, sed_inputs)
    return ((n_tank * sed_inputs['tank']['W'].to(u.m)) + sed_inputs['thickness_wall'].to(u.m) + \
            ((n_tank-1) * sed_inputs['thickness_wall'].to(u.m))).magnitude

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
    >>> sed_dict = {
    ...         'thickness_wall': 0.15*u.m,
    ...         'plate_settlers': {
    ...             'angle': 60*u.deg, 'S': 2.5*u.cm,
    ...             'thickness': 2*u.mm, 'L_cantilevered': 20*u.cm,
    ...             'vel_capture': 0.12*u.mm/u.s
    ...             },
    ...         'tank': {
    ...             'W': 42*u.inch, 'L': 5.8*u.m, 'vel_up': 1*u.mm/u.s
    ...         },
    ...         'manifold': {
    ...             'ratio_Q_man_orifice': 0.8,
    ...             'diffuser': {
    ...                 'thickness_wall': 1.17*u.inch, 'vel_max': 442.9*u.mm/u.s,
    ...                 'A': 0.419*u.inch**2
    ...             },
    ...             'exit_man': {
    ...                 'hl_orifice': 4*u.cm, 'N_orifices': 58
    ...             }
    ...         }
    ... }
    >>> ID_exit_man(20*u.L/u.s, 20*u.degC)
    0.21247905143432252 meter
    """
    #Inputs do not need to be checked here because they are checked by
    #functions this function calls.
    nu = pc.viscosity_dynamic(temp)
    hl = sed_inputs['manifold']['exit_man']['hl_orifice'].to(u.m)
    L = sed_inputs['tank']['L'].to(u.m)
    N_orifices = sed_inputs['manifold']['exit_man']['N_orifices']
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
                    / (1 - sed_inputs['manifold']['ratio_Q_man_orifice']**2)))**0.25
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
    >>> sed_dict = {
    ...         'thickness_wall': 0.15*u.m,
    ...         'plate_settlers': {
    ...             'angle': 60*u.deg, 'S': 2.5*u.cm,
    ...             'thickness': 2*u.mm, 'L_cantilevered': 20*u.cm,
    ...             'vel_capture': 0.12*u.mm/u.s
    ...             },
    ...         'tank': {
    ...             'W': 42*u.inch, 'L': 5.8*u.m, 'vel_up': 1*u.mm/u.s
    ...         },
    ...         'manifold': {
    ...             'ratio_Q_man_orifice': 0.8,
    ...             'diffuser': {
    ...                 'thickness_wall': 1.17*u.inch, 'vel_max': 442.9*u.mm/u.s,
    ...                 'A': 0.419*u.inch**2
    ...             },
    ...             'exit_man': {
    ...                 'hl_orifice': 4*u.cm, 'N_orifices': 58
    ...             }
    ...         }
    ... }
    >>> D_exit_man_orifice(20*u.L/u.s, mat.DIAM_DRILL_ENG)
    0.03125 meter

    """
    Q_orifice = Q_plant/sed_inputs['manifold']['exit_man']['N_orifices']
    D_orifice = np.sqrt(Q_orifice**4)/(np.pi *
                con.RATIO_VC_ORIFICE * np.sqrt(2 * con.GRAVITY.magnitude *
                sed_inputs['manifold']['exit_man']['hl_orifice'].to(u.m).magnitude))
    return ut.ceil_nearest(D_orifice, drill_bits)


@u.wraps(u.m, [None], False)
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
    >>> sed_dict = {
    ...         'thickness_wall': 0.15*u.m,
    ...         'plate_settlers': {
    ...             'angle': 60*u.deg, 'S': 2.5*u.cm,
    ...             'thickness': 2*u.mm, 'L_cantilevered': 20*u.cm,
    ...             'vel_capture': 0.12*u.mm/u.s
    ...             },
    ...         'tank': {
    ...             'W': 42*u.inch, 'L': 5.8*u.m, 'vel_up': 1*u.mm/u.s
    ...         },
    ...         'manifold': {
    ...             'ratio_Q_man_orifice': 0.8,
    ...             'diffuser': {
    ...                 'thickness_wall': 1.17*u.inch, 'vel_max': 442.9*u.mm/u.s,
    ...                 'A': 0.419*u.inch**2
    ...             },
    ...             'exit_man': {
    ...                 'hl_orifice': 4*u.cm, 'N_orifices': 58
    ...             }
    ...         }
    ... }
    >>> L_sed_plate()
    0.4618802153517006 meter

    """
    L_sed_plate = ((sed_inputs['plate_settlers']['S'] * ((sed_inputs['tank']['vel_up']/sed_inputs['plate_settlers']['vel_capture'])-1) \
                 + sed_inputs['plate_settlers']['thickness'] * (sed_inputs['tank']['vel_up']/sed_inputs['plate_settlers']['vel_capture'])) \
                 / (np.sin(sed_inputs['plate_settlers']['angle']) * np.cos(sed_inputs['plate_settlers']['angle'])) \
                 ).to(u.m).magnitude
    return L_sed_plate

@u.wraps(u.m, [], False)
def depth_end_floc(Q_plant, temp, sdr = 26, depth_above_exit_man = 5*u.cm,
                   plate_settler_to_exit_man = 5*u.cm,
                   angle_plate_settler = 60*u.deg,
                   floc_blanket_to_plate_settler = 10*u.cm,
                   depth_floc_blanket = 25 *u.cm,
                   angle_bottom_tank = 50*u.deg,
                   w_tank = 42*u.inch
                   sed_inputs=sed_dict):
    ID_exit_man_ = ID_exit_man(Q_plant, temp, sed_inputs=sed_dict)
    OD_exit_man_ = OD(ND_SDR_available(ID, sdr))
    L_sed_plate_ = L_sed_plate(sed_inputs=sed_dict)
    return (w_tank*np.tan(angle_bottom_tank)/2) + depth_floc_blanket +
            floc_blanket_to_plate_settler + (L_sed_plate_*np.sin(angle_plate_settler)
            + plate_settler_to_exit_man + OD_exit_man_ + depth_above_exit_man)
