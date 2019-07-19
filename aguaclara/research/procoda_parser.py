from aguaclara.core.units import u
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
from pathlib import Path


def get_data_by_time(path, columns, dates, start_time='00:00', end_time='23:59'):
    """Extract columns of data from a ProCoDA datalog based on date(s) and time(s)

    Note: Column 0 is time. The first data column is column 1.

    :param path: The path to the folder containing the ProCoDA data file(s)
    :type path: string
    :param columns: A single index of a column OR a list of indices of columns of data to extract.
    :type columns: int or int list
    :param dates: A single date or list of dates for which data was recorded, formatted "M-D-YYYY"
    :type dates: string or string list
    :param start_time: Starting time of data to extract, formatted 'HH:MM' (24-hour time)
    :type start_time: string, optional
    :param end_time: Ending time of data to extract, formatted 'HH:MM' (24-hour time)
    :type end_time: string, optional

    :return: a list containing the single column of data to extract, OR a list of lists containing the columns to extract, in order of the indices given in the columns variable
    :rtype: list or list list

    :Examples:

    .. code-block:: python

        data = get_data_by_time(path='/Users/.../ProCoDA Data/', columns=4, dates=['6-14-2018', '6-15-2018'], start_time='12:20', end_time='10:50')
        data = get_data_by_time(path='/Users/.../ProCoDA Data/', columns=[0,4], dates='6-14-2018', start_time='12:20', end_time='23:59')
        data = get_data_by_time(path='/Users/.../ProCoDA Data/', columns=[0,3,4], dates='6-14-2018')
    """
    data = data_from_dates(path, dates)

    first_time_column = pd.to_numeric(data[0].iloc[:, 0])
    start = max(day_fraction(start_time), first_time_column[0])
    start_idx = time_column_index(start, first_time_column)
    end_idx = time_column_index(day_fraction(end_time),
        pd.to_numeric(data[-1].iloc[:, 0])) + 1

    if isinstance(columns, int):
        return column_start_to_end(data, columns, start_idx, end_idx)
    else:
        result = []
        for c in columns:
            result.append(column_start_to_end(data, c, start_idx, end_idx))
    return result


def remove_notes(data):
    """Omit notes from a DataFrame object, where notes are identified as rows with non-numerical entries in the first column.

    :param data: DataFrame object to remove notes from
    :type data: Pandas.DataFrame

    :return: DataFrame object with no notes
    :rtype: Pandas.DataFrame
    """
    has_text = data.iloc[:, 0].astype(str).str.contains('(?!e-)[a-zA-Z]')
    text_rows = list(has_text.index[has_text])
    return data.drop(text_rows)


def day_fraction(time):
    """Convert a 24-hour time to a fraction of a day.

    For example, midnight corresponds to 0.0, and noon to 0.5.

    :param time: Time in the form of 'HH:MM' (24-hour time)
    :type time: string

    :return: A day fraction
    :rtype: float

    :Examples:

    .. code-block:: python

        day_fraction("18:30")
    """
    hour = int(time.split(":")[0])
    minute = int(time.split(":")[1])
    return hour/24 + minute/1440


def time_column_index(time, time_column):
    """Return the index of lowest time in the column of times that is greater
    than or equal to the given time.

    :param time: the time to index from the column of time; a day fraction
    :type time: float
    :param time_column: a list of times (in day fractions), must be increasing and equally spaced
    :type time_column: float list

    :return: approximate index of the time from the column of times
    :rtype: int
    """
    interval = time_column[1]-time_column[0]
    return int(round((time - time_column[0])/interval + .5))


def data_from_dates(path, dates):
    """Return list DataFrames representing the ProCoDA datalogs stored in
    the given path and recorded on the given dates.

    :param path: The path to the folder containing the ProCoDA data file(s)
    :type path: string
    :param dates: A single date or list of dates for which data was recorded, formatted "M-D-YYYY"
    :type dates: string or string list

    :return: a list DataFrame objects representing the ProCoDA datalogs corresponding with the given dates
    :rtype: pandas.DataFrame list
    """

    if not isinstance(dates, list):
        dates = [dates]

    data = []
    for d in dates:
        filepath = os.path.join(path, 'datalog ' + d + '.xls')
        data.append(remove_notes(pd.read_csv(filepath, delimiter='\t')))

    return data


