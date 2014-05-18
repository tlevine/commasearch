import os
import csv
import sys
import argparse
from urllib.parse import urlsplit

from commasearch.indexer import index
from commasearch.searcher import search
import commasearch.db as db

def parser():
    p = argparse.ArgumentParser(description = 'Search with CSV files.')
    p.add_argument('-v', '--verbose', action = 'store_true', default = False,
        help = 'Print information about how search results were chosen.')
    p.add_argument('-i', '--index', action = 'store_true', default = False,
        help = 'Index the files; don\'t search.')
    p.add_argument('-f', '--force', action = 'store_true', default = False,
        help = 'Refresh the index of the specified files.')
    p.add_argument('filenames', metavar = '[csv file]', nargs = '+',
        help = 'CSV files to search or index, or "-" to read from STDIN')
    return p

def add_file_scheme(maybe_url):
    if urlsplit(maybe_url).scheme == '':
        url = 'file://' + os.path.abspath(maybe_url)
    else:
        url = maybe_url
    return url

def main(db = db, stdin = sys.stdin, stdout = sys.stdout, stderr = sys.stderr):
    p = parser().parse_args()
    if p.tables == ['-']:
        tables = stdin
    else:
        tables = p.tables

    urls = map(add_file_scheme, tables)

    if p.index:
        for url in urls:
            if p.force or (url not in db.indices):
                index(url)
    else:
        url = next(urls)
        try:
            next(urls)
        except StopIteration:
            pass
        else:
            stderr.write('Warning: Using only the first file\n')
        if p.verbose:
            writer = csv.writer(stdout)
            writer.writerow(('index', 'result_url', 'overlap_count'))
            writer.writerows(search(url))
        else:
            for _, result_url, _ in search(url):
                stdout.write('/%s\n' % result_url)
