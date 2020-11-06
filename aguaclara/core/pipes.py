"""This file contains functions which convert between the nominal, inner, and
outer diameters of pipes based on their standard dimension ratio (SDR).
"""
from aguaclara.core.units import u
import aguaclara.core.utility as ut
import numpy as np
import pandas as pd
from enum import Enum


import os.path
dir_path = os.path.dirname(__file__)
csv_path = os.path.join(dir_path, 'data/pipe_database.csv')
with open(csv_path) as pipedbfile:
    pipedb = pd.read_csv(pipedbfile)

# TODO: Add a deprecation warning for this once manifold design code has been
# implemented. The socket_depth and cap_thickness functions are used in
# a manifold calculation in sed_tank, and can also be transferred to pipeline
# design code once manifold design code has been implemented.

class SCH(Enum):
    #labeled by column of this schedule's wall thickness (ex: SCH40Wall is column 5)
    SCH40 = 'SCH40Wall' #5
    SCH80 = 'SCH80Wall'#7
    SCH120 = 'SCH120Wall'#9
    SCH160 = 'SCH160Wall'#11


class Pipe:

    def __init__(self, nd,sdr):
        self.nd= nd
        self.sdr = sdr
        # print("ND "+nd)

    @property
    def od(self):
        index = (np.abs(np.array(pipedb['NDinch']) - self.nd.magnitude)).argmin()
        return pipedb.iloc[index, 1] * u.inch

    @property
    def id_sdr(self):
        return (self.od.magnitude * (self.sdr - 2) / self.sdr) * u.inch

    def id_sch(self, schedule):
        """ 
        Return the inner diameter of this pipe, given the desired schedule
        :param schedule: the schedule of the pipe (use SCH.SCH40, SCH.SCH80, etc)

        :return: inner diameter of pipe
        :rtype: u.inch
        """
        myindex = (np.abs(np.array(pipedb['NDinch']) - self.nd.magnitude)).argmin()
        thickness = pipedb.iloc[myindex][schedule.value]
        if (thickness == 0): 
            return schedule ^ "does not exist for this ND"
        return (pipedb.iloc[myindex, 1] - 2 * (thickness)) * u.inch

    def sch(self, NDarr=[], SCHarr=[]):
        """ 
        Return the nominal diameter and schedule that best fits this pipe's criteria and NDarr and SCHarr
        :param NDarr: an array of preferred nominal diameters
        :param SCHarr: an array of preferred schedules

        :return: (nominal diameter, schedule) or "no matches"
        :rtype: (u.inch, SCH) or string
        """

        available = sch_all_available(self.id_sdr, self.sdr, NDarr, SCHarr)
        if available==[]:
            return "no schedules fit"
        return available[min(available)[0]==available[0]][1:]
        

def sch_all_available(minID, maxSDR, NDarr=[], SCHarr=[]):
    """
    Returns a list of tuples (inner diameter, nominal diameter, schedule) representing schedule pipes that fit the criteria. 
    Meeting criteria means: has at least minID, has at most maxSDR, and whose ND and/or SCH are in NDarr and SCHarr respectively. 
    """
    #loop through all nd and sch available. 
    #If find a pipe whose SDR is \le the requirement (smaller SDR=handle more pressure) 
    # and whose inner diameter is \ge the id_sdr, 
    # put it in a list. Send back that list. 

    #look through array if given, else look through the whole list
    nds = (ND_all_available() if (NDarr == []) else NDarr).magnitude
    schs = [SCH.SCH40, SCH.SCH80, SCH.SCH120, SCH.SCH160] if (SCHarr == []) else SCHarr 

    # print("nds",nds)

    allschs = []
    rows = []
    for i in range(len(pipedb['NDinch'])):
        # print("row " + str(i), pipedb.iloc[i,:])
        # print(pipedb.iloc[i, 4] == 1)
        # print(pipedb.iloc[i]['NDinch'] in nds)
        if pipedb.iloc[i, 4] == 1 and pipedb.iloc[i]['NDinch'] in nds:
            # print(str(i) + "made it inside")
            rows.append((pipedb.iloc[i]))
    # print('rows', rows)

    for row in rows:
        # print("nd row",row)
        for sch in schs:

            od = row['ODinch']
            t = row[sch.value]
            sdr = od/t
            id = od - t

            # print("sch", sch)
            # print("id and minid",id, minID)

            # print(id >= minID.magnitude)
            # print(sdr <= maxSDR)
            if (id >= minID.magnitude and sdr <= maxSDR):
                allschs.append((id,row['NDinch']*u.inch, sch.name))
    # print(allschs)
    return allschs



