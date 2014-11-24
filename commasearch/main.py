import os
import json
import sys
import argparse
from urllib.parse import urlsplit
from logging import getLogger
from multiprocessing import Process
from functools import partial

import xapian

from commasearch.worker import index, search

logger = getLogger('commasearch')
dbpath = os.path.expanduser('~/.,')

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
    nice -n 19 'pluplusch --urls | , --index -'

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

def comma(p, dbpath = dbpath, stdin = sys.stdin, stdout = sys.stdout, stderr = sys.stderr):
    if p.tables == ['-']:
        tables = stdin
    else:
        tables = p.tables
    if p.index:
        for url in urls:
