
"""
name:     dummy.py
python:   3.4
author:   Graeme Nott
email:    graeme.nott@faam.ac.uk
created:  Mar 2017
modified:

Functions that act as dummy readers of different instruments. That is they
don't read actual data they produce a dictionary of artificial data to pass to
spif.py

notes:
All scalar strings will be stored with np.string_()
All lists of strings will be stored with dtype='Sn' where n is the max length of the strings in the list
"""
import numpy as np
import os.path

import pdb

def dummy_CIPgs():
    """
    Define and return a dictionary as would be returned from the actual
    CIP grayscale data reader function.
    """

    particle_s = [58079.082, 58080.01, 58080.092, 58081.022]
    particle_ns = [21,14,12,7]

    # Obtain path of called script to determine path to data file
    p = os.path.abspath(__file__)
    particle_file = os.path.join(os.path.dirname(p),'CIP15GS_ImageData.csv')

    # Load particle image data
    particle_image = np.genfromtxt(particle_file,
                                   delimiter=',',dtype=int)


    # Define an example instrument group for DMT CIP15 grayscale data
    # Create top-level dictionary for the CIP
    d = {'1CIP Grayscale': {}}

    # Create root attributes for this instrument group
    d['1CIP Grayscale'] = {
        'instrument_long_name': 'Cloud Imaging Probe - Grayscale',
        'institution': 'Facility for Airborne Atmospheric Research (FAAM)',
        'reference': 'http://dropletmeasurement.com/products/airborne/CIP',
        'instrument_serial_number': '0302-02',
        'manufacturer': 'Droplet Measurement Technologies',
        'instrument_firmware': '0.0',
        'instrument_software': '3.9.0',
        'platform': 'FAAM BAe146',
        'comment': 'CIP15-1 was mounted starboard upper-outer canister',
        # Create root attributes for instrument metadata
        'pixels': {
            'value': np.arange(64, dtype=int),
            'long_name': 'Vector of pixel numbers for CIP15',
            'comment': None},
        'resolution': {
            'value': 15.,
            'long_name': 'Physical resolution of array pixels',
            'units': 'micrometres',
            'ancillary_variables': 'resolution_err',
            'comment': "Manufacturer's nominal resolution only"},
        'resolution_err': {
            'value': None,
            'long_name': 'Uncertainty of physical resolution of array pixels',
            'units': 'micrometres',
            'comment': 'Uncertainty unknown'},
        'arm_seperation': {
            'value': 40.,
            'long_name': 'Physical distance between probe arms',
            'units': 'millimetres',
            'ancillary_variables': 'arm_seperation_err',
            'comment': "Manufacturer's nominal separation only"},
        'arm_seperation_err': {
            'value': None,
            'long_name': 'Uncertainty of physical distance between probe arms',
            'units': 'millimetres',
            'comment': 'Uncertainty unknown'},
        'anti-shatter_tips': {
            'value': True,
            'long_name': 'Use of antishatter- or Korolev-tips on probe arms',
            'comment': None},
        'bpp': {
            'value': 2,
            'long_name': 'Bits per pixel used in image data',
            'comment': None},
        'thresholds': {
            'value': np.array([0.25,0.5,0.75,1.],dtype=float),
            'long_name': 'Threshold levels defined for each pixel value',
            'comment': None},
        'channels': {
            'value': 1,
            'long_name': 'Number of measurement changes of probe',
            'comment': None}}

    # Define the core sub-dictionary for storing of 2D image data
    d['1CIP Grayscale']['core'] = {
        'particle_sec': {
            'value': np.asarray(particle_s, dtype=float),
            'standard_name': 'time',
            'long_name': 'Particle arrival time in seconds',
            'timezone': 'UTC',
            'units': 'seconds since start_date 00:00:00',
            'strftime': '%F %T %Z',
            'ancillary_variables': 'particle_nsec',
            'comments': None},
        'particle_nsec': {
            'value': np.asarray(particle_ns, dtype=int),
            'long_name': 'Fractional particle arrival time in nanoseconds',
            'timezone': 'UTC',
            'units': 'nanoseconds since particle_sec',
            'comments': 'Particle arrival time found with ' +\
                        'particle_sec + particle+nsec'},
        'particle_image': {
            'value': np.asarray(particle_image, dtype=int),
            'long_name': 'Particle image array',
            '_FillValue': -9999.,
            'comment': None}}

    d['1CIP Grayscale']['aux'] = {
        # Metadata entries from PADS 1D data
        'Instrument': '0',
        'Instrument Type': 'CIP Grayscale',
        'Sample Time': '1 sec (1 Hz)',
        'Enabled': 'FALSE',
        'COM Port': '7',
        'Baud Rate': '57600',
        'Image Card #': '0',
        # etc
        'End Seconds': {
            'value': np.asarray([58078.792969,58079.792969,58080.792969,
                                58081.792969], dtype=float),
            'standard_name': 'time',
            'timezone': 'UTC',
            'units': 'seconds since start_date 00:00:00',
            'strftime': '%F %T %Z',
            'comments': None},
        'Diode 1 Voltage': {
            'value': np.asarray([1.65,1.725,1.65,1.725], dtype=float),
            '_FillValue': -9999.,
            'comment': None},
        'Diode 32 Voltage': {
            'value': np.asarray([1.95,1.875,2.025,1.875], dtype=float),
            '_FillValue': -9999.,
            'comment': None},
        'Diode 64 Voltage': {
            'value': np.asarray([1.425,1.425,1.425,1.5], dtype=float),
            '_FillValue': -9999.,
            'comment': None}}
        # etc

    # Indicate to spif.py that there is no more information to come.
    d['1CIP Grayscale']['EOF'] = True

    return d

