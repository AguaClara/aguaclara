from aguaclara.research.procoda_parser import *
from aguaclara.core.units import u
import aguaclara.core.utility as ut
import pandas as pd
import numpy as np
from scipy import special
from scipy.optimize import curve_fit
import collections


# Carbonates
# The following code defines the carbonate system and provides functions for
# calculating Acid Neutralizing Capacity.
Kw = 10**(-14) * (u.mole/u.L)**2
K1_carbonate = 10**(-6.37)*u.mol/u.L
K2_carbonate = 10**(-10.25)*u.mol/u.L
K_Henry_CO2 = 10**(-1.5) * u.mole/(u.L*u.atm)
P_CO2 = 10**(-3.5) * u.atm


@ut.list_handler()
def invpH(pH):
    """Calculate inverse pH, i.e. hydronium ion concentration, given pH.

    :param pH: pH to be inverted
    :type pH: float

    :return: The inverse pH or hydronium ion concentration (in moles per liter)
    :rtype: float

    :Examples:

    >>> from aguaclara.research.environmental_processes_analysis import invpH
    >>> invpH(10)
    <Quantity(1e-10, 'mole / liter')>
    """
    return 10**(-pH)*u.mol/u.L


@ut.list_handler()
def alpha0_carbonate(pH):
    """Calculate the fraction of total carbonates in carbonic acid form (H2CO3)

    :param pH: pH of the system
    :type pH: float

    :return: Fraction of carbonates in carbonic acid form (H2CO3)
    :rtype: float

    :Examples:

    >>> from aguaclara.research.environmental_processes_analysis import alpha0_carbonate
    >>> round(alpha0_carbonate(10), 7)
    <Quantity(0.00015, 'dimensionless')>
    """
    alpha0_carbonate = 1/(1+(K1_carbonate/invpH(pH)) *
                            (1+(K2_carbonate/invpH(pH))))
    return alpha0_carbonate


@ut.list_handler()
def alpha1_carbonate(pH):
    """Calculate the fraction of total carbonates in bicarbonate form (HCO3-)

    :param pH: pH of the system
    :type pH: float

    :return: Fraction of carbonates in bicarbonate form (HCO3-)
    :rtype: float

    :Examples:

    >>> from aguaclara.research.environmental_processes_analysis import alpha1_carbonate
    >>> round(alpha1_carbonate(10), 7)
    <Quantity(0.639969, 'dimensionless')>
    """
    alpha1_carbonate = 1/((invpH(pH)/K1_carbonate) + 1 +
                          (K2_carbonate/invpH(pH)))
    return alpha1_carbonate


@ut.list_handler()
def alpha2_carbonate(pH):
    """Calculate the fraction of total carbonates in carbonate form (CO3-2)

    :param pH: pH of the system
    :type pH: float

    :return: Fraction of carbonates in carbonate form (CO3-2)
    :rtype: float

    :Examples:

    >>> from aguaclara.research.environmental_processes_analysis import alpha2_carbonate
    >>> round(alpha2_carbonate(10), 7)
    <Quantity(0.359881, 'dimensionless')>
    """
    alpha2_carbonate = 1/(1+(invpH(pH)/K2_carbonate) *
                            (1+(invpH(pH)/K1_carbonate)))
    return alpha2_carbonate


@ut.list_handler()
def ANC_closed(pH, total_carbonates):
    """Calculate the acid neutralizing capacity (ANC) under a closed system
    in which no carbonates are exchanged with the atmosphere during the
    experiment. Based on pH and total carbonates in the system.

    :param pH: pH of the system
    :type pH: float
    :param total_carbonates: Total carbonate concentration in the system (mole/L)
    :type total_carbonates: float

    :return: The acid neutralizing capacity of the closed system (eq/L)
    :rtype: float

    :Examples:

    >>> from aguaclara.research.environmental_processes_analysis import ANC_closed
    >>> from aguaclara.core.units import u
    >>> round(ANC_closed(10, 1*u.mol/u.L), 7)
    <Quantity(1.359831, 'equivalent / liter')>
    """
    return (total_carbonates * (u.eq/u.mol * alpha1_carbonate(pH) +
            2 * u.eq/u.mol * alpha2_carbonate(pH)) +
            1 * u.eq/u.mol * Kw/invpH(pH) - 1 * u.eq/u.mol * invpH(pH))


