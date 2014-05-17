import commasearch.db as db
from commasearch.indexer import index

def search(search_path:str):
    'Search for a file, given its absolute path.'

    # Index the file first.
    index(search_path)

    # Then look up its indices.
    indices = db.indices[search_path]

    # Then look for things that have high overlap.
    for i in indices:
        search_values = db.values(i)[search_path]
        overlaps = [(len(search_values.intersection(search_values)), result_path) for (result_path, result_values) in db.values(i).items()]
        for overlap_count, path in sorted(overlaps)[:5]:
            yield i, path, overlap_count