def column_start_to_end(data, column, start_idx, end_idx):
    """Return a list of numeric data entries in the given column from the starting
    index to the ending index. This can list can be compiled over one or more
    DataFrames.

    :param data: a list of DataFrames to extract data in one column from
    :type data: Pandas.DataFrame list
    :param column: a column index
    :type column: int
    :param start_idx: the index of the starting row
    :type start_idx: int
    :param start_idx: the index of the ending row
    :type start_idx: int

    :return: a list of data from the given column
    :rtype: float list
    """
    if len(data) == 1:
        result = list(pd.to_numeric(data[0].iloc[start_idx:end_idx, column]))
    else:
        result = list(pd.to_numeric(data[0].iloc[start_idx:, column]))
        for i in range(1, len(data)-1):
            data[i].iloc[0, 0] = 0
            result += list(pd.to_numeric(data[i].iloc[:, column]) +
                      (i if column == 0 else 0))
        data[-1].iloc[0, 0] = 0
        result += list(pd.to_numeric(data[-1].iloc[:end_idx, column]) +
                  (len(data)-1 if column == 0 else 0))

    return result


def get_data_by_state(path, dates, state, column):
    """Reads a ProCoDA file and extracts the time and data column for each
    iteration ofthe given state.

    Note: column 0 is time, the first data column is column 1.

    :param path: The path to the folder containing the ProCoDA data file(s), defaults to the current directory
    :type path: string
    :param dates: A single date or list of dates for which data was recorded, formatted "M-D-YYYY"
    :type dates: string or string list
    :param state: The state ID number for which data should be plotted
    :type state: int
    :param column: The integer index of the column that you want to extract OR the header of the column that you want to extract
    :type column: int or string

    :return: A list of lists of the time and data columns extracted for each iteration of the state. For example, if "data" is the output, data[i][:,0] gives the time column and data[i][:,1] gives the data column for the ith iteration of the given state and column. data[i][0] would give the first [time, data] pair.
    :type: list of lists of lists

    :Examples:

    .. code-block:: python

        data = get_data_by_state(path='/Users/.../ProCoDA Data/', dates=["6-19-2013", "6-20-2013"], state=1, column=28)
    """
    data_agg = []
    day = 0
    first_day = True
    overnight = False
    extension = ".xls"
    if path[-1] != '/':
        path += '/'

    if not isinstance(dates, list):
        dates = [dates]

    for d in dates:
        state_file = path + "statelog " + d + extension
        data_file = path + "datalog " + d + extension

        states = pd.read_csv(state_file, delimiter='\t')
        data = pd.read_csv(data_file, delimiter='\t')

        states = np.array(states)
        data = np.array(data)

        # get the start and end times for the state
        state_start_idx = states[:, 1] == state
        state_start = states[state_start_idx, 0]
        state_end_idx = np.append([False], state_start_idx[0:-1])
        state_end = states[state_end_idx, 0]

        if overnight:
            state_start = np.insert(state_start, 0, 0)
            state_end = np.insert(state_end, 0, states[0, 0])

        if state_start_idx[-1]:
            np.append(state_end, data[0, -1])

        # get the corresponding indices in the data array
        data_start = []
        data_end = []
        for i in range(np.size(state_start)):
            add_start = True
            for j in range(np.size(data[:, 0])):
                if (data[j, 0] > state_start[i]) and add_start:
                    data_start.append(j)
                    add_start = False
                if data[j, 0] > state_end[i]:
                    data_end.append(j-1)
                    break

        if first_day:
            start_time = data[0, 0]

        # extract data at those times
        for i in range(np.size(data_start)):
            t = data[data_start[i]:data_end[i], 0] + day - start_time
            if isinstance(column, int):
                c = data[data_start[i]:data_end[i], column]
            else:
                c = data[column][data_start[i]:data_end[i]]
            if overnight and i == 0:
                data_agg = np.insert(data_agg[-1], np.size(data_agg[-1][:, 0]),
                                     np.vstack((t, c)).T)
            else:
                data_agg.append(np.vstack((t, c)).T)

        day += 1
        if first_day:
            first_day = False
        if state_start_idx[-1]:
            overnight = True

    return data_agg


