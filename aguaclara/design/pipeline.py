"""Pipeline design functions

This module provides simple functions for creating pipeline components (pipes,
elbows, and tees), joining them together, and calculating ideal head loss/flow
rates. When they are created, pipeline components are checked against a set of
standard component sizes to ensure that they are readily constructible.

Constants:
    - ``AVAILABLE_SIZES (numpy.ndarray * u.inch)``: Set of available sizes for
      pipeline components
    - ``AVAILABLE_IDS_SCH40 (numpy.ndarray * u.inch)``: Set of available pipe
      inner diameters for SCH40 pipes
    - ``AVAILABLE_FITTING_SIZES (numpy.ndarray * u.inch)``: Set of available
      sizes for pipeline fittings
    - ``AVAILABLE_FITTING_IDS (numpy.ndarray * u.inch)``: Set of available
      inner diameters for pipeline fittings
"""
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

_fitting_database_path = \
    os.path.join(_dir_path, 'data/fitting_database.csv')
with open(_fitting_database_path) as _fitting_database_file:
    _fitting_database = pd.read_csv(_fitting_database_file)

# TODO: Once we support a Pint version that supports use with Pandas DataFrame's
# (>=0.10.0), we can assign units to DataFrame's rather than converting them to
# NumPy arrays.
_available_sizes_raw = _pipe_database.query('Used==1')['NDinch']
AVAILABLE_SIZES = np.array(_available_sizes_raw) * u.inch

_available_ids_sch40_raw = _pipe_database.query('Used==1')['ID_SCH40']
AVAILABLE_IDS_SCH40 = np.array(_available_ids_sch40_raw) * u.inch


_available_fitting_sizes_raw = _fitting_database.query('Used==1')['size']
AVAILABLE_FITTING_SIZES = np.array(_available_fitting_sizes_raw) * u.inch

_available_fitting_ids_raw = _fitting_database.query('Used==1')['id_inch']
AVAILABLE_FITTING_IDS = np.array(_available_fitting_ids_raw)* u.inch


