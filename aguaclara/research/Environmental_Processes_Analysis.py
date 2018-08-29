from aguaclara.core.units import unit_registry as u
from scipy import special
from scipy.optimize import curve_fit
import collections
import pandas as pd
import numpy as np

# Carbonates
# The following code defines the carbonate system and provides functions for
# calculating Acid Neutralizing Capacity.
Kw = 10**(-14) * (u.mole/u.L)**2
K1_carbonate = 10**(-6.37)*u.mol/u.L
K2_carbonate = 10**(-10.25)*u.mol/u.L
K_Henry_CO2 = 10**(-1.5) * u.mole/(u.L*u.atm)
P_CO2 = 10**(-3.5) * u.atm


def invpH(pH):
    """This function calculates inverse pH

    Parameters
    ----------
    pH : float
        pH to be inverted

    Returns
    -------
    The inverse pH (in moles per liter) of the given pH

    Examples
    --------
    >>> invpH(8.25)
    5.623413251903491e-09 mole/liter
    >>> invpH(10)
    1e-10 mole/liter

    """
    return 10**(-pH)*u.mol/u.L


def alpha0_carbonate(pH):
    """This function calculates the fraction of total carbonates of the form
    H2CO3

    Parameters
    ----------
    pH : float
        pH of the system

    Returns
    -------
    fraction of CT in the form H2CO3

    Examples
    --------
    >>> alpha0_carbonate(8.25)
    0.01288388583402879 dimensionless
    >>> alpha0_carbonate(10)
    0.00015002337123256595 dimensionless

    """
    alpha0_carbonate = 1/(1+(K1_carbonate/invpH(pH)) *
                            (1+(K2_carbonate/invpH(pH))))
    return alpha0_carbonate


def alpha1_carbonate(pH):
    """This function calculates the fraction of total carbonates of the form
    HCO3-

    Parameters
    ----------
    pH : float
        pH of the system

    Returns
    -------
    fraction of CT in the form HCO3-

    Examples
    --------
    >>> alpha1_carbonate(8.25)
    0.9773426872930407 dimensionless
    >>> alpha1_carbonate(10)
    0.6399689750938067 dimensionless

    """
    alpha1_carbonate = 1/((invpH(pH)/K1_carbonate) + 1 +
                          (K2_carbonate/invpH(pH)))
    return alpha1_carbonate


def alpha2_carbonate(pH):
    """This function calculates the fraction of total carbonates of the form
    CO3-2

    Parameters
    ----------
    pH : float
        pH of the system

    Returns
    -------
    fraction of CT in the form CO3-2

    Examples
    --------
    >>> alpha2_carbonate(8.25)
    0.009773426872930407 dimensionless
    >>> alpha2_carbonate(10)
    0.35988100153496067 dimensionless

    """
    alpha2_carbonate = 1/(1+(invpH(pH)/K2_carbonate) *
                            (1+(invpH(pH)/K1_carbonate)))
    return alpha2_carbonate


def ANC_closed(pH, Total_Carbonates):
    """Acid neutralizing capacity (ANC) calculated under a closed system where
    there are no carbonates exchanged with the atmosphere during the
    experiment. Based on pH and total carbonates in the system.

    Parameters
    ----------
    pH : float
        pH of the system

    Total_Carbonates
        total carbonates in the system (mole/L)

    Returns
    -------
    The acid neutralizing capacity of the closed system (eq/L)

    Examples
    --------
    >>> ANC_closed(8.25, 1*u.mol/u.L)
    0.9968913136948984 equivalents/liter
    >>> ANC_closed(10, 1*u.mol/u.L)
    1.359830978063728 equivalents/liter

    """
    return (Total_Carbonates * (u.eq/u.mol * alpha1_carbonate(pH) +
            2 * u.eq/u.mol * alpha2_carbonate(pH)) +
            1 * u.eq/u.mol * Kw/invpH(pH) - 1 * u.eq/u.mol * invpH(pH))


def ANC_open(pH):
    """Acid neutralizing capacity (ANC) calculated under an open system, based
    on pH.

    Parameters
    ----------
    pH : float
        pH of the system

    Returns
    -------
    The acid neutralizing capacity of the closed system (eq/L)

    Examples
    --------
    >>> ANC_open(8.25)
    0.0007755217825265541 equivalents/liter
    >>> ANC_open(10)
    0.09073461016054905 equivalents/liter

    """
    return ANC_closed(pH, P_CO2*K_Henry_CO2/alpha0_carbonate(pH))


