import aide_design.pipedatabase as pipe
from aide_design.units import unit_registry as u
from aide_design import physchem as pc
import aide_design.expert_inputs as exp
import aide_design.materials_database as mats
import numpy as np
""" Minor Loss Coefficients of Reductions Module.

This module includes all minor loss coefficient calculations for common complex geometries.
For reductions, the following resource is used: 
https://neutrium.net/fluid_flow/pressure-loss-from-fittings-expansion-and-reduction-in-pipe-size/

Note: there are several other cases listed in the above resource that should eventually be included.
These are round reducers, thin sharp orifices, and thick orifices.
"""

@u.wraps(None, [u.inch, u.inch, u.L/u.s])
def k_value_reduction(id_entrance:float, id_exit:float, flow, NU=exp.NU_WATER, ROUGHNESS=mats.PIPE_ROUGH_PVC, theta_reducer=180, ROUNDED=False) -> float:
    """This function calculates the minor loss coefficient of a square reduction in a pipe
     using the equation defined here, where Re is the reynolds number on the inlet side, D_in and D_out are the inner diameter
     of the entrance pipe and exit pipe, respectively, and f_in is the friction factor of the inlet pipe:

    K=   \left\{   {{\left(1.2+\frac{160}{Re_{in}}\right)\left[\left(\frac{D_{in}}{D_{out}}\right)^4-1\right]  if  Re_{in} < 2500}\atop
                   {\left(0.6+0.48f_{in}\right)\left(\frac{D_{in}}{D_{out}}\right)^2\left[\left(\frac{D_{in}}{D_{out}}\right)^2-1\right]  if  Re_{in} > 2500}}   \right.

        Args:
            id_entrance (length): This is the inner pipe diameter of the pipe from which the fluid is flowing.
            id_exit (length): This is the inner pipe diameter of the pipe into which the fluid is flowing.
            flow (volume/time): This is the inner pipe diameter of the pipe into which the fluid is flowing.
            NU (float, optional): The fluid dynamic viscosity of the fluid. Defaults to water at room temperature (1 * 10**-6 * m**2/s)
            ROUGHNESS (length, optional): The pipe roughness. Defaults to PVC roughness.
            theta_reducer (angle, optional): The angle of the reducer. Defaults to a square reducer (180 degrees.)
            ROUNDED (bool, optional): Whether or not the reducer is round. Defaults to square.
            theta_reducer (angle, optional): The angle of the reducer. Defaults to a square reducer (180 degrees.)

        Returns:
            float: the dimensionless minor loss coefficient, or k value of the reduction/expansion.
        """
    # Calculate constants
    # determine Darcy friction factor
    f = pc.fric(flow,id_entrance,NU,ROUGHNESS)
    # determine reynolds number in entrance pipe
    r = pc.re_pipe(flow,id_entrance,NU)

    # If the reducer is rounded
    if ROUNDED:
        return (0.1+(50/r))*((id_entrance/id_exit)**4-1)

    # Calculate minor loss coefficient for square reducer
    if r < 2500:
        k_square = (1.2+(160/r))*((id_entrance/id_exit) ** 4)
    else:
        k_square = (0.6 + 0.48 * f) * (id_entrance / id_exit) ** 2 * ((id_entrance / id_exit) ** 2 - 1)
    if theta_reducer == 180:
        return k_square

    # If the reducer has a taper (not square)
    if 45 < theta_reducer <= 180:
        k = k_square*np.sqrt(np.sin(theta_reducer/2))
    elif 0 < theta_reducer <= 45:
        k = k_square * 1.6 * np.sin(theta_reducer / 2)
    else:
        raise ValueError('The reducer angle cannot be outside the [0,180] range')
    return k