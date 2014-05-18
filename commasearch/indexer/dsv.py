'''
Why am I not writing this in Haskell!?
'''
import csv
import re
from urllib.parse import urlsplit
from io import StringIO

import special_snowflake
from thready import threaded
import requests

def index(db, url:str):
    fp = retrieve_csv(url)
    if fp != None:
        index_csv(db, fp, url)

def guess_dialect(fp):
    'Guess the dialect of a CSV file.'
    pos = fp.tell()
    try:
        dialect = csv.Sniffer().sniff(fp.read(1024))
    except csv.Error:
        dialect = 'excel' # the default
    fp.seek(pos)
    return dialect

def http_transporter(url):
    response = requests.get(url)
    if response.ok:
        return StringIO(response.text)

def gettransporters():
    t = {
        'file': lambda url: open(re.sub(r'^file://', '', url), 'r'),
        'http': http_transporter,
    }
    t['https'] = t['http']
    return t

def retrieve_csv(url:str, transporters = gettransporters()):
    def other(scheme):
        raise ValueError('The %s:// scheme is not supported' % scheme)
    return transporters.get(urlsplit(url).scheme, other)(url)

def index_csv(db, fp, url:str):
    '''
    Index a CSV file.
    '''
    # Dialect of the CSV file
    dialect = guess_dialect(fp)
    
    # Find the unique keys.
    indices = unique_keys(fp, dialect)

    # Save them to the database
    db.indices[url] = indices
    
    # Get the hashes of all the values.
    many_args = distinct_values(fp, dialect, indices)

    # Save them to the database threaded because it might go faster.
    def save_values(args):
        index, values = args
        db.values(index)[url] = values
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
            result[index].add(hash(tuple(row[column] for column in index)))
    fp.seek(pos)
    return result
