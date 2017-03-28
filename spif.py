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
    'source': 'spif.py',
    'references': '../docs/SPIF_definition.pdf',
    'history': datetime.datetime.strftime(datetime.datetime.now(tz=pytz.utc),
                                          '%Y-%m-%dT%H:%M%z'),
    # NOTE: pytz probably not the best way to include tz info, ok for UTC.
    # for v3.6 can use datetime.datetime.isoformat(x,timespec='minutes')
    'comment': '{t}: {c}'.format(
             t=datetime.datetime.strftime(datetime.datetime.now(tz=pytz.utc),
                                        '%Y-%m-%dT%H:%M%z'),
             c='initial implementation'),
    # Implement this by reading a file changelog
    'spif_version': '0.1dev',
    'hdf5_version': h5py.version.hdf5_version,
    'h5py_version': h5py.version.version,
    'project': '',      # ??
    'start_date': ''}   # ??



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
    pass
    # def __init__(self,fin,fout=None):

    #     # Open the hdf5 file
    #     self.spif = h5py.File(fout,'a')

    # def __str__(self):

    #     return 'Write.Append() not yet implemented.'


class Create(Write):
    """
    Sub-class of Write that creates a SPIF file and writes data into
    that file. All required metadata must also be supplied.

    """
    pass
    # def __init__(self,fin=[],fout=None,dummy=False):

    #     Write.__init__(self,fin,fout,dummy)

    #     # Open the hdf5 file
    #     self.spif = h5py.File(fout,'w')







    # def read_fin(self,fin):
    #     # Function to open and read raw data file
    #     pass


# ----------------------------------------------------------------------
class Test():
    """

    """


# ----------------------------------------------------------------------
def reader_map(instr):
    """
    Function to map raw data filename conventions to the appropriate
    raw data reader. The instr string is a common substring of the
    raw data filenames and is used to select data files with the
    --instr=instr option of __main__(). Due to overlaps in the instr
    strings, instr must be matched exactly.

    Input args:
        instr:      instrument identifying string

    Returns:
        reader:     function for reading raw data file

    NOTE: There is a cludge here as there is no identifying string in
    PADS2 CIP files to distinguish between gray and monoscale. The
    number appended to the string Imagefile depends on the order they
    occur in the PADS.ini and the number. Currently it is set up so that
    grayscale is first and monoscale is second. The rmap dict may need
    to be changed for certain set ups.
    """

    # Each list of strings can have many instr strings. However, each
    # of these strings must be unique within rmap.
    rmap = {readers.CIPgs_PADS3:    ['CIP Grayscale'],
            readers.CIP_PADS3:      ['CIP'],
            readers.CIPgs_PADS2:    ['Imagefile'],
            readers.CIP_PADS2:      ['Imagefile2'],
            readers.twoDS:          [],
            readers.CPI:            [],
            readers.HVPS:           [],
            readers.dummy_CIPgs:    ['dummy']}

    # Search rmap dictionary for exact match to instr string.
    # Will only return the first instance.
    for k,v in rmap.items():
        if instr in v:
            return k


# ----------------------------------------------------------------------
def read(fin):
    """
    Shorthand function to allow user to read SPIF files with;
        spif.read(f)

    """

    print('\nNot yet implemented\n')

    return

# ----------------------------------------------------------------------
def test(fin):
    """
    Shorthand function to allow user to test whether the input SPIF file
    meets definted standards for the format with;
        spif.test()

    """

    test_d = read(fin)

    return

