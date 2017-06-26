
"""
name:     dummy.py
python:   3.4
author:   Graeme Nott
email:    graeme.nott@faam.ac.uk
created:  Mar 2017

Functions that act as dummy readers of different instruments. That is
they don't read actual data they produce a spif.Spif() instance of
artificial data.

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

# TODO(Graeme): Add paticle zero-time indicies for each particle, what about array dimension?


import numpy as np
import os.path

import spif

import pdb



def dummy_CIPgs(f_unused,d=None):
    """
    Define and return a spif object as would be returned from the actual
    CIP grayscale data reader function.

    Args:
        f_unused: Dummy variable so matches other reader functions
        d (spif.Spif): If None [default] then create spif.Spif instance
            with data. If given then append/insert data into d

    """

    if d is None:
        # Create a bare-bones object if one has not been passed
        d = spif.Spif()


    particle_s = [58079.082, 58080.01, 58080.092, 58081.022]
    particle_ns = [21,14,12,7]

    # Obtain path of called script to determine path to data file
    p = os.path.abspath(__file__)
    particle_file = os.path.join(os.path.dirname(p),'CIP15GS_ImageData.csv')

    # Load particle image data
    particle_image = np.genfromtxt(particle_file,
                                   delimiter=',',dtype=int)

    # Designate that this is the only data to be written to h5 file
    d.eod = True

    # Create a group for CIP GS and populate instrument attributes
    d.group('CIP_Grayscale1',
       {'instrument_long_name': 'Cloud Imaging Probe - Grayscale',
        'institution': 'Facility for Airborne Atmospheric Research (FAAM)',
        'reference': 'http://dropletmeasurement.com/products/airborne/CIP',
        'instrument_serial_number': '0302-02',
        'manufacturer': 'Droplet Measurement Technologies',
        'instrument_firmware': '0.0',
        'instrument_software': '3.9.0',
        'platform': 'FAAM BAe146',
        'comment': 'CIP15-1 was mounted starboard upper-outer canister'})

    # Create variables for CIP GS
    d.CIP_Grayscale1.dataset('pixels',
        np.arange(64, dtype=int),
        {'long_name': 'Vector of pixel numbers for CIP15',
             'comment': None})
    d.CIP_Grayscale1.dataset('resolution',
        15.,
        {'long_name': 'Physical resolution of array pixels',
         'units': 'micrometres',
         'ancillary_variables': 'resolution_err',
         'comment': "Manufacturer's nominal resolution only"})
    d.CIP_Grayscale1.dataset('resolution_err',
        None,
        {'long_name': 'Uncertainty of physical resolution of array pixels',
        'units': 'micrometres',
        'comment': 'Uncertainty unknown'})
    d.CIP_Grayscale1.dataset('arm_seperation',
         40.,
        {'long_name': 'Physical distance between probe arms',
        'units': 'millimetres',
        'ancillary_variables': 'arm_seperation_err',
        'comment': "Manufacturer's nominal separation only"})
    d.CIP_Grayscale1.dataset('arm_seperation_err',
        None,
        {'long_name':'Uncertainty of physical distance between probe arms',
        'units': 'millimetres',
        'comment': 'Uncertainty unknown'})
    d.CIP_Grayscale1.dataset('anti-shatter_tips',
        True,
        {'long_name': 'Use of antishatter- or Korolev-tips on probe arms',
        'comment': None})
    d.CIP_Grayscale1.dataset('bpp',
        2,
        {'long_name': 'Bits per pixel used in image data',
        'comment': None})
    d.CIP_Grayscale1.dataset('thresholds',
        np.array([0.25,0.5,0.75,1.],dtype=float),
        {'long_name': 'Threshold levels defined for each pixel value',
        'comment': None})
    d.CIP_Grayscale1.dataset('channels',
        1,
        {'long_name': 'Number of measurement channels of probe',
        'comment': None})

    # Create the core data group and populate
    d.CIP_Grayscale1.group('core')

    d.CIP_Grayscale1.core.dataset('particle_sec',
        np.asarray(particle_s, dtype=float),
        {'standard_name': 'time',
        'long_name': 'Particle arrival time in seconds',
        'timezone': 'UTC',
        'units': 'seconds since start_date 00:00:00',
        'strftime': '%F %T %Z',
        'ancillary_variables': 'particle_nsec',
        'comments': None})
    d.CIP_Grayscale1.core.dataset('particle_nsec',
        np.asarray(particle_ns, dtype=int),
        {'long_name': 'Fractional particle arrival time in nanoseconds',
        'timezone': 'UTC',
        'units': 'nanoseconds since particle_sec',
        'comments': 'Particle arrival time found with ' +\
                    'particle_sec + particle+nsec'})
    d.CIP_Grayscale1.core.dataset('particle_image',
        np.asarray(particle_image, dtype=int),
        {'long_name': 'Particle image array',
        '_FillValue': -9999.,
        'comment': None})

    # Create aux data group and populate
    d.CIP_Grayscale1.core.group('aux',
        {'Instrument': '0',
        'Instrument Type': 'CIP Grayscale',
        'Sample Time': '1 sec (1 Hz)',
        'Enabled': 'FALSE',
        'COM Port': '7',
        'Baud Rate': '57600',
        'Image Card #': '0'})
        # etc
    d.CIP_Grayscale1.core.aux.dataset('End Seconds',
        np.asarray([58078.792969,58079.792969,58080.792969,
                    58081.792969], dtype=float),
        {'standard_name': 'time',
        'timezone': 'UTC',
        'units': 'seconds since start_date 00:00:00',
        'strftime': '%F %T %Z',
        'comments': None})
    d.CIP_Grayscale1.core.aux.dataset('Diode 1 Voltage',
        np.asarray([1.65,1.725,1.65,1.725], dtype=float),
        {'_FillValue': -9999.,
        'comment': None})
    d.CIP_Grayscale1.core.aux.dataset('Diode 32 Voltage',
        np.asarray([1.95,1.875,2.025,1.875], dtype=float),
        {'_FillValue': -9999.,
        'comment': None})
    d.CIP_Grayscale1.core.aux.dataset('Diode 64 Voltage',
        np.asarray([1.425,1.425,1.425,1.5], dtype=float),
        {'_FillValue': -9999.,
        'comment': None})
    # etc

    return d

