#! /usr/bin/env python3
"""
name:     spif.py
version:  0.2
python:   3.4
author:   Graeme Nott
email:    graeme.nott@faam.ac.uk
created:  Mar 2017


Program to create and read Single Particle Image Format (SPIF) files.

"""

import sys
import datetime, pytz

import numpy as np
import matplotlib
import netCDF4
import h5py

#import readers

import pdb

# Required python version for this code
py_major = 3
py_minor = 4

# SPIF code version
spif_major = 0
spif_minor = 2


# Do some python version checking
assert sys.version_info >= (py_major,py_minor), \
        'Update to python {M}.{m} to run SPIF\n'.format(M=py_major,m=py_minor)

# SPIF code version
spif_version = '{M}.{m}'.format(M=spif_major,m=spif_minor)


# Define default root attributes of SPIF file
default_spif_attrib = {
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
    'spif_version': spif_version,
    'hdf5_version': h5py.version.hdf5_version,
    'h5py_version': h5py.version.version,
    'python_version': '{0}.{1}.{2}-{3}'.format(sys.version_info.major,
                                               sys.version_info.minor,
                                               sys.version_info.micro,
                                               sys.version_info.releaselevel),
    'project': '',      # ??
    'start_date': ''}   # ??



# ----------------------------------------------------------------------
def reader_map(instr):
    """
    Map raw data filename conventions to the appropriate raw data reader.

    Function to map raw data filename conventions to the appropriate
    raw data reader. The instr string is a common substring of the
    raw data filenames and is used to select data files with the
    --instr=instr option of __main__(). Due to overlaps in the instr
    strings, instr must be matched exactly.

    Args:
        fin (str): Instrument identifying string

    Returns:
        function for reading raw data file

    NOTE: There is a cludge here as there is no identifying string in
    PADS2 CIP files to distinguish between gray and monoscale. The
    number appended to the string Imagefile depends on the order they
    occur in the PADS.ini and the number. Currently it is set up so that
    grayscale is first and monoscale is second. The rmap dict may need
    to be changed for certain set ups.
    """

    import readers

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
# Define module level methods

def dataset(self,name,data,kwargs={}):
    """
    Creates an instance of the dataset group within a Spif object

    Args:
        name (str): name of dataset
        data (various): data to put into object
        kwargs: dictionary of dataset attributes
    """

    _tmp = Dataset(self.path+name+'/',data,**kwargs)
    setattr(self,name,_tmp)


def group(self,name,kwargs={}):
    """
    Creates an instance of a group within a Spif object

    Args:
        name (str): name of dataset
        kwargs: dictionary of dataset attributes
    """

    _tmp = Group(self.path+name+'/',**kwargs)
    setattr(self,name,_tmp)


def walk_data(f,d,p):
    """
    Recursively walk through Spif object and output/write contents

    Args:
        f (file obj): open h5 spif file objects.
            If f is None then print data to stdout
        d (spif instance):
        p (str): string placeholder for path within Spif instance

    Create a list of attributes
    Create a list of datasets
    Create a list of groups

        Write all attributes
        Write all datasets and associated attributes
        Create group in list of groups

            Recurse into walk_data again...


    *** There is no facility for linking ancillary data together yet

    *** This function will only write to a file, it will not append
        data to an existing file. It will probably fail badly.
        This needs to be changed.

    Conversion from h5 to nc
    Write attribute:
    f[p].attrs[attr] ->
    Get attribute:
    v = getattr(d,grp) ->
    Create group:
    f[p].create_group(grp) -> f[p].createGroup(grp)
    Get group?
    f.get(grp, getclass=True) ->

    v is group
    isinstance(v,Group) ->
    v is dataset
    isinstance(v,Dataset) ->


    """
    # Allow writing to the variable endof_data_stream
    global endof_data_stream

    # Create lists of contents of group p of spif instance
    grps = [k for (k,v) in d.__dict__.items() if isinstance(v,Group)]
    dsets = [k for (k,v) in d.__dict__.items() if
             isinstance(v,Dataset)]
    attrs = [k for (k,v) in d.__dict__.items() if k not in dsets+grps]

    # Write attrs
    for attr in attrs:
        # Loop through attribute names

        # Don't write 'type' or 'path' entries to the h5
        if attr.lower() in ['type','path']:
            continue

        # Shortcut for attribute value
        v = getattr(d,attr)

        if v is None:
            v = ''