def column_of_time(path, start, end=-1):
    """This function extracts the column of times from a ProCoDA data file.

    :param path: The file path of the ProCoDA data file. If the file is in the working directory, then the file name is sufficient.
    :type path: string
    :param start: Index of first row of data to extract from the data file
    :type start: int
    :param end: Index of last row of data to extract from the data. Defaults to last row
    :type end: int

    :return: Experimental times starting at 0 day with units of days.
    :rtype: numpy.array

    :Examples:

    .. code-block:: python

        time = column_of_time("Reactor_data.txt", 0)
    """
    df = pd.read_csv(path, delimiter='\t')
    start_time = pd.to_numeric(df.iloc[start, 0])*u.day
    day_times = pd.to_numeric(df.iloc[start:end, 0])
    time_data = np.subtract((np.array(day_times)*u.day), start_time)
    return time_data


def column_of_data(path, start, column, end="-1", units=""):
    """This function extracts a column of data from a ProCoDA data file.

    Note: Column 0 is time. The first data column is column 1.

    :param path: The file path of the ProCoDA data file. If the file is in the working directory, then the file name is sufficient.
    :type path: string
    :param start: Index of first row of data to extract from the data file
    :type start: int
    :param end: Index of last row of data to extract from the data. Defaults to last row
    :type end: int, optional
    :param column: Index of the column that you want to extract OR name of the column header that you want to extract
    :type column: int or string
    :param units: The units you want to apply to the data, e.g. 'mg/L'. Defaults to "" (dimensionless)
    :type units: string, optional

    :return: Experimental data with the units applied.
    :rtype: numpy.array

    :Examples:

    .. code-block:: python

        data = column_of_data("Reactor_data.txt", 0, 1, -1, "mg/L")
    """
    if not isinstance(start, int):
        start = int(start)
    if not isinstance(end, int):
        end = int(end)

    df = pd.read_csv(path, delimiter='\t')
    if units == "":
        if isinstance(column, int):
            data = np.array(pd.to_numeric(df.iloc[start:end, column]))
        else:
            df[column][0:len(df)]
    else:
        if isinstance(column, int):
            data = np.array(pd.to_numeric(df.iloc[start:end, column]))*u(units)
        else:
            df[column][0:len(df)]*u(units)
    return data


def notes(path):
    """This function extracts any experimental notes from a ProCoDA data file.

    :param path: The file path of the ProCoDA data file. If the file is in the working directory, then the file name is sufficient.
    :type path: string

    :return: The rows of the data file that contain text notes inserted during the experiment. Use this to identify the section of the data file that you want to extract.
    :rtype: pandas.Dataframe
    """
    df = pd.read_csv(path, delimiter='\t')
    text_row = df.iloc[0:-1, 0].str.contains('[a-z]', '[A-Z]')
    text_row_index = text_row.index[text_row].tolist()
    notes = df.loc[text_row_index]
    return notes


def read_state(dates, state, column, units="", path="", extension=".xls"):
    """Reads a ProCoDA file and outputs the data column and time vector for
    each iteration of the given state.

    Note: Column 0 is time. The first data column is column 1.

    :param dates: A single date or list of dates for which data was recorded, formatted "M-D-YYYY"
    :type dates: string or string list
    :param state: The state ID number for which data should be extracted
    :type state: int
    :param column: Index of the column that you want to extract OR header of the column that you want to extract
    :type column: int or string
    :param units: The units you want to apply to the data, e.g. 'mg/L'. Defaults to "" (dimensionless)
    :type units: string, optional
    :param path: The file path of the ProCoDA data file. If the file is in the working directory, then the file name is sufficient.
    :type path: string
    :param extension: The file extension of the tab delimited file. Defaults to ".xls" if no argument is passed in
    :type extension: string, optional

    :return: time (numpy.array) - Times corresponding to the data (with units)
    :return: data (numpy.array) - Data in the given column during the given state with units

    :Examples:

    .. code-block:: python

        time, data = read_state(["6-19-2013", "6-20-2013"], 1, 28, "mL/s")
    """
    data_agg = []
    day = 0
    first_day = True
    overnight = False

    if not isinstance(dates, list):
        dates = [dates]

    for d in dates:
        state_file = path + "statelog " + d + extension
        data_file = path + "datalog " + d + extension

        states = pd.read_csv(state_file, delimiter='\t')
        data = pd.read_csv(data_file, delimiter='\t')

        states = np.array(states)
        data = np.array(data)

        # get the start and end times for the state
        state_start_idx = states[:, 1] == state
        state_start = states[state_start_idx, 0]
        state_end_idx = np.append([False], state_start_idx[0:(np.size(state_start_idx)-1)])
        state_end = states[state_end_idx, 0]

        if overnight:
            state_start = np.insert(state_start, 0, 0)
            state_end = np.insert(state_end, 0, states[0, 0])

        if state_start_idx[-1]:
            state_end.append(data[0, -1])

        # get the corresponding indices in the data array
        data_start = []
        data_end = []
        for i in range(np.size(state_start)):
            add_start = True
            for j in range(np.size(data[:, 0])):
                if (data[j, 0] > state_start[i]) and add_start:
                    data_start.append(j)
                    add_start = False
                if (data[j, 0] > state_end[i]):
                    data_end.append(j-1)
                    break

        if first_day:
            start_time = data[1, 0]

        # extract data at those times
        for i in range(np.size(data_start)):
            t = data[data_start[i]:data_end[i], 0] + day - start_time
            if isinstance(column, int):
                c = data[data_start[i]:data_end[i], column]
            else:
                c = data[column][data_start[i]:data_end[i]]
            if overnight and i == 0:
                data_agg = np.insert(data_agg[-1], np.size(data_agg[-1][:, 0]),
                                     np.vstack((t, c)).T)
            else:
                data_agg.append(np.vstack((t, c)).T)

        day += 1
        if first_day:
            first_day = False
        if state_start_idx[-1]:
            overnight = True

    data_agg = np.vstack(data_agg)
    if units != "":
        return data_agg[:, 0]*u.day, data_agg[:, 1]*u(units)
    else:
        return data_agg[:, 0]*u.day, data_agg[:, 1]


