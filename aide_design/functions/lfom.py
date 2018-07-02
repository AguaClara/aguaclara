
"""This file contains all the functions needed to design the linear flow
orifice meter (LFOM) for an AguaClara plant.

"""

#Here we import packages that we will need for this notebook. You can find out about these packages in the Help menu.

from aide_design.play import*
import numpy as np
import math
from aide_design.shared.units import unit_registry as u
import aide_design.shared.utility as ut
import aide_design.shared.physchem as pc
import aide_design.shared.constants as con
import aide_design.shared.materials_database as mat
import aide_design.shared.pipedatabase as pipe

#primary outputs from this file are
#Nominal diameter nom_diam_lfom_pipe(q,hl,con.RATIO_LFOM_SAFETY)
#number of rows n_lfom_rows(q,hl)
#orifice diameter orifice_diameter(q,hl,drill_series_uom)
#number of orifices in each row n_lfom_orifices(q,hl,drill_series_uom)
#height of the center of each row height_lfom_orifices(q,hl,drill_series_uom)

# output is width per flow rate.
@u.wraps(u.s/(u.m**2), [u.m, u.m], False)
def width_stout(hl, depth):
    """This equation relates the LFOM to a stout weir. A stout weir controls
    flow through the width of a stout. The specific weir we reference is the
    sutro weir, which is designed to linearly relate flow to height of water.
    The LFOM mimics this linear relationship through a series of orifices.

    Parameters
    ----------
    hl : float
        Headloss through the LFOM

    depth : float
        Depth of water

    Returns
    -------
    width_stout: float
        equivalent width of stout in width per flow rate

    Examples
    --------
    >>> from aide_design.play import*
    >>> width_stout(40*u.cm, 40*u.cm)
    <Quantity(0.9019329453483474, 'second / meter ** 2')>
    >>> width_stout(20*u.cm, 1*u.cm)
    <Quantity(11.408649616179787, 'second / meter ** 2')>


    """
    return (2/((2*con.GRAVITY*depth)**(1/2) *
            con.RATIO_VC_ORIFICE*np.pi*hl)).magnitude


