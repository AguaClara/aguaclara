from aguaclara.core.units import unit_registry as u
from aguaclara.core import physchem as pc
from aguaclara.core import head_loss as hl
import aguaclara.core.constants as con
import aguaclara.core.materials as mats
import aguaclara.core.utility as ut
from aguaclara.design.component import Component

import pandas as pd
import numpy as np
import os.path
from abc import ABC, abstractmethod

_dir_path = os.path.dirname(__file__)
_pipe_database_path = os.path.join(_dir_path, 'data/pipe_database.csv')
with open(_pipe_database_path) as pipe_database_file:
    _pipe_database = pd.read_csv(pipe_database_file)

_elbow_database_path = \
    os.path.join(_dir_path, 'data/elbow_database.csv')
with open(_elbow_database_path) as _elbow_database_file:
    _elbow_database = pd.read_csv(_elbow_database_file)

# TODO: Once we support a Pint version that supports use with Pandas DataFrame's
# (>=0.10.0), we can assign units to DataFrame's rather than converting them to
# NumPy arrays.
_available_sizes_raw = _pipe_database.query('Used==1')['NDinch']
AVAILABLE_SIZES = _available_sizes_raw.to_numpy() * u.inch

_available_ids_sch40_raw = _pipe_database.query('Used==1')['ID_SCH40']
AVAILABLE_IDS_SCH40 = _available_ids_sch40_raw.to_numpy() * u.inch

_available_elbow_sizes_raw = \
    _elbow_database.query('Used==1')['size']
AVAILABLE_ELBOW_SIZES = \
    _available_elbow_sizes_raw.to_numpy() * u.inch

_available_elbow_ids_raw = \
    _elbow_database.query('Used==1')['id_inch']
AVAILABLE_ELBOW_IDS = _available_elbow_ids_raw.to_numpy() * u.inch


class PipelineComponent(Component, ABC):

    def __init__(self, **kwargs):
        if all (key in kwargs for key in ('size', 'id')):
            raise AttributeError(
                'A PipelineComponent must be instantiated with either the size '
                'or inner diameter, but not both.'
            )

        self.size = 1 / 8 * u.inch
        self.temp = 20 * u.degC
        self.nu = pc.viscosity_kinematic(self.temp)
        self.next = None
        self.k_minor = 0

        super().__init__(**kwargs)

        if type(self) is type(self.next):
            raise TypeError('Pipeline components cannot be repeated.')

        self.size = self.get_available_size(self.size)

    def get_available_size(self, size):
        """Return the next larger size which is available."""
        return ut.ceil_nearest(size, AVAILABLE_SIZES)

    @abstractmethod
    def headloss(self):
        pass

    @property
    def headloss_pipeline(self):
        if self.next is None:
            return self.headloss
        else:
            return self.headloss + self.next.headloss_pipeline
    
    def set_next_components_q(self):
        if self.next is not None:
            self.next.q = self.q
            self.next.set_next_components_q()

    def flow_pipeline(self, target_headloss):
        """
        This function takes a single pipeline with multiple sections, each potentially with different diameters,
        lengths and minor loss coefficients and determines the flow rate for a given headloss.
        """
        if type(self) is Pipe:
            flow = pc.flow_pipe(self.id, 
                    target_headloss, 
                    self.length, 
                    self.nu,
                    self.pipe_rough, 
                    self.k_minor)
        else:
            try:
                flow = pc.flow_pipe(
                    self.next.id,
                    target_headloss,
                    self.next.length,
                    self.next.nu,
                    self.next.pipe_rough,
                    self.next.k_minor)
            except AttributeError:
                raise AttributeError('Neither of the first two components in'
                    'this pipeline are Pipe objects.')
        err = 1.0
        headloss = self.headloss_pipeline
        
        while abs(err) > 0.01 :
            err = (target_headloss - headloss) / (target_headloss + headloss)
            flow = flow + err * flow
            self.q = flow
            self.set_next_components_q()
            headloss = self.headloss_pipeline
        return flow
        
