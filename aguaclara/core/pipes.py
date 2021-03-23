"""This file contains functions which convert between the nominal, inner, and
outer diameters of pipes based on their standard dimension ratio (SDR).

Note: 
added to pipe database for schedule 80, 120 and 160 using 
https://www.engineersedge.com/pipe_schedules.htm#Related 
"""

from aguaclara.core.units import u
import aguaclara.core.utility as ut
import numpy as np
import pandas as pd
from enum import Enum


import os.path
import warnings
dir_path = os.path.dirname(__file__)
csv_path = os.path.join(dir_path, 'data/pipe_database.csv')
with open(csv_path) as pipedbfile:
    pipedb = pd.read_csv(pipedbfile)

# TODO: Add a deprecation warning for this once manifold design code has been
# implemented. The socket_depth and cap_thickness functions are used in
# a manifold calculation in sed_tank, and can also be transferred to pipeline
# design code once manifold design code has been implemented.

class SCH(Enum):
    # value is the column name for a schedule's wall thickness 
    SCH40 = 'SCH40Wall' 
    SCH80 = 'SCH80Wall' 
    SCH120 = 'SCH120Wall' 
    SCH160 = 'SCH160Wall' 


class Pipe:
    """A pipe using the SDR system, represented by its nominal diameter (ND) and standard dimension ratio (SDR)"""
    def __init__(self, nd,sdr):
        self.nd= nd
        self.sdr = sdr

    @property
    def od(self):
        """The outer diameter of the pipe."""
        index = (np.abs(np.array(pipedb['NDinch']) - self.nd.magnitude)).argmin()
        return pipedb.iloc[index, 1] * u.inch

    @property
    def id_sdr(self):
        """The inner diameter of the pipe, calculated using the pipe's OD and SDR."""
        return (self.od.magnitude * (self.sdr - 2) / self.sdr) * u.inch

    @property
    def id_sch40(self):
        """
        .. deprecated::
        `id_sch40` is deprecated; use `id_sch` instead.
        """
        warnings.warn('id_sch40 is deprecated; use id_sch instead.', UserWarning)
        myindex = (np.abs(np.array(pipedb['NDinch']) - self.nd.magnitude)).argmin()
        return (pipedb.iloc[myindex, 1] - 2 * (pipedb.iloc[myindex, 5])) * u.inch


    def id_sch(self, schedule):
        """ 
        The inner diameter of this pipe, based on schedule and nominal diameter
        :param schedule: the schedule of the pipe (Ex: pipes.SCH.SCH40)
        :type schedule: pipes.SCH

        :return: The inner diameter of the pipe
        :rtype: u.inch
        """
        myindex = (np.abs(np.array(pipedb['NDinch']) - self.nd.magnitude)).argmin()
        thickness = pipedb.iloc[myindex][schedule.value]
        if (thickness == 0): 
            return schedule ^ " does not exist for this ND"
        return (pipedb.iloc[myindex, 1] - 2 * (thickness)) * u.inch

    def sch(self, NDarr=None, SCHarr=None):
        """ 
        The nominal diameter and schedule that best fits this pipe's criteria and NDarr and SCHarr
        :param NDarr: an array of preferred nominal diameters (Ex: [10]*u.inch). Default: None
        :type NDarr: numpy.array * u.inch
        :param SCHarr: an array of preferred schedules (Ex: [pipes.SCH.SCH160, pipes.SCH.SCH40]). Default: None
        :type SCHarr: pipes.SCH list 

        :return: (nominal diameter, schedule) tuple or None
        :rtype: (u.inch, SCH) or None
        """

        # get list of all (ND, SCH) available and return the (ND, SCH) resulting in the least ID 
        available = SCH_all_available(self.id_sdr, self.sdr, NDarr, SCHarr)

        if available==[]:
            return None
        def sch_based_on_name(n):
            if n == SCH.SCH40.name:
                return SCH.SCH40
            elif n == SCH.SCH80.name:
                return SCH.SCH80
            elif n == SCH.SCH120.name:
                return SCH.SCH120
            elif n == SCH.SCH160.name:
                return SCH.SCH160
        def addID (p):
            # find id that goes with nd sch and add it to the tuple
            # p is of the structure (ND, schedule name)
            # outputs (id, nd, sch) tuple
            nd = p[0]
            sch = p[1]
            row = pipedb.loc[pipedb['NDinch'] == nd.magnitude] # 1 row df
            t = row[sch_based_on_name(sch).value].iloc[0]
            od = row['ODinch'].iloc[0]

            return (od-2*t, nd, sch)
        available = list(map(addID, available))
        m = min(available)[0]

        return list(filter(lambda x: m == x[0], available))[0][1:]
        

