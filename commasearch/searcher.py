import commasearch.db as db
from commasearch.indexer import index

def search(search_url:str):
    'Search for a file, given its url.'

    # Index the file first.
    if search_url not in db.indices:
        index(search_url)

    # Then look up its indices.
    indices = db.indices[search_url]

    # Then look for things that have high overlap.
    for i in indices:
        search_values = db.values(i)[search_url]
        overlaps = [(len(search_values.intersection(search_values)), result_url) for (result_url, result_values) in db.values(i).items()]
        for overlap_count, url in sorted(overlaps)[:5]:
            yield i, url, overlap_count

