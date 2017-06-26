"""
name:     spec.py
python:   3.4
author:   Graeme Nott
email:    graeme.nott@faam.ac.uk
created:  Mar 2017

File with SPEC Inc. instrument data readers.

Reader functions for SPEC Inc instruments that read raw particle
image files and produce a spif.Spif() instance.

Requirements, reserved keys, and writer behaviours:

- The 'ancillary_variables' key is used to link one dataset to another.
This is usually a dataset of errors/uncertainties of a dataset. The
value of this item should be the key of the linked dataset.
- None values will be converted to the _FillValue if this attribute has
been set for the dataset, numpy.nan for a dataset which has units (and
thus is assumed to be a number), or an empty string otherwise.

Notes:
Currently all h5 dtypes are handled automatically. Thus the dtype of a
dataset should be given explicitly in the numpy array.


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

    Args:
        fin (str or pathlib.path object): Path/file of a raw data file.
        d (spif.Spif): If None [default] then create spif.Spif instance
            with data. If given then append/insert data into d

    """

    print('reader: twoDS')

    if d is None:
        # Create a bare-bones object if one has not been passed
        d = spif.Spif()

    return d


def CPI(fin,d=None):
    """
    Reader function for a SPEC Cloud Particle Imager

    Args:
        fin (str or pathlib.path object): Path/file of a raw data file.
        d (spif.Spif): If None [default] then create spif.Spif instance
            with data. If given then append/insert data into d

    """

    print('reader: CPI')

    if d is None:
        # Create a bare-bones object if one has not been passed
        d = spif.Spif()

    return d


def HVPS(fin,d=None):
    """
    Reader function for a SPEC High Volume Precipitation Spectrometer

    Args:
        fin (str or pathlib.path object): Path/file of a raw data file.
        d (spif.Spif): If None [default] then create spif.Spif instance
            with data. If given then append/insert data into d

    """

    print('reader: HVPS')

    if d is None:
        # Create a bare-bones object if one has not been passed
        d = spif.Spif()

    return d

