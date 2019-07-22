from aguaclara.core.units import unit_registry as u
from aguaclara.core import physchem as pc
import aguaclara.core.constants as con
import aguaclara.core.materials as mats
import aguaclara.core.utility as ut
from aguaclara.design.component import Component

import pandas as pd
import numpy as np
import os.path

_dir_path = os.path.dirname(__file__)
_pipe_database_path = os.path.join(_dir_path, 'data/pipe_database.csv')
with open(_pipe_database_path) as pipe_database_file:
    _pipe_database = pd.read_csv(pipe_database_file)

_90_deg_elbow_database_path = \
    os.path.join(_dir_path, 'data/90_deg_elbow_database.csv')
with open(_90_deg_elbow_database_path) as _90_deg_elbow_database_file:
    _90_deg_elbow_database = pd.read_csv(_90_deg_elbow_database_file)

# TODO: Once we support a Pint version that supports use with Pandas DataFrame's
# (>=0.10.0), we can assign units to DataFrame's rather than converting them to
# NumPy arrays.
_available_sizes_raw = _pipe_database.query('Used==1')['NDinch']
AVAILABLE_SIZES = _available_sizes_raw.to_numpy() * u.inch

_available_ids_sch40_raw = _pipe_database.query('Used==1')['ID_SCH40']
AVAILABLE_IDS_SCH40 = _available_ids_sch40_raw.to_numpy() * u.inch

_available_90_deg_elbow_sizes_raw = \
    _90_deg_elbow_database.query('Used==1')['size']
AVAILABLE_90_DEG_ELBOW_SIZES = \
    _available_90_deg_elbow_sizes_raw.to_numpy() * u.inch

_available_90_deg_elbow_ids_raw = \
    _90_deg_elbow_database.query('Used==1')['id_inch']
AVAILABLE_90_DEG_ELBOW_IDS = _available_90_deg_elbow_ids_raw.to_numpy() * u.inch


class PipelineComponent(Component):
    def __init__(self, **kwargs):
        if type(self) is PipelineComponent:
            raise Exception(
                'The PipelineComponent class should not be instantiated. Instead, '
                'instantiate a Pipe or Elbow.'
            )
        if all (key in kwargs for key in ('size', 'id')):
            raise AttributeError(
                'A Pipe or Elbow must be instantiated with either the size '
                'or inner diameter, but not both.'
            )

        self.size = 1 / 8 * u.inch
        super().__init__(**kwargs)

        self.size = self.get_available_size(self.size)

    def get_available_size(self, size):
        """Return the next larger size which is available."""
        return ut.ceil_nearest(size, AVAILABLE_SIZES)


class Pipe(PipelineComponent):
    AVAILABLE_SPECS = ['sdr26', 'sdr41', 'sch40']

    def __init__(self, **kwargs):
        self.id = 0.3842 * u.inch
        self.spec = 'sdr41'
        self.length = 1 * u.m

        super().__init__(**kwargs)

        if self.spec not in self.AVAILABLE_SPECS:
            raise AttributeError('spec must be one of:', self.AVAILABLE_SPECS)

        if 'size' in kwargs:
            self.id = self._get_id(self.size, self.spec)
        elif 'id' in kwargs:
            self.size = self._get_size(self.id, self.spec)
            
    @property
    def od(self):
        """The outer diameter of the pipe"""
        index = (np.abs(np.array(_pipe_database['NDinch']) - self.size.magnitude)).argmin()
        return _pipe_database.iloc[index, 1] * u.inch

    def _get_size(self, id_, spec):
        """Get the size of """
        if spec[:3] is 'sdr':
            return self._get_size_sdr(id_, int(spec[3:]))
        elif spec is 'sch40':
            return self._get_size_sch40(id_)

    def _get_id(self, size, spec):
        if spec[:3] is 'sdr':
            return self._get_id_sdr(size, int(spec[3:]))
        elif spec is 'sch40':
            return self._get_id_sch40(size)

    def _get_id_sdr(self, size, sdr):
        return size.magnitude * (sdr - 2) / sdr

    def _get_id_sch40(self, size):
        myindex = (np.abs(np.array(_pipe_database['NDinch']) - size.magnitude)).argmin()
        return AVAILABLE_IDS_SCH40[myindex]

    def _get_size_sdr(self, id_, sdr):
        nd_approx = (id_ * sdr) / (sdr - 2)
        return super().get_available_size(nd_approx)

    def _get_size_sch40(self, id_):
        myindex = (np.abs(AVAILABLE_IDS_SCH40 - id_.magnitude)).argmin()
        return AVAILABLE_SIZES[myindex]

    def ID_SDR_all_available(self, SDR):
        """Return an array of inner diameters with a given SDR.

        IDs available are those commonly used based on the 'Used' column
        in the pipedb.
        """
        ID = []
        for i in range(len(AVAILABLE_SIZES)):
            ID.append(self._get_id_sdr(AVAILABLE_SIZES[i], SDR).magnitude)
        return ID * u.inch

class Elbow(PipelineComponent):
    """This class calculates necessary functions and holds fields for connectors"""
    def __init__(self, **kwargs):
        if all (key in kwargs for key in ('size', 'id')):
            raise AttributeError(
                'Elbow must be instantiated with either the size or inner '
                'diameter, but not both.'
            )
        
        self.angle = 90 * u.deg
        self.id = 0.417 * u.inch
        super().__init__(self, **kwargs)
        
        # TODO: Add more angles once their data pts are added.
        if self.angle not in (90 * u.deg):
            raise ValueError('angle must be 90 * u.deg')

        if 'size' in kwargs:
            self.id = self._get_id(self.size)
        elif 'id' in kwargs:
            self.size = self._get_size(self.id)
    
    def _get_size(self, id_):
        """Get the size of """
        id_ = id_.to(u.inch)
        myindex = (
                np.abs(
                    np.array(_90_deg_elbow_database['id_inch']) - id_.magnitude
                )
            ).argmin()
        return AVAILABLE_90_DEG_ELBOW_SIZES[myindex]

    def _get_id(self, size):
        size = size.to(u.inch)
        myindex = (
                np.abs(
                    np.array(_90_deg_elbow_database['size']) - size.magnitude
                )
            ).argmin()
        return AVAILABLE_90_DEG_ELBOW_IDS[myindex]


class Pipeline(PipelineComponent):
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
