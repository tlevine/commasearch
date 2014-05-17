import os
import argparse

from commasearch.indexer import index as _index
from commasearch.searcher import search as _search
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
    p = argparse.ArgumentParser()
#   p.add_argument('--index',
#   p.add_argument('--force',
#   p.add_argument('csv file',

def main():
    p = parser()
    path = os.abspath(filename)
