import os
import sys
import argparse

from commasearch.indexer import index
from commasearch.searcher import search
import commasearch.db as db

def parser():
    p = argparse.ArgumentParser(description = 'Search with CSV files.')
    p.add_argument('-i', '--index', action = 'store_true', default = False,
        help = 'Index the files; don\'t search.')
    p.add_argument('-f', '--force', action = 'store_true', default = False,
        help = 'Refresh the index of the specified files.')
    p.add_argument('filenames', metavar = '[CSV file(s)]', nargs = '*')
    return p

def main(stdin = sys.stdin, stdout = sys.stdout, stderr = sys.stderr):
    p = parser()
    if len(p.filenames) == 0:
        filenames = stdin
    else:
        filenames = p.filenames

    paths = map(os.abspath, filenames)

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
                stdout.write(result_path + '\n')
