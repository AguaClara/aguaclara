"""This utility is used to provide useful functions for all things related to
pipeline design.

"""

from aguaclara.core.units import u
from aguaclara.core import physchem as pc
import aguaclara.core.constants as con
import aguaclara.core.materials as mats
import numpy

class PipeComponent:
    """This class has functions and fields common to Pipe and Connector"""
    def __init__(self, diameter_inner = (1/8)*u.inch):
        """Instantiates a PipeComponent fields common to both class Pipe and Connector with the specified values.

        Args:
            diameter_inner (float *u.in): inner diameter of the pipes 

        Returns:
             PipeComponent object."""
        self.diameter_inner = diameter_inner

class Pipe(PipeComponent):
    """This class calculates necessary functions and holds fields for pipes"""
    def __init__(self, diameter_inner):
        super().__init__(self, diameter_inner)
    # length


class Connector(PipeComponent):
     """This class calculates necessary functions and holds fields for connectors"""
     def __init__(self, diameter_inner):
         super().__init__(self, diameter_inner)
    # angle



@u.wraps(u.m**3/u.s, [u.m, u.m, None, u.m], False)
def flow_pipeline(diameters, lengths, k_minors, target_headloss,
                  nu=con.WATER_NU, pipe_rough=mats.PVC_PIPE_ROUGH):
    """
    This function takes a single pipeline with multiple sections, each potentially with different diameters,
    lengths and minor loss coefficients and determines the flow rate for a given headloss.

    :param diameters: list of diameters, where the i_th diameter corresponds to the i_th pipe section
    :type diameters: numpy.ndarray
    :param lengths: list of diameters, where the i_th diameter corresponds to the i_th pipe section
    :type lengths: numpy.ndarray
    :param k_minors: list of diameters, where the i_th diameter corresponds to the i_th pipe section
    :type k_minors: numpy.ndarray
    :param target_headloss: a single headloss describing the total headloss through the system
    :type target_headloss: float
    :param nu: The fluid dynamic viscosity of the fluid. Defaults to water at room temperature (1 * 10**-6 * m**2/s)
    :type nu: float
    :param pipe_rough:  The pipe roughness. Defaults to PVC roughness.
    :type pipe_rough: float

    :return: the total flow through the system
    :rtype: float
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

