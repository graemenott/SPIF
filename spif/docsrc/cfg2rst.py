
"""
Function to convert config file designed for reading with ConfigParser to
restructured text for integration into documentation

"""

import configparser
import os.path
import pdb


__author__ = 'graeme.nott@faam.ac.uk'
__date__ = '2021 03 14'
__version__ = '0.1'
__all__ = ['ncParam',
           'main']

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
        return f"\n{self.group}\n{'-'*len(self.group)}\n"

    def _dimrst(self):
        """ Print attribute string block in rst format
        """
        return f"\t:dimension: \"{self.name}\" ;\n"

    def _attrrst(self):
        """ Print attribute string block in rst format
        """
        block = f"\t:{self.name}: "
        for attr, astr in self.attrs.items():
            block += f"\"{astr}\" ;\n\t"
        return block

    def _varrst(self):
        """ Print variable string block in rst format
        """
        try:
            block = f"\t|\t*{self.dtype}* **{self.name}**({', '.join(self.dims)})\n"
        except TypeError as err:
            # dims are None
            block = f"\t|\t*{self.dtype}* **{self.name}**\n"
        for attr, astr in self.attrs.items():
            block += f"\t|\t\t**{self.name}**:{attr} = \"{astr}\" ;\n"
        return block

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
def list_converter(s):
    s_list = s.split(',')
    return [None if _s.lower()=='none' else _s.strip() for _s in s_list]

# ----------------------------------------------------------------------
def main(cfg_file):

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
    pdb.set_trace()
    rst_list = []
    for i, param in enumerate(param_list):
        if i == 0:
            rst_list.append(param._grprst())
        elif param.group != param_list[i-1].group:
            rst_list.append(param._grprst())
        rst_list.append(param.rst)

    return '\n\n'.join(rst_list)


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
if __name__=='__main__':

    default_cfg = 'spif_mandatory.cfg'


    try:
        test = main(default_cfg)
    except:
        pdb.post_mortem()


    pdb.set_trace()