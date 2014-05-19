import os
import re, json

from pickle_warehouse import Warehouse

home = os.path.expanduser('~')
indices = Warehouse(os.path.join(home, '.,', 'indices'))
values = lambda index: Warehouse(os.path.join(home, '.,', 'values', re.sub(r'[\/]', '|', json.dumps(index))))
