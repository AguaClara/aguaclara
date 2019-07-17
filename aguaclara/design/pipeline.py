from aguaclara.core.units import unit_registry as u
from aguaclara.core import physchem as pc
import aguaclara.core.constants as con
import aguaclara.core.materials as mats
from aguaclara.design.component import Component

import pandas as pd
import numpy as np
import os.path

dir_path = os.path.dirname(__file__)
csv_path = os.path.join(dir_path, '/../core/data/pipe_database.csv')
with open(csv_path) as pipedbfile:
    pipedb = pd.read_csv(pipedbfile)

class PipelineComponent(Component):
    def __init__(self, **kwargs):
        self.size = 1 / 8 * u.inch
        super().__init__(**kwargs)

        self.size = ND_available(self.size)

    def ND_all_available():
    """Return an array of available nominal diameters.

    NDs available are those commonly used as based on the 'Used' column
    in the pipedb.
    """
        ND_all_available = []
        for i in range(len(pipedb['NDinch'])):
            if pipedb.iloc[i, 4] == 1:
                ND_all_available.append((pipedb['NDinch'][i]))
        return ND_all_available * u.inch

    def ND_available(NDguess):
    """Return the minimum ND that is available.

    1. Extract the magnitude in inches from the nominal diameter.
    2. Find the index of the closest nominal diameter.
    3. Take the values of the array, subtract the ND, take the
       absolute value, find the index of the minimium value.
    
    """
        myindex = (ND_all_available() >= NDguess)
        return min(ND_all_available()[myindex])


class Pipe(PipelineComponent):
    SPEC_AVAILABLE = ['sdr26', 'sdr41', 'sch40']

    def __init__(self, **kwargs):
        if spec not in self.SPEC_AVAILABLE:
            raise AttributeError('spec must be one of:', self.SPEC_AVAILABLE)
        
        if all (key in kwargs for key in ('size', 'id')):
            raise AttributeError(
                'Pipe must be instantiated with either the size or inner '
                'diameter, but not both.'
            )

        self.id = 0.3842 * u.inch
        self.spec = 'sdr41'

        super().__init__(**kwargs)

        elif 'size' in kwargs:
            self.id = self.get_id(self.size, self.spec)
        elif 'id' in kwargs:

    @property
    def od(self):
        index = (np.abs(np.array(self.pipedb['NDinch']) - self.size.magnitude)).argmin()
        return self.pipedb.iloc[index, 1] * u.inch
    
    def get_size(id, spec)
        if spec[:3] is 'sdr':
            return ND_SDR_available(id, spec[3:])
        else if spec is 'sch40':
            raise AttributeError('spec must be a sdr in order to calculate size')

    def get_id(self, size, spec):
        if spec[:3] is 'sdr':
            return _id_sdr(size, int(spec[3:]))
        else if spec is 'sch40':
            return _id_sch(size)

    def _id_sdr(self, size, sdr):
        return size.magnitude * (sdr - 2) / sdr

    def _id_sch40(self, size):
        myindex = (np.abs(np.array(self.pipedb['NDinch']) - size.magnitude)).argmin()
        return (self.pipedb.iloc[myindex, 1] - 2 * (self.pipedb.iloc[myindex, 5]))

    def ND_SDR_available(ID, SDR):
    """ Return an available ND given an ID and a schedule.

    Takes the values of the array, compares to the ID, and finds the index
    of the first value greater or equal.
    """
    for i in range(len(np.array(ID_SDR_all_available(SDR)))):
        if np.array(ID_SDR_all_available(SDR))[i] >= (ID.to(u.inch)).magnitude:
            return ND_all_available()[i]


class Elbow(PipelineComponent):
     """This class calculates necessary functions and holds fields for connectors"""
     def __init__(self, **kwargs):
         super().__init__(self, **kwargs)
    # angle


class Pipeline(PipelineComponent):
# @u.wraps(u.m**3/u.s, [u.m, u.m, None, u.m], False)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def flow_pipeline(self, diameters, lengths, k_minors, target_headloss,
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

