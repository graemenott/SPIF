
# Import all dummy reader functions
from readers.dummy import *
from readers.dmt import *
from readers.spec import *

# List of data reader modules in reader/
__all__ = ['dummy_CIPgs',
           'CIPgs', 'CIP',
           'twoDS', 'CPI', 'HVPS']