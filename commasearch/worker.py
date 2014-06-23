from urllib.parse import urlsplit
from functools import partial

from commasearch.util import traceback
import commasearch.dsv as dsv
import commasearch.rdbms as rdbms

RDBMS_SCHEMES = {'sqlite'}
DSV_SCHEMES = {'http','https','file'}

def work(function, db, stderr, url:str):
    try:
        results = _work(function, db, url)
    except:
        stderr.write('Error at %s:\n%s' % (url,traceback()))
    else:
        if function == 'search':
            return _emit_search_results(results)

def _work(function:str, db, url:str):
    '''
    function :: 'index' | 'search'
    '''
    scheme = urlsplit(url).scheme
    if scheme in DSV_SCHEMES:
        result = getattr(dsv, function)(db, url)
    elif scheme in RDBMS_SCHEMES:
        result = getattr(rdbms, function)(db, url)
    else:
        raise ValueError('The scheme %s:// is not supported.')
    return result

def _emit_search_results(results):
        for result in results:
            scheme, _, rest = result['path'].partition('/')
            result['url'] = '%s://%s' % (scheme, rest)
            del(result['path'])
            yield result

index = partial(work, 'index')
search = partial(work, 'search')