def makePipe_ND_SDR(ND, SDR):
    """
    Return a Pipe object, given a ND (nominal diameter) and SDR (standard diameter ratio).

    :param ND: nominal diameter of pipe
    :type ND: u.inch
    :param SDR: standard diameter ratio of pipe
    :type SDR: float

    :return: a pipe with the given ND and SDR
    :rtype: Pipe
    """
    return Pipe(ND, SDR)

def makePipe_minID_SDR(minID, SDR):
    """Return a new pipe, given its minID (minimum inner diameter) and SDR (standard diameter ratio).

    :param minID: minimum inner diameter of pipe
    :type minID: u.inch
    :param SDR: standard diameter ratio of pipe
    :type SDR: float

    :return: a pipe with SDR and ND calculated from given minID and SDR
    :rtype: Pipe
    """

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


def OD_SDR(ID,SDR):
    """ Return the minimum OD that is available given ID and SDR. 
    raises: ValueError if SDR is 2. 

    :param ID: inner diameter of pipe
    :type ID: u.inch
    :param SDR: the standard dimension ratio of the pipe
    :type SDR: float

    :return: minimum outer diameter available
    :rtype: u.inch
    """
    if SDR == 2:
        raise ValueError("SDR cannot be 2!")
    return OD_available((ID*SDR)/(SDR-2))


@ut.list_handler()
def fitting_od(pipe_nd, fitting_sdr=41):
    """
    Return the OD of a fitting given SDR and the ND of the pipe it will be fitted around

    :param pipe_nd: ND of the pipe to be fitted around
    :type pipe_nd: u.inch
    :param fitting_sdr: SDR of the pipe to be fitted around
    :type fitting_sdr: float

    :return: the outer diameter of a fitting
    :rtype: u.inch
    """
    pipe_od = OD(pipe_nd)
    fitting_nd = ND_SDR_available(pipe_od, fitting_sdr)
    fitting_od = OD(fitting_nd)
    return fitting_od


@ut.list_handler()
def ID_SDR(ND, SDR):
    """Return the inner diameter of a pipe given its nominal diameter and SDR
    (standard dimension ratio).

    :param ND: the nominal diameter 
    :type ND: u.inch
    :param SDR: the outer diameter divided by the wall thickness.
    :type SDR: float

    :return: inner diameter of a pipe
    :rtype: u.inch
    """
    return OD(ND) * (SDR-2) / SDR


def ID_sch(ND, schedule):
    """ 
    Return the inner diameter of this pipe, given the ND and desired schedule
    :param ND: the nominal diameter of the pipe
    :type ND: u.inch
    :param schedule: the schedule of the pipe (use SCH.SCH40, SCH.SCH80, etc)
    :type schedule: pipes.SCH

    :return: inner diameter of pipe
    :rtype: u.inch
    """
    myindex = (np.abs(np.array(pipedb['NDinch']) - ND.magnitude)).argmin()
    thickness = pipedb.iloc[myindex][schedule.value]
    if (thickness == 0): 
        return schedule ^ "does not exist for this ND"
    return (pipedb.iloc[myindex, 1] - 2 * (thickness)) * u.inch


def ND_all_available():
    """Return an array of available nominal diameters.

    NDs available are those commonly used as based on the 'Used' column
    in the pipedb.

    :return: an array of available nominal diameters
    :rtype: numpy.array * u.inch
    """
    return (pipedb['NDinch'][pipedb['Used'] == 1]).to_numpy() * u.inch



def OD_all_available():
    """Return an array of available outer diameters.

    NDs available are those commonly used as based on the 'Used' column
    in the pipedb.

    :return: an array of available outer diamters
    :rtype: numpy.array * u.inch
    """
    return (pipedb['ODinch'][pipedb['Used'] == 1]).to_numpy() * u.inch



@ut.list_handler()
def ID_SDR_all_available(SDR):
    """Return an array of inner diameters with a given SDR.

    IDs available are those commonly used based on the 'Used' column
    in the pipedb.

    :param SDR: the standard dimension ratio 
    :type SDR: float

    :return: an array of inner diamers
    :rtype: numpy.array * u.inch
    """
    nds = (pipedb['NDinch'][pipedb['Used'] == 1]).to_numpy() * u.inch
    return list(map(lambda x: ID_SDR(x,SDR).magnitude, nds)) * u.inch


