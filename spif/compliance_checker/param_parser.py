
"""
Function to convert config file designed for reading with ConfigParser to
restructured text for integration into documentation

"""

import yaml
import os.path
import re
from collections.abc import MutableMapping
import pdb


__all__ = ['parse_yaml']

DEFAULT_YAML_FILE = 'spif_parameters.yaml'

ALLOWED_TYPES = {'grp': ['grp', 'grps', 'group', 'groups'],
                 'attr': ['attr', 'attrs', 'attribute', 'attributes'],
                 'dim': ['dim', 'dims', 'dimension', 'dimensions'],
                 'coord': ['coord', 'coords', 'coordinate', 'coordinates'],
                 'var': ['var', 'vars', 'variable', 'variables']}

# ----------------------------------------------------------------------
class ncParam():

    def __init__(self, param):
        self.dtype = None
        self.group = None
        self.name = None
        self.path = None
        self.dims = []
        self.attrs = {}

        # Identify type of parameter
        nctypes = [(k1,k2) for k1,v1 in param.items()
                           for k2,v2 in ALLOWED_TYPES.items()
                           if k1 in v2 and v1==None]
        if len(nctypes) > 1:
            raise KeyError(
                       f"More than one parameter type given for {param.name}.")
        try:
            typekey, self.nctype = nctypes[0]
        except IndexError as err:
            raise err(f"No parameter type given for {param.name}. Must be one of ",
                      ', '.join(ALLOWED_TYPES.keys()))

        _ = param.pop(typekey)

        if self.nctype == 'grp':
            self.set_ncgrp(param)
        elif self.nctype == 'attr':
            self.set_ncattr(param)
        elif self.nctype == 'dim':
            self.set_ncdim(param)
        elif self.nctype == 'coord':
            self.set_ncvar(param)
        elif self.nctype == 'var':
            self.set_ncvar(param)
            if [self.name] == self.dims:
                self.nctype = 'coord'

    def _grprst(self):
        if self.group == '/':
            return "~~~~\nroot\n~~~~\n"
        else:
            return f"\n{self.group}\n{'~'*max(3, len(self.group))}\n"

    def _dimrst(self):
        """ Print attribute string block in rst format
        """
        return f" :dimension: \"{self.name}\" ;\n"

    def _attrrst(self):
        """ Print attribute string block in rst format
        """
        block = f" :{self.esc(self.name)}: "
        for attr, astr in self.attrs.items():
            block += f"\"{self.esc(astr)}\" ;\n "
        return block

    def _varrst(self):
        """ Print variable string block in rst format
        """
        try:
            block = f" | *{self.dtype}* **{self.esc(self.name)}** ({', '.join(self.dims)})\n"
        except TypeError as err:
            # dims are None
            block = f" | *{self.dtype}* **{self.esc(self.name)}**\n"
        for attr, astr in self.attrs.items():
            block += f" |  **{self.esc(self.name)}**:{self.esc(attr)} = \"{self.esc(astr)}\" ;\n"
        return block

    @staticmethod
    def esc(s):
        """ Include \ in strings to escape rst special characters
        """
        specials = '*_:'
        return re.sub(r'([\*\_\:])', r'\\\1', s)

    @staticmethod
    def root_path(path):
        return os.path.join('/', path)

    def set_ncgrp(self, param):
        self.path = self.root_path(param.name)
        self.group = self.path

    def set_ncattr(self, param):
        self.path = self.root_path(param.name)
        self.group, self.name = os.path.split(self.path)
        self.attrs = {k: v for k,v in param.items()}

    def set_ncdim(self, param):
        self.path = self.root_path(param.name)
        self.group, self.name = os.path.split(self.path)

    def set_ncvar(self, param):
        # May be variable or coordinate (name is same as dimension)
        self.path = self.root_path(param.name)
        self.group, self.name = os.path.split(self.path)
        try:
            self.dtype = param.pop('dtype')
        except KeyError as err:
            raise KeyError(f"'dtype' is required for a {param.name} declaration")
        self.dims = param.getlist('dimensions')
        _ = param.pop('dimensions', None)
        self.attrs = {k: v for k,v in param.items()}

    @property
    def rst(self):
        if self.nctype == 'grp':
            return self._grprst()
        elif self.nctype == 'attr':
            return self._attrrst()
        elif self.nctype == 'dim':
            return self._dimrst()
        elif self.nctype == 'coord':
            return self._varrst()
        elif self.nctype == 'var':
            return self._varrst()


# ----------------------------------------------------------------------
def mandatory_params(file=None):
    """ Allow file to be imported
    """
    if file is None:
        file = os.path.join(os.path.dirname(__file__),
                            DEFAULT_CFG_FILES['mandatory'])

    return file


