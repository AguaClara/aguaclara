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
    pipedb = pd.read_csv(pipedbfile).to_numpy()

ND_all_available = []
for i in range(len(pipedb['NDinch'])):
    if pipedb.iloc[i, 4] == 1:
        ND_all_available.append((pipedb['NDinch'][i]))
NDs = ND_all_available * u.inch

ID_SCH40_all_available = []
for i in range(len(pipedb['NDinch'])):
    if pipedb.iloc[i, 4] == 1:
        ID_SCH40_all_available.append((pipedb['ID_SCH40'][i]))
ID_SCH40s = ID_SCH40_all_available * u.inch

class PipelineComponent(Component):
    def __init__(self, **kwargs):
        self.size = 1 / 8 * u.inch
        super().__init__(**kwargs)

        self.size = self.get_available_size(self.size)

    def get_available_size(self, NDguess):
        """Return the minimum ND that is available.

        1. Extract the magnitude in inches from the nominal diameter.
        2. Find the index of the closest nominal diameter.
        3. Take the values of the array, subtract the ND, take the
        absolute value, find the index of the minimium value.
        """
        myindex = (NDs >= NDguess)
        return min(NDs[myindex])


class Pipe(PipelineComponent):
    SPEC_AVAILABLE = ['sdr26', 'sdr41', 'sch40']

    def __init__(self, **kwargs):
        self.id = 0.3842 * u.inch
        self.spec = 'sdr41'
        self.length = 1 * u.m
        
        if self.spec not in self.SPEC_AVAILABLE:
            raise AttributeError('spec must be one of:', self.SPEC_AVAILABLE)
        
        if all (key in kwargs for key in ('size', 'id')):
            raise AttributeError(
                'Pipe must be instantiated with either the size or inner '
                'diameter, but not both.'
            )

        super().__init__(**kwargs)

        if 'size' in kwargs:
            self.id = self._get_id(self.size, self.spec)
        elif 'id' in kwargs:
            self.size = self._get_size(self.id, self.spec)
            
    @property
    def od(self):
        """The outer diameter of the pipe"""
        index = (np.abs(np.array(pipedb['NDinch']) - self.size.magnitude)).argmin()
        return pipedb.iloc[index, 1] * u.inch

    def _get_size(self, id_, spec):
        """Get the size of """
        if spec[:3] is 'sdr':
            return self.nd_sdr(id_, spec[3:])
        elif spec is 'sch40':
            return self.nd_sch40(id_)

    def _get_id(self, size, spec):
        if spec[:3] is 'sdr':
            return self._id_sdr(size, int(spec[3:]))
        elif spec is 'sch40':
            return self._id_sch40(size)

    def _id_sdr(self, size, sdr):
        return size.magnitude * (sdr - 2) / sdr

    def _id_sch40(self, size):
        myindex = (np.abs(np.array(pipedb['NDinch']) - size.magnitude)).argmin()
        return ID_SCH40s[myindex]

    def nd_sdr(self, id_, sdr):
        nd_approx = (id_ * sdr) / (sdr - 2)
        return super().get_available_size(nd_approx)

    def nd_sch40(self, id_):
        myindex = (np.abs(ID_SCH40s - id_.magnitude)).argmin()
        return NDs[myindex]

    def ID_SDR_all_available(self, SDR):
        """Return an array of inner diameters with a given SDR.

        IDs available are those commonly used based on the 'Used' column
        in the pipedb.
        """
        ID = []
        for i in range(len(NDs)):
            ID.append(self._id_sdr(NDs[i], SDR).magnitude)
        return ID * u.inch

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
