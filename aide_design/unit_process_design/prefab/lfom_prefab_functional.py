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
FLOW = 10*u.L/u.s
HL_LFOM = 20*u.cm

# output is width per flow rate.
@u.wraps(u.s/(u.m**2), [u.m,u.m], False)
def width_stout(HL_LFOM,z):
    return (2/((2*pc.gravity*z)**(1/2)*ratio_VC_orifice*np.pi*HL_LFOM)).magnitude

#x = (HL_LFOM*np.pi/(2*width_stout(HL_LFOM,HL_LFOM)*FLOW)).to(u.m**3/u.m**3)
#print(x)



@u.wraps(None, [u.m**3/u.s,u.m], False)
def n_lfom_rows(FLOW,HL_LFOM):
    """This equation states that the open area corresponding to one row can be
    set equal to two orifices of diameter=row height. If there are more than 
    two orifices per row at the top of the LFOM then there are more orifices 
    than are convenient to drill and more than necessary for good accuracy. 
    Thus this relationship can be used to increase the spacing between the 
    rows and thus increase the diameter of the orifices. This spacing function 
    also sets the lower depth on the high flow rate LFOM with no accurate 
    flows below a depth equal to the first row height.
    """
    N_estimated = (HL_LFOM*np.pi/(2*width_stout(HL_LFOM,HL_LFOM)*FLOW))
    return min(10,max(4,math.trunc(N_estimated.magnitude)))



#x = n_lfom_rows(FLOW,HL_LFOM)
#print(x)


def dist_center_lfom_rows(FLOW,HL_LFOM):
    return HL_LFOM/n_lfom_rows(FLOW,HL_LFOM)



# average vertical velocity of the water inside the LFOM pipe 
# at the very bottom of the bottom row of orifices
# The speed of falling water is 0.841 m/s for all linear flow orifice meters of height 20cm, independent of total plant flow rate.
def vel_lfom_pipe_critical(HL_LFOM):
    return (4/(3*math.pi)*(2*u.g_0*HL_LFOM)**(1/2)).to(u.m/u.s)

def area_lfom_pipe_min(FLOW,HL_LFOM,Pi_LFOM_safety):
    return (Pi_LFOM_safety*FLOW/vel_lfom_pipe_critical(HL_LFOM)).to(u.m**2)

def nom_diam_lfom_pipe(FLOW,HL_LFOM,Pi_LFOM_safety,SDR_LFOM):
    ID=pc.diam_circle(area_lfom_pipe_min(FLOW,HL_LFOM,Pi_LFOM_safety))
    return pipe.ND_SDR_available(ID,SDR_LFOM)

# another possibility is to use integration to solve this problem.
# Here we use the width of the stout weir in the center of the top row
# to estimate the area of the top orifice
#@u.wraps(u.m, [(u.m**3)/u.s,u.m], False)
def area_lfom_orifices_max(FLOW,HL_LFOM):
    return ((FLOW*width_stout(HL_LFOM,HL_LFOM-0.5*dist_center_lfom_rows(FLOW,HL_LFOM))*dist_center_lfom_rows(FLOW,HL_LFOM))).to(u.m**2)


print(FLOW)
print(HL_LFOM)
print(width_stout(HL_LFOM,HL_LFOM-0.5*dist_center_lfom_rows(FLOW,HL_LFOM)))
print(dist_center_lfom_rows(FLOW,HL_LFOM))
print(((FLOW*width_stout(HL_LFOM,HL_LFOM-0.5*dist_center_lfom_rows(FLOW,HL_LFOM))*dist_center_lfom_rows(FLOW,HL_LFOM))))
print(area_lfom_orifices_max(FLOW,HL_LFOM))
print('what')




def d_lfom_orifices_max(FLOW,HL_LFOM):
    return (pc.diam_circle(area_lfom_orifices_max(FLOW,HL_LFOM)))

print(d_lfom_orifices_max(FLOW,HL_LFOM).to(u.inch))

from enum import Enum
class uomeasure(Enum):
    english = 0
    metric = 1