def average_state(dates, state, column, units="", path="", extension=".xls"):
    """Outputs the average value of the data for each instance of a state in
    the given ProCoDA files

    Note: Column 0 is time. The first data column is column 1.

    :param dates: A single date or list of dates for which data was recorded, formatted "M-D-YYYY"
    :type dates: string or string list
    :param state: The state ID number for which data should be extracted
    :type state: int
    :param column: Index of the column that you want to extract OR header of the column that you want to extract
    :type column: int or string
    :param units: The units you want to apply to the data, e.g. 'mg/L'. Defaults to "" (dimensionless)
    :type units: string, optional
    :param path: The file path of the ProCoDA data file. If the file is in the working directory, then the file name is sufficient.
    :type path: string
    :param extension: The file extension of the tab delimited file. Defaults to ".xls" if no argument is passed in
    :type extension: string, optional

    :return: A list of averages for each instance of the given state
    :rtype: float list

    :Examples:

    .. code-block:: python

        data_avgs = average_state(["6-19-2013", "6-20-2013"], 1, 28, "mL/s")

    """
    data_agg = []
    day = 0
    first_day = True
    overnight = False

    if not isinstance(dates, list):
        dates = [dates]

    for d in dates:
        state_file = path + "statelog " + d + extension
        data_file = path + "datalog " + d + extension

        states = pd.read_csv(state_file, delimiter='\t')
        data = pd.read_csv(data_file, delimiter='\t')

        states = np.array(states)
        data = np.array(data)

        # get the start and end times for the state
        state_start_idx = states[:, 1] == state
        state_start = states[state_start_idx, 0]
        state_end_idx = np.append([False], state_start_idx[0:(np.size(state_start_idx)-1)])
        state_end = states[state_end_idx, 0]

        if overnight:
            state_start = np.insert(state_start, 0, 0)
            state_end = np.insert(state_end, 0, states[0, 0])

        if state_start_idx[-1]:
            state_end.append(data[0, -1])

        # get the corresponding indices in the data array
        data_start = []
        data_end = []
        for i in range(np.size(state_start)):
            add_start = True
            for j in range(np.size(data[:, 0])):
                if (data[j, 0] > state_start[i]) and add_start:
                    data_start.append(j)
                    add_start = False
                if (data[j, 0] > state_end[i]):
                    data_end.append(j-1)
                    break

        if first_day:
            start_time = data[1, 0]

        # extract data at those times
        for i in range(np.size(data_start)):
            if isinstance(column, int):
                c = data[data_start[i]:data_end[i], column]
            else:
                c = data[column][data_start[i]:data_end[i]]
            if overnight and i == 0:
                data_agg = np.insert(data_agg[-1], np.size(data_agg[-1][:]), c)
            else:
                data_agg.append(c)

        day += 1
        if first_day:
            first_day = False
        if state_start_idx[-1]:
            overnight = True

    averages = np.zeros(np.size(data_agg))
    for i in range(np.size(data_agg)):
        averages[i] = np.average(data_agg[i])

    if units != "":
        return averages*u(units)
    else:
        return averages


