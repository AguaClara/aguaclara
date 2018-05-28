#Here we import packages that we will need for this notebook. You can find out about these packages in the Help menu.

# although math is "built in" it needs to be imported so it's functions can be used.
import math

from scipy import constants, interpolate

#see numpy cheat sheet https://www.dataquest.io/blog/images/cheat-sheets/numpy-cheat-sheet.pdf
#The numpy import is needed because it is renamed here as np.
import numpy as np

import pandas as pd

import matplotlib.pyplot as plt

# add imports for AguaClara code that will be needed
# physchem has functions related to hydraulics, fractal flocs, flocculation, sedimentation, etc.
from aide_design import physchem as pc

# pipedatabase has functions related to pipe diameters
from aide_design import pipedatabase as pipe

# units allows us to include units in all of our calculations
from aide_design.units import unit_registry as u

# utility has the significant digit display function
from aide_design import utility as ut

##---##

# The following constants need to go into the constants file
Pi_LFOM_safety = 1.2
# pipe schedule for LFOM
SDR_LFOM = 26

FLOW = 5*u.L/u.s
HL_LFOM = 20*u.cm

ratio_VC_orifice= 0.62

from enum import Enum

class uomeasure(Enum):
    english = 0
    metric = 1

def drill_series(uomeasure):
    if uomeasure is uomeasure.english:
        ds=np.arange(1/32, 1/4, 1/32)
        ds=np.append(ds,np.arange(3/8, 1, 1/8))
        ds=np.append(ds,np.arange(1.25, 3.25, 1/4))
        ds=ds*u.inch
    else:
        ds=np.arange(0.5, 4.9, 0.1)
        ds=np.append(ds,np.arange(5, 19, 1))
        ds=np.append(ds,np.arange(20, 50, 2))
        ds=ds*u.mm
    return ds

# Take the values of the array, compare to x, find the index of the first value less than or equal to x
def floor_nearest(x,array):
    myindex = np.argmax(array <= x)
    return array[myindex]

# Take the values of the array, compare to x, find the index of the first value greater or equal to x
def ceil_nearest(x,array):
    myindex = np.argmax(array >= x)
    return array[myindex]

