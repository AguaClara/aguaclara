"""Includes all minor loss coefficient calculations for common complex
geometries, based off of the following resource:

https://neutrium.net/fluid_flow/pressure-loss-from-fittings-expansion-and-reduction-in-pipe-size/
"""

import aguaclara.core.physchem as pc
import aguaclara.core.constants as con
import aguaclara.core.materials as mats
import aguaclara.core.utility as ut
from aguaclara.core.units import u

import numpy as np


# TODO: Add units to docstrings. - Oliver Leung (oal22)


@ut.list_handler()
def k_value_expansion(ent_pipe_id, exit_pipe_id, q,
                      fitting_angle=180, rounded=False,
                      nu=con.WATER_NU, pipe_rough=mats.PVC_PIPE_ROUGH):
    """Calculates the minor loss coefficient (k-value) of a square,
    tapered, or rounded expansion in a pipe. Defaults to square.

    To use tapered, set angle to something that isn't 180.

    To use rounded, set rounded to True.

    Parameters:
        ent_pipe_id: Entrance pipe's inner diameter from which fluid flows.
        exit_pipe_id: Exit pipe's inner diameter to which fluid flows.
        q: Fluid's flow rate.

        fitting_angle: Fitting angle. Default: square (180 degrees).
        rounded: Rounded fitting. Default: square (False).

        nu: Fluid's dynamic viscosity of the fluid. Default: room
            temperature water (1 * 10**-6 * m**2/s)
        pipe_rough: Pipe roughness. Default: PVC pipe roughness

    Returns:
        k-value of expansion.
    """

    if ent_pipe_id > exit_pipe_id:
        print('k_value_expansion: Entrance pipe\'s inner diameter is larger '
              'than exit pipe\'s inner diameter, using reduction instead.')
        return k_value_reduction(ent_pipe_id, exit_pipe_id, q,
                                 fitting_angle, rounded,
                                 nu, pipe_rough)

    f = pc.fric_pipe(q, ent_pipe_id, nu, pipe_rough)  # Darcy friction factor.
    re = pc.re_pipe(q, ent_pipe_id, nu)          # Entrance pipe's Reynolds number.

    fitting_type = _get_fitting_type(fitting_angle, rounded)

    if fitting_type == 'square':
        result = _k_value_square_expansion(ent_pipe_id, exit_pipe_id, re, f)
    elif fitting_type == 'tapered':
        result = _k_value_tapered_expansion(ent_pipe_id, exit_pipe_id, re, f)
    elif fitting_type == 'rounded':
        result = _k_value_rounded_expansion(ent_pipe_id, exit_pipe_id, re)
    elif fitting_type == 'ambiguous':
        result = ValueError('The fitting is ambiguously both tapered and rounded. '
                         'Please set only either fitting_angle or rounded.')
    return result.to(u.dimensionless)


@ut.list_handler()
def k_value_reduction(ent_pipe_id, exit_pipe_id, q,
                      fitting_angle=180, rounded=False,
                      nu=con.WATER_NU, pipe_rough=mats.PVC_PIPE_ROUGH):
    """Calculates the minor loss coefficient (k-value) of a square,
    tapered, or rounded reduction in a pipe. Defaults to square.

    To use tapered, set angle to something that isn't 180.

    To use rounded, set rounded to True.

    Parameters:
        ent_pipe_id: Entrance pipe's inner diameter from which fluid flows.
        exit_pipe_id: Exit pipe's inner diameter to which fluid flows.
        q: Fluid's q rate.

        fitting_angle: Fitting angle. Default: square (180 degrees).
        rounded: Rounded fitting. Default: square (False).

        nu: Fluid's dynamic viscosity of the fluid. Default: room
            temperature water (1 * 10**-6 * m**2/s)
        pipe_rough: Pipe roughness. Default: PVC pipe roughness

    Returns:
        k-value of reduction.
    """

    if ent_pipe_id < exit_pipe_id:
        print('k_value_reduction: Entrance pipe\'s inner diameter is less than '
              'exit pipe\'s inner diameter, using expansion instead.')
        return k_value_expansion(ent_pipe_id, exit_pipe_id, q,
                                 fitting_angle, rounded,
                                 nu, pipe_rough)

    f = pc.fric_pipe(q, ent_pipe_id, nu, pipe_rough)     # Darcy friction factor.
    re = pc.re_pipe(q, ent_pipe_id, nu)             # Entrance pipe's Reynolds number.

    fitting_type = _get_fitting_type(fitting_angle, rounded)

    if fitting_type == 'square':
        result = _k_value_square_reduction(ent_pipe_id, exit_pipe_id, re, f)
    elif fitting_type == 'tapered':
        result = _k_value_tapered_reduction(ent_pipe_id, exit_pipe_id, fitting_angle, re, f)
    elif fitting_type == 'rounded':
        result = _k_value_rounded_reduction(ent_pipe_id, exit_pipe_id, re)
    elif fitting_type == 'ambiguous':
        raise ValueError('The fitting is ambiguously both tapered and rounded.'
                         'Please set only either fitting_angle or rounded.')
    return result.to(u.dimensionless)