# define the constant. How do we make all of the constants available to designers?   
drill_series_uom=uomeasure

def drill_series(uomeasure):
    if uomeasure is uomeasure.english:
        ds=np.arange(1/32, 1/4, 1/32)
        ds=np.append(ds,np.arange(1/4, 1, 1/8))
        ds=np.append(ds,np.arange(1, 3.25, 1/4))
        ds=ds*u.inch
    else:
        ds=np.arange(0.5, 5, 0.1)
        ds=np.append(ds,np.arange(5, 19, 1))
        ds=np.append(ds,np.arange(20, 50, 2))
        ds=ds*u.mm
    return ds

print(drill_series(uomeasure.english))
maxdrill = (min((dist_center_lfom_rows(FLOW,HL_LFOM)).to(u.m).magnitude,(d_lfom_orifices_max(FLOW,HL_LFOM)).to(u.m).magnitude))*u.m
print('maxdrill')
print(maxdrill.to(u.inch))

def lfom_drillbit_diameter(FLOW,HL_LFOM,drill_series_uom):
    maxdrill = (min((dist_center_lfom_rows(FLOW,HL_LFOM)).to(u.m).magnitude,(d_lfom_orifices_max(FLOW,HL_LFOM)).to(u.m).magnitude))*u.m
    return ut.floor_nearest(maxdrill,drill_series(drill_series_uom))

#x=d_lfom_orifices_max(FLOW,HL_LFOM)
print('drillbit')
print((lfom_drillbit_diameter(FLOW,HL_LFOM,uomeasure.english)).to(u.inch))
#x=drill_series(uomeasure.metric).to(u.m).magnitude


def lfom_drillbit_area(FLOW,HL_LFOM,drill_series_uom):
    return pc.area_circle(lfom_drillbit_diameter(FLOW,HL_LFOM,drill_series_uom))
x=lfom_drillbit_area(FLOW,HL_LFOM,uomeasure)
print(x)
##A bound on the number of orifices allowed in each row.  
##The distance between consecutive orifices must be enough to retain structural integrity of the pipe

def n_lfom_orifices_per_row_max(FLOW,HL_LFOM,drill_series_uom,SDR_LFOM):
    S_lfom_orifices_Min= 3*u.mm
    return math.floor(math.pi*(pipe.ID_SDR(nom_diam_lfom_pipe(FLOW,HL_LFOM,Pi_LFOM_safety,SDR_LFOM),SDR_LFOM))/(lfom_drillbit_diameter(FLOW,HL_LFOM,drill_series_uom)+S_lfom_orifices_Min))

#locations where we will try to get the target flows is in between orifices at elevation Pi.H
def flow_ramp(FLOW,HL_LFOM):
    n_rows = n_lfom_rows(FLOW,HL_LFOM)
    return np.linspace(FLOW.magnitude/n_rows,FLOW.magnitude,n_rows)*FLOW.units
            
def height_lfom_orifices(FLOW,HL_LFOM,drill_series_uom):
    return np.arange(lfom_drillbit_diameter(FLOW,HL_LFOM,drill_series_uom.metric)*0.5,HL_LFOM,dist_center_lfom_rows(FLOW,HL_LFOM),dtype= object)


#Calculate the flow for a given number of submerged rows of orifices
#@u.wraps((u.m**3)/u.s, [(u.m**3)/u.s,u.m, u.dimensionless, u.dimensionless, u.dimensionless], False)
def flow_lfom_actual(FLOW,HL_LFOM,drill_series_uom,Row_Index_Submerged,N_LFOM_Orifices):
    D_LFOM_Orifices=lfom_drillbit_diameter(FLOW,HL_LFOM,drill_series_uom)
    print('D_LFOM_Orifices is ')
    row_height=dist_center_lfom_rows(FLOW,HL_LFOM)
    print(D_LFOM_Orifices)
    #harray is the distance from the water level to the center of the orifices when the water is at the max level 
    harray = (np.linspace(row_height.to(u.mm),HL_LFOM.to(u.mm),n_lfom_rows(FLOW,HL_LFOM)))*u.mm -0.5* D_LFOM_Orifices
    print('first h is ')
    print(harray)
    # d = np.arange(0.5* D_LFOM_Orifices,HL_LFOM,dist_center_lfom_rows(FLOW,HL_LFOM),dtype=object)
    #d = h-0.5* D_LFOM_Orifices
    #print('d is ')
    #print(d)
    FLOW_new=0*u.m**3/u.s
    for i in range(Row_Index_Submerged+1):   
        FLOW_new = FLOW_new + (N_LFOM_Orifices[i]*(pc.flow_orifice_vert(D_LFOM_Orifices,harray[Row_Index_Submerged-i],ratio_VC_orifice)))
        print(FLOW_new.to(u.L/u.s),harray[i],i)
    return FLOW_new