def perform_function_on_state(func, dates, state, column, units="", path="", extension=".xls"):
    """Performs the function given on each state of the data for the given state
    in the given column and outputs the result for each instance of the state

    Note: Column 0 is time. The first data column is column 1.

    :param func: A function that will be applied to data from each instance of the state
    :type func: function
    :param dates: A single date or list of dates for which data was recorded, formatted "M-D-YYYY"
    :type dates: string or string list
    :param state: The state ID number for which data should be extracted
    :type state: int
    :param column: Index of the column that you want to extract OR header of the column that you want to extract
    :type column: int or string
    :param units: The units you want to apply to the data, e.g. 'mg/L'. Defaults to "" (dimensionless)
    :type units: string, optional
    :param path: The file path of the ProCoDA data file. If the file is in the working directory, then the file name is sufficient.
    :type path: string
    :param extension: The file extension of the tab delimited file. Defaults to ".xls" if no argument is passed in
    :type extension: string, optional

    :requires: func takes in a list of data with units and outputs the correct units

    :return: The outputs of the given function for each instance of the given state
    :type: list

    :Examples:

    .. code-block:: python

        def avg_with_units(lst):
        num = np.size(lst)
        acc = 0
        for i in lst:
            acc = i + acc

        return acc / num

        data_avgs = perform_function_on_state(avg_with_units, ["6-19-2013", "6-20-2013"], 1, 28, "mL/s")
    """
    data_agg = []
    day = 0
    first_day = True
    overnight = False

    if not isinstance(dates, list):
        dates = [dates]

    for d in dates:
        state_file = path + "statelog " + d + extension
        data_file = path + "datalog " + d + extension

        states = pd.read_csv(state_file, delimiter='\t')
        data = pd.read_csv(data_file, delimiter='\t')

        states = np.array(states)
        data = np.array(data)

        # get the start and end times for the state
        state_start_idx = states[:, 1] == state
        state_start = states[state_start_idx, 0]
        state_end_idx = np.append([False], state_start_idx[0:(np.size(state_start_idx)-1)])
        state_end = states[state_end_idx, 0]

        if overnight:
            state_start = np.insert(state_start, 0, 0)
            state_end = np.insert(state_end, 0, states[0, 0])

        if state_start_idx[-1]:
            state_end.append(data[0, -1])

        # get the corresponding indices in the data array
        data_start = []
        data_end = []
        for i in range(np.size(state_start)):
            add_start = True
            for j in range(np.size(data[:, 0])):
                if (data[j, 0] > state_start[i]) and add_start:
                    data_start.append(j)
                    add_start = False
                if (data[j, 0] > state_end[i]):
                    data_end.append(j-1)
                    break

        if first_day:
            start_time = data[1, 0]

        # extract data at those times
        for i in range(np.size(data_start)):
            if isinstance(column, int):
                c = data[data_start[i]:data_end[i], column]
            else:
                c = data[column][data_start[i]:data_end[i]]
            if overnight and i == 0:
                data_agg = np.insert(data_agg[-1], np.size(data_agg[-1][:]), c)
            else:
                data_agg.append(c)

        day += 1
        if first_day:
            first_day = False
        if state_start_idx[-1]:
            overnight = True

    output = np.zeros(np.size(data_agg))
    for i in range(np.size(data_agg)):
        if units != "":
            output[i] = func(data_agg[i]*u(units)).magnitude
        else:
            output[i] = func(data_agg[i])

    if units != "":
        return output*func(data_agg[i]*u(units)).units
    else:
        return output


