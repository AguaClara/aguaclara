"""This utility is used to provide useful functions for all things related to
pipeline design.

"""

from aguaclara.core.units import unit_registry as u
import aguaclara.core.physchem as pc
import aguaclara.core.constants as con
import aguaclara.core.materials as mat

import numpy as np

# NOTE: This implementation of Pipeline presumes that Pipe has been
# implemented with:
# 1. id (inner diameter)
# 2. l (length)
# 3. minor_loss
# 4. q() (flow rate)
# Pipeline will work once that has been implemented.
# - Oliver Leung (oal22), 10/11/18

class Pipeline:

    def __init__(self,
                 pipes=np.array(), nu=con.WATER_NU, pipe_rough=mat.PVC_PIPE_ROUGH):
        """Initializes a Pipeline.

        Parameters:
            pipes: NumPy array of Pipe objects that comprise the Pipeline.
            nu: The pipeline fluid's kinematic viscosity.
            pipe_rough: The roughness of the pipes in the Pipeline.
        """
        self.pipes = pipes
        self.nu = nu
        self.pipe_rough = pipe_rough

    # TODO: Implement this with calculation instead of interpolation.
    # Oliver Leung (oal22), 10/11/18
    def q(self, hl):
        """Gets the flow rate of a """


@u.wraps(u.m**3/u.s, [u.m, u.m, None, u.m], False)
def flow_pipeline(diameters: np.ndarray, lengths: np.ndarray, k_minors: np.ndarray, target_headloss: float,
                  nu=con.WATER_NU, pipe_rough=mat.PVC_PIPE_ROUGH):
    """
    This function takes a single pipeline with multiple sections, each potentially with different diameters,
    lengths and minor loss coefficients and determines the flow rate for a given headloss.

    Args:
        diameters: list of diameters, where the i_th diameter corresponds to the i_th pipe section
        lengths: list of diameters, where the i_th diameter corresponds to the i_th pipe section
        k_minors: list of diameters, where the i_th diameter corresponds to the i_th pipe section
        target_headloss: a single headloss describing the total headloss through the system
        nu: The fluid dynamic viscosity of the fluid. Defaults to water at room temperature (1 * 10**-6 * m**2/s)
        pipe_rough:  The pipe roughness. Defaults to PVC roughness.
    Returns:
        flow: the total flow through the system
    """

    # Ensure all the arguments except total headloss are the same length
    #TODO

    # Total number of pipe lengths
    n = diameters.size

    # Start with a flow rate guess based on the flow through a single pipe section
    flow = pc.flow_pipe(diameters[0], target_headloss, lengths[0], nu, pipe_rough, k_minors[0])
    err = 1.0

    # Add all the pipe length headlosses together to test the error
    while abs(err) > 0.01 :
        headloss = sum([pc.headloss(flow, diameters[i], lengths[i], nu, pipe_rough,
                                    k_minors[i]).to(u.m).magnitude for i in range(n)])
        # Test the error. This is always less than one.
        err = (target_headloss - headloss) / (target_headloss + headloss)
        # Adjust the total flow in the direction of the error. If there is more headloss than target headloss,
        # The flow should be reduced, and vice-versa.
        flow = flow + err * flow

    return flow
