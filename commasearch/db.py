import os
import re, json
from functools import partial

from pickle_warehouse import Warehouse

home = os.path.expanduser('~')
errors = Warehouse(os.path.join(home, '.,', 'errors'))
columns = Warehouse(os.path.join(home, '.,', 'columns'))

def _subtable(name, ncol):
    return Warehouse(os.path.join(home, '.,', name, ncol))
combinations = partial(_subtable, 'combinations')
permutations = partial(_subtable, 'combinations')