# ----------------------------------------------------------------------
def optional_params(file=None):
    """ Allow file to be imported
    """
    if file is None:
        file = os.path.join(os.path.dirname(__file__),
                            DEFAULT_CFG_FILES['optional'])

    return file


# ----------------------------------------------------------------------
def list_converter(s):
    s_list = s.split(',')
    return [None if _s.lower()=='none' else _s.strip() for _s in s_list]


# ----------------------------------------------------------------------
def cfg2rst(cfg_file):

    # converter is accessed with cfg.getlist(sec, opt) or cfg[sec].getlist(opt)
    cfg = configparser.ConfigParser(
                    allow_no_value=True,
                    converters = {'list': list_converter})

    cfg.read(cfg_file)

    param_list = []
    for sec in cfg.sections():
        param = ncParam(cfg[sec])
        param_list.append(param)

    # Sort into groups, then type, then parameter name before formatting string
    param_list.sort(key=lambda x: (x.group, x.nctype, x.name))
    rst_list = []
    for i, param in enumerate(param_list):
        if i == 0:
            rst_list.append(param._grprst())
        elif param.group != param_list[i-1].group:
            rst_list.append(param._grprst())
        rst_list.append(param.rst)

    return '\n\n'.join(rst_list)


# ----------------------------------------------------------------------
def walk_dtree(top):
    """ Generator for walking down through recursive dict-like structure

    from: https://unidata.github.io/netcdf4-python/#groups-in-a-netcdf-file
    """

    yield top.items()
    for value in top.items():
        yield from walk_dtree(value)

def nested_dict_values_iterator(dict_obj):
    ''' This function accepts a nested dictionary as argument
        and iterate over all values of nested dictionaries
    '''
    # Iterate over all values of given dictionary
    for value in dict_obj.values():
        # Check if value is of dict type
        if isinstance(value, dict):
            # If value is dict then iterate over all its values
            for v in  nested_dict_values_iterator(value):
                yield v
        else:
            # If value is not dict type then yield the value
            yield value


def walk_dict(top, path='', nctype='grp'):

    # if element in cfg:
    # path = path + element + ' = ' + cfg[element]
    # print(path)
    # all_paths.append(path)


    if nctype == 'grp':
        pass

    if isinstance(top, dict):
        nctype = [k for k, v in ALLOWED_TYPES.items() if top in v]

    param_name, param_val = top.items()
    nctypes = [(k1,k2) for k1,v1 in top.items()
                           for k2,v2 in ALLOWED_TYPES.items()
                           if k1 in v2 and isinstance(v1, dict)]

    for key in d:
        if isinstance(d[key], dict):
            walk_dict(d[key],path)

def _flatten_dict_gen(top, toppath, sep):
    """ Generator for flattening dictionary.

    Any values that are a sub-dict are not explicitly returned
    """
    for k, child in top.items():
        childpath = toppath + sep + k if toppath else k
        if isinstance(child, MutableMapping):
            yield from flatten_dict(child, childpath, sep=sep).items()
        else:
            yield childpath, child

def flatten_dict(d, dpath='', sep='/'):
    """ Creates a flattened dictionary with complete path as keys.

    from
    https://www.freecodecamp.org/news/how-to-flatten-a-dictionary-in-python-in-4-different-ways/
    """
    return dict(_flatten_dict_gen(d, dpath, sep))


# ----------------------------------------------------------------------
class ncParams(object):
    """ Class for holding netCDF parameter information

    netCDF parameter information may come from the spif parameters yaml
    file or the netCDF file that is being evaluated for compliance.

    Creates a list (?) of
        - group objects (with associated attr objects)
        - dimension objects (with associated attr objects)
        - variable objects (with associated attr objects)

    """

    # def __init__(ncdict):

    #     self.source = ncdict
    #     self.data = None



