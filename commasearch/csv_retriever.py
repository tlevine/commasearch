import re
from urllib.parse import urlsplit
from io import StringIO
import requests

def retrieve_csv(url:str):
    transporters = {
        'file': lambda url: open(re.sub(r'^file://', '', url), 'r'),
        'http': lambda url: StringIO(requests.get(url).text),
    }
    transporters['https'] = transporters['http']
    def other(scheme):
        raise ValueError('The %s:// scheme is not supported' % scheme)
    return transporters.get(urlsplit(url).scheme, other)(url)
