"""
SPIF compliance checker

"""



import yaml
import os.path
import re
import pdb


__author__ = 'graeme.nott@faam.ac.uk'
__date__ = '2021 11 18'
__version__ = '0.2'
__all__ = ['ncParam',
           'cfg2rst',
           'mandatory_params',
           'optional_params']

DEFAULT_CFG_FILES = {'mandatory': 'spif_mandatory_params.cfg',
                     'optional':  'spif_optional_params.cfg'}

ALLOWED_TYPES = {'grp': ['grp', 'grps', 'group', 'groups'],
                 'attr': ['attr', 'attrs', 'attribute', 'attributes'],
                 'dim': ['dim', 'dims', 'dimension', 'dimensions'],
                 'coord': ['coord', 'coords', 'coordinate', 'coordinates'],
                 'var': ['var', 'vars', 'variable', 'variables']}


"""

PLAN:
    - Read in spif parameters with param_parser -> dict
    - Read in netCDF file -> dict-like
    - Class ncParam() (rename) for formatting into strings
    - Class for checking, inputs both dicts?