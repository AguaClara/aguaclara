"""The chemical dose controller (CDC) of an AguaClara plant uses the linear
relation between flow rate and entrance tank water level (set by the LFOM) to
dose the correct amount of coagulant and chlorine into the entrance tank.

Example:
    >>> from aguaclara.design.cdc import *
    >>> cdc = CDC(q = 20 * u.L/u.s, coag_type = 'pacl')
    >>> cdc.coag_stock_vol
    <Quantity(2500.0, 'liter')>
"""
import aguaclara.core.physchem as pc
import aguaclara.core.utility as ut
from aguaclara.core.units import u
from aguaclara.design.component import Component
import warnings

import numpy as np

class CDC(Component):
    """Design an AguaClara plant's chemical dose controller.

    Design Inputs:
        - ``q (float * u.L / u.s)``: Flow rate (required)
    """
    def __init__(self, **kwargs):
        self.hl = 20 * u.cm
        self.coag_type='pacl'
        if self.coag_type.lower() not in ['pacl', 'alum']:
            raise ValueError('coag_type must be either PACl or Alum.')

        self.coag_dose_conc_max=100 * u.mg / u.L
        self.coag_stock_conc=150 * u.g / u.L
        self.coag_stock_conc_est=150 * u.g / u.L # Deprecated since January 2021
        self.coag_stock_min_est_time=1 * u.day
        self.chem_tank_vol_supplier=[208.198, 450, 600, 750, 1100, 2500] * u.L
        self.chem_tank_dimensions_supplier=[
            [0.571, 0.851],
            [0.85, 0.99],
            [0.96, 1.10],
            [1.10, 1.02],
            [1.10, 1.39],
            [1.55, 1.65]
        ] * u.m
        self.train_n=1
        self.coag_sack_mass = 25 * u.kg
        self.coag_tube_id = 0.125 * u.inch
        self.error_ratio=0.1
        self.tube_k = 2

        super().__init__(**kwargs)

    def alum_nu(self, coag_conc):
        """
        Return the dynamic viscosity of water at a given temperature.

        If given units, the function will automatically convert to Kelvin.
        If not given units, the function will assume Kelvin.
        This function assumes that the temperature dependence can be explained
        based on the effect on water and that there is no confounding effect from
        the coagulant.
        """
        alum_nu = \
            (1 + (4.255 * 10 ** -6) * coag_conc.magnitude ** 2.289) * \
            pc.viscosity_kinematic_water(self.temp)
        return alum_nu
    
    def _alum_nu(self, coag_conc):
        """
        .. deprecated::
            `_alum_nu` is deprecated; use `alum_nu` instead.
        """
        # Deprecated since January 2021
        warnings.warn('_alum_nu is deprecated; use alum_nu instead.',
                  UserWarning)
    
        return self.alum_nu(coag_conc)
        
    def pacl_nu(self, coag_conc):
        """Return the dynamic viscosity of water at a given temperature.

        If given units, the function will automatically convert to Kelvin.
        If not given units, the function will assume Kelvin.
        This function assumes that the temperature dependence can be explained
        based on the effect on water and that there is no confounding effect 
        from the coagulant.
        """
        pacl_nu = \
            (1 + (2.383 * 10 ** -5) * (coag_conc).magnitude ** 1.893) * \
            pc.viscosity_kinematic_water(self.temp)
        return pacl_nu

    def _pacl_nu(self, coag_conc):
        """
        .. deprecated::
            `_pacl_nu` is deprecated; use `pacl_nu` instead.
        """
        # Deprecated since January 2021
        warnings.warn('_pacl_nu is deprecated; use pacl_nu instead.',
                  UserWarning)
    
        return self.pacl_nu(coag_conc)
        
    def _coag_nu(self, coag_conc, coag_type):
        """
        .. deprecated::
            `_coag_nu` is deprecated; use `coag_nu` instead.
        """
        # Deprecated since January 2021
        warnings.warn('_coag_nu is deprecated; use coag_nu instead.',
                  UserWarning)
    
        return self.coag_nu(coag_conc, coag_type)
       
    def coag_nu(self, coag_conc, coag_type):
        """Return the dynamic viscosity of water at a given temperature.

        If given units, the function will automatically convert to Kelvin.
        If not given units, the function will assume Kelvin.
        """
        if coag_type.lower() == 'alum':
            coag_nu = self.alum_nu(coag_conc)
        elif coag_type.lower() == 'pacl':
            coag_nu = self.pacl_nu(coag_conc)
        return coag_nu

    @property
    def coag_q_max_est(self):
        """The estimated maximum permissible flow rate of the coagulant stock,
        based on a whole number of sacks of coagulant used.

        .. deprecated::
            `coag_q_max_est` is deprecated; use `coag_q_max` instead, which is
            based on the exact user-defined coagulant stock concentration, 
            `coag_stock_conc`.
        """
        # Deprecated since January 2021
        warnings.warn('coag_q_max_est is deprecated; use coag_q_max instead,\
            which is based on the exact user-defined coagulant stock \
            concentration, coag_stock_conc.', UserWarning)
        
        coag_q_max_est = self.q * self.coag_dose_conc_max / \
            self.coag_stock_conc_est
        return coag_q_max_est

    @property
    def coag_q_max(self):
        """The maximum permissible flow rate of the coagulant stock."""
        coag_q_max = self.q * self.coag_dose_conc_max / self.coag_stock_conc
        return coag_q_max.to(u.L / u.s)

    @property
    def coag_stock_vol(self):
        """The volume of the coagulant stock tank, based on available sizes
        from the supplier.
        """
        coag_stock_vol = ut.ceil_nearest(
                self.coag_stock_min_est_time * self.train_n *
                    self.coag_q_max,
                self.chem_tank_vol_supplier
            )
        return coag_stock_vol

    @property
    def coag_sack_n(self):
        """The number of sacks of coagulant needed to make the coagulant stock,
        rounded to the nearest whole number.
        """
        coag_sack_n = round(
                (self.coag_stock_vol * self.coag_stock_conc /
                self.coag_sack_mass).to_base_units()
            )
        return coag_sack_n

    # Commented out January 2021
    # @property
    # def coag_stock_conc(self):
    #     """The concentration of the coagulant stock."""
    #     coag_stock_conc = self.coag_sack_n * self.coag_sack_mass / \
    #         self.coag_stock_vol
    #     return coag_stock_conc

    @property
    def coag_stock_time_min(self):
        """The minimum amount of time that the coagulant stock will last."""
        return self.coag_stock_vol / (self.train_n * self.coag_q_max)

    @property
    def coag_stock_nu(self):
        """The kinematic viscosity of the coagulant stock."""
        return self.coag_nu(self.coag_stock_conc, self.coag_type)
