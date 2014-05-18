from urllib.parse import urlsplit

import commasearch.indexer.dsv as dsv
import commasearch.indexer.rdbms as rdbms

RBDMS_SCHEMES = {}
DSV_SCHEMES = {'http','https','file'}

def index(url:str):
    scheme = urlsplit(url).scheme
    if scheme in DSV_SCHEMES:
        result = dsv.index(url)
    elif scheme in RDBMS_SCHEMES:
        result = rdbms.index(url)
    else:
        raise ValueError('The scheme %s:// is not supported.')
    return result
