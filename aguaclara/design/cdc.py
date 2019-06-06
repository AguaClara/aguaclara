"""The chemical dose controller (CDC) in a """

import aguaclara.core.physchem as pc
import aguaclara.core.utility as ut
from aguaclara.core.units import unit_registry as u
import aguaclara.core.constants as con


import numpy as np

class CDC(object):
    def init(self, q,
             coag_dose_conc_max, #What should this default to? -Oliver L., 6 Jun 19
             coag_type='pacl',
             temp=20 * u.degC,
             coag_stock_conc_est=150 * u.g / u.L,
             chem_tank_vol_supplier=[208.198, 450, 600, 750, 1100, 2500] * u.L,
             chem_tank_dimensions_supplier=[
                 [0.571, 0.851],
                 [0.85, 0.99],
                 [0.96, 1.10],
                 [1.10, 1.02],
                 [1.10, 1.39],
                 [1.55, 1.65]
             ] * u.m,
             coag_stock_min_est_time=1 * u.day,
             train_n=1,
             coag_sack_mass = 25 * u.kg,
             coag_tube_id = 0.125 * u.inch,
             error_ratio=0.1,
             hl = 20 * u.cm,
             tube_k = 2):
        self.q = q

        if coag_type.lower() not in ['pacl', 'alum']:
            raise ValueError('coag_type must be either PACl or Alum.')
        self.coag_type = coag_type

        self.temp = temp
        self.coag_dose_conc_max = coag_dose_conc_max
        self.coag_stock_conc_est = coag_stock_conc_est
        self.chem_tank_vol_supplier = chem_tank_vol_supplier
        self.chem_tank_dimensions_supplier = chem_tank_dimensions_supplier
        self.coag_stock_min_est_time = coag_stock_min_est_time
        self.train_n = train_n
        self.coag_sack_mass = coag_sack_mass
        self.coag_tube_id = coag_tube_id
        self.error_ratio = error_ratio
        self.hl = hl
        self.tube_k = tube_k

    def _alum_nu(self, coag_conc):
        """Return the dynamic viscosity of water at a given temperature.

        If given units, the function will automatically convert to Kelvin.
        If not given units, the function will assume Kelvin.
        This function assumes that the temperature dependence can be explained
        based on the effect on water and that there is no confounding effect from
        the coagulant.
        """
        alum_nu = \
            (1 + (4.255 * 10 ** -6) * coag_conc.magnitude ** 2.289) * \
            pc.viscosity_kinematic(self.temp)
        return alum_nu

    def _pacl_nu(self, coag_conc):
        """Return the dynamic viscosity of water at a given temperature.

        If given units, the function will automatically convert to Kelvin.
        If not given units, the function will assume Kelvin.
        This function assumes that the temperature dependence can be explained
        based on the effect on water and that there is no confounding effect from
        the coagulant.
        """
        pacl_nu = \
            (1 + (2.383 * 10 ** -5) * (coag_conc).magnitude ** 1.893) * \
            pc.viscosity_kinematic(self.temp)
        return pacl_nu

    def _coag_nu(self, coag_conc, coag_type):
        """Return the dynamic viscosity of water at a given temperature.

        If given units, the function will automatically convert to Kelvin.
        If not given units, the function will assume Kelvin.
        """
        if coag_type.lower() == 'alum':
            coag_nu = self._alum_nu(coag_conc)
        elif coag_type.lower() == 'pacl':
            coag_nu = self._pacl_nu(coag_conc)
        return coag_nu

    @property
    def coag_q_max_est(self):
        coag_q_max_est = self.q * self.coag_dose_conc_max / \
            self.coag_stock_conc_est
        return coag_q_max_est
    
    @property
    def coag_stock_vol(self):
        coag_stock_vol = ut.ceil_nearest(
                self.coag_stock_min_est_time * self.train_n * 
                    self.coag_q_max_est,
                self.chem_tank_vol_supplier
            )
        return coag_stock_vol
        
    @property
    def coag_sack_n(self):
        coag_sack_n = round(
                self.coag_stock_vol * self.coag_stock_conc_est /
                self.coag_sack_mass
            )
        return coag_sack_n
    
    @property
    def coag_stock_conc(self):
        coag_stock_conc = self.coag_sack_n * self.coag_sack_mass / \
            self.coag_stock_vol
        return coag_stock_conc

    @property
    def coag_q_max(self):
        return self.q * self.coag_dose_conc_max / self.coag_stock_vol

    @property
    def coag_stock_time_min(self):
        return self.coag_stock_vol / (self.train_n * self.coag_q_max)

    @property
    def coag_stock_nu(self):
        return self._coag_nu(self.coag_stock_conc, self.coag_type)    