def read_state_with_metafile(func, state, column, path, metaids=[],
                             extension=".xls", units=""):
    """Takes in a ProCoDA meta file and performs a function for all data of a
    certain state in each of the experiments (denoted by file paths in then
    metafile)

    Note: Column 0 is time. The first data column is column 1.

    :param func: A function that will be applied to data from each instance of the state
    :type func: function
    :param state: The state ID number for which data should be extracted
    :type state: int
    :param column: Index of the column that you want to extract OR header of the column that you want to extract
    :type column: int or string
    :param path: The file path of the ProCoDA data file (must be tab-delimited)
    :type path: string
    :param metaids: a list of the experiment IDs you'd like to analyze from the metafile
    :type metaids: string list, optional
    :param extension: The file extension of the tab delimited file. Defaults to ".xls" if no argument is passed in
    :type extension: string, optional
    :param units: The units you want to apply to the data, e.g. 'mg/L'. Defaults to "" (dimensionless)
    :type units: string, optional

    :return: ids (string list) - The list of experiment ids given in the metafile
    :return: outputs (list) - The outputs of the given function for each experiment

    :Examples:

    .. code-block:: python

        def avg_with_units(lst):
            num = np.size(lst)
            acc = 0
            for i in lst:
                acc = i + acc

            return acc / num

        path = "../tests/data/Test Meta File.txt"
        ids, answer = read_state_with_metafile(avg_with_units, 1, 28, path, [], ".xls", "mg/L")
    """
    outputs = []

    metafile = pd.read_csv(path, delimiter='\t', header=None)
    metafile = np.array(metafile)

    ids = metafile[1:, 0]

    if not isinstance(ids[0], str):
        ids = list(map(str, ids))

    if metaids:
        paths = []
        for i in range(len(ids)):
            if ids[i] in metaids:
                paths.append(metafile[i, 4])
    else:
        paths = metafile[1:, 4]

    basepath = os.path.join(os.path.split(path)[0], metafile[0, 4])

    # use a loop to evaluate each experiment in the metafile
    for i in range(len(paths)):
        # get the range of dates for experiment i
        day1 = metafile[i+1, 1]

        # modify the metafile date so that it works with datetime format
        if not (day1[2] == "-" or day1[2] == "/"):
            day1 = "0" + day1
        if not (day1[5] == "-" or day1[5] == "/"):
            day1 = day1[:3] + "0" + day1[3:]

        if day1[2] == "-":
            dt = datetime.strptime(day1, "%m-%d-%Y")
        else:
            dt = datetime.strptime(day1, "%m/%d/%y")
        duration = metafile[i+1, 3]

        if not isinstance(duration, int):
            duration = int(duration)

        date_list = []
        for j in range(duration):
            curr_day = dt.strftime("%m-%d-%Y")
            if curr_day[3] == "0":
                curr_day = curr_day[:3] + curr_day[4:]
            if curr_day[0] == "0":
                curr_day = curr_day[1:]

            date_list.append(curr_day)

            dt = dt + timedelta(days=1)

        path = str(Path(os.path.join(basepath, paths[i]))) + os.sep
        _, data = read_state(date_list, state, column, units, path, extension)

        outputs.append(func(data))

    return ids, outputs


def write_calculations_to_csv(funcs, states, columns, path, headers, out_name,
                              metaids=[], extension=".xls"):
    """Writes each output of the given functions on the given states and data
    columns to a new column in the specified output file.

    Note: Column 0 is time. The first data column is column 1.

    :param funcs: A function or list of functions which will be applied in order to the data. If only one function is given it is applied to all the states/columns
    :type funcs: function or function list
    :param states: The state ID numbers for which data should be extracted. List should be in order of calculation or if only one state is given then it will be used for all the calculations
    :type states: string or string list
    :param columns: The index of a column, the header of a column, a list of indexes, OR a list of headers of the column(s) that you want to apply calculations to
    :type columns: int, string, int list, or string list
    :param path: Path to your ProCoDA metafile (must be tab-delimited)
    :type path: string
    :param headers: List of the desired header for each calculation, in order
    :type headers: string list
    :param out_name: Desired name for the output file. Can include a relative path
    :type out_name: string
    :param metaids: A list of the experiment IDs you'd like to analyze from the metafile
    :type metaids: string list, optional
    :param extension: The file extension of the tab delimited file. Defaults to ".xls" if no argument is passed in
    :type extension: string, optional

    :requires: funcs, states, columns, and headers are all of the same length if they are lists. Some being lists and some single values are okay.

    :return: out_name.csv (CVS file) - A CSV file with the each column being a new calcuation and each row being a new experiment on which the calcuations were performed
    :return: output (Pandas.DataFrame)- Pandas DataFrame holding the same data that was written to the output file
    """
    if not isinstance(funcs, list):
        funcs = [funcs] * len(headers)

    if not isinstance(states, list):
        states = [states] * len(headers)

    if not isinstance(columns, list):
        columns = [columns] * len(headers)

    data_agg = []
    for i in range(len(headers)):
        ids, data = read_state_with_metafile(funcs[i], states[i], columns[i],
                                             path, metaids, extension)
        data_agg = np.append(data_agg, [data])

    output = pd.DataFrame(data=np.vstack((ids, data_agg)).T,
                          columns=["ID"]+headers)
    output.to_csv(out_name, sep='\t')

    return output