def aeration_data(DO_column, dirpath):
    """This function extracts the data from folder containing tab delimited
    files of aeration data. The file must be the original tab delimited file.
    All text strings below the header must be removed from these files.
    The file names must be the air flow rates with units of micromoles/s.
    An example file name would be "300.xls" where 300 is the flowr ate in
    micromoles/s. The function opens a file dialog for the user to select
    the directory containing the data.

    Parameters
    ----------
    DO_column : int
        index of the column that contains the dissolved oxygen concentration
        data.

    dirpath : string
        path to the directory containing aeration data you want to analyze

    Returns
    -------
    filepaths : string list
        all file paths in the directory sorted by flow rate

    airflows : numpy array
        sorted array of air flow rates with units of micromole/s attached

    DO_data : numpy array list
        sorted list of numpy arrays. Thus each of the numpy data arrays can
        have different lengths to accommodate short and long experiments

    time_data : numpy array list
        sorted list of numpy arrays containing the times with units of seconds

    Examples
    --------

    """
    #return the list of files in the directory
    filenames = os.listdir(dirpath)
    #extract the flowrates from the filenames and apply units
    airflows = ((np.array([i.split('.', 1)[0] for i in filenames])).astype(np.float32))
    #sort airflows and filenames so that they are in ascending order of flow rates
    idx = np.argsort(airflows)
    airflows = (np.array(airflows)[idx])*u.umole/u.s
    filenames = np.array(filenames)[idx]

    filepaths = [os.path.join(dirpath, i) for i in filenames]
    #DO_data is a list of numpy arrays. Thus each of the numpy data arrays can have different lengths to accommodate short and long experiments
    # cycle through all of the files and extract the column of data with oxygen concentrations and the times
    DO_data=[Column_of_data(i,0,-1,DO_column,'mg/L') for i in filepaths]
    time_data=[(ftime(i,0,-1)).to(u.s) for i in filepaths]
    aeration_collection = collections.namedtuple('aeration_results','filepaths airflows DO_data time_data')
    aeration_results = aeration_collection(filepaths, airflows, DO_data, time_data)
    return aeration_results


def O2_sat(P_air, temp):
    """This equation returns saturaed oxygen concentration in mg/L. It is valid
    for 278 K < T < 318 K

    Parameters
    ----------
    Pressure_air : float
        air pressure with appropriate units.
    Temperature :
        water temperature with appropriate units

    Returns
    -------
    Saturated oxygen concentration in mg/L

    Examples
    --------
    >>> O2_sat(1*u.atm , 300*u.kelvin)
    8.093157231428425 milligram/liter

    """
    fraction_O2 = 0.21
    P_O2 = P_air * fraction_O2
    return ((P_O2.to(u.atm).magnitude) *
            u.mg/u.L*np.exp(1727 / temp.to(u.K).magnitude - 2.105))


def Gran(data_file_path):
    """This function extracts the data from a ProCoDA Gran plot file.
    The file must be the original tab delimited file.

    Parameters
    ----------
    data_file_path : string
        File path. If the file is in the working directory, then the file name
        is sufficient.

    Returns
    -------
    V_titrant : float
        volume of titrant in mL

    ph_data : numpy array
        pH of the sample

    V_sample : float
        volume of the original sample that was titrated in mL

    Normality_titrant : float
        normality of the acid used to titrate the sample in mole/L

    V_equivalent : float
        volume of acid required to consume all of the ANC in mL

    ANC : float
        Acid Neutralizing Capacity of the sample in mole/L

    Examples
    --------

    """
    df = pd.read_csv(data_file_path, delimiter='\t', header=5)
    V_t = np.array(pd.to_numeric(df.iloc[0:, 0]))*u.mL
    pH = np.array(pd.to_numeric(df.iloc[0:, 1]))
    df = pd.read_csv(data_file_path, delimiter='\t', header=-1, nrows=5)
    V_S = pd.to_numeric(df.iloc[0, 1])*u.mL
    N_t = pd.to_numeric(df.iloc[1, 1])*u.mole/u.L
    V_eq = pd.to_numeric(df.iloc[2, 1])*u.mL
    ANC_sample = pd.to_numeric(df.iloc[3, 1])*u.mole/u.L
    Gran_collection = collections.namedtuple('Gran_results', 'V_titrant ph_data V_sample Normality_titrant V_equivalent ANC')
    Gran = Gran_collection(V_titrant=V_t, ph_data=pH, V_sample=V_S,
                           Normality_titrant=N_t, V_equivalent=V_eq,
                           ANC=ANC_sample)
    return Gran