#==============================================================================
# Small-diameter Tube Design
#==============================================================================
    @property
    def _coag_tube_q_max(self):
        """The maximum permissible flow through a coagulant tube."""
        coag_tube_q_max = ((np.pi * self.coag_tube_id ** 2)/4) * \
            np.sqrt((2 * self.error_ratio * self.hl * con.gravity)/self.tube_k)
        return coag_tube_q_max
    
    @property
    def coag_tubes_active_n(self):
        coag_tubes_active_n = np.ceil(self.coag_q_max / self._coag_tube_q_max)
        return coag_tubes_active_n

    @property
    def coag_tubes_n(self):
        coag_tubes_n = self.coag_tubes_active_n + 1 
        return coag_tubes_n
        
    @property
    def coag_tube_operating_q_max(self):
        """The maximum flow through a coagulant tube during actual operation."""
        coag_tube_operating_q_max = self.coag_q_max / self.coag_tubes_active_n
        return coag_tube_operating_q_max
    
    @property
    def coag_tube_l(self):
        coag_tube_l = (
                self.hl * con.GRAVITY * np.pi * self.coag_tube_id ** 4 /
                (128 * self.coag_stock_nu * self.coag_tube_operating_q_max)
            ) - (
                8 * self.coag_tube_operating_q_max * self.tube_k /
                (128 * np.pi * self.coag_stock_nu)
            )
        return coag_tube_l

    @property
    def coag_tank_r(self):
        index = self.chem_tank_vol_supplier.index(self.coag_stock_vol)
        coag_tank_r = self.chem_tank_dimensions_supplier[index][0] / 2
        return coag_tank_r
        
    @property
    def coag_tank_h(self):
        index = self.chem_tank_vol_supplier.index(self.coag_stock_vol)
        coag_tank_h = self.chem_tank_dimensions_supplier[index][1]
        return coag_tank_h

    def _DiamTubeAvail(self, en_tube_series = True):
        if en_tube_series:
            return 1*u.mm
        else:
            return (1/16)*u.inch


# testing
FlowPlant = 100*u.L/u.s
DiamTubeAvail = np.array(np.arange(1/16,6/16,1/16))*u.inch
temp = u.Quantity(20,u.degC)
HeadlossCDC = 20*(u.cm)
ConcStock = 51.4*(u.gram/u.L)
ConcDoseMax = 2*(u.mg/u.L)
LenCDCTubeMax = 4 * u.m
en_chem = 2
KMinor = 2
Ratio_Error=0.1
x=len_cdc_tube(FlowPlant, ConcDoseMax, ConcStock,
                 DiamTubeAvail, HeadlossCDC, LenCDCTubeMax, temp,
                 en_chem, KMinor)
#print(x)
#print(diam_cdc_tube(FlowPlant, ConcDoseMax, ConcStock, DiamTubeAvail, HeadlossCDC, LenCDCTubeMax, temp, en_chem, KMinor).to(u.inch))
#print(n_cdc_tube(FlowPlant, ConcDoseMax, ConcStock, DiamTubeAvail, HeadlossCDC, LenCDCTubeMax, temp, en_chem, KMinor))
LEVER_ARM_L = 0.5 * u.m
LEVER_CYLINDER_1_D = 1 * u.inch
LEVER_CYLINDER_4_D = 2 * u.inch
LEVER_CYLINDER_2_D = 0.5 * u.inch
LEVER_CYLINDER_2_PIVOT_DIST = 6 * u.cm
CYLINDER_2_CYLINDER_3_DIST = 9.5 * u.cm
LEVER_PIVOT_BOX_L = 2 * u.inch
LEVER_PIVOT_BOX_W = 1 * u.inch
LEVER_PIVOT_BOX_H = 1 * u.inch
LEVER_ARM_THICKNESS = 0.125 * u.inch
LEVER_ARM_H = 1 * u.inch
LEVER_INNERBAR_L = 7 * u.inch
LEVER_MOUNTING_PLATE_L = 6 * u.inch
LEVER_MOUNTING_PLATE_W = 0.5 * u.cm
LEVER_MOUNTING_PLATE_H = 2 * u.inch
LEVER_TO_ENT_TANK_Z_TOP_S = 1 * u.cm
FLOAT_THICKNESS = 5 * u.cm
FLOAT_CABLE_D = 0.5 * u.cm
LEVER_SLIDER_ORIGIN_TO_SCREW_L = 1 * u.inch
LEVER_SLIDER_THICKNESS = 0.25 * u.inch
LEVER_SLIDER_H = 1.5 * u.inch
LEVER_SLIDER_L = 3 * u.inch
LEVER_SLIDER_SHORT_H = 0.125 * u.inch
LEVER_CYLINDER_L = 6 * u.inch
ENT_TANK_FRONT_WALL_TO_CDC_FLOAT_L = 0.874 * u.m