def makePipe_ND_SDR(ND, SDR):
    """Return a new pipe, given its ND (nominal diameter) and SDR (standard diameter ratio).

    :param ND: nominal diameter of pipe
    :param SDR: standard diameter ratio of pipe

    :return: a pipe with the given ND and SDR
    :rtype: Pipe
    """
    return Pipe(ND, SDR)

def makePipe_minID_SDR(minID, SDR):
    """Return a new pipe, given its minID (minimum inner diameter) and SDR (standard diameter ratio).

    :param minID: minimum inner diameter of pipe
    :param SDR: standard diameter ratio of pipe

    :return: a pipe with SDR and ND calculated from given minID and SDR
    :rtype: Pipe
    """

    # print("ND made "+str(ND_SDR_available(minID, SDR).magnitude))
    # print('nd assigned')
    # print(ND_SDR_available(minID, SDR))

    return Pipe(ND_SDR_available(minID, SDR), SDR)

@ut.list_handler()
def OD(ND):
    """Return a pipe's outer diameter according to its nominal diameter.

    :param ND: nominal diameter of pipe
    :type ND: u.inch

    :return: outer diameter of pipe, in inches
    :rtype: u.inch
    """
    # The pipe schedule is not required here because all of the pipes of a
    # given nominal diameter have the same outer diameter.
    #
    # Steps:
    # 1. Find the index of the closest nominal diameter.
    #    (Should this be changed to find the next largest ND?)
    # 2. Take the values of the array, subtract the ND, take the absolute
    #    value, find the index of the minimium value.
    ND = ND.to(u.inch).magnitude
    index = (np.abs(np.array(pipedb['NDinch']) - (ND))).argmin()
    return pipedb.iloc[index, 1] * u.inch


def OD_from_IDSDR(ID,SDR):
    """ Return the minimum OD that is available given ID and SDR. 
    1. calculate OD matching with ID and SDR.
    2. find minimum OD available.
    raises: ValueError is SDR is 2. 

    ID is the inner diameter.
    SDR is the outer diameter divided by the wall thickness.
    """
    if SDR == 2:
        raise ValueError("SDR cannot be 2!")
    return od_available((ID*SDR)/(SDR-2))


@ut.list_handler()
def fitting_od(pipe_nd, fitting_sdr=41):
    pipe_od = OD(pipe_nd)
    fitting_nd = ND_SDR_available(pipe_od, fitting_sdr)
    fitting_od = OD(fitting_nd)
    return fitting_od


@ut.list_handler()
def ID_SDR(ND, SDR):
    """Return the inner diameter of a pipe given its nominal diameter and SDR
    (standard diameter ratio).

    SDR is the outer diameter divided by the wall thickness.
    """
    return OD(ND) * (SDR-2) / SDR


@ut.list_handler()
def ID_sch40(ND):
    """Return the inner diameter for schedule 40 pipes.

    The wall thickness for these pipes is in the pipedb.

    Take the values of the array, subtract the ND, take the absolute
    value, find the index of the minimium value.
    """
    ND = ND.to(u.inch).magnitude
    myindex = (np.abs(np.array(pipedb['NDinch']) - (ND))).argmin()
    return (pipedb.iloc[myindex, 1] - 2*(pipedb.iloc[myindex, 5])) * u.inch


