"""This file contains functions which convert between the nominal, inner, and
outer diameters of pipes based on their standard dimension ratio (SDR).
"""
from aguaclara.core.units import u
import aguaclara.core.utility as ut
import numpy as np
import pandas as pd

import os.path
dir_path = os.path.dirname(__file__)
csv_path = os.path.join(dir_path, 'data/pipe_database.csv')
with open(csv_path) as pipedbfile:
    pipedb = pd.read_csv(pipedbfile)

# TODO: Add a deprecation warning for this once manifold design code has been
# implemented. The socket_depth and cap_thickness functions are used in
# a manifold calculation in sed_tank, and can also be transferred to pipeline
# design code once manifold design code has been implemented.

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
        return (self.od.magnitude * (self.sdr - 2) / self.sdr) * u.inch

    @property
    def id_sch40(self):
        myindex = (np.abs(np.array(pipedb['NDinch']) - self.nd.magnitude)).argmin()
        return (pipedb.iloc[myindex, 1] - 2 * (pipedb.iloc[myindex, 5])) * u.inch


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