def SCH_all_available(minID, maxSDR, NDarr=None, SCHarr=[SCH.SCH40, SCH.SCH80, SCH.SCH120, SCH.SCH160]):
    """
    Return a list of tuples (nominal diameter, schedule) representing schedule pipes that fit the criteria. 
    Meeting criteria means: has at least minID, has at most maxSDR, and whose ND and/or SCH are in NDarr and SCHarr respectively. 
    Default: NDarr looks through all available ND, SCHarr looks through all schedules

    :param minID: the minimum inner diameter required
    :type minID: u.inch
    :param maxSDR: the maximum SDR required
    :type maxSDR: float
    :param NDarr: the preferred list of NDs to look through
    :type NDarr: numpy.array * u.inch
    :param SCHarr: the preferred list of schedules to look through
    :type SCHarr: pipes.SCH list

    :return: list of tuples in the form (nominal diameter, schedule). Example: (10*u.inch, "SCH160")
    :rtype: (float*u.inch, string) list
    """
    #loop through all nd and sch available. 
    #If find a pipe whose SDR is \le the requirement (smaller SDR=handle more pressure) 
    # and whose inner diameter is \ge the id_sdr, 
    # put it in a list. Send back that list. 

    #look through array if given, else look through the whole list
 
    nds = ND_all_available()/u.inch if NDarr is None  else NDarr/u.inch
    schs = [SCH.SCH40, SCH.SCH80, SCH.SCH120, SCH.SCH160] if (SCHarr is None) else SCHarr 

    allschs = []
    rows = pipedb.loc[(pipedb['Used'] == 1) & pipedb['NDinch'].isin(nds)]

    for index, row in rows.iterrows():
        for sch in schs:
            t = row[sch.value]
            if t != 0:
                od = row['ODinch']
                
                sdr = od/t
                id = od - 2*t

                if (id >= minID.magnitude and sdr <= maxSDR):
                    allschs.append( (row['NDinch']*u.inch, sch.name) )
    return allschs



@ut.list_handler()
def ND_SDR_available(ID, SDR):
    """ Return an available ND given an ID and a schedule.

    Takes the values of the array, compares to the ID, and finds the index
    of the first value greater or equal.

    :param ID: the inner diameter
    :type ID: u.inch
    :param SDR: the standard dimension ratio
    :type SDR: float

    :return: an available ND 
    :rtype: u.inch
    """
    for i in range(len(np.array(ID_SDR_all_available(SDR).magnitude))):
        if np.array(ID_SDR_all_available(SDR).magnitude)[i] >= (ID.to(u.inch)).magnitude:
            return ND_all_available()[i]


@ut.list_handler()
def ND_available(NDguess):
    """Return the minimum ND that is available.

    :param NDguess: the lower bound nominal diameter 
    :type NDguess: u.inch

    :return: the minimum ND available greater than NDguess
    :rtype: u.inch
    """
    # 1. Extract the magnitude in inches from the nominal diameter.
    # 2. Find the index of the closest nominal diameter.
    # 3. Take the values of the array, subtract the ND, take the
    #    absolute value, find the index of the minimium value.
    myindex = (ND_all_available() >= NDguess)
    return min(ND_all_available()[myindex])


@ut.list_handler()
def OD_available(ODguess):
    """Return the minimum OD that is available.

    :param ODguess: the lower bound outer diameter
    :type ODguess: u.inch

    :return: the minimum OD available greater than ODguess
    :rtype: u.inch
    """
    # 1. Extract the magnitude in inches from the outer diameter.
    # 2. Find the index of the closest outer diameter.
    # 3. Take the values of the array, subtract the OD, take the
    #    absolute value, find the index of the minimium value.
    myindex = (OD_all_available() >= ODguess)
    return min(OD_all_available()[myindex])


@ut.list_handler()
def socket_depth(ND):
    """
    Return the socket depth given ND

    :param ND: the nominal diameter
    :type ND: u.inch 

    :return: the socket depth
    :rtype: u.inch (or the type of ND)
    """
    return ND / 2


@ut.list_handler()
def cap_thickness(ND):
    """
    Return the cap thickness given ND

    :param ND: the nominal diameter
    :type ND: u.inch

    :return: the cap thickness
    :rtype: u.inch
    """
    cap_thickness = (fitting_od(ND) - OD(ND_available(ND))) / 2
    return cap_thickness


