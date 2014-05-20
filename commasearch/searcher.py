def search(db, search_url:str):
    'Search for table once you have indexed it.'

    # Index the file first.
    if search_url not in db.indices:
        raise ValueError('The table must be indexed before you can search it. (%s)' % search_url)

    # Then grab column combinations.
    colnames = db.colnames[search_url]
    indices = map(sorted, (itertools.chain(*(itertools.combinations(columns, i) for i in range(1, len(columns) + 1)))))

    # Then look for things that have high overlap.
    for i in indices:
        search_values = db.values(i)[search_url]
        overlaps = [(len(search_values.intersection(result_values)), result_url) for (result_url, result_values) in db.values(i).items()]
        for overlap_count, url in overlaps:
            yield overlap_count, i, url