def ND_all_available():
    """Return an array of available nominal diameters.

    NDs available are those commonly used as based on the 'Used' column
    in the pipedb.
    """
    ND_all_available = []
    for i in range(len(pipedb['NDinch'])):
        if pipedb.iloc[i, 4] == 1:
            ND_all_available.append((pipedb['NDinch'][i]))
    return ND_all_available * u.inch


def od_all_available():
    """Return an array of available outer diameters.

    NDs available are those commonly used as based on the 'Used' column
    in the pipedb.
    """
    od_all_available = []
    for i in range(len(pipedb['ODinch'])):
        if pipedb.iloc[i, 4] == 1:
            od_all_available.append((pipedb['ODinch'][i]))
    return od_all_available * u.inch


@ut.list_handler()
def ID_SDR_all_available(SDR):
    """Return an array of inner diameters with a given SDR.

    IDs available are those commonly used based on the 'Used' column
    in the pipedb.
    """
    ID = []
    ND = ND_all_available()
    for i in range(len(ND)):
        ID.append(ID_SDR(ND[i], SDR).magnitude)
    return ID * u.inch


@ut.list_handler()
def ND_SDR_available(ID, SDR):
    """ Return an available ND given an ID and a schedule.

    Takes the values of the array, compares to the ID, and finds the index
    of the first value greater or equal.
    """
    for i in range(len(np.array(ID_SDR_all_available(SDR)))):
        if np.array(ID_SDR_all_available(SDR))[i] >= (ID.to(u.inch)).magnitude:
            # print("ND AVAIL")
            # print(ND_all_available()[i].magnitude)
            return ND_all_available()[i]


@ut.list_handler()
def ND_available(NDguess):
    """Return the minimum ND that is available.

    1. Extract the magnitude in inches from the nominal diameter.
    2. Find the index of the closest nominal diameter.
    3. Take the values of the array, subtract the ND, take the
       absolute value, find the index of the minimium value.
    """
    myindex = (ND_all_available() >= NDguess)
    return min(ND_all_available()[myindex])


@ut.list_handler()
def od_available(od_guess):
    """Return the minimum OD that is available.

    1. Extract the magnitude in inches from the outer diameter.
    2. Find the index of the closest outer diameter.
    3. Take the values of the array, subtract the OD, take the
       absolute value, find the index of the minimium value.
    """
    myindex = (od_all_available() >= od_guess)
    return min(od_all_available()[myindex])


@ut.list_handler()
def socket_depth(nd):
    return nd / 2


@ut.list_handler()
def cap_thickness(nd):
    cap_thickness = (fitting_od(nd) - OD(ND_available(nd))) / 2
    return cap_thickness




""" TODO: Several updates can be made to core/pipes.py:

1. A class and/or static method should be defined to convert ID and SDR to the minimum available OD. 
   A class could ask for SDR and minimum ID in the constructor and include methods for available ID, ND, and OD. 
   A static method could calculate OD from ID and SDR and use the existing od_available(od_guess) method, or calculate ND using ND_SDR_available(ID, SDR) and convert ND to OD.

2. Method and method parameter names should be standardized. For example, ND_available(NDguess) and od_available(od_guess) have different formats.

3. All methods and classes should be fully and properly documented. 
   "Properly documented" means the descriptions should be accurate and include only information helpful to users 
   (implementation instructions and internal variable names like pipedb would not be helpful).

4. Functions ending in all_available can be made more efficient. 
   For example, most of the computation in ND_all_available() can be implemented one-line conditional indexing: return pipedb['NDinch'][pipedb['Used'] == 1]. 

5. Write test cases for each function

"""



"""
added to pipe database for schedule 80, 120 and 160 using 
https://www.engineersedge.com/pipe_schedules.htm#Related 
"""