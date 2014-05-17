import os
import csv
import sys
import argparse

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

def main(stdin = sys.stdin, stdout = sys.stdout, stderr = sys.stderr):
    p = parser().parse_args()
    if p.filenames == ['-']:
        filenames = stdin
    else:
        filenames = p.filenames

    paths = map(os.path.abspath, filenames)

    if p.index:
        for path in paths:
            if p.force or (path not in db.indices):
                index(path)
    else:
        path = next(paths)
        try:
            next(paths)
        except StopIteration:
            pass
        else:
            stderr.write('Warning: Using only the first file\n')
        if p.verbose:
            writer = csv.writer(stdout)
            writer.writerow(('index', 'result_path', 'overlap_count'))
            writer.writerows(search(path))
        else:
            for _, result_path, _ in search(path):
                stdout.write('/%s\n' % result_path)
