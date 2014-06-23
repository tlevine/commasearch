import os
import re, json

from pickle_warehouse import Warehouse

home = os.path.expanduser('~')
errors = Warehouse(os.path.join(home, '.,', 'errors'))
columns = Warehouse(os.path.join(home, '.,', 'columns'))
def multicolumns(ncol):
    return Warehouse(os.path.join(home, '.,', 'multicolumns', ncol))