# ----------------------------------------------------------------------
def write(fin,instr,fout):
    """
    Shorthand function to allow user to write data into a SPIF file
    with;
        spif.write(f)

    Input args:
        fin     list of data filenames to read in. May either be
                list of strings or pathlib path objects
        instr   list of instrument id strings associated with each fin
                Thus len(fin) == len(instr)
        fout    filename of output SPIF file. May either be string
                or pathlib path object

    Create spif file
    Loop through each of the file names
        Call reader until EOF returned
            Returns some data dict
            Create group if required
            Write data dict into spif, append or overwite

    NOTES:
        Read a (dataset) scalar:
            spif['1CIP Grayscale/channels'][()]

        Read an attribute:
            spif.attrs['title']

        Print off all groups:
            fred = lambda x: print(x)
            spif.visit(fred)
    """

    global endof_data_stream

    print_x = lambda x: print(x)

    def walk_data_dict(d,g):
        """
        Function to recursively walk through an arbitrary data
        dictionary and create equivalent spif data structures.

        Input args:
            d:      data dictionary
            g:      string placeholder for depth within recursion

        NOTE:   This function writes directly to the h5 file, 'spif', as
                defined in the parent function.

        *** This function will only write to a file, it will not append
            data to an existing file. It will fail badly.
            This needs to be changed.

        """
        # Allow writing to the variable endof_data_stream
        global endof_data_stream
        #pdb.set_trace()

#        print ('\nwalk_dict(d,{})\n'.format(g))

        for k, v in d.items():