LEVER_L = 0.5 * u.m #This may be obsolete now... mrf222 2/10/16

LEVER_ARM_W = 0.0032 * u.m

LEVER_ARM_H = 0.0254 * u.m

D_CDC_CHT = 6 * u.inch

#Distance from the top of the entrance tank to the to the middle of the
# lever arm hole for the cable - (minus the) radius of the hole.
LEVER_HOLE_H = 0.0132 * u.m - (0.0095/2 * u.m)

DIAM_CABLE = 0.1 * u.inch

#Edited DLABOrigintoLAOriginZ to accommodate dimensions from McMaster
# vs Inserted Drawing
DIAM_LAB_ORIGIN_TO_LA_ORIGIN_Z = 0.0245 * u.m

#Distance from the lever arm origin to the outside center of the top part
# of the drop tube in the y direction.
LA_ORIGIN_TO_DT_Y_L = 0.7812 * u.m

#Distance from the lever arm origin to the drop tube in the z direction.
LA_ORIGIN_TO_DT_Z_L = 0.0429 * u.m

#Distance from the lever arm origin to the center of the drop tube in the
#x direction.
LA_ORIGIN_TO_DT_CENTER_X_L = 0.0290 * u.m

#Measured from CDC research team's apparatus.
CDC_REDUCER_THICKNESS = 9.5 * u.mm

#Distance from the lever arm origin to the center of the reducer in the
# x direction.
LA_ORIGIN_TO_REDUCER_X_L = 0.0290 * u.m

#Distance from the lever arm origin to the outside center of the top part
# of the reducer in the y direction.
LA_ORIGIN_TO_REDUCER_Y_L = 0.7135 * u.cm

#Distance from the lever arm origin to the center of the reducer in the
# x direction.
LA_ORIGIN_TO_REDUCER_CENTER_X_L = 0.0290 * u.m

#Distance from the lever arm origin to the center of the reducer in the
# y direction.
LA_ORIGIN_TO_REDUCER_CENTER_Y_L = 0.7919 * u.m

LEVER_BRACKET_W = 0.625 * u.inch

LEVER_BRAKCET_L = 1.5 * u.inch

RADIUS_LA_BAR = 0.375 * u.inch

LEVER_BRACKET_THICKNESS = 0.08 * u.inch

DIAM_LA_BAR = 0.375 * u.inch

LA_BAR_L = 4 * u.inch

SLIDER_L = 3 * u.inch

SLIDER_W = 3.2 * 10**-3 * u.m

DROPTUBE_ND = 0.5 * u.inch

SLIDER_H = 0.625 * u.inch

DROPTUBE_L = 0.61 * u.m

#The length of the drop tube needs to be calculated. The drop tube must be
# as long as the supercritical flow.
#Thus the drop tube must extend down to the elevation of the sed tank
# effluent weir. This constant should be removed!

#Outer diameter of fitting- measured from CDC research team's fittin
OUTER_D_CDC_FITTING = 5/32 * u.inch

#Inner diameter of fitting- measured from CDC research team's fitting
CDC_FITTING_ID = 0.126 * u.inch

#Length of fitting - measured from CDC research team's fitting
CDC_FITTING_L = 0.75 * u.inch

#st587 addition
##Constant Head Tank Dimensions

#five gallons bucket dimensions for constant head tanks

DIAM_CHT = 10 * u.cm

CHT_H = 37/3 * u.cm

CHT_WALL_THICKNESS = 1/3 * u.cm

DELIVERY_PIPE_ND = 0.6 * u.inch

PIPE_SCHEDULE_FLEX_TUBE = 2

PVC_BALL_VALVE_L = 0.1625/4 * u.cm

MOUNTING_BOARD_THICKNESS = 1.5 * u.inch

##Manifold Dimensions

SPACE_CDC_LEVER_TO_MANIFOLD = 40 * u.cm

CHLOR_AIR_RELEASE_PIPE_L = 30 * u.cm #Arbitratily selected

# 0 is alum, 1 is PACl
# EN_COAG=1

COAG_SACK_MASS = 25 * u.kg

# The coagulant stock is relatively stable and can last many days. Here we
# set the minimum time the coagulant stock will last when applying the
# maximum possible dose to size the stock tanks. In general the dose will
# be less than this and the stock will last much longer.
COAG_STOCK_MIN_EST_TIME = 1 * u.day