class Pipe(PipelineComponent):
    AVAILABLE_SPECS = ['sdr26', 'sdr41', 'sch40']

    def __init__(self, **kwargs):
        self.id = 0.3842 * u.inch
        self.spec = 'sdr41'
        self.length = 1 * u.m
        self.pipe_rough = mats.PVC_PIPE_ROUGH

        super().__init__(**kwargs)

        if self.spec not in self.AVAILABLE_SPECS:
            raise AttributeError('spec must be one of:', self.AVAILABLE_SPECS)

        if 'size' in kwargs:
            self.id = self._get_id(self.size, self.spec)
        elif 'id' in kwargs:
            self.size = self._get_size(self.id, self.spec)

        if self.next is not None and self.size != self.next.size:
            raise ValueError('size of the next pipeline component must be the',
            'same size as the current pipeline component')
            
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
        if spec[:3] == 'sdr':
            return self._get_id_sdr(size, int(spec[3:]))
        elif spec == 'sch40':
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
    
    @property
    def headloss(self):
        """Return the total head loss from major and minor losses in a pipe."""
        return pc.headloss_fric(
                self.q, self.id, self.length, self.nu, self.pipe_rough
            )
    

class Elbow(PipelineComponent):

    AVAILABLE_ANGLES = [90 * u.deg, 45 * u.deg]

    def __init__(self, **kwargs):
        self.angle = 90 * u.deg
        self.id = 0.417 * u.inch

        super().__init__(**kwargs)

        if self.angle == 45 * u.deg:
            self.k_minor = hl.EL45_K_MINOR
        elif self.angle == 90 * u.deg:
            self.k_minor = hl.EL90_K_MINOR
        else:
            raise ValueError('angle must be in ', self.AVAILABLE_ANGLES)

        if 'size' in kwargs:
            self.id = self._get_id(self.size)
        elif 'id' in kwargs:
            self.size = self._get_size(self.id)

        if self.next is not None and self.size != self.next.size:
            raise ValueError('The next component doesn\'t have the same size.')
    
    def _get_size(self, id_):
        """Get the size of """
        id_ = id_.to(u.inch)
        myindex = (
                np.abs(
                    AVAILABLE_ELBOW_IDS - id_
                )
            ).argmin()
        return AVAILABLE_ELBOW_SIZES[myindex]

    def _get_id(self, size):
        size = size.to(u.inch)
        myindex = (
                np.abs(
                    AVAILABLE_ELBOW_SIZES - size
                )
            ).argmin()
        return AVAILABLE_ELBOW_IDS[myindex]

    @property
    def headloss(self):
        return pc.elbow_minor_loss(self.q, self.id, self.k_minor).to(u.m)


class Tee(PipelineComponent):

    AVAILABLE_PATHS = ['branch', 'run', 'stopper']
    
    def __init__(self, **kwargs):
        
        self.left = None
        self.left_type = 'branch'
        self.left_k_minor = None

        self.right = None
        self.right_type = 'stopper'
        self.right_k_minor = None
        
        self.id = 0.417 * u.inch

        super().__init__(**kwargs)
        self.rep_ok()
        
        if self.left_type == 'branch':
            self.left_k_minor = hl.TEE_FLOW_BR_K_MINOR
        elif self.left_type == 'run':
            self.left_k_minor = hl.TEE_FLOW_RUN_K_MINOR
        elif self.left_type == 'stopper':
            self.left_k_minor = None

        if self.right_type == 'branch':
            self.right_k_minor = hl.TEE_FLOW_BR_K_MINOR
        elif self.right_type == 'run':
            self.right_k_minor = hl.TEE_FLOW_RUN_K_MINOR
        elif self.right_type == 'stopper':
            self.right_k_minor = None
        
        if self.left_type == 'stopper':
            self.next = self.right
        else:
            self.next = self.left
    
    @property
    def _headloss_left(self):
        return pc.elbow_minor_loss(self.q, self.id, self.left_k_minor).to(u.m)

    @property
    def _headloss_right(self):
        return pc.elbow_minor_loss(self.q, self.id, self.right_k_minor).to(u.m)

    @property
    def headloss(self):
        if self.left_type =='stopper':
            return self._headloss_right
        else:
            return self._headloss_left 
            
    def rep_ok(self):
        if [self.left_type, self.right_type].count('stopper') != 1:
            raise ValueError('All tees must have one stopper.')
        if self.left_type not in self.AVAILABLE_PATHS:
            raise ValueError(
                'type of branch for left outlet must be in ', 
                self.AVAILABLE_PATHS)
        
        if self.right_type not in self.AVAILABLE_PATHS:
            raise ValueError(
                'type of branch for right outlet must be in ', 
                self.AVAILABLE_PATHS)

        if self.next is not None and self.size != self.next.size:
            raise ValueError('The next component doesn\'t have the same size.')