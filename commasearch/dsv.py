'''
Why am I not writing this in Haskell!?
'''
from collections import Counter
from hashlib import md5
import csv
import re
from urllib.parse import urlsplit
from io import StringIO
from logging import getLogger
from functools import partial
from itertools import combinations, permutations, count

from thready import threaded
import requests

from commasearch.util import traceback, column_combinations

logger = getLogger('commasearch')

WIDEST_MULTICOL = 3

def _download(func, db, url:str):
    if url not in db.errors:
        fp = retrieve_csv(url)
        if fp == None:
            db.errors[url] = True
            logger.error('Could not load %s' % (url))
        else:
            result = func(db, fp, url)
            return result
   
def _index(db, fp, url:str):
    '''
    Index a CSV file.
    '''
    # Open the file with the appropriate dialect.
    dialect = guess_dialect(fp)
    reader = csv.reader(fp, dialect = dialect)
    header = next(reader)

    # How many columns?
    ncol = len(header)

    # Get the hashes
    hashed_columns = [[]] * ncol
    for row in reader:
        for i, cell in enumerate(row):
            hashed_columns[i].append(md5(cell.encode('utf-8')).hexdigest())

    # Save multicolums
    def dohash(combination):
        return [md5(''.join(row).encode('utf-8')) for row in combination]
    def explode(explosion_func, hashed_columns, n):
        c = explosion_func(hashed_columns, n)
        return [dohash(explosion) for explosion in c]

    for n in range(1, min(WIDEST_MULTICOL, ncol) + 1):
        db.combinations(n)[url] = explode(combinations, hashed_columns, n)
        db.permutations(n)[url] = explode(permutations, hashed_columns, n)

    # Save columns last so we can use this to check completeness.
    db.columns[url] = hashed_columns

def _search(db, fp, search_url:str):
    '''
    Search for table.
    '''

    # Index the file first.
    if search_url not in db.columns:
        raise ValueError('The table must be indexed before you can search it. (%s)' % search_url)

    # Then grab column permutations for this spreadsheet.
    this_url = search_url
    for ncol in count(1, 1):
        if this_url not in db.permutations(ncol):
            break
        these = list(map(Counter, db.permutations(ncol)[this_url]))
        for that_path, c in db.combinations(ncol):
            those = list(map(Counter, c))
            for this in these:
                for that in those:
                    yield {
                        'path': path,
                        'nrow': length(that),
                        'overlap': sum((this - that).values()),
                    }

index = partial(_download, _index)
search = partial(_download, _search)

# Utilities follow.

def get_colnames(fp, dialect) -> list:
    pos = fp.tell()
    reader = csv.reader(fp, dialect = dialect)
    result = next(reader)
    fp.seek(pos)
    return result

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
    try:
        response = requests.get(url)
    except Exception as e:  
        logger.error('Error downloading %s:\n%s' % (url,traceback()))
    else:
        if response.ok:
            return StringIO(response.text)
        else:
            logger.error('Status %d at %s' % (response.status_code, url))

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
