'''
Why am I not writing this in Haskell!?
'''
import os
import csv
import special_snowflake
from pickle_warehouse import Warehouse

# Database
HOME = os.path.expathuser('~')
INDICES = Warehouse(os.path.join(HOME, '.,', 'indices'))
VALUES = lambda index: Warehouse(os.path.join(HOME, '.,', 'values', str(hash(index))))

def index(fp):
    # Find the unique keys.
    indices = special_snowflake.fromcsv(fp)

    # Get the hashes of all the values.
    

    # Check for overlaps between these datasets.

    # Emit the datasets with the highest overlap.

def unique_keys(dictreader:iter) -> set:
    '''
    dictreader :: [dict str a] -> {str}

    Find the unique keys in a dataset.
    '''

def histograms(unique_indices:set, dictreader:iter) -> dict:
    '''
    The resulting dict will be formatted like this. ::

        {("column1",): Counter({8:23,7:2,9:17}),
         ("column2","column4"): Counter({(3,8):42}),
        }
    '''
