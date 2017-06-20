"""
name:     dmt.py
python:   3.4
author:   Graeme Nott
email:    graeme.nott@faam.ac.uk
created:  Mar 2017

File with Droplet Measurement Technologies instrument data readers
"""

import numpy as np

import pdb


def DMT_lib():
    """
    Reader library of universal functions for DMT probes

    Input args:
        ver:       version of PADS files
    """

    print('DMT_lib')

    return


# ----------------------------------------------------------------------
def CIPgs_PADS2(fin,d=None):
    """
    Reader function for a DMT Cloud Imaging Probe - Grayscale
    PADS version 2.x

    Input args:

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

    Input args:

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

    Input args:

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

    Input args:

    """

    print('reader: CIP_PADS3')

    if d is None:
        # Create a bare-bones object if one has not been passed
        d = spif.Spif()

    return d

