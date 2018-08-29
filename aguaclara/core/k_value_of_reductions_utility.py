""" Minor Loss Coefficients of Reductions Module.

This module includes all minor loss coefficient calculations for common complex
geometries. For reductions and expansions, the following resource is used:
https://neutrium.net/fluid_flow/pressure-loss-from-fittings-expansion-and-reduction-in-pipe-size/

"""

from aguaclara.core.units import unit_registry as u
from aguaclara.core import physchem as pc
import aguaclara.core.constants as con
import aguaclara.core.materials_database as mats
import numpy as np
import aguaclara.core.utility as ut


@u.wraps(u.dimensionless, [u.m, u.m, u.L/u.s])
@ut.list_handler
def k_value_expansion(id_entrance:float, id_exit:float, flow, NU=con.NU_WATER, ROUGHNESS=mats.PIPE_ROUGH_PVC, theta=180, ROUNDED=False) -> float:
    """This function calculates the minor loss coefficient of a square, tapered or rounded expansion in a pipe
     using the equation defined here, where Re is the reynolds number on the inlet side, D_in and D_out are the inner diameter
     of the entrance pipe and exit pipe, respectively, and f_in is the Darcy friction factor of the inlet pipe:

    K_{square}  =   \left\{   {{    2\left[1-\left(\frac{D_{in}}{D_{out}}\right)^4\right]  if  Re_{in} < 4000}\atop
                   {     \left(1+0.8f_{in}\right)\left[1-\left(\frac{D_{in}}{D_{out}}\right)^{2}\right]^{2}  if  Re_{in} > 4000}}   \right.

    If the expansion is tapered, the K_{square} is multiplied by:

    C_{angle} =   \left\{   {{  1  if  45 < theta < 180}\atop
                             {   2.6\sin{\frac{\theta}{2}}  if  theta < 45}}   \right.

    If the expansion is rounded, k_{square} is used.

        Args:
            id_entrance (length): This is the inner pipe diameter of the pipe from which the fluid is flowing.
            id_exit (length): This is the inner pipe diameter of the pipe into which the fluid is flowing.
            flow (volume/time): This is the inner pipe diameter of the pipe into which the fluid is flowing.
            NU (float, optional): The fluid dynamic viscosity of the fluid. Defaults to water at room temperature (1 * 10**-6 * m**2/s)
            ROUGHNESS (length, optional): The pipe roughness. Defaults to PVC roughness.
            theta (angle, optional): The angle of the expansion. Defaults to a square reducer (180 degrees).
            ROUNDED (bool, optional): Whether or not the expansion is round. Defaults to square (False).

        Returns:
            k (float): the dimensionless minor loss coefficient, or k value of the expansion.
        """

    if id_entrance > id_exit:
        raise ValueError('For an expansion, the diameter of the exit pipe must be larger than that of the '
                         'entrance pipe. Use the k_value_reduction equation.')

    # Calculate constants
    # determine Darcy friction factor
    f = pc.fric(flow, id_entrance, NU, ROUGHNESS)
    # determine reynolds number in entrance pipe
    re = pc.re_pipe(flow, id_entrance, NU)

    # The reducer is rounded
    if ROUNDED:
        k = _k_value_rounded_expansion(id_entrance, id_exit, re)

    # The reducer is square
    elif theta == 180:
        k = _k_value_square_expansion(id_entrance, id_exit, re, f)

    # The reducer is tapered
    else:
        k = _k_value_tapered_expansion(id_entrance, id_exit, re, f)

    return k


@u.wraps(u.dimensionless, [u.m, u.m, u.L/u.s])
@ut.list_handler
def k_value_reduction(id_entrance:float, id_exit:float, flow, NU=con.NU_WATER, ROUGHNESS=mats.PIPE_ROUGH_PVC, theta=180, ROUNDED=False) -> float:
    """This function calculates the minor loss coefficient of a square, tapered or round reduction in a pipe
     using the equation defined here, where Re is the reynolds number on the inlet side, D_in and D_out are the inner diameter
     of the entrance pipe and exit pipe, respectively, and f_in is the Darcy friction factor of the inlet pipe:

    K_{square} =   \left\{   {{   \left(1.2+\frac{160}{Re_{in}}\right)\left[\left(\frac{D_{in}}{D_{out}}\right)^4-1\right]  if  Re_{in} < 2500}\atop
                              {   \left(0.6+0.48f_{in}\right)\left(\frac{D_{in}}{D_{out}}\right)^2\left[\left(\frac{D_{in}}{D_{out}}\right)^2-1\right]  if  Re_{in} > 2500}}   \right.

    If the reduction is tapered, the K_{square} is multiplied by:

    C_{angle} =   \left\{   {{  \sqrt{\sin{\frac{\theta}{2}}}}  if  45 < theta < 180}\atop
                             {   1.6\sin{\frac{\theta}{2}}  if  theta < 45}}   \right.

    If the reduction is rounded, it is calculated with the following equation:

    K_{rounded} = \left(0.1+\frac{50}{Re_{in}}\right)\left[\left(\frac{D_{in}}{D_{out}}\right)^4-1\right]



        Args:
            id_entrance (length): This is the inner pipe diameter of the pipe from which the fluid is flowing.
            id_exit (length): This is the inner pipe diameter of the pipe into which the fluid is flowing.
            flow (volume/time): This is the inner pipe diameter of the pipe into which the fluid is flowing.
            NU (float, optional): The fluid dynamic viscosity of the fluid. Defaults to water at room temperature (1 * 10**-6 * m**2/s)
            ROUGHNESS (length, optional): The pipe roughness. Defaults to PVC roughness.
            theta (angle, optional): The angle of the reducer. Defaults to a square reducer (180 degrees).
            ROUNDED (bool, optional): Whether or not the reducer is round. Defaults to square (False).

        Returns:
            k (float): the dimensionless minor loss coefficient, or k value of the reduction.
        """

    if id_entrance < id_exit:
        raise ValueError('For a reduction, the diameter of the exit pipe must be smaller than that of the '
                         'entrance pipe. Use the k_value_expansion equation.')

    # Calculate constants
    # determine Darcy friction factor
    f = pc.fric(flow, id_entrance, NU, ROUGHNESS)
    # determine reynolds number in entrance pipe
    re = pc.re_pipe(flow, id_entrance, NU)

    # The reducer is rounded
    if ROUNDED:
        k = _k_value_rounded_reduction(id_entrance, id_exit, re)

    # The reducer is square
    elif theta == 180:
        k = _k_value_square_reduction(id_entrance, id_exit, re, f)

    # The reducer is tapered
    else:
        k = _k_value_tapered_reduction(id_entrance, id_exit, re, f)

    return k


