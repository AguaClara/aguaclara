# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 17:16:46 2017

@author: cc2467
"""

#Here we import packages that we will need for this notebook. You can find out about these packages in the Help menu.

# although math is "built in" it needs to be imported so it's functions can be used.
import math

#see numpy cheat sheet https://www.dataquest.io/blog/images/cheat-sheets/numpy-cheat-sheet.pdf
#The numpy import is needed because it is renamed here as np.
import numpy as np

# add imports for AguaClara code that will be needed
# physchem has functions related to hydraulics, fractal flocs, flocculation, sedimentation, etc.
from aide_design import physchem as pc

# pipedatabase has functions related to pipe diameters
from aide_design import pipedatabase as pipe

# units allows us to include units in all of our calculations
from aide_design.units import unit_registry as u

# utility has the significant digit display function
from aide_design import utility as ut
ratio_VC_orifice= 0.62

# The following constants need to go into the constants file
Pi_LFOM_safety = 1.2
# pipe schedule for LFOM
SDR_LFOM = 26

def width_stout(HL_LFOM,z):
    return 2/((2*u.g_0*z)**(1/2)*np.pi*HL_LFOM)

def n_lfom_rows(Q,HL_LFOM):
    N_estimated = (HL_LFOM*math.pi/(2*width_stout(HL_LFOM,HL_LFOM)*Q)).to(u.dimensionless)
    return min(10,max(4,math.trunc(N_estimated.magnitude)))

FLOW = 5*u.L/u.s
HL_LFOM = 20*u.cm


def dist_center_lfom_rows(FLOW,HL_LFOM):
    return HL_LFOM/n_lfom_rows(FLOW,HL_LFOM)



# average vertical velocity of the water inside the LFOM pipe 
# at the very bottom of the bottom row of orifices
# The speed of falling water is 0.841 m/s for all linear flow orifice meters of height 20cm, independent of total plant flow rate.
def vol_lfom_pipe_critical(HL_LFOM):
    return (4/(3*math.pi)*(2*u.g_0*HL_LFOM)**(1/2)).to(u.m/u.s)

def area_lfom_pipe_min(FLOW,HL_LFOM,Pi_LFOM_safety):
    return (Pi_LFOM_safety*FLOW/vol_lfom_pipe_critical(HL_LFOM)).to(u.m**2)

def nom_diam_lfom_pipe(FLOW,HL_LFOM,Pi_LFOM_safety,SDR_LFOM):
    ID=pc.diam_circle(area_lfom_pipe_min(FLOW,HL_LFOM,Pi_LFOM_safety))
    return pipe.ND_SDR_available(ID,SDR_LFOM)

# another possibility is to use integration to solve this problem.
# Here we use the width of the stout weir in the center of the top row
# to estimate the area of the top orifice
def area_lfom_orifices_max(FLOW,HL_LFOM):
    return FLOW*width_stout(HL_LFOM,HL_LFOM-0.5*dist_center_lfom_rows(FLOW,HL_LFOM))*dist_center_lfom_rows(FLOW,HL_LFOM)

def d_lfom_orifices_max(FLOW,HL_LFOM):
    return (pc.diam_circle(area_lfom_orifices_max(FLOW,HL_LFOM)))

from enum import Enum
class uomeasure(Enum):
    english = 0
    metric = 1

# define the constant. How do we make all of the constants available to designers?   
drill_series_uom=uomeasure

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



def lfom_drillbit_diameter(FLOW,HL_LFOM,drill_series_uom):
    return ut.ceil_nearest(d_lfom_orifices_max(FLOW,HL_LFOM),drill_series(drill_series_uom))

def lfom_drillbit_area(FLOW,HL_LFOM,drill_series_uom):
    return pc.area_circle(lfom_drillbit_diameter(FLOW,HL_LFOM,drill_series_uom))

##A bound on the number of orifices allowed in each row.  
##The distance between consecutive orifices must be enough to retain structural integrity of the pipe

def n_lfom_orifices_per_row_max(FLOW,HL_LFOM,drill_series_uom,SDR_LFOM):
    S_lfom_orifices_Min= 3*u.mm
    return math.floor(math.pi*(pipe.ID_SDR(nom_diam_lfom_pipe(FLOW,HL_LFOM,Pi_LFOM_safety,SDR_LFOM),SDR_LFOM))/(lfom_drillbit_diameter(FLOW,HL_LFOM,drill_series_uom)+S_lfom_orifices_Min))

#locations where we will try to get the target flows is in between orifices at elevation Pi.H
def flow_ramp(FLOW,HL_LFOM):
    return((np.arange((dist_center_lfom_rows(FLOW,HL_LFOM)/u.cm),(HL_LFOM/u.cm),(dist_center_lfom_rows(FLOW,HL_LFOM)/u.cm))*FLOW)*u.cm)/HL_LFOM

def height_lfom_orifices(FLOW,HL_LFOM,drill_series_uom):
    return np.arange(lfom_drillbit_diameter(FLOW,HL_LFOM,drill_series_uom.metric)*0.5,HL_LFOM,dist_center_lfom_rows(FLOW,HL_LFOM),dtype= object)


#Calculate the flow for a given number of submerged rows of orifices
def flow_lfom_actual(FLOW,HL_LFOM,drill_series_uom,Row_Index_Submerged,N_LFOM_Orifices):
    D_LFOM_Orifices=lfom_drillbit_diameter(FLOW,HL_LFOM,drill_series_uom).to(u.m)
    FLOW_new=[]
    for i in range(Row_Index_Submerged):
        h = np.arange(dist_center_lfom_rows(FLOW,HL_LFOM),HL_LFOM,dist_center_lfom_rows(FLOW,HL_LFOM),dtype=object)
        h = h[Row_Index_Submerged].to(u.m)
        d = np.arange(0.5* D_LFOM_Orifices,HL_LFOM,dist_center_lfom_rows(FLOW,HL_LFOM),dtype=object)
        FLOW_new.append(N_LFOM_Orifices[i]*(pc.flow_orifice_vert(D_LFOM_Orifices,h-d[i],ratio_VC_orifice)))
    return sum(FLOW_new)

#Calculate number of orifices at each level given a diameter
def n_lfom_orifices(FLOW,HL_LFOM,drill_series_uom,SDR_LFOM):
    FLOW_ramp_local=flow_ramp(FLOW,HL_LFOM)
    D_LFOM_Orifices=lfom_drillbit_diameter(FLOW,HL_LFOM,drill_series_uom)
    H_ramp_local=np.arange(D_LFOM_Orifices*0.5,HL_LFOM,dist_center_lfom_rows(FLOW,HL_LFOM),dtype=object)
    n=[]
    for i in range (len(H_ramp_local)-1):
        h=np.arange(dist_center_lfom_rows(FLOW,HL_LFOM),HL_LFOM,dist_center_lfom_rows(FLOW,HL_LFOM),dtype=object)
        d=H_ramp_local
        n.append(min(max(0,round((FLOW_ramp_local[i]-flow_lfom_actual(FLOW,HL_LFOM,drill_series_uom,i,n))/pc.flow_orifice_vert(D_LFOM_Orifices,h[i]-d[i],ratio_VC_orifice))),n_lfom_orifices_per_row_max(FLOW,HL_LFOM,drill_series_uom,SDR_LFOM)))
    return n


#This function calculates the error of the design based on the differences between the predicted flow rate
#and the actual flow rate through the LFOM.
def flow_lfom_error(FLOW,HL_LFOM,drill_series_uom,SDR_LFOM):
    N_lfom_orifices=n_lfom_orifices(FLOW,HL_LFOM,drill_series_uom,SDR_LFOM)
    FLOW_lfom_error=[]
    for j in range (len(N_lfom_orifices)-1):
        FLOW_lfom_error.append((flow_lfom_actual(FLOW,HL_LFOM,drill_series_uom,j,N_lfom_orifices)-flow_ramp(FLOW,HL_LFOM)[j])/FLOW)
    return FLOW_lfom_error


#This funciton returns the maximum error, the absolute value of the errors is take into account positive 
#and negative errors
x= max(flow_lfom_error(FLOW,HL_LFOM,drill_series_uom,SDR_LFOM))
y=x**2
FLOW_LFOM_ERROR_MAX=y**1/2


def flow_lfom_ideal(FLOW,HL_LFOM,H):
    flow_lfom_ideal=(FLOW*H)/HL_LFOM
    return flow_lfom_ideal


def flow_lfom(FLOW,HL_LFOM,drill_series_uom,SDR_LFOM,H):
    D_lfom_orifices=lfom_drillbit_diameter(FLOW,HL_LFOM,drill_series_uom)
    H_submerged=np.arange(H-0.5*D_lfom_orifices,HL_LFOM,H-dist_center_lfom_rows(FLOW,HL_LFOM),dtype=object)
    N_lfom_orifices=n_lfom_orifices(FLOW,HL_LFOM,drill_series_uom,SDR_LFOM)
    flow=[]
    for i in range (len(H_submerged)):
        flow.append(pc.flow_orifice_vert(D_lfom_orifices,H_submerged[i],ratio_VC_orifice)*N_lfom_orifices[i])
    return sum (flow)


if FLOW==1.6*(u.L/u.s):
   NOM_DIAM_RAPID_MIX_pipe=2*u.inch
else:
   NOM_DIAM_RAPID_MIX_pipe=nom_diam_lfom_pipe(11*u.L/u.s,HL_LFOM,Pi_LFOM_safety,SDR_LFOM)
   
HEIGHT_LFOM_ORIFICES=height_lfom_orifices(FLOW,HL_LFOM,drill_series_uom)
   
N_LFOM_ORIFICES=n_lfom_orifices(FLOW,HL_LFOM,drill_series_uom,SDR_LFOM)
   
N_LFOM_ROWS=len(N_LFOM_ORIFICES)
   