#        print('  Adding attribute: ',attr)

        # Write attribute
        # Note that if p == '/' then will be written into root
        if f is None:
            print(' {}'.format(attr))
        else:
            f[p].attrs[attr] = v

    # Write datasets
    for dset in dsets:
        # Datasets have attributes attached but no recursion is required
        # Dataset values are denoted by the key '_data_'

        # Create list of attributes without 'type' and 'path' entries
        # which are not written to the h5
        dset_attrs = [l for l in getattr(d,dset).__dict__.keys() if \
                      l.lower() not in ['type','path']]

        if '_data_' not in dset_attrs:
            # Dataset instance in spif instance does not contain required field
            continue

        # Attempt to deal somewhat gracefully with empty data
        if getattr(d,dset)._data_ in [None,'']:
            if '_fillvalue' in [v.lower() for v in getattr(d,dset).__dict__]:
                # value not given so use _FillValue
                _data = getattr(d,dset)._FillValue
            elif 'units' in [v.lower() for v in getattr(d,dset).__dict__]:
                # If units are given then assume requires a number
                _data = np.nan
            else:
                # value not given so use empty string
                _data = ''
        else:
            _data = getattr(d,dset)._data_

#        print('Adding dataset {}'.format(getattr(getattr(d,dset),'path')))

        # Write dataset
        if f is None:
            print('*{}'.format(dset))
        else:
            dset_tmp = f.create_dataset(p+dset, data = _data)
        dset_attrs.remove('_data_')

        # Write dataset attributes
        for dset_attr in dset_attrs:
            v = getattr(getattr(d,dset),dset_attr)
            if v is None:
                v = ''
            if f is None:
                print(' {}'.format(dset_attr))
            else:
                dset_tmp.attrs[dset_attr] = v

    # Write groups
    for grp in grps:

        # Shortcut for attribute value
        v = getattr(d,grp)

#        print('Adding group {}'.format(getattr(v,'path')))

        if f is None:
            print('{}/'.format(grp))
        elif f.get(grp, getclass=True) is None:
            # If group k does not exist then create group
            # Note that if p == '/' then will be written into root
            f[p].create_group(grp)
        elif f.get(grp, getclass=True) is not Group:
            # Name already exists for an attribute or dataset
            print("\n'{}' already exists but is not a Group\n".format(grp))
            pdb.set_trace()
        else:
            # Group already exists so do nothing
            #print(' Existant group {}'.format(g+k+'/'))
            pass

        # Recurse with each group
        walk_data(f,v,getattr(v,'path'))

    return


# ----------------------------------------------------------------------
# Define sub-classes created within the spif class instance
# These are not created independently

## NOTE: Do we need to include some form of variable name checking to ensure
##       easy usage by user?
##

class Group():
    """
    Class to define a spif object group and the contents

    Attributes:
        path: Path of object relative to root of the Spif object
        grp_attrib (dict): attributes associated with this group
        type (str): String abbreviation for type of object as to be written
            into the h5 file. Is 'grp'.


    """

    # Access module methods
    group = group
    dataset = dataset

    def __init__(self,path,**grp_attrib):
        """
        Initialisation of a sub-class for definition of groups and contents

        """

        # Create user-defined group attributes
        for k,v in grp_attrib.items():
            setattr(self,k,v)

        # Create standard group attributes
        self.type = 'grp'
        self.path = path


class Dataset():
    """
    Class to define dataset objects

    Attributes:
        path: Path of object relative to root of the Spif object
        data: data to write into Dataset instance
        grp_attrib (dict): attributes associated with this group
        type (str): String abbreviation for type of object as to be written
            into the h5 file. Is 'data'.

    """

    # Access module methods
    dataset = dataset


    def __init__(self,path,data,**var_attrib):
        """
        Initialisation of a sub-class for definition of variables and
        associated attributes
        """

        # Write dataset data into instance
        self.set_value(data)

        # Create user-defined dataset attributes
        for k,v in var_attrib.items():
            setattr(self,k,v)

        # Create standard dataset attributes
        self.type = 'data'
        self.path = path


    def set_value(self,value):
        """
        Create the data for the dataset. This is stored in an internal _data_
        variable. Variable name chosen to minimise possibility of clash with
        user-defined variable names
        """

        self._data_ = value



