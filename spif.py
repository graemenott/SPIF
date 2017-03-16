#! /usr/bin/env python3
"""
name:     spif.py
python:   3.4
author:   Graeme Nott
email:    graeme.nott@faam.ac.uk
created:  Mar 2017
modified: 

Program to create and read Single Particle Image Format (SPIF) files.

"""

import sys, os.path
import datetime, pytz

import numpy as np
import matplotlib
import h5py

import pdb

import readers

pdb.set_trace()

# Define default root attributes of SPIF file
default_root = {
    'title': 'SPIF-Single Particle Image Format',
    'institution': 'SPIF Working Group',
    'source': 'version 0.1',
    'references': '../docs/SPIF_definition.pdf',
    'history': datetime.datetime.now(tz=pytz.utc),
    # NOTE: pytz probably not the best way to include tz info. Fine for UTC.
    'comment': [datetime.datetime.now(tz=pytz.utc),
                'Initial implementation',''],
    'project': None,
    'start_date': None}


def dummy():
    """
    Function to create a dummy data dictionary for writing to a SPIF file for
    testing purposes.
    """
    
    fred = readers.dummy_CIPgs()

    pdb.set_trace()
    return readers.dummy_CIPgs()

def call(args):
    """
    Main function that can be called from other programs if spif is imported.

    """

    if args['dummy'] is True:
        data = dummy()

class read():
    """
    Shorthand function to allow user to read SPIF files with;
        spif.read(f)

    """

class write():
    """
    Shorthand function to allow user to write data into a SPIF file with;
        spif.write()
    
    _init_ to determine whether to write new file or append data to existing
    """

        

class test():
    """
    Shorthand function to allow user to test whether the input SPIF file meets
    definted standards for the format with;
        spif.write()

    """    

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
if __name__=='__main__':

    import argparse
    
    # Define commandline options
    usage = '%(prog)s filename [options]'
    version = 'ver: Mar 2017'
    description = 'Program to produce, read, and test Single Particle Image '+\
                  'Format (SPIF) files.\n {0}'.format(version)
    epilog = 'Usage examples.\n' +\
             'Create a SPIF file with default filename based on a single '+\
             'instrument raw data file ;\n' +\
             " $ python3 spif.py 'Imagefile_1CIP Grayscale_20170215114606'\n"+\
             'Create a SPIF file with a customised filename based on a ' +\
             ' single instrument raw data file ;\n' +\
             " $ python3 spif.py 'Imagefile_1CIP Grayscale_20170215114606' " +\
             '-o outputfile.spif\n' +\
             'Create a SPIF file with default filename based on all raw ' +\
             'data files from a single instrument ;' +\
             " $ python3 spif.py data_dir/ -i '1CIP Grayscale'\n" +\
             'Create a SPIF file with default filename based on all raw ' +\
             'data files from two different instruments ;' +\
             " $ python3 spif.py data_dir/ -i '1CIP Grayscale' 4CIP\n" +\
             'Read a SPIF file and return a pickle file;' +\
             " $ python3 spif.py file.spif -r -o file.pickle\n"

    parser = argparse.ArgumentParser(usage=usage,
                     formatter_class=argparse.RawDescriptionHelpFormatter,
                     description=description,
                     epilog=epilog)

    # Mandatory argument
    parser.add_argument('file',
                        nargs='+',
                        help='White-space delineated path/filename of ' +\
                        'input file/s. If path is the same for all '+\
                        'then only required once.')
    
    # Optional arguments
    parser.add_argument('-r', '--read', action='store_true',
                        dest='read', default=False,
                        help='Option to read in a SPIF file and output as ' +\
                        'a python object. May be used with a direct call ' +\
                        'to spif.read().')
    parser.add_argument('-w', '--write', action='store_true',
                        dest='write', default=None,
                        help='Option to write a SPIF file from raw data ' +\
                        'data files. Is the inverse of --read and the ' +\
                        'default. May be used with a direct call to ' +\
                        'spif.write().')
    parser.add_argument('-t', '--test', action='store_true',
                        dest='test', default=False,
                        help='Option to test an existing SPIF file. Result ' +\
                        'of test written to stdout if --output not given. ' +\
                        'May be used with a direct call to spif.test().')
    parser.add_argument('-i', '--instr', action='store',
                        nargs='+',
                        dest='instr', default=None,
                        help='White-space delineated list of instrument ' +\
                        'identifiers. If file is path only then all files ' +\
                        'associated with instrument/s will be read.')
    parser.add_argument('-o', '--output', action='store',
                        dest='outfile', default=None,
                        help='Explicitly give output path/filename. If not ' +\
                        'given then filename is based on that of input ' +\
                        'file/s.')
    parser.add_argument('-d', '--dummy', action='store_true',
                        dest='dummy', default=False,
                        help='Use dummy raw data dictionary to create SPIF ' +\
                        'output. Used for development only.')
    parser.add_argument('-v', '--version', action='version',
                        version=version,
                        help='Display program version number.')
    

    # Process arguments and convert to dictionary -----------------------------
    args_dict = vars(parser.parse_args())
    print()
    
    # Welcome splash
    print('\n-----------------------------------------------------')
    print('\t    Single Particle Image Format')
    print('-----------------------------------------------------\n')

    pdb.set_trace()
    call(args_dict)
    
    print('\nDone.\n')
    # EOF