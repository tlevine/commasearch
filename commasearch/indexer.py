'''
Why am I not writing this in Haskell!?
'''
import csv
import special_snowflake
from thready import threaded

from commasearch.util import guess_dialect
import commasearch.db as db

def index_csv(fp, url:str):
    '''
    Index a CSV file.
    '''
    # Dialect of the CSV file
    dialect = guess_dialect(fp)
    
    # Find the unique keys.
    indices = unique_keys(fp, dialect)

    # Save them to the database
    db.indices[absolute_filepath] = indices
    
    # Get the hashes of all the values.
    many_args = distinct_values(fp, dialect, indices)

    # Save them to the database threaded because it might go faster.
    def save_values(args):
        index, values = args
        db.values(index)[absolute_filepath] = values
    threaded(many_args.items(), save_values, max_queue = 0)

def unique_keys(fp, dialect) -> set:
    '''
    Find the unique keys in a dataset.
    '''
    pos = fp.tell()
    result = special_snowflake.fromcsv(fp, dialect = dialect)
    fp.seek(pos)
    return result

def distinct_values(fp, dialect, indices) -> dict:
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
