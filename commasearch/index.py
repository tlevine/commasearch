'''
Why am I not writing this in Haskell!?
'''
import os
import csv
import special_snowflake
from pickle_warehouse import Warehouse
from thready import threaded

from commasearch.util import guess_dialect

# Database
HOME = os.path.expathuser('~')
INDICES = Warehouse(os.path.join(HOME, '.,', 'indices'))
VALUES = lambda index: Warehouse(os.path.join(HOME, '.,', 'values', str(hash(index))))

def index(absolute_filepath:str):
    '''
    Index a CSV file.
    '''
    with open(absolute_filepath, 'r') as fp:
        # Dialect of the CSV file
        dialect = dialect(fp))
    
        # Find the unique keys.
        indices = unique_keys(fp, dialect)

        # Save them to the database
        INDICES[absolute_filepath] = indices
    
        # Get the hashes of all the values.
        many_args = distinct_values(fp, dialect, indices)

        # Save them to the database threaded because it might go faster.
        def save_values(args):
            index, values = args
            VALUES(index)[absolute_filepath] = values
        threaded(many_args, save_values, max_queue = 0)

def unique_keys(fp, dialect) -> set:
    '''
    Find the unique keys in a dataset.
    '''
    pos = fp.tell()
    result = special_snowflake.fromcsv(fp, dialect = dialect)
    fp.seek(pos)
    return result

def distinct_values(fp, dialect, indices) -> set:
    '''
    Find the distinct values of an index in a csv file.
    '''
    result = {index: set() for index in indices}
    pos = fp.tell()
    reader = csv.DictReader(fp, dialect = dialect)
    for row in reader:
        for index in indices:
            result[index].add(hash(row[column] for column in index))
    fp.seek(pos)
    return result
