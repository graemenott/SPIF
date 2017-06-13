#! /usr/bin/env python3
"""
name:     spif.py
version:  0.2
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
# Define module level methods

def dataset(self,name,data,kwargs={}):
    """
    Create a dataset within the spif object
    Creates an instance of the dataset group
    """
    #pdb.set_trace()
    _tmp = Dataset(self.path+name+'/',data,**kwargs)
    setattr(self,name,_tmp)


def group(self,name,kwargs={}):
    """
    Create a sub-group within the spif object
    Creates an instance of the class group

    Note that it is more convenient if 'name' is 'nice' (need proper words)
    """
    #pdb.set_trace()
    _tmp = Group(self.path+name+'/',**kwargs)
    setattr(self,name,_tmp)


def walk_data(f,d,p):
    """
    Function to recursively walk through an arbitrary data
    dictionary and create equivalent spif data structures.

    Input args:
        f:      open spif file objects. If f is None then print data to stdout
        d:      spif instance
        p:      string placeholder for depth within recursion

    Create a list of attributes
    Create a list of datasets
    Create a list of groups

        Write all attributes
        Write all datasets and associated attributes
        Create group in list of groups

            Recurse into walk_data again...


    *** There is no facility for linking ancillary data together yet

    *** This function will only write to a file, it will not append
        data to an existing file. It will fail badly.
        This needs to be changed.

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

        print('  Adding attribute: ',attr)
        # Write attribute
        # Note that if p == '/' then will be written into root
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

        print('Adding dataset {}'.format(getattr(getattr(d,dset),'path')))
        # Write dataset
        dset_tmp = f.create_dataset(p+dset, data = _data)
        dset_attrs.remove('_data_')

        # Write dataset attributes
        for dset_attr in dset_attrs:

            v = getattr(getattr(d,dset),dset_attr)
            if v is None:
                v = ''
            dset_tmp.attrs[dset_attr] = v

    # Write groups
    for grp in grps:

        # Shortcut for attribute value
        v = getattr(d,grp)

        print('Adding group {}'.format(getattr(v,'path')))

        if f.get(grp, getclass=True) is None:
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

## NOTE: Do need to include some form of variable name checking to ensure
##       easy usage by user?
##

class Group():
    """
    Class to define a spif object group and the contents
    """

    # Access module methods
    group = group
    dataset = dataset

    def __init__(self,path,**grp_attrib):
        """
        Initialisation of a sub-class for definition of groups and contents

        parent is the class above
        """
        # Create instrument root attributes
        for k,v in grp_attrib.items():
            setattr(self,k,v)

        self.type = 'grp'
        self.path = path



    # def set_data(self,name,data,kwargs={}):
    #     """
    #     Create a dataset within the spif object
    #     Creates an instance of the dataset group
    #     """
    #     set_data(name,data,kwargs)


class Dataset():
    """
    Class to define dataset objects
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

        # Create variable attributes
        for k,v in var_attrib.items():
            setattr(self,k,v)

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
    Parent class to define spif objects. 
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

        # The end of file marker designates the end of the data file that is
        # being inserted into this object. If True then the h5 file will be
        # closed once this object has been read.
        # Default is True
        self.eof = True


    def __str__(self):
        """
        Function prints out the structure of the spif object in human-readable
        form. Sub-groups are marked with a double asterix.
        """

        # Create string of all attributes first
        attrib_str = '\n'.join(
            [' '+k for k,v in sorted(self.__dict__.items()) if
             isinstance(v,spif) is False])

        var_str = '\n'.join(
            [' {}\t**'.format(k) for k,v in sorted(self.__dict__.items()) if
             isinstance(v,spif) is True])

        return '\n{0}\n{1}\n{2}\n'.format(self.path,attrib_str,var_str)


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


    # def set_group(self,name,kwargs={}):
    #     """
    #     Create a sub-group within the spif object
    #     Creates an instance of the class group

    #     Note that it is more convenient if 'name' is 'nice' (need proper words)
    #     """
    #     pdb.set_trace()
    #     _tmp = spif.group(self.path+name+'/',**kwargs)
    #     setattr(self,name,_tmp)


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


    def write(self,filename,append=False):
        """
        Method for writing spif instance into a hdf5 file.

        
        Keyword args:
            filename: String of Path and filename of hdf5 file to be written
            append:   Boolean. If False [default], an existing file will be
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
            walk_data(f,self,'/')

            print('\nWritten:',str(filename))



    # ----------------------------------------------------------------------


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
def create(fin):
    """
    Shorthand function to allow user to read input files and create a 
    spif object with;
        spif.create(f)

    """

    print('\nNot yet implemented\n')

    return


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

    Tests to do:
        All instances of Spif, Group, or Dataset must have a valid 'type' k,v
        All instances of Spif, Group, or Dataset must have a valid 'path' k,v
    """

    test_d = read(fin)




    return

# ----------------------------------------------------------------------
def write(fin,instr,fout):


    ###
    ### THIS NEEDS TO BE CHANGED TO;
    ###         Read raw data files
    ###         Create a spif instance
    ###         Write instance to h5 file
    ###
    
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
               '_data_' not in [v_.lower() for v_ in v]:
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