class stdParams(ncParams):
    """ Create ncParams object based on spif standard parameters

    """

    def __init__(self, std_file):

        self.src_file = std_file
        self.src_type = 'std'
        self.std_parse(std_file)

        self.grps = []
        self.dims = {}
        self.vars = {}


    def std_parse(self, std_file):
        """ Constructs obj data from dictionary
        """

        self.data_d = parse_yaml(std_file)
        data = flatten_dict(self.data_d)
                            #['root']['attributes'],
                            #'root/attributes')

        pdb.set_trace()
        d_params = [os.path.dirname(k) for k in data.keys()]

        self.data = {}
        for param in list(dict.fromkeys(d_params)):
            # Loop through (ordered) list of unique parameter types
            param_vals = {os.path.basename(k):v for k,v in data.items()
                          if os.path.dirname(k) == param}

            self.data[param] = spifParam(param_vals.pop('nctype'), param)
            self.data[param].value = param_vals

    def get_attrs(self, param):
        """ Find all attributes of parameter, param

        param must be able to hold attributes, ie group, or variable
        """

        pass

    def get_vars(self, param):
        """ Find all variables of group, param
        """

        pass




        grps_list = ['/']
        for children in walk_dtree(self.std_d):
            for child in children:
                grps_list.append(child.path)

        self.dtype = None
        self.group = None
        self.name = None
        self.path = None
        self.dims = []
        self.attrs = {}

        # Identify type of parameter
        nctypes = [(k1,k2) for k1,v1 in param.items()
                           for k2,v2 in ALLOWED_TYPES.items()
                           if k1 in v2 and v1==None]
        if len(nctypes) > 1:
            raise KeyError(
                       f"More than one parameter type given for {param.name}.")
        try:
            typekey, self.nctype = nctypes[0]
        except IndexError as err:
            raise err(f"No parameter type given for {param.name}. Must be one of ",
                      ', '.join(ALLOWED_TYPES.keys()))

        _ = param.pop(typekey)

        if self.nctype == 'grp':
            self.set_ncgrp(param)
        elif self.nctype == 'attr':
            self.set_ncattr(param)
        elif self.nctype == 'dim':
            self.set_ncdim(param)
        elif self.nctype == 'coord':
            self.set_ncvar(param)
        elif self.nctype == 'var':
            self.set_ncvar(param)
            if [self.name] == self.dims:
                self.nctype = 'coord'











class spifParam(object):

    def __init__(self, ptype, path):

        self.nctype = ptype
        self.path = path
        self.name = os.path.basename(path)

        self._dict = None

    @property
    def value(self):
        return self._dict

    @value.setter
    def value(self, param_vals):
        self._dict = param_vals




class spifAttr(spifParam):

    def __init__(self, path):
        super().__init__('attr', path)

class spifGroup(spifParam):

    def __init__(self, path):
        super().__init__('grp', path)

class spifDim(spifParam):

    def __init__(self, path):
        super().__init__('dim', path)

class spifVar(spifParam):

    def __init__(self, path):
        super().__init__('var', path)





def parse_yaml(yaml_file):
    """ Parse yaml config which uses custom parameter tags
    """
    class Dice(tuple):
        def __new__(cls, a, b):
            return tuple.__new__(cls, [a, b])
        def __repr__(self):
            return "Dice(%s,%s)" % self

    def dice_constructor(loader, node):
        value = loader.construct_scalar(node)
        a, b = map(int, value.split('d'))
        return Dice(a, b)


    def ncattr_constructor(loader, node):
        d = loader.construct_mapping(node)
        d.update({'nctype': 'attr'})
        return d

    def ncvar_constructor(loader, node):
        d = loader.construct_mapping(node)
        d.update({'nctype': 'var'})
        return d

    def ncdim_constructor(loader, node):
        d = loader.construct_mapping(node)
        d.update({'nctype': 'dim'})
        return d

    def ncgrp_constructor(loader, node):
        d = loader.construct_mapping(node)
        d.update({'nctype': 'grp'})
        return d

    yaml.add_constructor(u'!dice', dice_constructor, Loader=yaml.SafeLoader)
    yaml.add_constructor(u'!ncattr', ncattr_constructor, Loader=yaml.SafeLoader)
    yaml.add_constructor(u'!ncvar', ncvar_constructor, Loader=yaml.SafeLoader)
    yaml.add_constructor(u'!ncdim', ncdim_constructor, Loader=yaml.SafeLoader)
    yaml.add_constructor(u'!ncgrp', ncgrp_constructor, Loader=yaml.SafeLoader)

    with open(yaml_file) as f:
        cfg = yaml.load(f, Loader=yaml.SafeLoader)

    return cfg


def parse_yaml2(yaml_file):
    """ Parse yaml parameters file

    """
    try:
        with open(yaml_file) as f:
            try:
                cfg = yaml.load(f, Loader=yaml.SafeLoader)
            except yaml.scanner.ScannerError as err:
                print('\nThis is not a recognised parameters yaml file:')
                print('  ', f.name, '\n')
                return None
    except FileNotFoundError as err:
        print('\n', err, '\n')
        return None

    return cfg


class ComplianceParams(yaml.YAMLObject):
    """
    Do I need this/can I use this. This is for defining yaml objects?
    """
    pass



# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
if __name__=='__main__':

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', action='store',
                        dest='yaml_file', default=None,
                        help=('SPIF definition yaml file'))


    # Process arguments and convert to dictionary ----------------------
    args_dict = vars(parser.parse_args())

    pdb.set_trace()
    if args_dict['yaml_file'] == None:
        args_dict['yaml_file'] = DEFAULT_YAML_FILE

    test = stdParams(args_dict['yaml_file'])

    pdb.set_trace()