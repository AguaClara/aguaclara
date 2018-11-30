from aguaclara.core.units import unit_registry as u
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
from pathlib import Path


def get_data_by_time(path, columns, start_date, start_time="00:00", end_date=None, end_time="23:59"):
    """Extracts columns of data from a ProCoDA datalog based on starting and ending date(s) and times

    Note: currently only works for 1 or 2 days of data, i.e. end_date must be unspecified or one day after start_date

    Parameters
    ----------
    path : string
        The path to the folder containing your ProCoDA data files
    columns : int (list)
        A single index of a column or a list of indices of columns of data to extract
        Note: Column 0 is time. The first data column is column 1.
    start_date : string
        Starting date of data to extract, formatted 'M-D-YYYY'
    start_time: string, optional
        Starting time of data to extract, formatted 'HH:MM' (24-hour time)
    end_date : string, optional
        Ending date of data to extract, formatted 'M-D-YYYY'
    end_time: string, optional
        Ending time of data to extract, formatted 'HH:MM' (24-hour time)

    Return
    ------
    list (2D list)
        list :
            contains the single column of data to extract
        2D list:
            a list of lists containing the columns to extract, in order of the indices given in the columns variable

    Examples
    --------
    get_data_by_time(path='/Users/.../ProCoDA Data/', columns=4, start_date='6-14-2018', start_time='12:20',
        end_date='6-15-2018', end_time='10:50')
    get_data_by_time(path='/Users/.../ProCoDA Data/', columns=[0,4], start_date='6-14-2018', start_time='12:20',
         end_time='23:59')
    get_data_by_time(path='/Users/.../ProCoDA Data/', columns=[0,3,4], start_date='6-14-2018', end_date='6-18-2018')
    """

    # Locate and read data file(s)
    if path[-1] != '/':
        path += '/'
    paths = [path + "datalog " + start_date + '.xls']
    data = [remove_notes(pd.read_csv(paths[0], delimiter='\t'))]

    if end_date is not None:
        paths.append(path + "datalog " + end_date + ".xls")
        data.append(remove_notes(pd.read_csv(paths[1], delimiter='\t')))

    # Calculate start index
    time_column = pd.to_numeric(data[0].iloc[:, 0])
    interval = time_column[1]-time_column[0]
    start_idx = int(round((day_fraction(start_time) - time_column[0])/interval + .5)) #round up

    # Calculate end index
    time_column = pd.to_numeric(data[-1].iloc[:, 0])
    end_idx = int(round((day_fraction(end_time) - time_column[0])/interval + .5)) + 1 #round up

    # Get columns of interest
    if len(paths) == 1:
        if isinstance(columns, int):
            result = list(pd.to_numeric(data[0].iloc[start_idx:end_idx, columns]))
        else:
            result = []
            for c in columns:
                result.append(list(pd.to_numeric(data[0].iloc[start_idx:end_idx, c])))
    else:
        data[1].iloc[0, 0] = 0
        if isinstance(columns, int):
            result = list(pd.to_numeric(data[0].iloc[start_idx:, columns])) + \
                     list(pd.to_numeric(data[1].iloc[:end_idx, columns]) + (1 if columns == 0 else 0))
        else:
            result = []
            for c in columns:
                result.append(list(pd.to_numeric(data[0].iloc[start_idx:, c])) +
                              list(pd.to_numeric(data[1].iloc[:end_idx, c])+(1 if c == 0 else 0)))

    return result


def remove_notes(data):
    """Omits any rows containing text from a pandas.DataFrame object, except for headers

    Text is defined as characters of the alphabet. The resulting DataFrame should have only headers and numerical data.

    Parameters
    ----------
    data : pandas.DataFrame
        DataFrame object to remove text from

    Returns
    -------
    pandas.DataFrame
        DataFrame object with no text, except for headers
    """
    has_text = data.iloc[:, 0].astype(str).str.contains('(?!e-)[a-zA-Z]')
    text_rows = list(has_text.index[has_text])
    return data.drop(text_rows)


def day_fraction(time):
    """Converts a 24-hour time to a fraction of a day.

    For example, midnight corresponds to 0.0, and noon to 0.5.

    Parameters
    ----------
    time : string
        Time in the form of 'HH:MM' (24-hour time)

    Returns
    -------
    float
        A day fraction

    Examples
    --------
    >>> from aguaclara.research.procoda_parser import day_fraction
    >>> day_fraction("00:21")
    0.014583333333333334
    >>> day_fraction("18:30")
    0.7708333333333334
    """
    hour = int(time.split(":")[0])
    minute = int(time.split(":")[1])
    return hour/24 + minute/1440