#==============================================================================
# Small-diameter Tube Design
#==============================================================================
    @property
    def _coag_tube_q_max(self):
        """The maximum permissible flow through a coagulant tube."""
        coag_tube_q_max = ((np.pi * self.coag_tube_id ** 2)/4) * \
            np.sqrt((2 * self.error_ratio * self.hl * u.gravity)/self.tube_k)
        return coag_tube_q_max.to(u.L / u.s)

    @property
    def coag_tubes_active_n(self):
        """The number of coagulant tubes in use."""
        coag_tubes_active_n = \
            np.ceil((self.coag_q_max / self._coag_tube_q_max).to_base_units())
        return coag_tubes_active_n

    @property
    def coag_tubes_n(self):
        """The number of coagulant tubes in use, plus a spare tube for 
        maintenance.
        """
        coag_tubes_n = self.coag_tubes_active_n + 1
        return coag_tubes_n

    @property
    def coag_tube_operating_q_max(self):
        """The maximum flow through a coagulant tube during actual operation."""
        coag_tube_operating_q_max = self.coag_q_max / self.coag_tubes_active_n
        return coag_tube_operating_q_max

    @property
    def coag_tube_l(self):
        """The length of a coagulant tube."""
        coag_tube_l = (
                self.hl * u.gravity * np.pi * self.coag_tube_id ** 4 /
                (128 * self.coag_stock_nu * self.coag_tube_operating_q_max)
            ) - (
                8 * self.coag_tube_operating_q_max * self.tube_k /
                (128 * np.pi * self.coag_stock_nu)
            )
        return coag_tube_l.to_base_units()

    @property
    def coag_tank_r(self):
        """The radius of the coagulant stock tank, based on available sizes
        from the supplier."""
        index = np.argmax(self.chem_tank_vol_supplier == self.coag_stock_vol)
        coag_tank_r = self.chem_tank_dimensions_supplier[index][0] / 2
        return coag_tank_r

    @property
    def coag_tank_h(self):
        """The height of the coagulant stock tank, based on available sizes
        from the supplier."""
        index = np.argmax(self.chem_tank_vol_supplier == self.coag_stock_vol)
        coag_tank_h = self.chem_tank_dimensions_supplier[index][1]
        return coag_tank_h

    def _DiamTubeAvail(self, en_tube_series = True):
        if en_tube_series:
            return 1*u.mm
        else:
            return (1/16)*u.inch
