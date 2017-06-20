"""
name:     spec.py
python:   3.4
author:   Graeme Nott
email:    graeme.nott@faam.ac.uk
created:  Mar 2017
modified: 

File with SPEC Inc. instrument data readers
"""

import numpy as np

import pdb


def SPEC_lib():
    """
    Reader library of universal functions for SPEC probes
    """

    print('SPEC_lib')

    return


# ----------------------------------------------------------------------
def twoDS(fin,d=None):
    """
    Reader function for a SPEC 2D Stereo probe
    """

    print('reader: twoDS')

    if d is None:
        # Create a bare-bones object if one has not been passed
        d = spif.Spif()

    return d


def CPI(fin,d=None):
    """
    Reader function for a SPEC Cloud Particle Imager
    """

    print('reader: CPI')

    if d is None:
        # Create a bare-bones object if one has not been passed
        d = spif.Spif()

    return d


def HVPS(fin,d=None):
    """
    Reader function for a SPEC High Volume Precipitation Spectrometer
    """

    print('reader: HVPS')

    if d is None:
        # Create a bare-bones object if one has not been passed
        d = spif.Spif()

    return d