# Reactors
# The following code is for reactor responses to tracer inputs.
def CMFR(t, C_initial, C_influent):
    """This function calculates the output concentration of a completely mixed
    flow reactor given an influent and initial concentration.

    Parameters
    ----------
    C_initial : float
        The concentration in the CMFR at time zero.

    C_influent : float
        The concentration entering the CMFR.

    t : float (array)
        time made dimensionless by dividing by the residence time of the CMFR.
        It can be a single value or a numpy array.

    Returns
    -------
    float
        Effluent concentration

    Examples
    --------
    >>> CMFR(0.1, 0*u.mg/u.L, 10*u.mg/u.L)
    0.9516258196404048 milligram/liter
    >>> CMFR(0.9, 5*u.mg/u.L, 10*u.mg/u.L)
    7.967151701297004 milligram/liter

    """
    return C_influent * (1-np.exp(-t)) + C_initial*np.exp(-t)


def E_CMFR_N(t, N):
    """This function calculates a dimensionless measure of the output tracer
    concentration from a spike input to a series of completely mixed flow
    reactors.

    Parameters
    ----------
    t : float (array)
        time made dimensionless by dividing by the reactor residence time.
        t can be a single value or a numpy array.

    N : float
        number of completely mixed flow reactors (CMFRS) in series.
        This would logically be constrained to real numbers greater than 1.

    Returns
    -------
    float
        dimensionless measure of the output tracer concentration
        (Concentration * volume of 1 CMFR) / (mass of tracer)

    Examples
    --------
    >>> E_CMFR_N(0.5, 3)
    0.7530642905009506
    >>> E_CMFR_N(0.1, 1)
    0.9048374180359595

    """
    return (N**N)/special.gamma(N) * (t**(N-1))*np.exp(-N*t)


def E_Advective_Dispersion(t, Pe):
    """This function calculates a dimensionless measure of the output tracer
    concentration from a spike input to reactor with advection and dispersion.
    Parameters
    ----------
    t : float (array)
        time made dimensionless by dividing by the reactor residence time.
        t can be a single value or a numpy array.

    Pe : float
        The ratio of advection to dispersion
        ((mean fluid velocity)/(Dispersion*flow path length))

    Returns
    -------
    float
        dimensionless measure of the output tracer concentration
        (Concentration * volume of reactor) / (mass of tracer)

    Examples
    --------
    >>> E_Advective_Dispersion(0.5, 5)
    0.47748641153355664

    """
    # replace any times at zero with a number VERY close to zero to avoid
    # divide by zero errors
    if isinstance(t, list):
        t[t == 0] = 10**(-50)
    return (Pe/(4*np.pi*t))**(0.5)*np.exp((-Pe*((1-t)**2))/(4*t))


def Tracer_CMFR_N(t_seconds, t_bar, C_bar, N):
    """Used by Solver_CMFR_N. All inputs and outputs are unitless. This is
    The model function, f(x, ...). It takes the independent variable as the
    first argument and the parameters to fit as separate remaining arguments.

    Parameters
    ----------
    t_seconds : float list
        Array of times

    t_bar : float
        Average time spent in the reactor

    C_bar : float
        Average concentration.
        (Mass of tracer)/(volume of the reactor)

    N : float
        number of completely mixed flow reactors (CMFRS) in series.
        This would logically be constrained to real numbers greater than 1.

    Returns
    -------
    float list
        The model concentration as a function of time

    Examples
    --------
    >>> Tracer_CMFR_N([1, 2, 3, 4, 5]*u.s, 5*u.s, 10*u.mg/u.L, 3)
    \\[\\begin{pmatrix}2.963582834907743 & 6.505794977303565 & 8.033525967569107 & 7.838031164205239 & 6.721254229661633\\end{pmatrix} milligram/liter\\]

    """
    return C_bar*E_CMFR_N(t_seconds/t_bar, N)