# ----------------------------------------------------------------------
class Spif:
    """
    Creation of Spif objects for python-readable single particle data.

    This class relies on two other classes, Group() and Dataset(), that are
    not inherited or nested but create instances within the Spif instance.
    This class also utilises two module-level methods that are related to the
    above classes, group() and dataset().

    Attributes:
        type: String abbreviation for type of object as to be written
            into the h5 file. 'grp' or 'data' (attributes need no such label)
        path: Path of object relative to root of the h5 file
        eod: If True then there is no more data to be written into
            the h5 file.
        save: Write Spif instance into h5 file
        get_data: Return a dataset (and dataset attributes if required) from
            a Spif instance

    """

    # Access module methods
    group = group
    dataset = dataset


    def __init__(self, instr=''):
        """
        Create a new spif object which is defined by the instr string id
        """

        for k,v in default_spif_attrib.items():
            setattr(self,k,v)

        self.type = 'grp'

        # String designation of root of spif
        self.path = '/'

        # The end of data marker designates the end of the data that is
        # being inserted into this object. If True then the h5 file will be
        # closed once this object has been read.
        # Default is True
        self.eod = True


    def __str__(self):
        """
        Function prints out the structure of the spif object in human-readable
        form. Sub-groups are marked with a double asterix.

        """

        # Create introduction strings first
        intro_str = 'SPIF v{M}.{m} instance'.format(M=spif_major,m=spif_minor)
        key_str = "List of groups (end in '/'), datasets ('*'), and attributes."
        print('\n',intro_str,'\n',key_str)

        # Use walk_data to write to stdout instead of file
        walk_data(None,self,'/')
        print('')


    def set_attr(self,key,value):
        """
        Create a attribute of a group or variable with a given
        key,value pair. Any existing attribute is destroyed in the
        process
        """
        setattr(self,key,value)


    def get_group(self,name):
        """
        Returns the contents of a group as a dictionary
        """
        return getattr(self,name).__dict__


    def get_data(self,name,data_only=True):
        """
        Function to return the data and attributes (if data_only is False)
        from within a dataset instance
        """
        dataset = getattr(self,name).__dict__

        if data_only is True:
            return dataset['_data_']
        else:
            return dataset


    def save(self,filename,append=False):
        """
        Method for writing spif instance into a hdf5 file.

        Args:
            filename (str): String of Path and filename of hdf5 file to be written
            append (Boolean): If False [default], an existing file will be
                      overwritten and closed. If True, an existing file will
                      have data appended, any attributes and datasets with
                      existing names will have data appended (if possible) and
                      any new names will be added to the h5 file.

        Returns:
            success:  Returns None if h5 file written and closed successfully
                      but an exception if not.

        """

        with h5py.File(str(filename), 'w') as f:

            # Variable marks the end of a stream of data from a single file
            endof_data_stream = False
            # while endof_data_stream is False:
            #     # Read multiple data dictionaries from reader as required
            #     data = reader()

            # Walk through data dictionary and write to open spif file
            try:
                walk_data(f,self,'/')
            except Exception as err:
                # Has been unidentified error in the Spif.save method
                print('\nCannot save Spif instance to {}'.format(str(filename)))
                return err

            print('\nWritten:',str(filename))
            return None



    # ----------------------------------------------------------------------

    # TODO(Graeme): This just here as may need the code. Delete as necessary

        # def append(self,var_):
        #     """
        #     Function to append to an existing spifvar.
        #         If this is an attribute then use string methods to append
        #         If this is a variable then use native append for var type
        #         If group then exit as this doesn't make any sense

        #     Note that this function has been written for future-proofing.
        #     Users should normally use inbuilt methods specific to the
        #     variable type being used.
        #     """

        #     if self.type == 'grp':
        #         return None
        #     if self.type == 'attr':
        #         self.var = self.var.join(', ' + var_)
        #     elif self.type == 'var':
        #         if type(self.var) == str:
        #             # If string then make into a single element list of string
        #             self.var = [self.var[:]]
        #         if type(self.var) == list:
        #             # If list then append new element to end of list
        #             try:
        #                 # Assume that var_ is also an iterable
        #                 self.var.extend(var_)
        #             except TypeError:
        #                 self.var.append(var_)
        #         if type(self.var) in [int,float]:
        #             # If var is a scalar then create an array and append
        #             self.var = np.atleast_1d(self.var).append(var_)
        #         elif type(self.var) == np.ndarray:
        #             # If var_ has the same dimension as self.var then expand
        #             # first dimension. If this is not possible due to a
        #             # dimension mismatch then extend zeroth dimension.
        #             try:
        #                 self.var = np.stack((self.var[:],var_))
        #             except ValueError as e:
        #                 self.var = np.append(self.var[:],var_)
        #     else:
        #         return None



