
"""This file contains all the functions needed to design the linear flow
orifice meter (LFOM) for an AguaClara plant.

"""

#Here we import packages that we will need for this notebook. You can find out about these packages in the Help menu.
import aguaclara.design.lfom as lfom
from aguaclara.play import*

#primary outputs from this file are
#TODO: con.RATIO_LFOM_SAFETY has been moved
#Nominal diameter nom_diam_lfom_pipe(FLOW,HL_LFOM,con.RATIO_LFOM_SAFETY)
#number of rows n_rows(FLOW,HL_LFOM)
#orifice diameter orifice_diameter(FLOW,HL_LFOM,drill_series_uom)
#number of orifices in each row n_lfom_orifices(FLOW,HL_LFOM,drill_series_uom)
#height of the center of each row height_lfom_orifices(FLOW,HL_LFOM,drill_series_uom)

# output is width per flow rate.
@u.wraps(u.s/(u.m**2), [u.m,u.m], False)
def width_stout(HL_LFOM,z):
    return (2 / ((2*pc.gravity*z) ** (1/2) * con.VC_ORIFICE_RATIO * np.pi * HL_LFOM)).magnitude


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
    variablerow = min(10,max(4,math.trunc(N_estimated.magnitude)))
    # Forcing the LFOM to either have 4 or 8 rows, for design purposes
    # If the hydraulic calculation finds that there should be 4 rows, then there
    # will be 4 rows. If anything other besides 4 rows is found, then assign 8
    # rows.
    # This can be improved in the future.
    if variablerow == 4:
        variablerow = 4
    else:
        variablerow = 8
    return variablerow

@u.wraps(u.m, [u.m**3/u.s, u.m], False)
def dist_center_lfom_rows(FLOW,HL_LFOM):
    return HL_LFOM/n_lfom_rows(FLOW,HL_LFOM)

@u.wraps(u.m/u.s, [u.m], False)
def vel_lfom_pipe_critical(HL_LFOM):
    """The average vertical velocity of the water inside the LFOM pipe
    at the very bottom of the bottom row of orifices
    The speed of falling water is 0.841 m/s for all linear flow orifice meters
    of height 20 cm, independent of total plant flow rate."""
    return 4/(3*math.pi)*(2*pc.gravity.magnitude*HL_LFOM)**(1/2)

@u.wraps(u.m**2, [u.m**3/u.s, u.m], False)
def area_lfom_pipe_min(FLOW, HL_LFOM):
    return (
            aguaclara.design.lfom.SAFETY_RATIO * FLOW / vel_lfom_pipe_critical(HL_LFOM).magnitude)

@u.wraps(u.inch, [u.m**3/u.s, u.m], False)
def nom_diam_lfom_pipe(FLOW,HL_LFOM):
    ID = pc.diam_circle(area_lfom_pipe_min(FLOW, HL_LFOM))
    return pipe.ND_SDR_available(ID, design.lfom.SDR_LFOM).magnitude

@u.wraps(u.m**2, [u.m**3/u.s, u.m], False)
def area_lfom_orifices_top(FLOW,HL_LFOM):
    """Estimate the orifice area corresponding to the top row of orifices.
    Another solution method is to use integration to solve this problem.
    Here we use the width of the stout weir in the center of the top row
    to estimate the area of the top orifice
    """
    return ((FLOW*width_stout(HL_LFOM*u.m,HL_LFOM*u.m-0.5*dist_center_lfom_rows(FLOW,HL_LFOM)).magnitude *
        dist_center_lfom_rows(FLOW,HL_LFOM).magnitude))

@u.wraps(u.m, [u.m**3/u.s, u.m], False)
def d_lfom_orifices_max(FLOW, HL_LFOM):
    return (pc.diam_circle(area_lfom_orifices_top(FLOW,HL_LFOM).magnitude).magnitude)

@u.wraps(u.m, [u.m**3/u.s, u.m, u.inch], False)
def orifice_diameter(FLOW,HL_LFOM,drill_bits):
    maxdrill = (min((dist_center_lfom_rows(FLOW,HL_LFOM).magnitude),(d_lfom_orifices_max(FLOW,HL_LFOM).magnitude)))
    return ut.floor_nearest(maxdrill,drill_bits)

@u.wraps(u.m**2, [u.m**3/u.s, u.m, u.inch], False)
def drillbit_area(FLOW,HL_LFOM,drill_bits):
    return pc.area_circle(orifice_diameter(FLOW,HL_LFOM,drill_bits)).magnitude

@u.wraps(None, [u.m**3/u.s, u.m, u.inch], False)
def n_lfom_orifices_per_row_max(FLOW,HL_LFOM,drill_bits):
    """A bound on the number of orifices allowed in each row.
    The distance between consecutive orifices must be enough to retain
    structural integrity of the pipe.
    """
    return math.floor(math.pi * (pipe.ID_SDR(
        nom_diam_lfom_pipe(FLOW, HL_LFOM), design.lfom.SDR_LFOM).magnitude)
                      / (orifice_diameter(FLOW, HL_LFOM, drill_bits).magnitude +
                         aguaclara.design.lfom.ORIFICE_S.magnitude))

@u.wraps(u.m**3/u.s, [u.m**3/u.s, u.m], False)
def flow_ramp(FLOW,HL_LFOM):
    n_rows = n_lfom_rows(FLOW,HL_LFOM)
    return np.linspace(FLOW/n_rows,FLOW,n_rows)

@u.wraps(u.m, [u.m**3/u.s, u.m, u.inch], False)
def height_lfom_orifices(FLOW,HL_LFOM,drill_bits):
    """Calculates the height of the center of each row of orifices.
    The bottom of the bottom row orifices is at the zero elevation
    point of the LFOM so that the flow goes to zero when the water height
    is at zero.
    """
    return (np.arange((orifice_diameter(FLOW,HL_LFOM,drill_bits)*0.5),
                      HL_LFOM,
                      (dist_center_lfom_rows(FLOW,HL_LFOM))))

