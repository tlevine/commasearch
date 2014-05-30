from urllib.parse import urlsplit
import commasearch.db as db

import commasearch.dsv_indexer as dsv
import commasearch.rdbms_indexer as rdbms

RBDMS_SCHEMES = {}
DSV_SCHEMES = {'http','https','file'}

def index(url:str):
    scheme = urlsplit(url).scheme
    if scheme in DSV_SCHEMES:
        result = dsv.index(db, url)
    elif scheme in RDBMS_SCHEMES:
        result = rdbms.index(db, url)
    else:
        raise ValueError('The scheme %s:// is not supported.')
    return result
