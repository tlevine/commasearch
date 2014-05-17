import os
import sys
import argparse

from commasearch.indexer import index as _index
import commasearch.db as db

def search(search_path:str):
    'Search for a file, given its absolute path.'

    # Index the file first.
    index(search_path)

    # Then look up its indices.
    search_path = os.abspath(filename)
    indices = db.indices[path]

    # Then look for things that have high overlap.
    for i in indices:
        search_values = db.values(i)[search_path]
        overlaps = [(len(search_values.intersection(search_values)), result_path) for (result_path, result_values) in db.values(i).items()]
        for overlap_count, path in sorted(overlaps)[:5]:
            yield i, path, overlap_count

def index(path:str):
    'Index a file, given its absolute path.'
    if path not in db.indices:
        _index(path)

def parser():
    p = argparse.ArgumentParser(description = 'Search with CSV files.')
    p.add_argument('-i', '--index', action = 'store_true', default = False,
        help = 'Index the files; don\'t search.')
    p.add_argument('-f', '--force', action = 'store_true', default = False,
        help = 'Refresh the index of the specified files.')
    p.add_argument('filenames', metavar = '[CSV file(s)]', nargs = '*')
    return p

def main(fp_in = sys.stdin, fp_out = sys.stdout):
    p = parser()
    if len(p.filenames) == 0:
        filenames = fp_in
    else:
        filenames = p.filenames
    paths = map(os.abspath, filenames)

    if p.index:
        for path in paths:
            index(path)
    else:
        if p.verbose:
            writer = csv.writer(fp_out)
            writer.writerow(('index', 'result_path', 'overlap_count'))
            writer.writerows(search(next(paths)))
        else:
            for _, result_path, _ in search(next(paths)):
                fp.write(result_path + '\n')
