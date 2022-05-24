
from vocal.schema_types import *

# Add your attribute default values here:

"""
Uncomment when spif-std moved into spif repo
--------------------------------------------
from .. import spif
SPIF_MAJOR_VERSION = spif.__version_major__
SPIF_MINOR_VERSION = spif.__version_minor__
"""
SPIF_MAJOR_VERSION = 0
SPIF_MINOR_VERSION = 9


default_global_attrs = {
    'SPIF_MAJOR_VERSION': SPIF_MAJOR_VERSION,
    'SPIF_MINOR_VERSION': SPIF_MINOR_VERSION
}

default_group_attrs = {}
default_variable_attrs = {}
