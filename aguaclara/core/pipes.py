"""This file contains functions which convert between the nominal, inner, and
outer diameters of pipes based on their standard dimension ratio (SDR).

"""

#Let's begin to create the pipe database
# https://docs.python.org/2/library/csv.html
from aguaclara.core.units import unit_registry as u
import numpy as np
import pandas as pd
# load the pipedb from a csv file

import os.path
dir_path = os.path.dirname(__file__)
csv_path = os.path.join(dir_path, 'data/pipe_database.csv')
with open(csv_path) as pipedbfile:
    pipedb = pd.read_csv(pipedbfile)

""""""
class Pipe:


    def __init__(self, nd,sdr):
        self.nd= nd
        self.sdr = sdr

    @property
    def od(self):
        index = (np.abs(np.array(pipedb['NDinch']) - self.nd.magnitude)).argmin()
        return pipedb.iloc[index, 1] * u.inch

    @property
    def id_sdr(self):
        return self.od.magnitude * (self.sdr - 2) / self.sdr

    @property
    def id_sch40(self):
        myindex = (np.abs(np.array(pipedb['NDinch']) - self.nd.magnitude)).argmin()
        return (pipedb.iloc[myindex, 1] - 2 * (pipedb.iloc[myindex, 5]))

@u.wraps(u.inch, u.inch, False)
def OD(ND):
    """Return a pipe's outer diameter according to its nominal diameter.

    The pipe schedule is not required here because all of the pipes of a
    given nominal diameter have the same outer diameter.

    Steps:
    1. Find the index of the closest nominal diameter.
       (Should this be changed to find the next largest ND?)
    2. Take the values of the array, subtract the ND, take the absolute
       value, find the index of the minimium value.
    """
    index = (np.abs(np.array(pipedb['NDinch']) - (ND))).argmin()
    return pipedb.iloc[index, 1]

@u.wraps(u.inch, [u.inch, None], False)
def ID_SDR(ND, SDR):
    """Return the inner diameter for SDR(standard diameter ratio) pipes.

    For these pipes the wall thickness is the outer diameter divided by
    the SDR.
    """
    return OD(ND).magnitude * (SDR-2) / SDR

@u.wraps(u.inch, u.inch, False)
def ID_sch40(ND):
    """Return the inner diameter for schedule 40 pipes.

    The wall thickness for these pipes is in the pipedb.

    Take the values of the array, subtract the ND, take the absolute
    value, find the index of the minimium value.
    """
    myindex = (np.abs(np.array(pipedb['NDinch']) - (ND))).argmin()
    return (pipedb.iloc[myindex, 1] - 2*(pipedb.iloc[myindex, 5]))


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


def ND_SDR_available(ID, SDR):
    """ Return an available ND given an ID and a schedule.

    Takes the values of the array, compares to the ID, and finds the index
    of the first value greater or equal.
    """
    for i in range(len(np.array(ID_SDR_all_available(SDR)))):
        if np.array(ID_SDR_all_available(SDR))[i] >= (ID.to(u.inch)).magnitude:
            return ND_all_available()[i]


def ND_available(NDguess):
    """Return the minimum ND that is available.

    1. Extract the magnitude in inches from the nominal diameter.
    2. Find the index of the closest nominal diameter.
    3. Take the values of the array, subtract the ND, take the
       absolute value, find the index of the minimium value.
    """
    myindex = (ND_all_available() >= NDguess)
    return min(ND_all_available()[myindex])
