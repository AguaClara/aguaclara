"""
This module is intended to provide easy set up for an aide design playground/environment.

It imports all commonly used aide packages with one line, ensures Python is run in the correct
virtual environment, sets sig figs correctly and provides any additional environment
massaging to get to designing as quickly as possible. This should NOT be used by other
modules within aide_design as it results in unnecessary imports.
"""

def setup():
    """
    This is the public function that should be called to completely setup the aide environment
    in a jupyter notebook.
    :return:
    """


def imports():
    """
    imports all commonly used modules.
    :return:
    """
    import numpy as np


def set_sig_figs():
    """
    This should set the appropriate number of sigfigs to be displayed with pint, pandas and numpy,
    and any additional packages aide uses that are in charge of printing numbers
    """
    return 0


def ensure_in_a_virtual_environment():
    """
    Warn users if not in a virtual environment
    """
    import sys
    # way to test for virtual environment: https://stackoverflow.com/a/1883251/5136799
    if hasattr(sys, 'real_prefix'):
        raise UserWarning("aide_design should always be run in a virtual environment to ensure"
                          "that all dependencies are correctly installed. Please refer to the"
                          "readme for virtual environment setup instructions.")