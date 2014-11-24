
    urls = (add_file_scheme(table.rstrip('\r\n')) for table in tables)

    processes = {}
    def start_index_worker(url):
        if p.force or (url not in db.columns):
            if p.verbose:
                stderr.write('Indexing %s\n' % url)
            processes[url] = Process(None, target = index, args = (db, stderr, url), name = url)
            processes[url].start()

    if p.index:
        for url in urls:
            while sum(1 for process in processes.values() if process.is_alive()) > 10:
                pass
            start_index_worker(url)
    else:
        url = next(urls)
        try:
            next(urls)
        except StopIteration:
            pass
        else:
            stderr.write('Warning: Using only the first file\n')

        if url not in db.columns:
            index(db, stderr, url)
        for result in search(db, stderr, url):
            if url != result['url']: # Don't print the input url in the results.
                line = json.dumps(result) if p.verbose else result['url']
                stdout.write(line + '\n')
                stdout.flush()