# ----------------------------------------------------------------------
def output(spif,fout):
    """
    Take a spif.Spif instance and output to a h5 file

    An input spif.Spif instance is written to a h5 SPIF file.

    Args:
        spif (spif.Spif instance): An existing instance
        fout (str or pathlib.path object): Path/file of the spif h5 file to be
            written. If already exists then add/append data.

    Returns:
        Indication of successful write?

    """

#    pdb.set_trace()
    try:
        spif.save(fout,append=False)
    except:
        # Some save error
        return 1


# ----------------------------------------------------------------------
def initialise():
    """
    Create an empty spif.Spif() instance for population by user.

    This function creates an almost empty instance of the spif.Spif class.
    Mandatory attributes and groups are created but datasets are not.

    Args:
        None

    Returns:
        Instance of spif.Spif()

    """

    return Spif()


# ----------------------------------------------------------------------
def read_spif(fin):
    """
    Read spif h5 file and return a spif.Spif() instance.

    Args:
        fin (str or pathlib.path object): Path/file of a spif file.

    Returns:
        Instance of spif.Spif()

    """

    print('\nread() not yet implemented\n')

    return


# ----------------------------------------------------------------------
def read_raw(fin,reader,spif=None):
    """
    Read a raw data file and return a spif.Spif() instance.

    Args:
        fin (str or pathlib.path object): Path/file of a raw data file.
        reader ():
        spif (spif.Spif instance): If None then create new instance, if given
            then add new data into existing instance.
    Returns:
        Instance of spif.Spif()

    """

    return reader(fin,spif)


# ----------------------------------------------------------------------
def test(fin):
    """
    Test whether a spif/h5 file meets the criteria of the standard.

    This function allows user to test whether the input spif file meets
    the defined standards of the format.

    Args:
        fin (str or pathlib.path object): Path/file of a spif file.

    Returns:
        result (tuple): Returns one of the following;
            (0,None): success
            (1,list of failures): Non-fatal fail with list of issues returned
            (2,list of failures): Fatal fail with as list of issues up to fail

    Tests to do:
        All instances of Spif, Group, or Dataset must have a valid 'type' k,v
        All instances of Spif, Group, or Dataset must have a valid 'path' k,v
    """

    test_d = read(fin)

    print('\ntest() not yet implemented\n')


    return

# ----------------------------------------------------------------------
def write(fin,instr,fout):
    """
    Read raw data file/s spif h5 file and return a spif.Spif() instance

    Args:
        fin (list or str or pathlib.path object): Path/file of raw data file/s.
        instr (list or str): list of instrument id strings associated with
            each fin. Thus len(fin) == len(instr) or if instr is a string then
            same instr string applied to each fin in list
        fout (str or pathlib.path object): Path/file of h5 spif file.

    Returns:
        Indication of successful write?

    Exceptions:
    """

    # Test list args
    # TODO (Graeme): More pythonic tests required
    if type(fin) not in [list,tuple]:
        fin = [fin]
    if type(instr) not in [list,tuple]:
        instr = [instr]
    if len(instr) == 1:
        instr = instr * len(fin)
    if len(fin) != len(instr):
        # TODO (Graeme): Fix handling of errors in fin and instr list lengths