x = flow_lfom_actual(FLOW,HL_LFOM,uomeasure.english,6,[13,3,4,3,3,2,2,3,1,3])
#x = lfom_drillbit_diameter(FLOW,HL_LFOM,uomeasure)
#print(x.to(u.L/u.s))
print(flow_ramp(FLOW,HL_LFOM))

#Calculate number of orifices at each level given a diameter
def n_lfom_orifices(FLOW,HL_LFOM,drill_series_uom,SDR_LFOM):
    FLOW_ramp_local = flow_ramp(FLOW,HL_LFOM)
    print('here is the flow ramp')
    print(FLOW_ramp_local)
    D_LFOM_Orifices = lfom_drillbit_diameter(FLOW,HL_LFOM,drill_series_uom)
    # H is distance from the elevation between two rows of orifices down to the center of the orifices
    H=dist_center_lfom_rows(FLOW,HL_LFOM)-D_LFOM_Orifices*0.5
    n=[]
    for i in range (n_lfom_rows(FLOW,HL_LFOM)):
        n.append((min(max(0,round((FLOW_ramp_local[i]-flow_lfom_actual(FLOW,HL_LFOM,drill_series_uom,i,n))/
                                  pc.flow_orifice_vert(D_LFOM_Orifices,H,ratio_VC_orifice))),
                      n_lfom_orifices_per_row_max(FLOW,HL_LFOM,drill_series_uom,SDR_LFOM))))
        print('current n is')
        print(n)
        # n.append((min(max(0,round((FLOW_ramp_local[i]-flow_lfom_actual(FLOW,HL_LFOM,drill_series_uom,i,n))/pc.flow_orifice_vert(D_LFOM_Orifices,H,ratio_VC_orifice))),n_lfom_orifices_per_row_max(FLOW,HL_LFOM,drill_series_uom,SDR_LFOM))))
    return n

x=n_lfom_orifices(FLOW,HL_LFOM,uomeasure.english,SDR_LFOM)

print(x)

#D_LFOM_Orifices = lfom_drillbit_diameter(FLOW,HL_LFOM,drill_series_uom)
#H=dist_center_lfom_rows(FLOW,HL_LFOM)-D_LFOM_Orifices*0.5
#print(H)                       

#This function calculates the error of the design based on the differences between the predicted flow rate
#and the actual flow rate through the LFOM.
def flow_lfom_error(FLOW,HL_LFOM,drill_series_uom,SDR_LFOM):
    N_lfom_orifices=n_lfom_orifices(FLOW,HL_LFOM,drill_series_uom,SDR_LFOM)
    FLOW_lfom_error=[]
    for j in range (len(N_lfom_orifices)-1):
        FLOW_lfom_error.append((flow_lfom_actual(FLOW,HL_LFOM,drill_series_uom,j,N_lfom_orifices)-flow_ramp(FLOW,HL_LFOM)[j])/FLOW)
    return FLOW_lfom_error



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
   
#HEIGHT_LFOM_ORIFICES=height_lfom_orifices(FLOW,HL_LFOM,drill_series_uom)
   
#N_LFOM_ORIFICES=n_lfom_orifices(FLOW,HL_LFOM,drill_series_uom,SDR_LFOM)
   
#N_LFOM_ROWS=len(N_LFOM_ORIFICES)
   