def Solver_CMFR_N(t_data, C_data, theta_guess, C_bar_guess):
    """Use non-linear least squares to fit the function
    Tracer_CMFR_N(t_seconds, t_bar, C_bar, N), to reactor data.

    Parameters
    ----------
    t_data : float list
        Array of times with units

    C_data : float list
        Array of tracer concentration data with units

    theta_guess : float
        Estimate of time spent in one CMFR with units.

    C_bar_guess : float
        Estimate of average concentration with units
        (Mass of tracer)/(volume of one CMFR)

    Returns
    -------
    tuple
        theta : float
            residence time in seconds

        C_bar : float
            average concentration with same units as C_bar_guess

        N : float
            number of CMFRS in series that best fit the data

    """
    C_unitless = C_data.magnitude
    C_units = str(C_bar_guess.units)
    t_seconds = (t_data.to(u.s)).magnitude
    # assume that a guess of 1 reactor in series is close enough to get a solution
    p0 = [theta_guess.to(u.s).magnitude, C_bar_guess.magnitude,1]
    popt, pcov = curve_fit(Tracer_CMFR_N, t_seconds, C_unitless, p0)
    Solver_theta = popt[0]*u.s
    Solver_C_bar = popt[1]*u(C_units)
    Solver_N = popt[2]
    Reactor_results = collections.namedtuple('Reactor_results','theta C_bar N')
    CMFR = Reactor_results(theta=Solver_theta, C_bar=Solver_C_bar, N=Solver_N)
    return CMFR


def Tracer_AD_Pe(t_seconds, t_bar, C_bar, Pe):
    """Used by Solver_AD_Pe. All inputs and outputs are unitless. This is the
    model function, f(x, ...). It takes the independent variable as the
    first argument and the parameters to fit as separate remaining arguments.

    Parameters
    ----------
    t_seconds : float list
        Array of times

    t_bar : float
        Average time spent in the reactor

    C_bar : float
        Average concentration.
        (Mass of tracer)/(volume of the reactor)

    Pe : float
        The Peclet number for the reactor.

    Returns
    -------
    float
        The model concentration as a function of time

    Examples
    --------
    >>> Tracer_AD_Pe([1, 2, 3, 4, 5]*u.s, 5*u.s, 10*u.mg/u.L, 5)
    \\[\\begin{pmatrix}0.2583373169261504 & 3.237939891647294 & 5.834983303390744 & 6.625088308600714 & 6.307831305050401\\end{pmatrix} milligram/liter\\]

    """
    return C_bar*E_Advective_Dispersion(t_seconds/t_bar, Pe)


def Solver_AD_Pe(t_data, C_data, theta_guess, C_bar_guess):
    """Use non-linear least squares to fit the function
    Tracer_AD_Pe(t_seconds, t_bar, C_bar, Pe) to reactor data.

    Parameters
    ----------
    t_data : float list
        Array of times with units

    C_data : float list
        Array of tracer concentration data with units

    theta_guess : float
        Estimate of time spent in one CMFR with units.

    C_bar_guess : float
        Estimate of average concentration with units
        (Mass of tracer)/(volume of one CMFR)

    Returns
    -------
    tuple
        theta : float
            residence time in seconds

        C_bar : float
            average concentration with same units as C_bar_guess

        Pe : float
            peclet number that best fits the data

    """

    C_unitless = C_data.magnitude
    C_units = str(C_bar_guess.units)
    t_seconds = (t_data.to(u.s)).magnitude
    # assume that a guess of 1 reactor in series is close enough to get a solution
    p0 = [theta_guess.to(u.s).magnitude, C_bar_guess.magnitude,5]
    popt, pcov = curve_fit(Tracer_AD_Pe, t_seconds, C_unitless, p0)
    Solver_theta = popt[0]*u.s
    Solver_C_bar = popt[1]*u(C_units)
    Solver_Pe = popt[2]
    Reactor_results = collections.namedtuple('Reactor_results', 'theta C_bar Pe')
    AD = Reactor_results(theta=Solver_theta, C_bar=Solver_C_bar, Pe=Solver_Pe)
    return AD
