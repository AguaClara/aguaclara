from aguaclara.core.units import u
import aguaclara.core.utility as ut
import numpy as np
import pandas as pd
import os

# pump rotor radius based on minimizing error between predicted and measured
# values
R_pump = 1.62 * u.cm
# empirically derived correction factor due to the fact that larger diameter
# tubing has more loss due to space smashed by rollers
k_nonlinear = 13


@ut.list_handler()
def vol_per_rev_3_stop(color="", inner_diameter=0):
    """Return the volume per revolution of an Ismatec 6 roller pump
    given the inner diameter (ID) of 3-stop tubing. The calculation is
    interpolated from the table found at
    http://www.ismatec.com/int_e/pumps/t_mini_s_ms_ca/tubing_msca2.htm.

    Note:
    1. Either input a string as the tubing color code or a number as the
    tubing inner diameter. If both are given, the function will default to using
    the color.
    2. The calculation is interpolated for inner diameters between 0.13 and 3.17
    mm. Accuracy is not guaranteed for tubes with smaller or larger diameters.

    :param color: Color code of the Ismatec 3-stop tubing
    :type color: string
    :param inner_diameter: Inner diameter of the Ismatec 3-stop tubing. Results will be most accurate for inner diameters between 0.13 and 3.17 mm.
    :type inner_diameter: float

    :return: Volume per revolution output by a 6-roller pump through the 3-stop tubing (mL/rev)
    :rtype: float

    :Examples:

    >>> from aguaclara.research.peristaltic_pump import vol_per_rev_3_stop
    >>> from aguaclara.core.units import u
    >>> round(vol_per_rev_3_stop(color="yellow-blue"), 6)
    <Quantity(0.148846, 'milliliter / rev')>
    >>> round(vol_per_rev_3_stop(inner_diameter=.20*u.mm), 6)
    <Quantity(0.003116, 'milliliter / rev')>
    """
    if color != "":
        inner_diameter = ID_colored_tube(color)
    term1 = (R_pump * 2 * np.pi - k_nonlinear * inner_diameter) / u.rev
    term2 = np.pi * (inner_diameter ** 2) / 4
    return (term1 * term2).to(u.mL/u.rev)


@ut.list_handler()
def ID_colored_tube(color):
    """Look up the inner diameter of Ismatec 3-stop tubing given its color code.

    :param color: Color of the 3-stop tubing
    :type color: string

    :returns: Inner diameter of the 3-stop tubing (mm)
    :rtype: float

    :Examples:

    >>> from aguaclara.research.peristaltic_pump import ID_colored_tube
    >>> from aguaclara.core.units import u
    >>> ID_colored_tube("yellow-blue")
    <Quantity(1.52, 'millimeter')>
    >>> ID_colored_tube("orange-yellow")
    <Quantity(0.51, 'millimeter')>
    >>> ID_colored_tube("purple-white")
    <Quantity(2.79, 'millimeter')>
    """
    tubing_data_path = os.path.join(os.path.dirname(__file__), "data",
        "3_stop_tubing.txt")
    df = pd.read_csv(tubing_data_path, delimiter='\t')
    idx = df["Color"] == color
    return df[idx]['Diameter (mm)'].values[0] * u.mm


@ut.list_handler()
def vol_per_rev_LS(id_number):
    """Look up the volume per revolution output by a Masterflex L/S pump
    through L/S tubing of the given ID number.

    :param id_number: Identification number of the L/S tubing. Valid numbers are 13-18, 24, 35, and 36.
    :type id_number: int

    :return: Volume per revolution output by a Masterflex L/S pump through the L/S tubing
    :rtype: float

    :Examples:

    >>> from aguaclara.research.peristaltic_pump import vol_per_rev_LS
    >>> from aguaclara.core.units import u
    >>> vol_per_rev_LS(13)
    <Quantity(0.06, 'milliliter / turn')>
    >>> vol_per_rev_LS(18)
    <Quantity(3.8, 'milliliter / turn')>
    """
    tubing_data_path = os.path.join(os.path.dirname(__file__), "data",
        "LS_tubing.txt")
    df = pd.read_csv(tubing_data_path, delimiter='\t')
    idx = df["Number"] == id_number
    return df[idx]['Flow (mL/rev)'].values[0] * u.mL/u.turn


@ut.list_handler()
def flow_rate(vol_per_rev, rpm):
    """Return the flow rate from a pump given the volume of fluid pumped per
    revolution and the desired pump speed.

    :param vol_per_rev: Volume of fluid output per revolution (dependent on pump and tubing)
    :type vol_per_rev: float
    :param rpm: Desired pump speed in revolutions per minute
    :type rpm: float

    :return: Flow rate of the pump (mL/s)
    :rtype: float

    :Examples:

    >>> from aguaclara.research.peristaltic_pump import flow_rate
    >>> from aguaclara.core.units import u
    >>> flow_rate(3*u.mL/u.rev, 5*u.rev/u.min)
    <Quantity(0.25, 'milliliter / second')>
    """
    return (vol_per_rev * rpm).to(u.mL/u.s)