@u.wraps(None, [u.m**3/u.s, u.m], False)
def n_lfom_rows(Q, hl):
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

    Parameters
    ----------
    Q: float
        flow through the LFOM

    hl : float
        Headloss through the LFOM

    Returns
    -------
    n_lfom_rows : int
        number of rows the LFOM should contain

    Examples
    --------
    >>> from aide_design.play import*
    >>> n_lfom_rows(20 *u.L/u.s, 20*u.cm)
    8
    >>> n_lfom_rows(60 *u.L/u.s, 20*u.cm)
    4
    """
    N_estimated = hl * np.pi/(2*width_stout(hl, hl) * Q)
    variablerow = min(10, max(4, math.trunc(N_estimated.magnitude)))
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
def dist_center_lfom_rows(Q, hl):
    """This function determines the center-to-center distance between rows in
    the LFOM

    Parameters
    ----------
    Q: float
        flow through the LFOM

    hl : float
        Headloss through the LFOM

    Returns
    -------
    float
        center-to-center distance between rows in the LFOM

    Examples
    --------
    >>> from aide_design.play import*
    >>> dist_center_lfom_rows(20*u.L/u.s, 20*u.cm)
    <Quantity(0.025, 'meter')>
    >>> dist_center_lfom_rows(60*u.L/u.s, 60*u.cm)
    <Quantity(0.075, 'meter')>
    """
    return hl/n_lfom_rows(Q, hl)


@u.wraps(u.m/u.s, [u.m], False)
def vel_lfom_pipe_critical(hl):
    """The average vertical velocity of the water inside the LFOM pipe
    at the very bottom of the bottom row of orifices.
    The speed of falling water is 0.841 m/s for all linear flow orifice meters
    of height 20 cm, independent of total plant flow rate.

    Parameters
    ----------
    hl: float
        headloss through the LFOM

    Returns
    -------
    float
        average velocity of the water inside the LFOM at the bottow row of
        orifices

    Examples
    --------
    >>> from aide_design.play import*
    >>> vel_lfom_pipe_critical(20*u.cm)
    <Quantity(0.8405802802312778, 'meter / second')>
    >>> vel_lfom_pipe_critical(60*u.cm)
    <Quantity(1.4559277532010582, 'meter / second')>
    """
    return 4/(3*math.pi)*(2*con.GRAVITY.magnitude*hl)**(1/2)


@u.wraps(u.m**2, [u.m**3/u.s, u.m], False)
def area_lfom_pipe_min(Q, hl):
    """This function calculates the minimum cross sectional area of the LFOM

    Parameters
    ----------
    Q: float
        flow through the LFOM

    hl: float
        headloss through the LFOM

    Returns
    -------
    float
        minimum cross sectional area of the LFOM

    Examples
    --------
    >>> from aide_design.play import*
    >>> area_lfom_pipe_min(20*u.L/u.s, 20*u.cm)
    <Quantity(0.035689630967485675, 'meter ** 2')>
    >>> area_lfom_pipe_min(60*u.L/u.s, 60*u.cm)
    <Quantity(0.061816254139068764, 'meter ** 2')>

    """
    return (con.RATIO_LFOM_SAFETY*Q/vel_lfom_pipe_critical(hl).magnitude)


@u.wraps(u.inch, [u.m**3/u.s, u.m], False)
def nom_diam_lfom_pipe(Q, hl):
    """Returns the nominal diameter of the LFOM pipe based on the required
    cross sectional area for the given flow rate and head loss.

    Parameters
    ----------
    Q: float
        flow through the LFOM

    hl: float
        headloss through the LFOM

    Returns
    -------
    float
        nominal diameter of the LFOM pipe

    Examples
    --------
    >>> from aide_design.play import*
    >>> nom_diam_lfom_pipe(20*u.L/u.s, 20*u.cm)
    <Quantity(10.0, 'inch')>
    >>> nom_diam_lfom_pipe(60*u.L/u.s, 60*u.cm)
    <Quantity(12.0, 'inch')>
    """
    ID = pc.diam_circle(area_lfom_pipe_min(Q, hl))
    return pipe.ND_SDR_available(ID, mat.SDR_LFOM).magnitude


@u.wraps(u.m**2, [u.m**3/u.s, u.m], False)
def area_lfom_orifices_top(Q, hl):
    """Estimate the orifice area corresponding to the top row of orifices.
    Another solution method is to use integration to solve this problem.
    Here we use the width of the stout weir in the center of the top row
    to estimate the area of the top orifice

    Parameters
    ----------
    Q: float
        flow through the LFOM

    hl: float
        headloss through the LFOM

    Returns
    -------
    float
        estimated total area of the top row of LFOM orifices

    Examples
    --------
    >>> from aide_design.play import*
    >>> area_lfom_orifices_top(20*u.L/u.s, 20*u.cm)
    <Quantity(0.0013173573853983045, 'meter ** 2')>
    >>> area_lfom_orifices_top(60*u.L/u.s, 60*u.cm)
    <Quantity(0.002281729923235958, 'meter ** 2')>
    """
    return ((Q*width_stout(hl*u.m, hl*u.m - 0.5 *
             dist_center_lfom_rows(Q, hl)).magnitude *
             dist_center_lfom_rows(Q, hl).magnitude))


@u.wraps(u.m, [u.m**3/u.s, u.m], False)
def d_lfom_orifices_max(Q, hl):
    """This function calculates the maximum diameter of LFOM orifices for the
    given flow rate and headloss

    Parameters
    ----------
    Q: float
        flow through the LFOM

    hl: float
        headloss through the LFOM

    Returns
    -------
    float
        maximum orifice diameter

    Examples
    --------
    >>> from aide_design.play import*
    >>> d_lfom_orifices_max(20*u.L/u.s, 20*u.cm)
    <Quantity(0.04095499380586013, 'meter')>
    """
    return (pc.diam_circle(area_lfom_orifices_top(Q, hl).magnitude).magnitude)


@u.wraps(u.m, [u.m**3/u.s, u.m], False)
def orifice_diameter(Q, hl, drill_bits=mat.DIAM_DRILL_ENG):
    """Calculates the actual diameter of LFOM orifices given the available
    drill bits and maximum LFOM orifices

    Parameters
    ----------
    Q: float
        flow through the LFOM

    hl : float
        headloss through the LFOM

    drill_bits: array of floats
        an array of potential drill bit sizes to create the orifices

    Returns
    -------
    float
        orifice diameter

    Examples
    --------
    >>> from aide_design.play import*
    >>> orifice_diameter(20*u.L/u.s, 20*u.cm)
    <Quantity(0.022224999999999998, 'meter')>

    """
    maxdrill = min(dist_center_lfom_rows(Q, hl).magnitude,
                   d_lfom_orifices_max(Q, hl).magnitude) * u('meter')

    # Make a new list, convert drill bit sizes to metric, then populate the list.
    drill_bits_metric = []
    for drill_bit in drill_bits:
        new_drill_bits.append(drill_bit.to(u.m).magnitude)
    
    # Temporarily make the list a Quantity so it can be compared by ut.floor_nearest().
    drill_bits_metric = new_drill_bits * u('meter')

    # .magnitude prevents it from returning '0.022222 meter' within the magnitude value.
    return ut.floor_nearest(maxdrill, new_drill_bits).magnitude


@u.wraps(u.m**2, [u.m**3/u.s, u.m], False)
def drillbit_area(Q, hl, drill_bits=mat.DIAM_DRILL_ENG):
    """Returns the area of each hole created by the drill bit given the
    headloss, flow, and available drill bit sizes

    Parameters
    ----------
    Q: float
        flow through the LFOM

    hl : float
        headloss through the LFOM

    drill_bits: array of floats
        an array of potential drill bit sizes to create the orifices

    Returns
    -------
    float
        area of the hole created by the selected drill bit

    Examples
    --------
    >>> from aide_design.play import*
    >>> drillbit_area(20*u.L/u.s, 20*u.cm, mat.DIAM_DRILL_ENG)
    <Quantity(0.00038794791368402165, 'meter ** 2')>

    """
    return pc.area_circle(orifice_diameter(Q, hl, drill_bits)).magnitude


@u.wraps(None, [u.m**3/u.s, u.m], False)
def n_lfom_orifices_per_row_max(Q, hl, drill_bits=mat.DIAM_DRILL_ENG,
                                S_orifice=1*u.cm):
    """A bound on the number of orifices allowed in each row.
    The distance between consecutive orifices must be enough to retain
    structural integrity of the pipe.

    Parameters
    ----------
    Q: float
        flow through the LFOM

    hl : float
        headloss through the LFOM

    drill_bits: array of floats
        an array of potential drill bit sizes to create the orifices

    S_orifice : float
        Edge to edge spacing between orifices

    Returns
    -------
    float
        maximum number of orifices per row

    Examples
    --------
    >>> from aide_design.play import*
    >>> n_lfom_orifices_per_row_max(20*u.L/u.s, 20*u.cm)
    30

    """
    return math.floor(math.pi*(pipe.ID_SDR(
        nom_diam_lfom_pipe(Q, hl), mat.SDR_LFOM).magnitude)
        / (orifice_diameter(Q, hl, drill_bits).magnitude +
            S_orifice.to(u.cm).magnitude))


@u.wraps(u.m**3/u.s, [u.m**3/u.s, u.m], False)
def flow_ramp(Q, hl):
    """?

    Parameters
    ----------
    Q: float
        flow through the LFOM

    hl : float
        headloss through the LFOM

    Returns
    -------
    float
        ?

    Examples
    --------
    >>> from aide_design.play import*
    >>> flow_ramp(20*u.L/u.s, 40*u.cm)
    <Quantity([0.0025 0.005  0.0075 0.01   0.0125 0.015  0.0175 0.02  ], 'meter ** 3 / second')>
    """
    n_rows = n_lfom_rows(Q, hl)
    return np.linspace(Q/n_rows, Q, n_rows)


@u.wraps(u.m, [u.m**3/u.s, u.m], False)
def height_lfom_orifices(Q, hl, drill_bits=mat.DIAM_DRILL_ENG):
    """Calculates the height of the center of each row of orifices.
    The bottom of the bottom row orifices is at the zero elevation
    point of the LFOM so that the flow goes to zero when the water height
    is at zero.

    Parameters
    ----------
    Q: float
        flow through the LFOM

    hl : float
        headloss through the LFOM

    drill_bits: array of floats
        an array of potential drill bit sizes to create the orifices

    Returns
    -------
    float
        height of each row from the base of the LFOM

    Examples
    --------
    >>> from aide_design.play import*
    >>> height_lfom_orifices(20*u.L/u.s, 20*u.cm, mat.DIAM_DRILL_ENG)
    <Quantity([0.0111125 0.0361125 0.0611125 0.0861125 0.1111125 0.1361125 0.1611125
     0.1861125], 'meter')>

    """
    return (np.arange((orifice_diameter(Q, hl, drill_bits).magnitude*0.5),
                      hl,
                      (dist_center_lfom_rows(Q, hl)).magnitude))


@u.wraps(u.m**3/u.s, [u.m**3/u.s, u.m, None, None], False)
def flow_lfom_actual(Q, hl, Row_Index_Submerged, N_lfom_orifices,
                     drill_bits=mat.DIAM_DRILL_ENG):
    """Calculates the flow for a given number of submerged rows of orifices
    harray is the distance from the water level to the center of the orifices
    when the water is at the max level

    Parameters
    ----------
    Q: float
        flow through the LFOM

    hl : float
        headloss through the LFOM

    Row_Index_Submerged : int
        index of the row in the n_lfom_orifices array up to which the orifices
        are submerged

    N_lfom_Orifices:
        list with each entry being the number of orifices in that row of the
        LFOM

    drill_bits: array of floats
        an array of potential drill bit sizes to create the orifices

    Returns
    -------
    float
        flow from the LFOM under the conditions where every row up to the given
        row is submerged

    Examples
    --------
    >>> from aide_design.play import*
    >>> flow_lfom_actual(20*u.L/u.s, 20*u.cm, 1, [1,1])
    <Quantity(0.00033756816936411334, 'meter ** 3 / second')>

    """
    D_lfom_orifices = orifice_diameter(Q, hl, drill_bits).magnitude
    row_height = dist_center_lfom_rows(Q, hl).magnitude
    harray = (np.linspace(row_height, hl, n_lfom_rows(Q, hl))) - 0.5 * D_lfom_orifices
    Q_new = 0
    for i in range(Row_Index_Submerged+1):
        Q_new = Q_new + (N_lfom_orifices[i]*(
            pc.flow_orifice_vert(D_lfom_orifices,
                                 harray[Row_Index_Submerged-i],
                                 con.RATIO_VC_ORIFICE)))
    return Q_new.magnitude


#Calculate number of orifices at each level given a diameter
@u.wraps(None, [u.m**3/u.s, u.m], False)
def n_lfom_orifices(Q, hl, drill_bits=mat.DIAM_DRILL_ENG, S_orifice=1*u.cm):
    """This function calculates an array for each row of the LFOM with the
    number of orifices in that row

    Parameters
    ----------
    Q: float
        flow through the LFOM

    hl : float
        headloss through the LFOM

    drill_bits: array of floats
        an array of potential drill bit sizes to create the orifices

    S_orifice : float
        Edge to edge spacing between orifices

    Returns
    -------
    int array
        number of orifices in each row of the LFOM

    Examples
    --------
    >>> from aide_design.play import*
    >>> n_lfom_orifices(20*u.L/u.s, 20*u.cm, mat.DIAM_DRILL_ENG, 1*u.cm)
    array([20.,  6.,  6.,  5.,  4.,  5.,  3.,  3.])

    """
    q_ramp_local = flow_ramp(Q, hl).magnitude
    n_orifices_max = n_lfom_orifices_per_row_max(Q, hl, drill_bits, S_orifice)
    n_rows = (n_lfom_rows(Q, hl))
    D_LFOM_Orifices = orifice_diameter(Q, hl, drill_bits).magnitude
    # H is distance from the elevation between two rows of orifices
    # down to the center of the orifices
    H = dist_center_lfom_rows(Q, hl).magnitude-D_LFOM_Orifices*0.5
    n = []
    for i in range(n_rows):
        #place zero in the row that we are going to calculate the required number of orifices
        n = np.append(n, 0)
        #calculate the ideal number of orifices at the current row without constraining to an integer
        n_orifices_real=((q_ramp_local[i]-flow_lfom_actual(Q,hl,i,n,drill_bits).magnitude)/
                                  pc.flow_orifice_vert(D_LFOM_Orifices,H,con.RATIO_VC_ORIFICE)).magnitude
        #constrain number of orifices to be less than the max per row and greater or equal to 0
        n[i] = min((max(0, round(n_orifices_real))), n_orifices_max)
    return n

# This function takes the output of n_lfom_orifices and converts it to a list with 8
# entries that corresponds to the 8 possible rows. This is necessary to make the lfom
# easier to construct in Fusion using patterns
@u.wraps(None, [u.m**3/u.s, u.m, None], False)
def n_lfom_orifices_fusion(Q, hl, num_rows, drill_bits=mat.DIAM_DRILL_ENG,
                           S_orifice=1*u.cm):
    """This function takes the output of n_lfom_orifices and converts it to a list with 8
    entries that corresponds to the 8 possible rows. This is necessary to make the lfom
    easier to construct in Fusion using patterns

    Parameters
    ----------
    Q: float
        flow through the LFOM

    hl : float
        headloss through the LFOM

    num_rows : int
        number of rows of orifices in the LFOM

    drill_bits: array of floats
        an array of potential drill bit sizes to create the orifices

    S_orifice : float
        Edge to edge spacing between orifices

    Returns
    -------
    num_orifices_final : int array
        number of orifices in row of the LFOM

    centerline : int
        whether this row of orifices should be drawn using centerline 0 or 1

    Examples
    --------
    >>> from aide_design.play import*
    >>> n_lfom_orifices_fusion(20*u.L/u.s, 20*u.cm, 8, mat.DIAM_DRILL_ENG, 1*u.cm)
    (array([20.,  6.,  6.,  5.,  4.,  5.,  3.,  3.]), array([1., 0., 1., 0., 1., 0., 1., 0.]))

    """
    num_orifices_per_row = n_lfom_orifices(Q, hl, drill_bits, S_orifice)
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


@u.wraps(u.m**3/u.s, [u.m**3/u.s, u.m], False)
def flow_lfom_error(Q, hl, drill_bits, S_orifice):
    """This function calculates the error of the design based on the differences
    between the predicted flow rate and the actual flow rate through the LFOM.

    Parameters
    ----------
    Q: float
        flow through the LFOM

    hl : float
        headloss through the LFOM

    drill_bits: array of floats
        an array of potential drill bit sizes to create the orifices

    S_orifice : float
        Edge to edge spacing between orifices

    Returns
    -------
    float array
        difference between actual and expected flow rate

    Examples
    --------
    >>> from aide_design.play import*
    >>> flow_lfom_error(20*u.L/u.s, 20*u.cm, mat.DIAM_DRILL_ENG, 1*u.cm)
    <Quantity([-0.00032912  0.00029856 -0.00040128 -0.00041468 -0.00290567  0.00170122
      0.00089814], 'meter ** 3 / second')>
    """
    N_lfom_orifices = n_lfom_orifices(Q, hl, drill_bits, S_orifice)
    Q_lfom_error = []
    for j in range(len(N_lfom_orifices)-1):
        Q_lfom_error.append((flow_lfom_actual(
            Q, hl, j, N_lfom_orifices, drill_bits).magnitude-flow_ramp(
            Q, hl)[j].magnitude)/Q)
    return Q_lfom_error


@u.wraps(u.m**3/u.s, [u.m**3/u.s, u.m, u.m], False)
def flow_lfom_ideal(Q, hl, H):
    """This function calculates the expected flow rate of the LFOM under ideal
    conditions

    Parameters
    ----------
    Q: float
        flow through the LFOM

    hl : float
        headloss through the LFOM

    H: float
        height (includes freeboard)

    Returns
    -------
    float
        Ideal LFOM flow

    Examples
    --------
    >>> from aide_design.play import*
    >>> flow_lfom_ideal(20*u.L/u.s, 20*u.cm, 20*u.cm)
    <Quantity(0.02, 'meter ** 3 / second')>

    """
    flow_lfom_ideal = (Q*H)/hl
    return flow_lfom_ideal

@u.wraps(u.m**3/u.s, [u.m**3/u.s, u.m, u.m], False)
def flow_lfom(Q, hl, H, drill_bits=mat.DIAM_DRILL_ENG, S_orifice=1*u.cm):
    """Calculates the total flow from the LFOM under the given conditions

    Parameters
    ----------
    Q: float
        designed flow through the LFOM

    hl : float
        headloss through the LFOM

    H : float
        depth of the water

    drill_bits : array of floats
        an array of potential drill bit sizes to create the orifices

    S_orifice : float
        Edge to edge spacing between orifices

    Returns
    -------
    float
        total flow from the LFOM

    Examples
    --------
    >>> from aide_design.play import*
    >>> flow_lfom(20*u.L/u.s, 20*u.cm, 20*u.cm)
    <Quantity(0.00940749311972628, 'meter ** 3 / second')>

    """
    D_lfom_orifices = orifice_diameter(Q, hl, drill_bits).magnitude
    H_submerged = np.arange(H-0.5*D_lfom_orifices, hl,
                            H-dist_center_lfom_rows(Q,hl).magnitude,dtype=object)
    N_lfom_orifices = n_lfom_orifices(Q, hl, drill_bits, S_orifice)
    flow = []
    for i in range(len(H_submerged)):
        flow.append(pc.flow_orifice_vert(D_lfom_orifices, H_submerged[i], con.RATIO_VC_ORIFICE)*N_lfom_orifices[i])
    return sum(flow).magnitude
