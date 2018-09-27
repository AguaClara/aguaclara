"""Includes all minor loss coefficient calculations for common complex
geometries, based off of the following resource:

https://neutrium.net/fluid_flow/pressure-loss-from-fittings-expansion-and-reduction-in-pipe-size/
"""

import aguaclara.core.physchem as pc
import aguaclara.core.constants as con
import aguaclara.core.materials_database as mats
import aguaclara.core.utility as ut
import aguaclara.core.units.unit_registry as u

import numpy as np


# TODO: Write fitting and orifice type functions, then replace checks
# with a switch statement.

@u.wraps(u.dimensionless, [u.m, u.m, u.L/u.s])
@ut.list_handler
def k_value_expansion(ent_pipe_id, exit_pipe_id, q,
                      fitting_angle=180, rounded=False,
                      nu=con.NU_WATER, pipe_rough=mats.PIPE_ROUGH_PVC):
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
        print('Entrance pipe\'s inner diameter is larger than exit, using '
              'reduction instead.')
        return k_value_reduction(ent_pipe_id, exit_pipe_id, q,
                                 fitting_angle, rounded,
                                 nu, pipe_rough)

    f = pc.fric(q, ent_pipe_id, nu, pipe_rough)     # Darcy friction factor.
    re = pc.re_pipe(q, ent_pipe_id, nu)             # Entrance pipe's Reynolds number.

    # Ambiguous fitting
    if fitting_angle != 180 and rounded:
        print('The fitting is ambiguously both tapered and rounded. Please set'
              'only either fitting_angle or rounded.')
        return 0

    # Rounded fitting
    elif rounded:
        return _k_value_rounded_expansion(ent_pipe_id, exit_pipe_id, re)

    # Tapered fitting
    elif fitting_angle != 180:
        return _k_value_tapered_expansion(ent_pipe_id, exit_pipe_id, re, f)

    # Square fitting
    else:
        return _k_value_square_expansion(ent_pipe_id, exit_pipe_id, re, f)


@u.wraps(u.dimensionless, [u.m, u.m, u.L/u.s])
@ut.list_handler
def k_value_reduction(ent_pipe_id, exit_pipe_id, q,
                      fitting_angle=180, rounded=False,
                      nu=con.NU_WATER, pipe_rough=mats.PIPE_ROUGH_PVC):
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
        print('Entrance pipe\'s inner diameter is less than exit, using '
              'expansion instead.')
        return k_value_expansion(ent_pipe_id, exit_pipe_id, q,
                                 fitting_angle, rounded,
                                 nu, pipe_rough)

    f = pc.fric(q, ent_pipe_id, nu, pipe_rough)     # Darcy friction factor.
    re = pc.re_pipe(q, ent_pipe_id, nu)             # Entrance pipe's Reynolds number.

    # Ambiguous fitting
    if fitting_angle != 180 and rounded:
        raise ValueError('The fitting is ambiguously both tapered and rounded.'
                         'Please set only either fitting_angle or rounded.')

    # Rounded fitting
    elif rounded:
        return _k_value_rounded_reduction(ent_pipe_id, exit_pipe_id, re)

    # Tapered fitting
    elif fitting_angle != 180:
        return _k_value_tapered_reduction(ent_pipe_id, exit_pipe_id, re, f)

    # Square fitting
    else:
        return _k_value_square_reduction(ent_pipe_id, exit_pipe_id, re, f)


@u.wraps(u.dimensionless, [u.m, u.m, u.m, u.m**3/u.s])
@ut.list_handler
def k_value_orifice(pipe_id, orifice_id, orifice_l, q,
                    nu=con.NU_WATER):
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

    # Thin orifice
    if orifice_l == 0:
        return _k_value_thin_sharp_orifice(pipe_id, orifice_id, re)

    # Thick orifice
    elif orifice_l/orifice_id < 5:
        return _k_value_thick_orifice(pipe_id, orifice_id, orifice_l, re)

    # Oversize orifice (use square reduction and expansion instead)
    else:
        return k_value_reduction(pipe_id, orifice_id, q)\
               + k_value_expansion(orifice_id, pipe_id, q * u.m)

###############################################___________PRIVATE FUNCTIONS_____________################################

######### Reductions:


def _k_value_square_reduction(id_entrance: float, id_exit: float, re: float, f: float) -> float:
    # Calculate minor loss coefficient for square reducer
    if re < 2500:
        k = (1.2+(160/re))*((id_entrance/id_exit) ** 4)
    else:
        k = (0.6 + 0.48 * f) * (id_entrance / id_exit) ** 2 * ((id_entrance / id_exit) ** 2 - 1)
    return k


def _k_value_tapered_reduction(id_entrance: float, id_exit: float, re: float, f, theta: float) -> float:
    # Calculate minor loss coefficient for a tapered reducer
    k_square = _k_value_square_reduction(id_entrance, id_exit, re, f)
    if 45 < theta <= 180:
        k = k_square*np.sqrt(np.sin(theta / 2))
    elif 0 < theta <= 45:
        k = k_square * 1.6 * np.sin(theta / 2)
    else:
        raise ValueError('The reducer angle cannot be outside the [0,180] range')
    return k


def _k_value_rounded_reduction(id_entrance: float, id_exit: float, re: float) -> float:
    return (0.1 + (50 / re)) * ((id_entrance / id_exit) ** 4 - 1)

######### Expansions:


def _k_value_square_expansion(id_entrance: float, id_exit: float, re: float, f: float) -> float:
    # Calculate minor loss coefficient for square expansion
    if re < 4000:
        k = 2*(1-(id_entrance/id_exit) ** 4)
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
        k = ((2.72+(id_orifice/id_pipe) ** 2)*((120/re) - 1)) * (1 - (id_orifice/id_pipe) ** 2) * \
            ((id_pipe/id_orifice) ** 4 - 1)
    else:
        k = ((2.72 + (id_orifice / id_pipe) ** 2) * (4000 / re)) * (1 - (id_orifice / id_pipe) ** 2) * \
            ((id_pipe / id_orifice) ** 4 - 1)
    return k


def _k_value_thick_orifice(id_pipe: float, id_orifice: float, length_orifice: float, re: float) -> float:
    # Calculate minor loss coefficient for a thick orifice
    # if L/id_orifice > 5, use the equation for a square reduction and expansion.
    k_thin = _k_value_thin_sharp_orifice(id_pipe, id_orifice, re)
    # thickness coefficient:
    c = 0.584 + (0.0936 / ((length_orifice/id_orifice) ** 1.5 + 0.225))
    return c * k_thin