def get_data_by_state(path, dates, state, column):
    """Reads a ProCoDA file and extracts the time and data column for each iteration of
    the given state.

    Parameters
    ----------
    dates : string (list)
        A list of dates or single date for which data was recorded, in
        the form "M-D-YYYY"
    state : int
        The state ID number for which data should be plotted
    column : int or string
        int:
            Index of the column that you want to extract. Column 0 is time.
            The first data column is column 1.
        string:
            Name of the column header that you want to extract
    path : string, optional
        Optional argument of the path to the folder containing your ProCoDA
        files. Defaults to the current directory if no argument is passed in
    extension : string, optional
        The file extension of the tab delimited file. Defaults to ".xls" if
        no argument is passed in

    Returns
    -------
    3-D list
        A list of lists of the time and data columns extracted for each iteration of the state.
         For example, if "data" is the output, data[i][:,0] gives the time column and data[i][:,1]
         gives the data column for the ith iteration of the given state and column. data[i][0]
         would give the first [time, data] pair.

    Examples
    --------
    get_data_by_state(["6-19-2013", "6-20-2013"], 1, 28)
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


def column_of_time(data_file_path, start, end=-1):
    """This function extracts the column of times from a ProCoDA data file.

    Parameters
    ----------
    data_file_path : string
        File path. If the file is in the working directory, then the file name
        is sufficient.

    start : int or float
        Index of first row of data to extract from the data file

    end : int or float, optional
        Index of last row of data to extract from the data
        Defaults to -1, which extracts all the data in the file

    Returns
    -------
    numpy array
        Experimental times starting at 0 day with units of days.

    Examples
    --------
    ftime(Reactor_data.txt, 0)

    """
    if not isinstance(start, int):
        start = int(start)
    if not isinstance(end, int):
        end = int(end)

    df = pd.read_csv(data_file_path, delimiter='\t')
    start_time = pd.to_numeric(df.iloc[start, 0])*u.day
    day_times = pd.to_numeric(df.iloc[start:end, 0])
    time_data = np.subtract((np.array(day_times)*u.day), start_time)
    return time_data


def column_of_data(data_file_path, start, column, end="-1", units=""):
    """This function extracts a column of data from a ProCoDA data file.

    Parameters
    ----------
    data_file_path : string
        File path. If the file is in the working directory, then the file name
        is sufficient.

    start : int
        Index of first row of data to extract from the data file

    end : int, optional
        Index of last row of data to extract from the data
        Defaults to -1, which extracts all the data in the file

    column : int or string
        int:
            Index of the column that you want to extract. Column 0 is time.
            The first data column is column 1.
        string:
            Name of the column header that you want to extract

    units : string, optional
        The units you want to apply to the data, e.g. 'mg/L'.
        Defaults to "" which indicates no units

    Returns
    -------
    numpy array
        Experimental data with the units applied.

    Examples
    --------
    column_of_data(Reactor_data.txt, 0, 1, -1, "mg/L")

    """
    if not isinstance(start, int):
        start = int(start)
    if not isinstance(end, int):
        end = int(end)

    df = pd.read_csv(data_file_path, delimiter='\t')
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


def notes(data_file_path):
    """This function extracts any experimental notes from a ProCoDA data file.

    Parameters
    ----------
    data_file_path : string
        File path. If the file is in the working directory, then the file name
        is sufficient.

    Returns
    -------
    dataframe
        The rows of the data file that contain text notes inserted during the
        experiment. Use this to identify the section of the data file that you
        want to extract.

    Examples
    --------

    """
    df = pd.read_csv(data_file_path, delimiter='\t')
    text_row = df.iloc[0:-1, 0].str.contains('[a-z]', '[A-Z]')
    text_row_index = text_row.index[text_row].tolist()
    notes = df.loc[text_row_index]
    return notes


def read_state(dates, state, column, units="", path="", extension=".xls"):
    """Reads a ProCoDA file and outputs the data column and time vector for
    each iteration of the given state.

    Parameters
    ----------
    dates : string (list)
        A list of dates or single date for which data was recorded, in
        the form "M-D-Y"

    state : int
        The state ID number for which data should be extracted

    column : int or string
        int:
            Index of the column that you want to extract. Column 0 is time.
            The first data column is column 1.
        string:
            Name of the column header that you want to extract

    units : string, optional
        The units you want to apply to the data, e.g. 'mg/L'.
        Defaults to "" which indicates no units

    path : string, optional
        Optional argument of the path to the folder containing your ProCoDA
        files. Defaults to the current directory if no argument is passed in

    extension : string, optional
        The file extension of the tab delimited file. Defaults to ".xls" if
        no argument is passed in

    Returns
    -------
    time : numpy array
        Times corresponding to the data (with units)

    data : numpy array
        Data in the given column during the given state with units

    Examples
    --------
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

    Parameters
    ----------
    dates : string (list)
        A list of dates or single date for which data was recorded, in
        the form "M-D-Y"

    state : int
        The state ID number for which data should be extracted

    column : int or string
        int:
            Index of the column that you want to extract. Column 0 is time.
            The first data column is column 1.
        string:
            Name of the column header that you want to extract

    units : string, optional
        The units you want to apply to the data, e.g. 'mg/L'.
        Defaults to "" which indicates no units

    path : string, optional
        Optional argument of the path to the folder containing your ProCoDA
        files. Defaults to the current directory if no argument is passed in

    extension : string, optional
        The file extension of the tab delimited file. Defaults to ".xls" if
        no argument is passed in

    Returns
    -------
    float list
        A list of averages for each instance of the given state

    Examples
    --------
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

    Parameters
    ----------
    func : function
        A function which will be applied to data from each instance of the state

    dates : string (list)
        A list of dates or single date for which data was recorded, in
        the form "M-D-Y"

    state : int
        The state ID number for which data should be extracted

    column : int or string
        int:
            Index of the column that you want to extract. Column 0 is time.
            The first data column is column 1.
        string:
            Name of the column header that you want to extract

    units : string, optional
        The units you want to apply to the data, e.g. 'mg/L'.
        Defaults to "" which indicates no units

    path : string, optional
        Optional argument of the path to the folder containing your ProCoDA
        files. Defaults to the current directory if no argument is passed in

    extension : string, optional
        The file extension of the tab delimited file. Defaults to ".xls" if
        no argument is passed in

    Returns
    -------
    list
        The outputs of the given function for each instance of the given state

    Requires
    --------
    func takes in a list of data with units and outputs the correct units

    Examples
    --------
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

    Parameters
    ----------
    func : function
        A function which will be applied to data from each instance of the state

    state : int
        The state ID number for which data should be extracted

    column : int or string
        int:
            Index of the column that you want to extract. Column 0 is time.
            The first data column is column 1.
        string:
            Name of the column header that you want to extract

    path : string
        Path to your ProCoDA metafile (must be tab-delimited)

    metaids : string list, optional
        a list of the experiment IDs you'd like to analyze from the metafile

    extension : string, optional
        The file extension of the tab delimited file. Defaults to ".xls" if
        no argument is passed in

    units : string, optional
        The units you want to apply to the data, e.g. 'mg/L'.
        Defaults to "" which indicates no units

    Returns
    -------
    ids : string list
        The list of experiment ids given in the metafile

    outputs : list
        The outputs of the given function for each experiment

    Examples
    --------
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
    columns to a new column in a

    Parameters
    ----------
    funcs : function (list)
        A function or list of functions which will be applied in order to the
        data. If only one function is given it is applied to all the
        states/columns

    states : string (list)
        The state ID numbers for which data should be extracted. List should be
        in order of calculation or if only one state is given then it will be
        used for all the calculations

    columns : int or string (list)
        If only one column is given it is used for all the calculations
            int:
                Index of the column that you want to extract. Column 0 is time.
                The first data column is column 1.
            string:
                Name of the column header that you want to extract

    path : string
        Path to your ProCoDA metafile (must be tab-delimited)

    headers : string list
        List of the desired header for each calculation, in order

    out_name : string
        Desired name for the output file. Can include a relative path

    metaids : string list, optional
        a list of the experiment IDs you'd like to analyze from the metafile

    extension : string, optional
        The file extension of the tab delimited file. Defaults to ".xls" if
        no argument is passed in

    Returns
    -------
    out_name.csv
        A CSV file with the each column being a new calcuation and each row
        being a new experiment on which the calcuations were performed

    output : DataFrame
        Pandas dataframe which is the same data that was written to CSV

    Requires
    --------
    funcs, states, columns, and headers are all of the same length if they are
    lists. Some being lists and some single values are okay.

    Examples
    --------


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
