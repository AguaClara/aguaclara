# -*- coding: utf-8 -*-
"""
Edited on September 1, 2017
@author: Monroe Weber-Shirk

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

# import export inputs and define the VC coefficient
from aide_design import expert_inputs as exp
ratio_VC_orifice= exp.RATIO_VC_ORIFICE

# The following constants need to go into the constants file
Pi_LFOM_safety = 1.2
# pipe schedule for LFOM
#SDR_LFOM = 26
#FLOW = 10*u.L/u.s
#HL_LFOM = 20*u.cm

#primary outputs from this file are
#Nominal diameter nom_diam_lfom_pipe(FLOW,HL_LFOM,Pi_LFOM_safety,SDR_LFOM)
#number of rows n_lfom_rows(FLOW,HL_LFOM)
#orifice diameter orifice_diameter(FLOW,HL_LFOM,drill_series_uom)
#number of orifices in each row n_lfom_orifices(FLOW,HL_LFOM,drill_series_uom,SDR_LFOM)
#height of the center of each row height_lfom_orifices(FLOW,HL_LFOM,drill_series_uom)

# output is width per flow rate.
@u.wraps(u.s/(u.m**2), [u.m,u.m], False)
def width_stout(HL_LFOM,z):
    return (2/((2*pc.gravity*z)**(1/2)*ratio_VC_orifice*np.pi*HL_LFOM)).magnitude


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
    
    But it might be better to always set then number of rows to 10.
    The challenge is to figure out a reasonable system of constraints that
    reliably returns a valid solution.
    """
    N_estimated = (HL_LFOM*np.pi/(2*width_stout(HL_LFOM,HL_LFOM)*FLOW))
    #variablerow=min(10,max(4,math.trunc(N_estimated.magnitude)))
    return 10


def dist_center_lfom_rows(FLOW,HL_LFOM):
    return HL_LFOM/n_lfom_rows(FLOW,HL_LFOM)


def vel_lfom_pipe_critical(HL_LFOM):
    """The average vertical velocity of the water inside the LFOM pipe 
    at the very bottom of the bottom row of orifices
    The speed of falling water is 0.841 m/s for all linear flow orifice meters
    of height 20 cm, independent of total plant flow rate."""
    return (4/(3*math.pi)*(2*u.g_0*HL_LFOM)**(1/2)).to(u.m/u.s)

def area_lfom_pipe_min(FLOW,HL_LFOM,Pi_LFOM_safety):
    return (Pi_LFOM_safety*FLOW/vel_lfom_pipe_critical(HL_LFOM)).to(u.m**2)

def nom_diam_lfom_pipe(FLOW,HL_LFOM,Pi_LFOM_safety,SDR_LFOM):
    ID=pc.diam_circle(area_lfom_pipe_min(FLOW,HL_LFOM,Pi_LFOM_safety))
    return pipe.ND_SDR_available(ID,SDR_LFOM)

def area_lfom_orifices_max(FLOW,HL_LFOM):
    """Estimate the orifice area corresponding to the top row of orifices.
    Another solution method is to use integration to solve this problem.
    Here we use the width of the stout weir in the center of the top row
    to estimate the area of the top orifice
    """
    return ((FLOW*width_stout(HL_LFOM,HL_LFOM-0.5*dist_center_lfom_rows(FLOW,HL_LFOM))*dist_center_lfom_rows(FLOW,HL_LFOM))).to(u.m**2)

def d_lfom_orifices_max(FLOW,HL_LFOM):
    return (pc.diam_circle(area_lfom_orifices_max(FLOW,HL_LFOM)))

def orifice_diameter(FLOW,HL_LFOM,drill_bits):
    maxdrill = (min((dist_center_lfom_rows(FLOW,HL_LFOM)).to(u.m).magnitude,(d_lfom_orifices_max(FLOW,HL_LFOM)).to(u.m).magnitude))*u.m
    return ut.floor_nearest(maxdrill,drill_bits)


def drillbit_area(FLOW,HL_LFOM,drill_bits):
    return pc.area_circle(orifice_diameter(FLOW,HL_LFOM,drill_bits))



def n_lfom_orifices_per_row_max(FLOW,HL_LFOM,drill_bits,SDR_LFOM):
    """A bound on the number of orifices allowed in each row.  
    The distance between consecutive orifices must be enough to retain 
    structural integrity of the pipe.
    """
    S_lfom_orifices_Min= 3*u.mm
    return math.floor(math.pi*(pipe.ID_SDR(nom_diam_lfom_pipe(FLOW,HL_LFOM,Pi_LFOM_safety,SDR_LFOM),SDR_LFOM))/(orifice_diameter(FLOW,HL_LFOM,drill_bits)+S_lfom_orifices_Min))

