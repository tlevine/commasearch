'''
Why am I not writing this in Haskell!?
'''
import csv

def index(fp):
    pass

def unique_keys(dictreader:iter) -> set:
    '''
    dictreader :: [dict str a] -> {str}

    Find the unique keys in a dataset.
    '''

def column_histograms(unique_indices:set, dictreader:iter) -> dict:
    '''
    The resulting dict will be formatted like this. ::

        {("column1",): { "ndigit": Counter({8:23,7:2,9:17}),
                         "nlowercase": Counter({0:37,1:5})},
         ("column2",): { "ndigit": Counter({0:42}),
                         "nlowercase": Counter({2:37,1:5})},
        }
    '''
