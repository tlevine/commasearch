'''
Why am I not writing this in Haskell!?
'''
import csv

def index(fp):
    pass
    # Find the unique keys and the histograms within the unique keys.

    # Choose the datasets with the same unique keys.

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