@u.wraps(u.m**3/u.s, [u.m**3/u.s, u.m, u.inch, None, None], False)
def flow_lfom_actual(FLOW,HL_LFOM,drill_bits,Row_Index_Submerged,N_LFOM_Orifices):
    """Calculates the flow for a given number of submerged rows of orifices
    harray is the distance from the water level to the center of the orifices
    when the water is at the max level
    """
    D_LFOM_Orifices=orifice_diameter(FLOW, HL_LFOM, drill_bits).magnitude
    row_height=dist_center_lfom_rows(FLOW, HL_LFOM).magnitude
    harray = (np.linspace(row_height, HL_LFOM, n_lfom_rows(FLOW, HL_LFOM))) - 0.5 * D_LFOM_Orifices
    FLOW_new = 0
    for i in range(Row_Index_Submerged+1):
        FLOW_new = FLOW_new + (N_LFOM_Orifices[i] * (
            pc.flow_orifice_vert(D_LFOM_Orifices, harray[Row_Index_Submerged-i],
                                 con.VC_ORIFICE_RATIO).magnitude))
    return FLOW_new


#Calculate number of orifices at each level given a diameter
@u.wraps(None, [u.m**3/u.s, u.m, u.inch], False)
def n_lfom_orifices(FLOW,HL_LFOM,drill_bits):
    FLOW_ramp_local = flow_ramp(FLOW,HL_LFOM).magnitude
    n_orifices_max =n_lfom_orifices_per_row_max(FLOW,HL_LFOM,drill_bits)
    n_rows = (n_lfom_rows(FLOW,HL_LFOM))
    D_LFOM_Orifices = orifice_diameter(FLOW,HL_LFOM,drill_bits).magnitude
    # H is distance from the elevation between two rows of orifices down to the center of the orifices
    H=dist_center_lfom_rows(FLOW,HL_LFOM).magnitude-D_LFOM_Orifices*0.5
    n=[]
    for i in range(n_rows):
        #place zero in the row that we are going to calculate the required number of orifices
        n=np.append(n,0)
        #calculate the ideal number of orifices at the current row without constraining to an integer
        n_orifices_real=((FLOW_ramp_local[i]-flow_lfom_actual(FLOW,HL_LFOM,drill_bits,i,n).magnitude) /
                         pc.flow_orifice_vert(D_LFOM_Orifices, H, con.VC_ORIFICE_RATIO)).magnitude
        #constrain number of orifices to be less than the max per row and greater or equal to 0
        n[i]=min((max(0,round(n_orifices_real))),n_orifices_max)
    return n

#This function takes the output of n_lfom_orifices and converts it to a list with 8
#entries that corresponds to the 8 possible rows. This is necessary to make the lfom
# easier to construct in Fusion using patterns
@u.wraps(None, [u.m**3/u.s, u.m, u.inch, None], False)
def n_lfom_orifices_fusion(FLOW,HL_LFOM,drill_bits,num_rows):
    num_orifices_per_row = n_lfom_orifices(FLOW, HL_LFOM, drill_bits)
    num_orifices_final = np.zeros(8)
    centerline = np.zeros(8)
    center = True
    for i in range(8):
        if i % 2 == 1 and num_rows == 4:
            centerline[i] = int(center)
        elif num_rows == 4:
            num_orifices_final[i] = num_orifices_per_row[i/2]
            centerline[i] = int(center)
            center = not center
        else:
            num_orifices_final[i] = num_orifices_per_row[i]
            centerline[i] = int(center)
            center = not center

    return num_orifices_final, centerline



#This function calculates the error of the design based on the differences between the predicted flow rate
#and the actual flow rate through the LFOM.
@u.wraps(u.m**3/u.s, [u.m**3/u.s, u.m, u.inch], False)
def flow_lfom_error(FLOW,HL_LFOM,drill_bits):
    N_lfom_orifices=n_lfom_orifices(FLOW, HL_LFOM, drill_bits, design.lfom.SDR_LFOM)
    FLOW_lfom_error=[]
    for j in range (len(N_lfom_orifices)-1):
        FLOW_lfom_error.append((flow_lfom_actual(
            FLOW, HL_LFOM, drill_bits, j, N_lfom_orifices).magnitude-flow_ramp(
            FLOW, HL_LFOM)[j].magnitude)/FLOW)
    return FLOW_lfom_error


@u.wraps(u.m**3/u.s, [u.m**3/u.s, u.m, u.m], False)
def flow_lfom_ideal(FLOW, HL_LFOM, H):
    flow_lfom_ideal=(FLOW*H)/HL_LFOM
    return flow_lfom_ideal

@u.wraps(u.m**3/u.s, [u.m**3/u.s, u.m, u.inch, u.m], False)
def flow_lfom(FLOW,HL_LFOM,drill_bits,H):
    D_lfom_orifices=orifice_diameter(FLOW,HL_LFOM,drill_bits).magnitude
    H_submerged=np.arange(H-0.5*D_lfom_orifices, HL_LFOM, H-dist_center_lfom_rows(FLOW,HL_LFOM).magnitude,dtype=object)
    N_lfom_orifices=n_lfom_orifices(FLOW, HL_LFOM, drill_bits, design.lfom.SDR_LFOM)
    flow=[]
    for i in range(len(H_submerged)):
        flow.append(pc.flow_orifice_vert(D_lfom_orifices, H_submerged[i], con.VC_ORIFICE_RATIO) * N_lfom_orifices[i])
    return sum(flow)
