import itertools

import nose.tools as n

from commasearch.searcher import search
from commasearch.test.mockdb import mockdb

def test_search_not_indexed():
    db = mockdb()
    with n.assert_raises(EnvironmentError):
      search(db, 'postgres://tlevine:password@dada.pink/bar')

def test_search_indexed():
    db = populated_db()
    observed = list(search(db, 'file:///home/tlevine/ChickWeight Subset.csv'))
    expected = []
    n.assert_list_equal(observed, expected)

def populated_db():
    db_contents = [{
        'url: 'postgres://tlevine:password@dada.pink/bar',
        'data': {
            ('a','b'): {'apple','pear'},
            ('c',): {'cow','pig'},
            ('d','e'): {'bucket-wheel excavator', 'dumptruck'},
        }
    },{
        'url': 'file:///home/tlevine/iris.csv',
        'data': { ('',): range(180) },
    },{
        'url': 'file:///home/tlevine/ChickWeight Subset.csv',
        'data': {
            ('',): range(2 * 12),
            ('Chick','Time'): itertools.product(range(2), range(12)),
         },
    },{
        'url': 'file:///home/tlevine/ChickWeight.csv',
        'data': {
            ('',): range(4 * 12),
            ('Chick','Time'): itertools.product(range(4), range(12)),
         },
    }]
    db = mockdb()
    for table in data:
        db.indices[url] = set(table.keys())
        for index, values in table.items():
            db.values[index] = set(map(hash, values))
    return db
