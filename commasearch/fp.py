'''
Convert URLs into file-like objects.
'''
from io import StringIO
import urllib.parse

import requests

def getfp(url):
    return functions.get(urllib.parse.urlsplit(url).scheme, not_supported)(url)

def not_supported(url):
    msg = 'The %s:// scheme is not supported.'
    scheme = urllib.parse.urlsplit(url).scheme
    raise ValueError(msg % scheme)

def fromfile(url):
    _, almost_path = urllib.parse.splittype(url)
    path = almost_path[1:] # Remove a slash
    return open(path, 'r')

def fromhttp(url):
    response = requests.get(url)
    return StringIO(response.text)

functions = {
    'file': fromfile,
    'http': fromhttp,
    'https': fromhttp,
}