class LFOM: 

    def __init__(self, flow, hl, ratio_safety, sdr, drill_series_uom):
        self.flow = flow
        self.hl = hl 
        self.ratio_safety = ratio_safety
        self.sdr = sdr
        self.drill_series_uom = drill_series_uom

    def set_flow(self, flow):
        self.flow = flow

    def set_hl(self, hl):
        self.hl = hl

    def set_ratio_safety(self, ratio_safety):
        self.ratio_safety = ratio_safety

    def set_sdr(self, sdr):
        self.sdr = sdr

    def set_drill_series(self, drill_series_uom):
        self.drill_series_uom = drill_series_uom


    def __width_stout(self, z):
        return 2 / ((2 * u.g_0 * z)**(1/2) * math.pi * self.hl)

    def __n_rows(self):
        n_est = (self.hl * math.pi / (2 * self.__width_stout(self.hl) * self.flow)).to(u.dimensionless)
        return min(10, max(4, math.trunc(n_est.magnitude)))

    def __dist_center_rows(self):
        return self.hl / self.__n_rows()

    # average vertical velocity of the water inside the LFOM pipe 
    # at the very bottom of the bottom row of orifices
    # The speed of falling water is 0.841 m/s for all linear flow orifice meters of height 20cm,
    # independent of total plant flow rate.
    def __vol_pipe_critical(self):
        return (4 / (3 * math.pi) * (2 * u.g_0 * self.hl)**(1/2)).to(u.m/u.s)

    def __area_pipe_min(self):
        return (self.ratio_safety * self.flow / self.__vol_pipe_critical()).to(u.m**2)

    def nom_diam_pipe(self):
        id = pc.diam_circle(self.__area_pipe_min())
        return pipe.ND_SDR_available(id, self.sdr)

    # another possibility is to use integration to solve this problem.
    # Here we use the width of the stout weir in the center of the top row
    # to estimate the area of the top orifice
    def __area_orifices_max(self):
        z = self.hl - 0.5 * self.__dist_center_rows()
        return self.flow * self.__width_stout(z) * self.__dist_center_rows()

    def __d_orifices_max(self):
        return pc.diam_circle(self.__area_orifices_max())

    def drillbit_diameter(self):
        return ceil_nearest(self.__d_orifices_max(), drill_series(self.drill_series_uom))

    def __drillbit_area(self):
        return pc.area_circle(self.drillbit_diameter())

    ##A bound on the number of orifices allowed in each row.  
    ##The distance between consecutive orifices must be enough to retain structural integrity of the pipe
    def __n_orifices_per_row_max(self):
        S_lfom_orifices_Min= 3 * u.mm
        nom_diam = self.nom_diam_pipe()
        drillbit_diam = self.drillbit_diameter() + S_lfom_orifices_Min
        return math.floor(math.pi * (pipe.ID_SDR(nom_diam, self.sdr)) / (drillbit_diam))

    #locations where we will try to get the target flows is in between orifices at elevation Pi.H
    def __flow_ramp(self):
        dist_center = self.__dist_center_rows() / u.cm
        return np.arange(dist_center, self.hl / u.cm, dist_center) * self.flow * u.cm / self.hl

    def height_orifices(self):
        drillbit_diam = self.drillbit_diameter() * 0.5
        return np.arange(drillbit_diam, self.hl, self.__dist_center_rows(), dtype= object)

    #Calculate the flow for a given number of submerged rows of orifices
    def __flow_actual(self, Row_Index_Submerged, N_LFOM_Orifices):
        D_LFOM_Orifices = self.drillbit_diameter().to(u.m)
        FLOW_new=[]
        dist_center = self.__dist_center_rows()
        for i in range(Row_Index_Submerged):
            h = np.arange(dist_center, self.hl, dist_center, dtype=object)
            h = h[Row_Index_Submerged].to(u.m)
            d = np.arange(0.5* D_LFOM_Orifices, self.hl, dist_center, dtype=object)
            FLOW_new.append(N_LFOM_Orifices[i]*(pc.flow_orifice_vert(D_LFOM_Orifices, h - d[i], ratio_VC_orifice)))
        return sum(FLOW_new)

    #Calculate number of orifices at each level given a diameter
    def fric_n_orifices(self):
        FLOW_ramp_local = self.__flow_ramp()
        D_LFOM_Orifices = self.drillbit_diameter()
        h = np.arange(self.__dist_center_rows(), self.hl, self.__dist_center_rows(), dtype=object)
        d = np.arange(D_LFOM_Orifices * 0.5, self.hl, self.__dist_center_rows(), dtype=object)
        n = []
        for i in range (len(d) - 1):
            flow_actual = self.__flow_actual(i, n)
            Height = h[i] - d[i]
            rounded = np.round((FLOW_ramp_local[i] - flow_actual).to(u.m**3 / u.seconds) / pc.flow_orifice_vert(D_LFOM_Orifices, Height, ratio_VC_orifice))
            if self.nom_diam_pipe() <= 12 * u.inch:
                n.append(min(max(0, rounded), self.__n_orifices_per_row_max()))
            else:
                n.append(max(0,rounded))
        return n

    #This function calculates the error of the design based on the differences between the predicted flow rate
    #and the actual flow rate through the LFOM.
    def __flow_error(self):
        N_lfom_orifices = self.fric_n_orifices()
        FLOW_lfom_error = []
        for j in range (len(N_lfom_orifices) - 1):
            flow_actual = self.__flow_actual(j, N_lfom_orifices)
            FLOW_lfom_error.append((flow_actual - self.__flow_ramp()[j]) / self.flow)
        return FLOW_lfom_error

    def __flow_error_max(self):
        x = max(self.__flow_error())
        y = x**2
        return y**1/2

    def __flow_ideal(self, height):
        __flow_ideal=(self.flow * height) / self.hl
        return __flow_ideal
    
    def flow_lfom(self, height):
        D_lfom_orifices = self.drillbit_diameter()
        H_submerged = np.arange(height - 0.5 * D_lfom_orifices, self.hl, height - self.__dist_center_rows(), dtype=object)
        N_lfom_orifices = self.fric_n_orifices()
        flow = []
        for i in range (len(H_submerged)):
            flow.append(pc.flow_orifice_vert(D_lfom_orifices, H_submerged[i], ratio_VC_orifice) * N_lfom_orifices[i])
        return sum(flow)


lfom = LFOM(FLOW, HL_LFOM, Pi_LFOM_safety, SDR_LFOM, uomeasure.english)

print(lfom.nom_diam_pipe())
print(lfom.drillbit_diameter())
print(lfom.height_orifices())
print(lfom.fric_n_orifices())