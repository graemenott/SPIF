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

import readers

import pdb

# Define default root attributes of SPIF file
default_root = {
    'title': 'SPIF-Single Particle Image Format',
    'institution': 'SPIF Working Group',
    'source': 'version 0.1',
    'references': '../docs/SPIF_definition.pdf',
    'history': datetime.datetime.now(tz=pytz.utc),
    # NOTE: pytz probably not the best way to include tz info.
    # Fine for UTC.
    'comment': [datetime.datetime.now(tz=pytz.utc),
                'Initial implementation',''],
    'project': None,
    'start_date': None}



# ----------------------------------------------------------------------
class Read():
    """

    """

# ----------------------------------------------------------------------
class Write():
    """
    Class to create and write to a SPIF file.
    """

    def __init__(self,fin=[],fout=None,dummy=False):

        if len(fin) == 0:
            return None




class Append(Write):
        """
        Sub-class of Write that appends data into an existing SPIF file.
        Additional metadata etc is not required.
        """

        def __str__(self):

            return 'Write.Append() not yet implemented.'


class Create(Write):
        """
        Sub-class of Write that creates a SPIF file and writes data into
        that file. All required metadata must also be supplied.

        """

        def __init__(self,fin=[],fout=None,dummy=False):

            Write.__init__(self,fin,fout,dummy)

        def read_fin(self,fin):
            # Function to open and read raw data file

# ----------------------------------------------------------------------
class Test():
    """

    """

# ----------------------------------------------------------------------
def dummy():
    """
    Function to create a dummy data dictionary for writing to a SPIF
    file for testing purposes.
    """

    fred = readers.dummy_CIPgs()

    pdb.set_trace()
    return readers.dummy_CIPgs()

# ----------------------------------------------------------------------
def read():
    """
    Shorthand function to allow user to read SPIF files with;
        spif.read(f)

    """
# ----------------------------------------------------------------------
def test():
    """
    Shorthand function to allow user to test whether the input SPIF file
    meets definted standards for the format with;
        spif.test()

    """
# ----------------------------------------------------------------------
def write():
    """
    Shorthand function to allow user to write data into a SPIF file
    with;
        spif.write(f)

    """

# ----------------------------------------------------------------------
def call(args):
    """
    Main function that can be called from other programs if spif is
    imported.

    Input args:
        args:   A dictionary of arguments for code.
            'files':    List of filename and/or glob strings
            'read':     Boolean, True to read SPIF file
            'write':    Boolean, True to write SPIF file from raw data
            'test':     Boolean, True to test format of existing SPIF
            'instr':    List of instrument identifying strings
            'outfile':  Output SPIF file name. If not given then is
                        generated from inputs
            'recurse':  Boolean, True to use recursive globbing


    """
    from pathlib import Path    # For 3.5+ use glob recursion instead?

    # Convert glob/s to list of discrete files
    # Path also removes any non-existant filesnames
    path_obj = Path('.')
    if args['recurse'] is True:
        path_mod = '**/'
    else:
        path_mod = ''

    infiles = []
    for f in args['files']:
        # Create a list of Path objects
        infiles_ = [f_ for f_ in path_obj.glob(path_mod+f) if f_.exists()]
        infiles.extend(infiles_)

    if len(infiles) == 0:
        print('\nNo valid input files.')
        return None

    # Remove any files for instruments that are not required
    # Currently this involves searching for a instr string within the
    # filename only. Bit crude.
    if len(args['instr']) != 0:

        infiles = [f for f in infiles[::] for i in args['instr']
                   if i in str(f)]


    pdb.set_trace()



    if args['dummy'] is True:
        data = dummy()




# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
if __name__=='__main__':

    import argparse

    # Define commandline options
    usage = '%(prog)s filename [options]'
    version = 'ver: Mar 2017'
    description = 'Program to produce, read, and test Single Particle'+\
                  ' Image Format (SPIF) files.\n {0}'.format(version)
    epilog = 'Usage examples.\n' +\
             'Create a SPIF file with default filename based on a '+\
             'single instrument raw data file ;\n' +\
             " $ python3 spif.py 'Imagefile_1CIP Grayscale_"+\
             "20170215114606'\n"+\
             'Create a SPIF file with a customised filename based ' +\
             'on a single instrument raw data file ;\n' +\
             " $ python3 spif.py 'Imagefile_1CIP Grayscale_"+\
             "20170215114606' -o outputfile.spif\n" +\
             'Create a SPIF file with default filename based on all ' +\
             'raw data files from a single instrument ;' +\
             " $ python3 spif.py data_dir/ -i '1CIP Grayscale'\n" +\
             'Create a SPIF file with default filename based on all ' +\
             'raw data files from two different instruments ;' +\
             " $ python3 spif.py data_dir/ -i '1CIP Grayscale' 4CIP\n"+\
             'Read a SPIF file and return a pickle file;' +\
             " $ python3 spif.py file.spif -r -o file.pickle\n"

    parser = argparse.ArgumentParser(usage=usage,
                formatter_class=argparse.RawDescriptionHelpFormatter,
                description=description,
                epilog=epilog)

    # Mandatory argument
    parser.add_argument('files',
                        nargs='+',
                        help='White-space delineated path/filename ' +\
                        'of input file/s. Glob or list of globs '+\
                        'may be used.')

    # Optional arguments
    parser.add_argument('-r', '--read', action='store_true',
                        dest='read', default=False,
                        help='Option to read in a SPIF file and ' +\
                        'output as a python object. May be used with '+\
                        'a direct call to spif.read().')
    parser.add_argument('-w', '--write', action='store_true',
                        dest='write', default=None,
                        help='Option to write a SPIF file from raw ' +\
                        'data files. Is the inverse of --read and ' +\
                        'the default. May be used with a direct ' +\
                        'call to spif.write().')
    parser.add_argument('-t', '--test', action='store_true',
                        dest='test', default=False,
                        help='Option to test an existing SPIF file. ' +\
                        'Result of test written to stdout if ' +\
                        '--output not given. May be used with a ' +\
                        'direct call to spif.test().')
    parser.add_argument('-i', '--instr', action='store',
                        nargs='+',
                        dest='instr', default=[],
                        help='White-space delineated list of ' +\
                        'instrument identifiers. If file is path ' +\
                        'only then all files associated with ' +\
                        'instrument/s will be read.')
    parser.add_argument('-o', '--output', action='store',
                        dest='outfile', default=None,
                        help='Explicitly give output path/filename. ' +\
                        'If not given then filename is based on ' +\
                        'that of input file/s.')
    parser.add_argument('-d', '--dummy', action='store_true',
                        dest='dummy', default=False,
                        help='Use dummy raw data dictionary to ' +\
                        'create SPIF output. Used for development ' +\
                        'purposes only.')
    parser.add_argument('-R', '--recursive', action='store_true',
                        dest='recurse', default=False,
                        help='Recurse into sub-directories during ' +\
                        'any globbing of input files. ' +\
                        'Default is False.')
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

    call(args_dict)

    print('\nDone.\n')
    # EOF