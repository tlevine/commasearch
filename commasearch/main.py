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
    indices = db.indices[search_path]

    # Then look for things that have high overlap.
    for i in indices:
        search_values = db.values(i)[search_path]
        overlaps = [(len(search_values.intersection(search_values)), result_path) for (result_path, result_values) in db.values(i).items()]
        for overlap_count, path in sorted(overlaps)[:5]:
            yield i, path, overlap_count

def index(absolute_path:str):
    db.indices[absolute_path] = _index(absolute_path)

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