class PipelineComponent(Component, ABC):
    """An abstract representation of pipeline components

    This abstract base class (ABC) contains common functionality for:

    #. describing and designing readily constructible pipeline components
    #. calculating the head loss of a pipeline given its flow rate, and
       vice-versa.
    #. printing the dimensions of either an individual pipe or an entire
       pipeline

    Design Inputs:
        - ``q (float * u.L/u.s)``: Flow rate (recommended, defaults to 20 L/s)
        - ``temp (float * u.degC)``: Water temperature (recommended, defaults to
          20°C)
        - ``size (float * u.inch)``: Nominal size (recommended, defaults to 0.5
          in)
        - ``fluid_type (str)``: Fluid type. Must be 'water', 'pacl', or 'alum'
          (optional, defaults to 'water')
        - ``next (PipelineComponent)``: The next pipeline component with respect
          to the flow direction. This can be either a newly-instantiated
          ``PipelineComponent`` child class, or a variable that contains such
          a component (optional, defaults to None)
        - ``k_minor (float)``: The minor loss coefficient (k-value) (optional,
          defaults to 0)
    """
    _AVAILABLE_FLUID_TYPES = ['water', 'pacl', 'alum']

    def __init__(self, **kwargs):
        if all (key in kwargs for key in ('size', 'id')):
            raise AttributeError(
                'A PipelineComponent must be instantiated with either the size '
                'or inner diameter, but not both.'
            )

        self.size = 0.5 * u.inch
        self.fluid_type = 'water'
        self.next = None
        self.k_minor = 0

        super().__init__(**kwargs)

        self._rep_ok()

        self.size = self._get_available_size(self.size)

    @property
    def nu(self):
        """The kinematic viscosity of the fluid passing through the pipeline
        component.
        """
        if self.fluid_type == 'water':
            return pc.viscosity_kinematic_water(self.temp)
        elif self.fluid_type == 'pacl':
            print('unimplemented')
            pass
        elif self.fluid_type == 'alum':
            print('unimplemented')
            pass

    def _get_available_size(self, size):
        """Return the next larger size which is available, given the list of
        available sizes.
        """
        return ut.ceil_nearest(size, AVAILABLE_SIZES)

    @abstractmethod
    def headloss(self):
        """The head loss of this pipeline component."""
        pass

    @property
    def headloss_pipeline(self):
        """The head loss of the entire pipeline following this component."""
        if self.next is None:
            return self.headloss
        else:
            return self.headloss + self.next.headloss_pipeline

    def _set_next_components_q(self):
        """Set the flow rates of the next components in this pipeline to be
        the same as this component.
        """
        if self.next is not None:
            self.next.q = self.q
            self.next._set_next_components_q()

    def flow_pipeline(self, target_headloss):
        """Calculate the required flow through a pipeline component and all of
        its next components to reach a desired head loss.

        Args:
            - ``target_headloss (float * u.m)``: The desired head loss through
              the pipeline
        """
        if type(self) is Pipe:
            flow = pc.flow_pipe(self.id,
                    target_headloss,
                    self.l,
                    self.nu,
                    self.pipe_rough,
                    self.k_minor)
        else:
            try:
                flow = pc.flow_pipe(
                    self.next.id,
                    target_headloss,
                    self.next.l,
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
            self._set_next_components_q()
            headloss = self.headloss_pipeline
        return flow.to(u.L / u.s)

    @abstractmethod
    def format_print(self):
        """The string representation of a pipeline component, disregarding other
        components in its pipeline.
        """
        pass

    def _pprint(self):
        """The pretty-printed string representation of a pipeline component
        and its next components.
        """
        if self.next is None:
            return self.format_print()
        else:
            return self.format_print() + '\n' + self.next._pprint()

    def __str__(self):
        return self._pprint()

    def __repr__(self):
        return self.__str__()

    def _rep_ok(self):
        """Ensure that the Python representation of a pipeline component is
        valid.
        """
        if self.fluid_type not in self._AVAILABLE_FLUID_TYPES:
            raise ValueError('fluid_type must be in', self._AVAILABLE_FLUID_TYPES)

        if self.next is not None:
            if type(self) is Pipe and type(self.next) not in [Elbow, Tee]:
                raise TypeError('Pipes must be connected with fittings.')
            elif type(self) in [Elbow] and type(self.next) not in [Pipe]:
                raise TypeError('Fittings must be followed by pipes.')


class Pipe(PipelineComponent):
    """Design class for a pipe

    Instantiate this class to create a readily constructible pipe and calculate
    its hydraulic features.

    ``Pipe``'s may be instantiated from a nominal size (to fit into an existing
    pipeline) or inner diameter (to follow hydraulic constraints), but not both.

    Design Inputs:
        - ``q (float * u.L/u.s)``: Flow rate (recommended, defaults to 20 L/s)
        - ``temp (float * u.degC)``: Water temperature (recommended, defaults to
          20°C)
        - ``size (float * u.inch)``: Nominal size (recommended, defaults to 0.5
          in)
        - ``fluid_type (str)``: Fluid type. Must be 'water', 'pacl', or 'alum'
          (optional, defaults to 'water')
        - ``next (PipelineComponent)``: The next pipeline component with respect
          to the flow direction. This can be either a newly-instantiated
          ``PipelineComponent`` child class, or a variable that contains such
          a component (optional, defaults to None)
        - ``id (float * u.inch)``: Inner diameter (optional, defaults to 0.476
          in)
        - ``spec (str)``: The pipe specification. Must be one of 'sdr26',
          'sdr41', or 'sch40'. (optional, defaults to 'sdr41')
        - ``l (float * u.m)``: Length of the pipe (optional, defaults to
          1 m)
        - ``pipe_rough (float * u.mm)``: Pipe roughness (optional, defaults to
          PVC pipe roughness of 12 mm)
        - ``k_minor (float)``: The minor loss coefficient (k-value) (optional,
          defaults to 0)
    """
    AVAILABLE_SPECS = ['sdr26', 'sdr41', 'sch40']

    def __init__(self, **kwargs):
        self.id = 0.476 * u.inch
        self.spec = 'sdr41'
        self.l = 1 * u.m
        self.pipe_rough = mats.PVC_PIPE_ROUGH

        super().__init__(**kwargs)

        if 'size' in kwargs:
            self.id = self._get_id(self.size, self.spec)
        elif 'id' in kwargs:
            self.size = self._get_size(self.id, self.spec)

        self._rep_ok()

    @property
    def od(self):
        """The outer diameter of the pipe"""
        index = (
                np.abs(np.array(_pipe_database['NDinch']) - self.size.magnitude)
            ).argmin()
        return _pipe_database.iloc[index, 1] * u.inch

    def _get_size(self, id_, spec):
        """Get the size of a pipe given an inner diameter and specification.

        Args:
            - ``id_ (float * u.inch)``: Inner diameter
            - ``spec (str)``: Pipe specification
        """
        if spec[:3] == 'sdr':
            return self._get_size_sdr(id_, int(spec[3:]))
        elif spec == 'sch40':
            return self._get_size_sch40(id_)

    def _get_id(self, size, spec):
        """Get the inner diameter of a pipe given the size and specification.

        Args:
            - ``size (float * u.inch)``: Nominal size
            - ``spec (str)``: Pipe specifcation
        """
        if spec[:3] == 'sdr':
            return self._get_id_sdr(size, int(spec[3:]))
        elif spec == 'sch40':
            return self._get_id_sch40(size)

    def _get_id_sdr(self, size, sdr):
        """Get the inner diameter of a pipe given the size and SDR.

        Args:
            - ``size (float * u.inch)``: Nominal size
            - ``sdr (int)``: Standard dimension ratio
        """
        self.size = super()._get_available_size(size)
        return self.size * (sdr - 2) / sdr

    def _get_id_sch40(self, size):
        """Get the inner diameter of a SCH40 pipe.

        Args:
            - ``size (float * u.inch)``: Nominal size
        """
        self.size = super().get_available_size(size)
        myindex = (np.abs(AVAILABLE_SIZES - self.size)).argmin()
        return AVAILABLE_IDS_SCH40[myindex]

    def _get_size_sdr(self, id_, sdr):
        """Get the size of an SDR pipe.

        Args:
            - ``id_ (float * u.inch)``: Inner diameter
            - ``sdr (int)``: Standard dimension ratio
        """
        nd = super()._get_available_size((id_ * sdr) / (sdr - 2))
        self.id = self._get_id_sdr(nd, sdr)
        return nd

    def _get_size_sch40(self, id_):
        """Get the size of a SCH40 pipe.

        Args:
            - ``id_ (float * u.inch)``: Inner diameter
        """
        myindex = (np.abs(AVAILABLE_IDS_SCH40 - id_)).argmin()
        self.id = AVAILABLE_IDS_SCH40[myindex]
        return AVAILABLE_SIZES[myindex]

    def ID_SDR_all_available(self, SDR):
        """Return an array of inner diameters with a given SDR."""
        ID = []
        for i in range(len(AVAILABLE_SIZES)):
            ID.append(self._get_id_sdr(AVAILABLE_SIZES[i], SDR).magnitude)
        return ID * u.inch

    @property
    def headloss(self):
        """Return the total head loss from major and minor losses in a pipe."""
        return pc.headloss_fric(
                self.q, self.id, self.l, self.nu, self.pipe_rough
            ).to(u.cm)

    def format_print(self):
        """Return the string representation of this pipe."""
        return 'Pipe: (OD: {}, Size: {}, ID: {}, Length: {}, Spec: {})'.format(
            self.od, self.size, self.id, self.l, self.spec)

    def _rep_ok(self):
        """Verify that this representation of a Pipe is valid."""
        if self.spec not in self.AVAILABLE_SPECS:
            raise AttributeError('spec must be one of:', self.AVAILABLE_SPECS)

        if self.next is not None and self.size != self.next.size:
            raise ValueError('size of the next pipeline component must be the '
            'same size as the current pipeline component')


class Elbow(PipelineComponent):
    """Design class for an Elbow

    Instantiate this class to create a readily constructible Elbow fitting and
    calculate its hydraulic features.

    ``Elbow``'s may be instantiated from a nominal size (to fit into an existing
    pipeline) or inner diameter (to follow hydraulic constraints), but not both.

    Constants:
        - ``AVAILABLE_ANGLES (int * u.deg list)``: The possible angles for this
          fitting.

    Design Inputs:
        - ``q (float * u.L/u.s)``: Flow rate (recommended, defaults to 20L/s)
        - ``temp (float * u.degC)``: Water temperature
          (recommended, defaults to 20°C)
        - ``size (float * u.inch)``: The nominal size
          (recommended, defaults to 0.5 in.)
        - ``fluid_type (str)``: Fluid type. Must be 'water', 'pacl', or 'alum'
          (optional, defaults to 'water')
        - ``next (PipelineComponent)``: The next pipeline component after the
          outlet, cannot be another Elbow or a Tee fitting.
          outlet, cannot be another Elbow or a Tee fitting.
          outlet, cannot be another Elbow or a Tee fitting.
          (optional, defaults to None)
        - ``angle (float * u.deg)``: The angle of the fitting, which must be
          found in ``AVAILABLE_ANGLES`` (recommended, defaults to 90 °)
        - ``id (float * u.inch)``: The inner diameter.
          (recommended, defaults to 0.848 * u.inch)
    """
    AVAILABLE_ANGLES = [90 * u.deg, 45 * u.deg]

    def __init__(self, **kwargs):
        self.angle = 90 * u.deg
        self.id = 0.848 * u.inch

        super().__init__(**kwargs)

        self._set_k_minor()

        if 'size' in kwargs:
            self.id = self._get_id(self.size)
        elif 'id' in kwargs:
            self.size = self._get_size(self.id)

        self._rep_ok()

    def _set_k_minor(self):
        """Sets k minor"""
        if self.angle == 45 * u.deg:
            self.k_minor = hl.EL45_K_MINOR
        elif self.angle == 90 * u.deg:
            self.k_minor = hl.EL90_K_MINOR


    def _get_size(self, id_):
        """Get the size based off the inner diameter.

        Args:
            - ``id_ (float * u.inch)``: Inner diameter
        """
        myindex = (np.abs(AVAILABLE_FITTING_IDS - id_)).argmin()
        self.id = AVAILABLE_FITTING_IDS[myindex]
        return AVAILABLE_FITTING_SIZES[myindex]

    def _get_id(self, size):
        """Get the inner diameter based off the size.

        Args:
            - ``size (float * u.inch)``: Nominal Size
        """
        myindex = (np.abs(AVAILABLE_FITTING_SIZES - size)).argmin()
        self.size = AVAILABLE_FITTING_SIZES[myindex]
        return AVAILABLE_FITTING_IDS[myindex]

    @property
    def headloss(self):
        """The headloss"""
        return pc.elbow_minor_loss(self.q, self.id, self.k_minor).to(u.cm)

    def format_print(self):
        """The string representation for an Elbow Fitting."""
        return 'Elbow: (Size: {}, ID: {}, Angle: {})'.format(
            self.size, self.id, self.angle)

    def _rep_ok(self):
        """Verify that this representation of a Elbow is valid."""
        if self.angle not in self.AVAILABLE_ANGLES:
            raise ValueError('angle must be in ', self.AVAILABLE_ANGLES)

        if self.next is not None and self.size != self.next.size:
            raise ValueError('The next component doesn\'t have the same size.')

class Tee(PipelineComponent):
    """Design class for a Tee

    Instantiate this class to create a readily constructible tee fitting and
    calculate its hydraulic features.

    ``Tee``'s may be instantiated from a nominal size (to fit into an existing
    pipeline) or inner diameter (to follow hydraulic constraints), but not both.

    Constants:
        - ``AVAILABLE_PATHS (str list)``: The available paths for the left and
          right outlet. Branch meaning the flow would turn, run meaning the flow
          stays straight, and stopper meaning there is no flow for that outlet
          due to a stopper.

    Design Inputs:
        - ``q (float * u.L / u.s)``: Flow rate (recommended, defaults to 20L/s)
        - ``temp (float * u.degC)``: Water temperature
          (recommended, defaults to 20°C )
        - ``size (float * u.inch)``: The size (recommended, defaults to 0.5 in.)
        - ``fluid_type (str)``: The type of fluid flowing inside
          (optional, defaults to water)
        - ``left (PipelineComponent)``: The type of piping for the left outlet,
          cannot be an elbow or tee (recommended, defaults to None)
        - ``left_type (str)``: The type of path for the left outlet,
          can only be one of the elements in AVAILABLE_PATHS.
          can only be one of the elements in AVAILABLE_PATHS.
          can only be one of the elements in AVAILABLE_PATHS.
          (recommended, defaults to 'branch')
        - ``right (PipelineComponent)``: The type of piping for the right outlet,
          cannot be an elbow or tee. (recommended, defaults to None)
        - ``right_type (str)``: The type of path for the right outlet,
          can only be one of the elements in AVAILABLE_PATHS.
          can only be one of the elements in AVAILABLE_PATHS.
          can only be one of the elements in AVAILABLE_PATHS.
          (recommended, defaults to 'stopper')
        - ``id (float * u.inch)``: The inner diameter.
          (recommended, defaults to 0.848 * u.inch)

        """
    AVAILABLE_PATHS = ['branch', 'run', 'stopper']

    def __init__(self, **kwargs):
        self.left = None
        self.left_type = 'branch'

        self.right = None
        self.right_type = 'stopper'

        self.id = 0.848 * u.inch

        super().__init__(**kwargs)

        self._set_k_minor()
        self._set_next()

        if 'size' in kwargs:
            self.id = self._get_id(self.size)
        elif 'id' in kwargs:
            self.size = self._get_size(self.id)

        self._rep_ok()

    def _set_k_minor(self):
        """Sets k minor for the left and right outlet"""
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

    def _set_next(self):
        """Sets the next outlet as well the the type of branch for the next
        outlet.
        """
        if self.left_type == 'stopper':
            self.next = self.right
            self.next_type = self.right_type
        else:
            self.next = self.left
            self.next_type = self.left_type

    def _headloss_left(self):
        """The headloss of the left outlet"""
        return pc.elbow_minor_loss(self.q, self.id, self.left_k_minor).to(u.cm)

    def _headloss_right(self):
        """The headloss of the right outlet"""
        return pc.elbow_minor_loss(self.q, self.id, self.right_k_minor).to(u.cm)

    @property
    def headloss(self):
        """The headloss"""
        if self.left_type =='stopper':
            return self._headloss_right()
        else:
            return self._headloss_left()

    def _get_size(self, id_):
        """Get the nominal size based off the inner diameter

        Args:
            - ``id_ (float * u.inch)``: Inner diameter
        """
        myindex = (np.abs(AVAILABLE_FITTING_IDS - id_)).argmin()
        self.id = AVAILABLE_FITTING_IDS[myindex]
        return AVAILABLE_FITTING_SIZES[myindex]

    def _get_id(self, size):
        """Get the inner diameter based off the size.

        Args:
            - ``size (float * u.inch)``: Nominal size
        """
        myindex = (np.abs(AVAILABLE_FITTING_SIZES - size)).argmin()
        self.size = AVAILABLE_FITTING_SIZES[myindex]
        return AVAILABLE_FITTING_IDS[myindex]

    def format_print(self):
        """The string representation of this tee."""
        return 'Tee: (Size: {}, ID: {}, Next Path Type: {})'.format(
            self.size, self.id, self.next_type)

    def _rep_ok(self):
        """Verify that this representation of a Tee is valid."""
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

        if self.next is not None and type(self.next) in [Elbow, Tee]:
             raise ValueError('Tees cannot be followed by other fittings.')
