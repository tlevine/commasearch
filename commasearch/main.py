import os
import csv
import sys
import argparse
from urllib.parse import urlsplit
from logging import getLogger

from thready import threaded

from commasearch.searcher import search
import commasearch.db as db
import commasearch.dsv_indexer as dsv
import commasearch.rdbms_indexer as rdbms

logger = getLogger('commasearch')

RBDMS_SCHEMES = {}
DSV_SCHEMES = {'http','https','file'}

def _index(url:str):
    scheme = urlsplit(url).scheme
    if scheme in DSV_SCHEMES:
        result = dsv.index(db, url)
    elif scheme in RDBMS_SCHEMES:
        result = rdbms.index(db, url)
    else:
        raise ValueError('The scheme %s:// is not supported.')
    return result

def parser():
    epilog = '''
Data tables are either paths to local files, links to files on
the web, or SQLAlchemy URLs to database tables. For example,

    , --index ../iris.csv /opt/ChickWeight.tsv \\
        postgres://tlevine:secretpassword@dada.pink/toilets \\
        http://big.dada.pink/scarsdale/assessments.csv

You should index a bunch of files before you search; otherwise,
the search won't be that interesting. To that end, you might run

    pip3 install pluplusch
    pluplusch --urls | , --index

This indexes files from data catalogs that pluplusch knows about.
'''
    p = argparse.ArgumentParser(description = 'Search with data tables.',
        epilog = epilog, formatter_class = argparse.RawDescriptionHelpFormatter)
    p.add_argument('-v', '--verbose', action = 'store_true', default = False,
        help = 'print information about how search results were chosen.')
    p.add_argument('-i', '--index', action = 'store_true', default = False,
        help = 'index the files; don\'t search.')
    p.add_argument('-f', '--force', action = 'store_true', default = False,
        help = 'refresh the index of the specified files.')
    p.add_argument('tables', metavar = '[data table]', nargs = '+',
        help = 'tables to search or index, or "-" to read from STDIN')
    return p

def add_file_scheme(maybe_url):
    if urlsplit(maybe_url).scheme == '':
        url = 'file://' + os.path.abspath(maybe_url)
    else:
        url = maybe_url
    return url

def main():
    p = parser().parse_args()
    comma(p)

def comma(p, db = db, stdin = sys.stdin, stdout = sys.stdout, stderr = sys.stderr):
    if p.tables == ['-']:
        tables = stdin
    else:
        tables = p.tables

    urls = map(add_file_scheme, tables)

    def index(url:str):
        if p.force or (url not in db.indices):
            if p.verbose:
                stdout.write('Indexing %s\n' % url)
            try:
                _index(url)
            except Exception as e:
                logger.error('Error at %s' % url)
                logger.error(e)

    if p.index:
        threaded(urls, index, num_threads = 50, max_queue = 1000)
    else:
        url = next(urls)
        try:
            next(urls)
        except StopIteration:
            pass
        else:
            stderr.write('Warning: Using only the first file\n')

        index(url)
        if p.verbose:
            writer = csv.writer(stdout)
            writer.writerow(('index', 'result_url', 'overlap_count'))
            writer.writerows(search(db, url))
        else:
            results = sorted(search(db, url), reverse = True)
            printed = {url} # Don't print the input url in the results.
            for overlap_count, _, result_path in results:
                scheme, _, rest = result_path.partition('/')
                result_url = '%s://%s' % (scheme, rest)
                if result_url not in printed:
                    stdout.write(result_url + '\n')
                    printed.add(result_path)
