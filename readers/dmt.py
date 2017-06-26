"""
name:     dmt.py
python:   3.4
author:   Graeme Nott
email:    graeme.nott@faam.ac.uk
created:  Mar 2017

File with Droplet Measurement Technologies instrument data readers

Reader functions for Droplet Measurement Technologies instruments
that read raw particle image files and produce a spif.Spif() instance.

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


def DMT_lib(ver):
    """
    Reader library of universal functions for DMT probes

    Args:
        ver:       version of PADS files
    """

    print('DMT_lib')

    return


# ----------------------------------------------------------------------
def CIPgs_PADS2(fin,d=None):
    """
    Reader function for a DMT Cloud Imaging Probe - Grayscale
    PADS version 2.x

    Args:
        fin (str or pathlib.path object): Path/file of a raw data file.
        d (spif.Spif): If None [default] then create spif.Spif instance
            with data. If given then append/insert data into d

    """

    print('reader: CIPgs_PADS2')

    if d is None:
        # Create a bare-bones object if one has not been passed
        d = spif.Spif()

    return d


def CIPgs_PADS3(fin,d=None):
    """
    Reader function for a DMT Cloud Imaging Probe - Grayscale
    PADS version 3.x

    Args:
        fin (str or pathlib.path object): Path/file of a raw data file.
        d (spif.Spif): If None [default] then create spif.Spif instance
            with data. If given then append/insert data into d

    """

    print('reader: CIPgs_PADS3')

    if d is None:
        # Create a bare-bones object if one has not been passed
        d = spif.Spif()

    return d



def CIP_PADS2(fin,d=None):
    """
    Reader function for a DMT Cloud Imaging Probe - Monoscape
    PADS version 2.x

    Args:
        fin (str or pathlib.path object): Path/file of a raw data file.
        d (spif.Spif): If None [default] then create spif.Spif instance
            with data. If given then append/insert data into d

    """

    print('reader: CIP_PADS2')

    if d is None:
        # Create a bare-bones object if one has not been passed
        d = spif.Spif()

    return d


def CIP_PADS3(fin,d=None):
    """
    Reader function for a DMT Cloud Imaging Probe - Monoscape
    PADS version 3.x

    Args:
        fin (str or pathlib.path object): Path/file of a raw data file.
        d (spif.Spif): If None [default] then create spif.Spif instance
            with data. If given then append/insert data into d

    """

    print('reader: CIP_PADS3')

    if d is None:
        # Create a bare-bones object if one has not been passed
        d = spif.Spif()

    return d