@ut.list_handler()
def k_value_orifice(pipe_id, orifice_id, orifice_l, q,
                    nu=con.WATER_NU):
    """Calculates the minor loss coefficient of an orifice plate in a
    pipe.

    Parameters:
        pipe_id: Entrance pipe's inner diameter from which fluid flows.
        orifice_id: Orifice's inner diameter.
        orifice_l: Orifice's length from start to end.
        q: Fluid's q rate.

        nu: Fluid's dynamic viscosity of the fluid. Default: room
            temperature water (1 * 10**-6 * m**2/s)

    Returns:
        k-value at the orifice.
    """

    if orifice_id > pipe_id:
        raise ValueError('The orifice\'s inner diameter cannot be larger than'
                         'that of the entrance pipe.')

    re = pc.re_pipe(q, pipe_id, nu)  # Entrance pipe's Reynolds number.

    orifice_type = _get_orifice_type(orifice_l, orifice_id)

    if orifice_type == 'thin':
        result = _k_value_thin_sharp_orifice(pipe_id, orifice_id, re)
    elif orifice_type == 'thick':
        result = _k_value_thick_orifice(pipe_id, orifice_id, orifice_l, re)
    elif orifice_type == 'oversize':
        result = k_value_reduction(pipe_id, orifice_id, q) \
               + k_value_expansion(orifice_id, pipe_id, q)
    return result.to(u.dimensionless)


def _k_value_square_reduction(ent_pipe_id, exit_pipe_id, re, f):
    """Returns the minor loss coefficient for a square reducer.

    Parameters:
        ent_pipe_id: Entrance pipe's inner diameter.
        exit_pipe_id: Exit pipe's inner diameter.
        re: Reynold's number.
        f: Darcy friction factor.
    """

    if re < 2500:
        return (1.2 + (160 / re)) * ((ent_pipe_id / exit_pipe_id) ** 4)
    else:
        return (0.6 + 0.48 * f) * (ent_pipe_id / exit_pipe_id) ** 2\
            * ((ent_pipe_id / exit_pipe_id) ** 2 - 1)


def _k_value_tapered_reduction(ent_pipe_id, exit_pipe_id, fitting_angle, re, f):
    """Returns the minor loss coefficient for a tapered reducer.

    Parameters:
        ent_pipe_id: Entrance pipe's inner diameter.
        exit_pipe_id: Exit pipe's inner diameter.
        fitting_angle: Fitting angle between entrance and exit pipes.
        re: Reynold's number.
        f: Darcy friction factor.
    """

    k_value_square_reduction = _k_value_square_reduction(ent_pipe_id, exit_pipe_id,
                                                         re, f)

    if 45 < fitting_angle <= 180:
        return k_value_square_reduction * np.sqrt(np.sin(fitting_angle / 2))
    elif 0 < fitting_angle <= 45:
        return k_value_square_reduction * 1.6 * np.sin(fitting_angle / 2)
    else:
        raise ValueError('k_value_tapered_reduction: The reducer angle ('
                         + fitting_angle + ') cannot be outside of [0,180].')


def _k_value_rounded_reduction(id_entrance, id_exit, re):
    return (0.1 + (50 / re)) * ((id_entrance / id_exit) ** 4 - 1)


