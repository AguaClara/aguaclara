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
    >>> sed_dict = {
    ...         'thickness_wall': 0.15*u.m,
    ...         'plate_settlers': {
    ...             'angle': 60*u.deg, 'S': 2.5*u.cm,
    ...             'thickness': 2*u.mm, 'L_cantilevered': 20*u.cm,
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
    >>> n_sed_plates_max()
    13
    """
    B_plate = sed_inputs['plate_settlers']['S'] + sed_inputs['plate_settlers']['thickness']
    return math.floor((sed_inputs['plate_settlers']['L_cantilevered'].magnitude / B_plate.magnitude \
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
    return L_diffuser_outer(sed_inputs['tank']['W']) - \
    (2 * (sed_inputs['manifold']['diffuser']['thickness_wall']).to(u.m)).magnitude

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
    return (q_diffuser(sed_inputs).magnitude \
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
    >>>

    """
    vel_manifold_max = (sed_inputs['diffuser']['vel_max'].to(u.m/u.s).magnitude * \
        sqrt(2*((1-(sed_inputs['manifold']['ratio_Q_man_orifice'])**2)) / \
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
    return ((n_tanks * sed_inputs['tank']['W']) + sed_inputs['thickness_wall'] + \
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
    >>> sed_dict = {
    ...         'thickness_wall': 0.15*u.m,
    ...         'plate_settlers': {
    ...             'angle': 60*u.deg, 'S': 2.5*u.cm,
    ...             'thickness': 2*u.mm, 'L_cantilevered': 20*u.cm,
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
    L = sed_inputs['tank']['L']
    N_orifices = sed_inputs['manifold']['exit_man']['N_orifices']
    K_minor = con.K_MINOR_PIPE_EXIT
    pipe_rough = mat.PIPE_ROUGH_PVC.to(u.m)

    D = max(pc.diam_pipemajor(Q_plant, hl, L, nu, pipe_rough).magnitude,
                   pc.diam_pipeminor(Q_plant, hl, K_minor).magnitude)
    err = 1.00
    while err > 0.01:
            D_prev = D
            f = pc.fric(Q_plant, D_prev, nu, pipe_rough)
            D = ((8*Q_plant**2 / pc.GRAVITY.magnitude * np.pi**2 * hl.magnitude) *
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
    L_sed_plate = ((sed_input['plate_settlers']['S'] * ((sed_input['tank']['vel_up']/sed_input['plate_settlers']['vel_capture'])-1) \
                 + sed_input['plate_settlers']['thickness'] * (sed_input['tank']['vel_up']/sed_input['plate_settlers']['vel_capture'])) \
                 / (np.sin(sed_input['plate_settlers']['angle']) * np.cos(sed_input['plate_settlers']['angle'])) \
                 ).to(u.m)
    return L_sed_plate
