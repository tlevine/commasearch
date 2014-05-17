import re
from urllib.parse import urlsplit
from io import StringIO
import requests

def retrieve_csv(url:str):
    transporters = {
        'file': lambda url: open(re.sub(r'^file://', '', url), 'r'),
        'http': lambda url: StringIO(requests.get(url).text),
    }
    urlsplit(url).scheme
    return fp
