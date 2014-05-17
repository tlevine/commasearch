from urllib.parse import urlsplit

RBDMS_SCHEMES = {}
CSV_SCHEMES = {'http','https','file'}

def separate_scheme(url:str) -> str:
    return 'file://' + url if urlsplit(url).scheme == '' else url

def index(url:str):
    if 