def flow_ramp(FLOW,HL_LFOM):
    n_rows = n_lfom_rows(FLOW,HL_LFOM)
    return np.linspace(FLOW.magnitude/n_rows,FLOW.magnitude,n_rows)*FLOW.units
            
def height_lfom_orifices(FLOW,HL_LFOM,drill_bits):
    """Calculates the height of the center of each row of orifices.
    The bottom of the bottom row orifices is at the zero elevation
    point of the LFOM so that the flow goes to zero when the water height
    is at zero.
    """
    
    return (np.arange(((orifice_diameter(FLOW,HL_LFOM,drill_bits)*0.5).to(u.m)).magnitude,
                      (HL_LFOM.to(u.m)).magnitude,
                      ((dist_center_lfom_rows(FLOW,HL_LFOM)).to(u.m)).magnitude))*u.m

#print(height_lfom_orifices(10*u.L/u.s,20*u.cm,[0.75]*u.inch))

def flow_lfom_actual(FLOW,HL_LFOM,drill_bits,Row_Index_Submerged,N_LFOM_Orifices):
    """Calculates the flow for a given number of submerged rows of orifices
    """
    D_LFOM_Orifices=orifice_diameter(FLOW,HL_LFOM,drill_bits)
    row_height=dist_center_lfom_rows(FLOW,HL_LFOM)
    #harray is the distance from the water level to the center of the orifices when the water is at the max level 
    harray = (np.linspace(row_height.to(u.mm).magnitude,HL_LFOM.to(u.mm).magnitude,n_lfom_rows(FLOW,HL_LFOM)))*u.mm -0.5* D_LFOM_Orifices 
    FLOW_new=0*u.m**3/u.s
    for i in range(Row_Index_Submerged+1):   
        FLOW_new = FLOW_new + (N_LFOM_Orifices[i]*(pc.flow_orifice_vert(D_LFOM_Orifices,harray[Row_Index_Submerged-i],ratio_VC_orifice)))
    return FLOW_new


#Calculate number of orifices at each level given a diameter
def n_lfom_orifices(FLOW,HL_LFOM,drill_bits,SDR_LFOM):
    FLOW_ramp_local = flow_ramp(FLOW,HL_LFOM)
    n_orifices_max =n_lfom_orifices_per_row_max(FLOW,HL_LFOM,drill_bits,SDR_LFOM)
    n_rows = (n_lfom_rows(FLOW,HL_LFOM))
    D_LFOM_Orifices = orifice_diameter(FLOW,HL_LFOM,drill_bits)
    # H is distance from the elevation between two rows of orifices down to the center of the orifices
    H=dist_center_lfom_rows(FLOW,HL_LFOM)-D_LFOM_Orifices*0.5
    n=[]                       
    for i in range(n_rows):
        #place zero in the row that we are going to calculate the required number of orifices
        n=np.append(n,0)
        #calculate the ideal number of orifices at the current row without constraining to an integer
        n_orifices_real=((FLOW_ramp_local[i]-flow_lfom_actual(FLOW,HL_LFOM,drill_bits,i,n))/
                                  pc.flow_orifice_vert(D_LFOM_Orifices,H,ratio_VC_orifice)).to(u.dimensionless).magnitude
        #constrain number of orifices to be less than the max per row and greater or equal to 0                 
        n[i]=min((max(0,round(n_orifices_real))),n_orifices_max)
    return n
                     

#This function calculates the error of the design based on the differences between the predicted flow rate
#and the actual flow rate through the LFOM.
def flow_lfom_error(FLOW,HL_LFOM,drill_bits,SDR_LFOM):
    N_lfom_orifices=n_lfom_orifices(FLOW,HL_LFOM,drill_bits,SDR_LFOM)
    FLOW_lfom_error=[]
    for j in range (len(N_lfom_orifices)-1):
        FLOW_lfom_error.append((flow_lfom_actual(FLOW,HL_LFOM,drill_bits,j,N_lfom_orifices)-flow_ramp(FLOW,HL_LFOM)[j])/FLOW)
    return FLOW_lfom_error



def flow_lfom_ideal(FLOW,HL_LFOM,H):
    flow_lfom_ideal=(FLOW*H)/HL_LFOM
    return flow_lfom_ideal


def flow_lfom(FLOW,HL_LFOM,drill_bits,SDR_LFOM,H):
    D_lfom_orifices=orifice_diameter(FLOW,HL_LFOM,drill_bits)
    H_submerged=np.arange(H-0.5*D_lfom_orifices,HL_LFOM,H-dist_center_lfom_rows(FLOW,HL_LFOM),dtype=object)
    N_lfom_orifices=n_lfom_orifices(FLOW,HL_LFOM,drill_bits,SDR_LFOM)
    flow=[]
    for i in range (len(H_submerged)):
        flow.append(pc.flow_orifice_vert(D_lfom_orifices,H_submerged[i],ratio_VC_orifice)*N_lfom_orifices[i])
    return sum (flow)


