"""This file contains all the functions needed to design a sedimentation tank
for an AguaClara plant.

"""
from aide_design.play import*

# again we will change this to an important statment from the URL of  aide_template repo
sed_dict = {
            'thickness_wall': 0.15*u.m,
            'plate_settlers': {
                'angle_plate': 60*u.deg, 'S_plate': 2.5*u.cm,
                'thickness_plate': 2*u.mm, 'L_sed_plate_cantilevered': 20*u.cm,
                'plate_modules': {}
                },
            'tank': {
                'W': 42*u.inch, 'vel_up': 1*u.mm/u.s, 'L': 5.8*u.m
            },
            'manifold': {
                'inlet_man': {

                },
                'diffuser': {
                    'thickness_wall': 1.17*u.inch, 'vel_max': 442.9*u.mm/u.s,
                    'A': 0.419*u.inch**2
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
    B_plate = sed_inputs['plate_settlers']['S_plate'] + sed_inputs['plate_settlers']['thickness_plate']
    return math.floor((sed_inputs['plate_settlers']['L_sed_plate_cantilevered'].magnitude / B_plate.magnitude
                      * np.tan(sed_inputs['plate_settlers']['angle_plate'].to(u.rad).magnitude)) + 1)

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
    """Return the maximum flow throughout one sedimentation tank.

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