######### Expansions:


def _k_value_square_expansion(id_entrance: float, id_exit: float, re: float, f: float) -> float:
    # Calculate minor loss coefficient for square expansion
    if re < 4000:
        k = 2 * (1 - (id_entrance / id_exit) ** 4)
    else:
        k = (1 + 0.8 * f) * (1 - (id_entrance / id_exit) ** 2) ** 2
    return k


def _k_value_tapered_expansion(id_entrance: float, id_exit: float, re: float, f, theta: float) -> float:
    # Calculate minor loss coefficient for a tapered expansion
    k_square = _k_value_square_expansion(id_entrance, id_exit, re, f)
    if 45 < theta <= 180:
        k = k_square
    elif 0 < theta <= 45:
        k = k_square * 2.6 * np.sin(theta / 2)
    else:
        raise ValueError('The reducer angle cannot be outside the [0,180] range')
    return k


def _k_value_rounded_expansion(id_entrance: float, id_exit: float, re: float, f: float) -> float:
    return _k_value_square_expansion(id_entrance, id_exit, re, f)


######### Orifices:


def _k_value_thin_sharp_orifice(id_pipe: float, id_orifice: float, re: float) -> float:
    # Calculate minor loss coefficient for a thin, sharp orifice
    if re < 2500:
        k = ((2.72 + (id_orifice / id_pipe) ** 2) * ((120 / re) - 1)) * (1 - (id_orifice / id_pipe) ** 2) * \
            ((id_pipe / id_orifice) ** 4 - 1)
    else:
        k = ((2.72 + (id_orifice / id_pipe) ** 2) * (4000 / re)) * (1 - (id_orifice / id_pipe) ** 2) * \
            ((id_pipe / id_orifice) ** 4 - 1)
    return k


def _k_value_thick_orifice(id_pipe: float, id_orifice: float, length_orifice: float, re: float) -> float:
    # Calculate minor loss coefficient for a thick orifice
    # if L/id_orifice > 5, use the equation for a square reduction and expansion.
    k_thin = _k_value_thin_sharp_orifice(id_pipe, id_orifice, re)
    # thickness coefficient:
    c = 0.584 + (0.0936 / ((length_orifice / id_orifice) ** 1.5 + 0.225))
    return c * k_thin


def _get_fitting_type(fitting_angle, rounded):
    """Returns fitting type for expansions and reductions.

    Parameters:
        fitting_angle: Fitting angle. Usually is 180 for square fittings.
        rounded: Rounded fitting. Usually is False for square fittings.
    """

    if fitting_angle != 180 and rounded:
        return 'ambiguous'
    elif rounded:
        return 'rounded'
    elif fitting_angle != 180:
        return 'tapered'
    else:
        return 'square'


def _get_orifice_type(orifice_l, orifice_id):
    """Returns orifice type for orifice k-value caluclations.

    Parameters:
        orifice_l: Orifice's length.
        orifice_id: Orifice's inner diameter.
    """

    if orifice_l == 0:
        return 'thin'
    elif orifice_l / orifice_id < 5:
        return 'thick'
    else:
        return 'oversize'

#: 90 degree elbow
EL90_K_MINOR = 0.9

#:
EL45_K_MINOR = 0.45

#: The loss coefficient for the channel transition in a 90 degree turn
RIGHT_ANGLE_K_MINOR = 0.4

#:
ANGLE_VALVE_K_MINOR = 4.3

#:
GLOBE_VALVE_K_MINOR = 10

#:
GATE_VALVE_K_MINOR = 0.39

#:
CHECK_VALVE_CONV_K_MINOR = 4

#:
CHECK_VALVE_BALL_K_MINOR = 4.5

#: Headloss coefficient of a jet
EXP_K_MINOR = 1

#:
TEE_FLOW_RUN_K_MINOR = 0.6

#:
TEE_FLOW_BR_K_MINOR = 1.8

#:
PIPE_ENTRANCE_K_MINOR = 0.5

#:
PIPE_EXIT_K_MINOR = 1

#:
RM_GATE_VIN_K_MINOR = 25