# Want chlorine stock to run out on average every day so that the stock
# is made fresh frequently because the chlorine stock degrades with time
# depending on temperature, concentration, and pH.
CHLOR_STOCK_AVE_TIME = 1 * u.day

COAG_TUBE_ID = 0.125 * u.inch
# 1/8" tubes are readily available in hardware stores in Honduras
CHLOR_TUBE_ID = 0.125 * u.inch

COAG_STOCK_EST_CONC = 150 * u.g / u.L

CHLOR_STOCK_EST_CONC = 15 * u.g / u.L

CHLOR_P = 0.7

# This is the elevation difference between the outlet of the coagulant
# stock tanks and the water level in the constant head tank, which is set
# by the hydraulic head required to provide the desired max chemical flow
# rate through the float valve orifice in the CHT.
# It is treated as constant here to ensure a practical elevation difference
# is left between the stock tanks and the CHT even when a float valve is
# selected which requires very little hydraulic head to deliver the
# required maximum chemical flow rate.
COAG_TANK_ABOVE_HEAD_TANK_H = 30 * u.cm

# This is the distance from the bottom of the stock tanks to the outlets
# to allow space for solids to settle.
CENTER_STOCK_OUTLET_DIST = 10 * u.cm

# Distance between a tank and the border of the platform
CHEM_TANK_BORDER_S = 5 * u.cm

# This is the estimated elevation difference between the water level in
# the constant head tank and the top of the entrance tank wall.
# The constant head tank water level is the same as the elevation of the
# outlet of the dosing tube when the lever arm is horizontal (zero flow).
# Therefore this height depends only on the hardware used to make the
# slider/drop tube assembly and to mount the lever arm to the entrance
# tank wall.
# Note that this will vary depending on hardware used, and is only
# defined here to calculate the elevation of the stock tanks, which can
# be approximate.
DOSER_ASSEMBLY_H = 6.77 * u.cm

# Maximum error allowed between a linear flow vs tube head loss
# relationship and the actual performance (which is affected by non-linear
# minor losses), assuming calibration at the maximum flow rate.
LINEAR_CDC_ERROR_RATIO = 0.1

# Estimated minor loss coefficient for the small-diameter flexible tubing
# using fittings that have larger ID than the tubing.
CDC_TUBE_K_MINOR = 2

# Head loss through the doser at maximum flow rate.
# Maximum head loss through the small-diameter dosing tubing, which
# corresponds to the variation in water levels in the entrance tank and
# the difference between the maximum and minimum elevation of the dosing
# tube outlet attached to the lever arm.
HL = 20 * u.cm

# Estimated distance between fluid level in constant head tank and float
# valve orifice
FLOAT_VALVE_H = 5 * u.cm

# Nominal diameter of the PVC plumbing for the chlorine dosing system.
CHLOR_PIPE_ND = 0.5 * u.inch

# Nominal diameter of the PVC plumbing for the coagulant dosing system.
COAG_PIPE_ND = 0.5 * u.inch

# Supplier Information:
# http://www.rotoplas.com/assets/files/industria/catalogo.pdf
# 5-gallon bucket
# http://www.mcmaster.com/#storage-buckets/=kd23oh
# 35-gallon drum
# http://www.jlmovingsupplies.com/c31/DIXIE-OPEN-CLOSED-HEAD-DRUMS-p36721.html
VOL_CHEM_TANK_AVAIL = [5 * u.gal, 35 * u.gal, 55 * u.gal,
                       450 * u.L, 750 * u.L, 1100 * u.L, 2500 * u.L]

D_CHEM_TANK_AVAIL = [11.875 * u.inch, 20.75 * u.inch, 22.5 * u.inch,
                     0.85 * u.m, 1.10 * u.m, 1.10 * u.m, 1.55 * u.m]

CHEM_TANK_AVAIL_H = [17.75 * u.inch, 31.75 * u.inch, 33.5 * u.inch,
                     0.99 * u.inch, 1.02 * u.inch, 1.39 * u.inch,
                     1.65 * u.inch]

##added 12/5/16 by mrf222 ensures weir does not overtop backwards if
# filter weir is too high
SED_WEIR_FREE_BOARD_H = 5 * u.cm

# Space beyond the entrance tank in the plant drain channel where the
# drop pipes from the CDC lever arm can come down and be connected with
# the chlorine and coagulant dosing points.
CHEM_LEVER_ARM_SPACE_L = 75 * u.cm
DIAM_TUBE_ENGLISH = [1, 2, 3 ,4 ,5 ,6, 7]*u.inch/16
DIAM_TUBE_METRIC = [2, 3, 4, 6, 8, 10]*u.mm
DIAM_FLT_VLV_ORIFICES_AVAIL = [0.093, 0.187, 0.25, 0.312]*u.inch