@ut.list_handler()
def ANC_open(pH):
    """Calculate the acid neutralizing capacity (ANC) calculated under an open
    system based on pH.

    :param pH: pH of the system
    :type pH: float

    :return: The acid neutralizing capacity of the closed system (eq/L)
    :rtype: float

    :Examples:

    >>> from aguaclara.research.environmental_processes_analysis import ANC_open
    >>> round(ANC_open(10), 7)
    <Quantity(0.0907346, 'equivalent / liter')>
    """
    return ANC_closed(pH, P_CO2*K_Henry_CO2/alpha0_carbonate(pH))


def aeration_data(DO_column, dirpath):
    """Extract the data from folder containing tab delimited
    files of aeration data. The file must be the original tab delimited file.
    All text strings below the header must be removed from these files.
    The file names must be the air flow rates with units of micromoles/s.
    An example file name would be "300.xls" where 300 is the flow rate in
    micromoles/s. The function opens a file dialog for the user to select
    the directory containing the data.

    :param DO_column: Index of the column that contains the dissolved oxygen concentration data.
    :type DO_columm: int
    :param dirpath: Path to the directory containing aeration data you want to analyze
    :type dirpath: string

    :return: collection of

        * **filepaths** (*string list*) - All file paths in the directory sorted by flow rate
        * **airflows** (*numpy.array*) - Sorted array of air flow rates with units of micromole/s
        * **DO_data** (*numpy.array list*) - Sorted list of Numpy arrays. Thus each of the numpy data arrays can have different lengths to accommodate short and long experiments
        * **time_data** (*numpy.array list*) - Sorted list of Numpy arrays containing the times with units of seconds
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
    DO_data=[column_of_data(i,0,DO_column,-1,'mg/L') for i in filepaths]
    time_data=[(column_of_time(i,0,-1)).to(u.s) for i in filepaths]
    aeration_collection = collections.namedtuple('aeration_results','filepaths airflows DO_data time_data')
    aeration_results = aeration_collection(filepaths, airflows, DO_data, time_data)
    return aeration_results


@ut.list_handler()
def O2_sat(P_air, temp):
    """Calculate saturaed oxygen concentration in mg/L for 278 K < T < 318 K

    :param P_air: Air pressure with appropriate units
    :type P_air: float
    :param temp: Water temperature with appropriate units
    :type temp: float

    :return: Saturated oxygen concentration in mg/L
    :rtype: float

    :Examples:

    >>> from aguaclara.research.environmental_processes_analysis import O2_sat
    >>> from aguaclara.core.units import u
    >>> round(O2_sat(1*u.atm , 300*u.kelvin), 7)
    <Quantity(8.0931572, 'milligram / liter')>
    """
    fraction_O2 = 0.21
    P_O2 = P_air * fraction_O2
    return ((P_O2.to(u.atm).magnitude) *
            u.mg/u.L*np.exp(1727 / temp.to(u.K).magnitude - 2.105))


def Gran(data_file_path):
    """Extract the data from a ProCoDA Gran plot file. The file must be the original tab delimited file.

    :param data_file_path: The path to the file. If the file is in the working directory, then the file name is sufficient.

    :return: collection of

        * **V_titrant** (*float*) - Volume of titrant in mL
        * **ph_data** (*numpy.array*) - pH of the sample
        * **V_sample** (*float*) - Volume of the original sample that was titrated in mL
        * **Normality_titrant** (*float*) - Normality of the acid used to titrate the sample in mole/L
        * **V_equivalent** (*float*) - Volume of acid required to consume all of the ANC in mL
        * **ANC** (*float*) - Acid Neutralizing Capacity of the sample in mole/L
    """
    df = pd.read_csv(data_file_path, delimiter='\t', header=5)
    V_t = np.array(pd.to_numeric(df.iloc[0:, 0]))*u.mL
    pH = np.array(pd.to_numeric(df.iloc[0:, 1]))
    df = pd.read_csv(data_file_path, delimiter='\t', header=None, nrows=5)
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
    """Calculate the effluent concentration of a conversative (non-reacting)
    material with continuous input to a completely mixed flow reactor.

    Note: time t=0 is the time at which the material starts to flow into the
    reactor.

    :param C_initial: The concentration in the CMFR at time t=0.
    :type C_initial: float
    :param C_influent: The concentration entering the CMFR.
    :type C_influent: float
    :param t: The time(s) at which to calculate the effluent concentration. Time can be made dimensionless by dividing by the residence time of the CMFR.
    :type t: float or numpy.array

    :return: Effluent concentration
    :rtype: float

    :Examples:

    >>> from aguaclara.research.environmental_processes_analysis import CMFR
    >>> from aguaclara.core.units import u
    >>> round(CMFR(0.1, 0*u.mg/u.L, 10*u.mg/u.L), 7)
    <Quantity(0.9516258, 'milligram / liter')>
    >>> round(CMFR(0.9, 5*u.mg/u.L, 10*u.mg/u.L), 7)
    <Quantity(7.9671517, 'milligram / liter')>
    """
    return C_influent * (1-np.exp(-t)) + C_initial*np.exp(-t)


def E_CMFR_N(t, N):
    """Calculate a dimensionless measure of the output tracer concentration
    from a spike input to a series of completely mixed flow reactors.

    :param t: The time(s) at which to calculate the effluent concentration. Time can be made dimensionless by dividing by the residence time of the CMFR.
    :type t: float or numpy.array
    :param N: The number of completely mixed flow reactors (CMFRS) in series. Must be greater than 1.
    :type N: int

    :return: Dimensionless measure of the output tracer concentration (concentration * volume of 1 CMFR) / (mass of tracer)
    :rtype: float

    :Examples:

    >>> from aguaclara.research.environmental_processes_analysis import E_CMFR_N
    >>> round(E_CMFR_N(0.5, 3), 7)
    0.7530643
    >>> round(E_CMFR_N(0.1, 1), 7)
    0.9048374
    """
    return (N**N)/special.gamma(N) * (t**(N-1))*np.exp(-N*t)


def E_Advective_Dispersion(t, Pe):
    """Calculate a dimensionless measure of the output tracer concentration from
    a spike input to reactor with advection and dispersion.

    :param t: The time(s) at which to calculate the effluent concentration. Time can be made dimensionless by dividing by the residence time of the CMFR.
    :type t: float or numpy.array
    :param Pe: The ratio of advection to dispersion ((mean fluid velocity)/(Dispersion*flow path length))
    :type Pe: float

    :return: dimensionless measure of the output tracer concentration (concentration * volume of reactor) / (mass of tracer)
    :rtype: float

    :Examples:

    >>> from aguaclara.research.environmental_processes_analysis import E_Advective_Dispersion
    >>> round(E_Advective_Dispersion(0.5, 5), 7)
    0.4774864
    """
    # replace any times at zero with a number VERY close to zero to avoid
    # divide by zero errors
    if isinstance(t, list):
        t[t == 0] = 10**(-10)
    return (Pe/(4*np.pi*t))**(0.5)*np.exp((-Pe*((1-t)**2))/(4*t))


def Tracer_CMFR_N(t_seconds, t_bar, C_bar, N):
    """Used by Solver_CMFR_N. All inputs and outputs are unitless. This is
    The model function, f(x, ...). It takes the independent variable as the
    first argument and the parameters to fit as separate remaining arguments.

    :param t_seconds: List of times
    :type t_seconds: float list
    :param t_bar: Average time spent in the reactor
    :type t_bar: float
    :param C_bar: Average concentration (mass of tracer)/(volume of the reactor)
    :type C_bar: float
    :param N: Number of completely mixed flow reactors (CMFRs) in series, must be greater than 1
    :type N: int

    :return: The model concentration as a function of time
    :rtype: float list

    :Examples:

    >>> from aguaclara.research.environmental_processes_analysis import Tracer_CMFR_N
    >>> from aguaclara.core.units import u
    >>> Tracer_CMFR_N([1, 2, 3, 4, 5]*u.s, 5*u.s, 10*u.mg/u.L, 3)
    <Quantity([2.96358283 6.50579498 8.03352597 7.83803116 6.72125423], 'milligram / liter')>
    """
    return C_bar*E_CMFR_N(t_seconds/t_bar, N)


def Solver_CMFR_N(t_data, C_data, theta_guess, C_bar_guess):
    """Use non-linear least squares to fit the function
    Tracer_CMFR_N(t_seconds, t_bar, C_bar, N) to reactor data.

    :param t_data: Array of times with units
    :type t_data: float list
    :param C_data: Array of tracer concentration data with units
    :type C_data: float list
    :param theta_guess: Estimate of time spent in one CMFR with units.
    :type theta_guess: float
    :param C_bar_guess: Estimate of average concentration with units ((mass of tracer)/(volume of one CMFR))
    :type C_bar_guess: float

    :return: tuple of

        * **theta** (*float*)- Residence time in seconds
        * **C_bar** (*float*) - Average concentration with same units as C_bar_guess
        * **N** (*float*)- Number of CMFRS in series that best fit the data
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

    :param t_seconds: List of times
    :type t_seconds: float list
    :param t_bar: Average time spent in the reactor
    :type t_bar: float
    :param C_bar: Average concentration ((mass of tracer)/(volume of the reactor))
    :type C_bar: float
    :param Pe: The Peclet number for the reactor.
    :type Pe: float

    :return: The model concentration as a function of time
    :rtype: float list

    :Examples:

    >>> from aguaclara.research.environmental_processes_analysis import Tracer_AD_Pe
    >>> from aguaclara.core.units import u
    >>> Tracer_AD_Pe([1, 2, 3, 4, 5]*u.s, 5*u.s, 10*u.mg/u.L, 5)
    <Quantity([0.25833732 3.23793989 5.8349833  6.62508831 6.30783131], 'milligram / liter')>

    """
    return C_bar*E_Advective_Dispersion(t_seconds/t_bar, Pe)


def Solver_AD_Pe(t_data, C_data, theta_guess, C_bar_guess):
    """Use non-linear least squares to fit the function
    Tracer_AD_Pe(t_seconds, t_bar, C_bar, Pe) to reactor data.

    :param t_data: Array of times with units
    :type t_data: float list
    :param C_data: Array of tracer concentration data with units
    :type C_data: float list
    :param theta_guess: Estimate of time spent in one CMFR with units.
    :type theta_guess: float
    :param C_bar_guess: Estimate of average concentration with units ((mass of tracer)/(volume of one CMFR))
    :type C_bar_guess: float

    :return: tuple of

        * **theta** (*float*)- Residence time in seconds
        * **C_bar** (*float*) - Average concentration with same units as C_bar_guess
        * **Pe** (*float*) - Peclet number that best fits the data
    """
    #remove time=0 data to eliminate divide by zero error
    t_data = t_data[1:-1]
    C_data = C_data[1:-1]
    C_unitless = C_data.magnitude
    C_units = str(C_bar_guess.units)
    t_seconds = (t_data.to(u.s)).magnitude
    # assume that a guess of 1 reactor in series is close enough to get a solution
    p0 = [theta_guess.to(u.s).magnitude, C_bar_guess.magnitude,5]
    popt, pcov = curve_fit(Tracer_AD_Pe, t_seconds, C_unitless, p0, bounds=(0.01,np.inf))
    Solver_theta = popt[0]*u.s
    Solver_C_bar = popt[1]*u(C_units)
    Solver_Pe = popt[2]
    Reactor_results = collections.namedtuple('Reactor_results', 'theta C_bar Pe')
    AD = Reactor_results(theta=Solver_theta, C_bar=Solver_C_bar, Pe=Solver_Pe)
    return AD