#            print ('** for k={} loop:'.format(k))

            if isinstance(v, dict) and \
               'value' not in [v_.lower() for v_ in v]:
                # This subdictionary is converted into a h5 group

                # Create a group based on current k string
                # Need to seperate root and non-root instances (?)
                if g == '' and spif.get(k) is None:
                    #print(' Adding group {}'.format(g+k+'/'))
                    spif.create_group(k)
                elif spif.get(k) is None:
                    #print(' Adding group {}'.format(g+k+'/'))
                    spif[g].create_group(k)
                else:
                    # Group already exists so do nothing
                    #print(' Existant group {}'.format(g+k+'/'))
                    pass
                #spif.visit(print_x)

                # Recurse into sub-dictionary k
                walk_data_dict(v,g+k+'/')

            elif isinstance(v, dict):
                # Item will not be converted into h5 group.
                # If isinstance(v, dict) is True -> convert to Dataset

                #print(' Adding dataset {}'.format(g+k))

                if g[:-1] == '':
                    # Attempt to write dataset directly into root of
                    # spif file. In this case use the k value
                    key = k
                else:
                    key = g+k

                if v['value'] is None:
                    if '_fillvalue' in [v_.lower() for v_ in v]:
                        # value not given so use _FillValue
                        spif.create_dataset(key, data=v['_FillValue'])
                    elif 'units' in [v_.lower() for v_ in v]:
                        # If units are given then assume requires a number
                        spif.create_dataset(key, data=np.nan)
                    else:
                        # value not given so use empty string
                        spif.create_dataset(key, data='')
                else:
                    spif.create_dataset(key, data=v['value'])#, dtype=None)

                # Recurse into Dataset sub-dict and create attributes
                walk_data_dict(v,g+k+'/')

            elif k.lower() == 'value':
                # dictionaries with 'value' attribute have already been
                # converted to a dataset so can ignore these
                #print('Ignore this!')
                continue

            else:
                # If isinstance(v, dict) is False -> convert to Attribute
                # Create attributes

                #print("  {0}{1}: {2}".format(g, k, v))
                #pdb.set_trace()

                if k.lower() == 'ancillary_variables':
                    # Create link to another variable
                    # What happens if it hasn't been created?
                    pass
                elif k.upper() == 'EOF':
                    # End of data file maker
                    endof_data_stream = v
                    #print('endof_data_stream is',endof_data_stream)
                else:
                    # Write attributes for this dataset or group
                    # Convert any None entries into emptry strings
                    #print(' Adding attribute: {}'.format(k))

                    if g[:-1] == '':
                        # Write attribute into root of SPIF file
                        if v is None:
                            spif.attrs[k] = ''
                        else:
                            spif.attrs[k] = v
                        #print([k for k in spif.attrs])
                    else:
                        # Write attribute into group
                        if v is None:
                            spif[g[:-1]].attrs[k] = ''
                        else:
                            spif[g[:-1]].attrs[k] = v

                        #print([k for k in spif[g[:-1]].attrs])
                    #print()

        return


    with h5py.File(str(fout), 'w') as spif:

        # Create root and write default root attributes

        for k,v in default_root.items():
            spif.attrs[k] = v

        print('Reading...')
        for f,i in zip(fin,instr):
            # Loop through each input file and write into same spif file
            print('\t{}'.format(f))

            # Determine correct reader function
            reader = reader_map(i)

            # Variable marks the end of a stream of data from a single file
            endof_data_stream = False
            while endof_data_stream is False:
                # Read multiple data dictionaries from reader as required
                data = reader()

                # Walk through data dictionary and write to open spif file
                walk_data_dict(data,'')

        print('\nWritten:',str(fout))
    # Finished reading all input files and spif output file is closed
    return



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
            'force_write': Boolean, True to overwrite existing SPIF
            'recurse':  Boolean, True to use recursive globbing


    """
    from pathlib import Path    # For 3.5+ use glob recursion instead?

    # Convert glob/s to list of discrete files
    # Path also removes any non-existant filesnames
#    path_obj = Path('.')
    if args['recurse'] is True:
        path_mod = '**/'
    else:
        path_mod = ''

    infiles = []
    for f in args['files']:
        # Create a list of Path objects
        path = Path(f)
        infiles_ = [f_ for f_ in path.parents[0].glob(path_mod+path.name)
                    if f_.exists()]
        infiles.extend(sorted(infiles_))

    if len(infiles) == 0 and args['dummy'] is False:
        print('\nNo valid input files.')
        return None

    # Remove any files for instruments that are not required
    # Currently this involves searching for a instr string within the
    # filename only. Bit crude.
    if len(args['instr']) != 0 and args['dummy'] is False:

        fstr = [(f,i) for f in infiles[::]
                for i in args['instr'] if i in str(f)]

        # Create two lists of input filename strings and associated
        # instrument id string
        if len(fstr) == 0:
            infiles = []
            instr_strs = []
        else:
            infiles, instr_strs = zip(*fstr)

    # Create dummy instrument if required.
    if args['dummy'] is True:
        args['instr'] = ['dummy']
        args['write'] = True
        infiles = ['']
        instr_strs = ['dummy']

    # Construct output filename if necessary
    if args['outfile'] is None:
        # Output filename built from common elements of input filenames
        datestr = datetime.date.strftime(datetime.date.today(),'%Y%m%d_')
        timestr = datetime.datetime.strftime(datetime.datetime.now(),
                                             '-%H%M.spif')
        instr_str = ''.join(sorted(args['instr']))
        outfile = Path(datestr+instr_str+timestr)
    else:
        outfile = Path(args['outfile'])

        if outfile.is_file() is True:
            print('\nOutput file already exists;',
                  '  {0}'.format(str(outfile)),
                  'Use -f to overwrite',sep='\n')
            return None

    if args['write'] is True:

        write(infiles, instr_strs, outfile)

    elif args['read'] is True:

        read(infiles)

    elif args['test'] is True:

        test(infiles)


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
             'Create a SPIF file with default filename based ' +\
             'on dummy data;\n' +\
             "$ python3 spif.py fred --dummy\n" +\
             'Create a SPIF file with default filename based on a '+\
             'single instrument raw data file;\n' +\
             " $ python3 spif.py 'Imagefile_1CIP Grayscale_" +\
             "20170215114606'\n" +\
             'Create a SPIF file with a customised filename based ' +\
             'on a single instrument raw data file;\n' +\
             " $ python3 spif.py 'Imagefile_1CIP Grayscale_" +\
             "20170215114606' -o outputfile.spif\n" +\
             'Create a SPIF file with default filename based on all ' +\
             'raw data files from a single instrument;\n' +\
             " $ python3 spif.py data_dir/ -i '1CIP Grayscale'\n" +\
             'Create a SPIF file with default filename based on all ' +\
             'raw data files from two different instruments;\n' +\
             " $ python3 spif.py data_dir/ -i '1CIP Grayscale' 4CIP\n"+\
             'Read a SPIF file and return a pickle file;\n' +\
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
    parser.add_argument('-f', '--force', action='store_true',
                        dest='force_write', default=False,
                        help='Allow an existing outfile to be over-' +\
                        'written.')
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