@u.wraps(u.dimensionless, [u.m, u.m, u.m, u.m**3/u.s])
@ut.list_handler
def k_value_orifice(id_pipe: float, id_orifice: float, length_orifice: float, flow: float, NU=con.NU_WATER) -> float:
    """This function calculates the minor loss coefficient of a thick and thin orifice plate in a pipe
     using the equation defined here, where Re is the reynolds number on the inlet side, and D_pipe and D_orifice are
     the inner diameter of the enclosing pipe and orifice, respectively, and L is the length of the orifice:

    K_{thin} =   \left\{   {{   \displaystyle K=\left[2.72+\left(\frac{D_{2}}{D_{1}}\right)^{2}\
                                                    left(\frac{120}{Re_{1}}-1\right)\right]\left[1-\
                                                    left(\frac{D_{2}}{D_{1}}\right)^{2}\right]\left[\
                                                    left(\frac{D_{1}}{D_{2}}\right)^{4}-1\right]
                                                    if  Re_{in} < 2500}\atop
                              {     \displaystyle K=\left[2.72+\left(\frac{D_{2}}{D_{1}}\right)^{2}\
                                                    left(\frac{4000}{Re_{1}}\right)\right]\left[1-\
                                                    left(\frac{D_{2}}{D_{1}}\right)^{2}\right]\left[\
                                                    left(\frac{D_{1}}{D_{2}}\right)^{4}-1\right]
                                                    if  Re_{in} > 2500}}   \right.

    If the reduction is longer so as not to be sharp, but still has a L/D_orifice < 5, k_thin is multiplied by the
    following coefficient:

    C_{length} =    \displaystyle  0.584+\left(\frac{0.0936}{\left(L/D_{2}\right)^{1.5}+0.225}\right)

    If the orifice is so long such that L/D_orifice > 5, a square reduction and expansion are used.

        Args:
            id_pipe (length): This is the inner pipe diameter of the pipe enclosing the orifice.
            id_orifice (length): This is the inner diameter of the orifice itself.
            length_orifice (length): This is the length of the orifice. 0 signifies a thin, sharp orifice.
            flow (volume/time): This is the inner pipe diameter of the pipe into which the fluid is flowing.
            NU (float, optional): The fluid dynamic viscosity of the fluid. Defaults to water at
                room temperature (1 * 10**-6 * m**2/s)
            ROUGHNESS (length, optional): The pipe roughness. Defaults to PVC roughness.

        Returns:
            k (float): the dimensionless minor loss coefficient (k value) of the orifice.
        """

    # The orifice cannot be larger than the enclosing pipe:
    if id_orifice > id_pipe:
        raise ValueError('The orifice cannot be larger than the enclosing pipe.')

    # Calculate constants
    # determine reynolds number in entrance pipe
    re = pc.re_pipe(flow, id_pipe, NU)

    # The orifice is thin
    if length_orifice == 0:
            k = _k_value_thin_sharp_orifice(id_pipe, id_orifice, re)

    # The orifice is thick
    elif length_orifice/id_orifice < 5:
        k = _k_value_thick_orifice(id_pipe, id_orifice, length_orifice, re)

    # The orifice is too thick to be considered an orifice, square reduction and expansion is used to model
    else:
        k = k_value_reduction(id_pipe * u.m, id_orifice * u.m, flow * u.m**3/u.s) + k_value_expansion(id_orifice * u.m,
                                                                                                      id_pipe * u.m,
                                                                                                      flow * u.m**3/u.s)
        # raise ValueError('For an orifice that is so long such that length_orifice/id_orifice > 5, use a'
        #                  ' reduction and expansion to determine the k value')

    return k

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