#        print(('\nError in number of input files ({}) and instrument'
#               'strings ({}).'.format(len(fin),len(instr))))
        return 1

    # Initialise a temporary spif.Spif instance
    spif_tmp = initialise()

    print('Reading...')
    for f,i in zip(fin,instr):
        # Loop through each input file and write into same spif file

        try:
            print('  {}'.format(f.name))
        except AttributeError:
            # f is a string
            print('  {}'.format(f))

        # Determine correct reader function
        reader = reader_map(i)

        if reader is None:
            # Reader function for i cannot be found
            continue

        # TODO (Graeme): Deal with multiple instances of the same instr into the same spif file

        # Populate spif instance
        spif_tmp = read_raw(f,reader,spif_tmp)


    # Write spif instance to h5 spif file
    write_ok = output(spif_tmp,fout)

    if write_ok != 1:
        print('Written: {!s}'.format(fout))
    else:
        print('Write fail: error {}'.format(write_ok))

    """
    OBSOLETE!

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


# ----------------------------------------------------------------------
def call(**args):
    """
    Main function call of spif.py.

    Function to allow impotation and calling of complete spif.py
    functionality. Generally however, one would import the spif.Spif() class
    and create instances of this.

    Args:
        **args (dict): A dictionary of arguments for function. Is a replica
            of the args dictionary that is created by argparse in __main__.
            Recognised fields are;
            'files': List of filename and/or glob strings
            'read' (Boolean): True to read SPIF file
            'write' (Boolean): True to write SPIF file from raw data
            'test' (Boolean): True to test format of existing SPIF
            'instr': List of instrument identifying strings
            'outfile' (str): Output SPIF file name. If not given then is
                generated from inputs
            'force_write' (Boolean): True to overwrite existing SPIF
            'recurse' (Boolean): True to use recursive globbing


    """
    from pathlib import Path    # For 3.5+ use glob recursion instead?

    # Convert glob/s to list of discrete files
    # Path also removes any non-existant filesnames

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
    # Currently this involves searching for an instr string within the
    # filename only. Bit crude.

    # TODO (Graeme): Change this so can use files with arbitrary names
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
                                             '-%H%M.h5')
        instr_str = ''.join(sorted(args['instr']))
        outfile = Path(datestr+instr_str+timestr)
    else:
        outfile = Path(args['outfile'])

        if outfile.suffix == '':
            # Add the default h5 extension if one not given
            outfile = outfile.with_suffix('.h5')

        if outfile.is_file() is True and args['force_write'] is False:
            # If file already exists notify user and fail
            print('\nOutput file already exists;',
                  '  {0}'.format(str(outfile)),
                  'Use -f to overwrite',sep='\n')
            return None

#    pdb.set_trace()

    if args['write'] in [True,None]:

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
    version = 'version: {M}.{m}'.format(M=spif_major,m=spif_minor)
    description = ('Program to produce, read, and test Single Particle'
                   'Image Format (SPIF) files.\n {0}'.format(version))
    epilog = 'Usage examples.\n' +\
             'Create a SPIF file, fred.h5, with default filename based ' +\
             'on dummy data;\n' +\
             "$ python3 spif.py --dummy -o fred.h5\n" +\
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
                        help=('White-space delineated path/filename '
                        'of input file/s. Glob or list of globs '
                        'may be used.'))

    # Optional arguments
    parser.add_argument('-r', '--read', action='store_true',
                        dest='read', default=False,
                        help=('Option to read in a SPIF file and '
                        'output as a python object. May be used with '
                        'a direct call to spif.read().'))
    parser.add_argument('-w', '--write', action='store_true',
                        dest='write', default=None,
                        help=('Option to write a SPIF file from raw '
                        'data files. Is the inverse of --read and '
                        'the default. May be used with a direct '
                        'call to spif.write().'))
    parser.add_argument('-t', '--test', action='store_true',
                        dest='test', default=False,
                        help=('Option to test an existing SPIF file. '
                        'Result of test written to stdout if '
                        '--output not given. May be used with a '
                        'direct call to spif.test().'))
    parser.add_argument('-i', '--instr', action='store',
                        nargs='+',
                        dest='instr', default=[],
                        help=('White-space delineated list of '
                        'instrument identifiers. If file is path '
                        'only then all files associated with '
                        'instrument/s will be read.'))
    parser.add_argument('-o', '--output', action='store',
                        dest='outfile', default=None,
                        help=('Explicitly give output path/filename. '
                        'If not given then filename is based on '
                        'that of input file/s.'))
    parser.add_argument('-f', '--force', action='store_true',
                        dest='force_write', default=False,
                        help=('Allow an existing outfile to be over-'
                        'written.'))
    parser.add_argument('-d', '--dummy', action='store_true',
                        dest='dummy', default=False,
                        help=('Use dummy raw data dictionary to '
                        'create SPIF output. Used for development '
                        'purposes only.'))
    parser.add_argument('-R', '--recursive', action='store_true',
                        dest='recurse', default=False,
                        help=('Recurse into sub-directories during '
                        'any globbing of input files. '
                        'Default is False.'))
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

    call(**args_dict)

    print('\nDone.\n')
    # EOF