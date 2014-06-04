import itertools

import nose.tools as n
n.assert_list_equal.__self__.maxDiff = None

from commasearch.searcher import search
from commasearch.test.mockdb import mockdb

def test_search_not_indexed():
    db = mockdb()
    url = 'postgres://tlevine:password@dada.pink/bar'
    with n.assert_raises(ValueError):
        next(search(db, url))

@n.nottest
def test_search_indexed():
    db = populated_db()
    fn = 'file:///home/tlevine/ChickWeight.csv'
    db.indices = {
        'file:///home/tlevine/ChickWeight Subset.csv': {('Id',),('Chick','Time')},
        'file:///home/tlevine/ChickWeight.csv': {('Chick','Time',)},
        'file:///home/tlevine/iris subset.csv': {('',)},
        'file:///home/tlevine/irises.csv': {('Id',)},
        'file:///home/tlevine/iris.csv': {('',)},
    } 
    db.values.values = {
        ('',): {
            'file:///home/tlevine/iris subset.csv': set(map(tuple, '123')),
            'file:///home/tlevine/irises.csv': set(map(tuple, '123456789')),
            'file:///home/tlevine/iris.csv': set(map(tuple, '123456789')),
        },
        ('Chick', 'Time'): {
            'file:///home/tlevine/ChickWeight Subset.csv': {('2','1'),('2','2'),('2','3'),('2','4')},
            'file:///home/tlevine/ChickWeight.csv': set((str(i),str(j)) for i,j in itertools.product(range(4),range(20))),
        }
    }
    for fn, indices in db.indices.items():
        db.colnames[fn] = list(itertools.chain(*indices))
    db.colnames[fn] = ['Chick','Time','Diet','weight']
    observed = list(sorted(search(db, fn)))
    expected = [
        (('Chick', 'Time'), 'file:///home/tlevine/ChickWeight Subset.csv', 4),
        (('Chick', 'Time'), 'file:///home/tlevine/ChickWeight.csv', 80),
    ]
    n.assert_list_equal(observed, expected)

def populated_db():
    db_contents = [{
        'url': 'postgres://tlevine:password@dada.pink/bar',
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
    for table in db_contents:
        db.indices[table['url']] = set(table['data'].keys())
        for index, values in table['data'].items():
            db.values(index)[table['url']] = set(map(hash, values))
    return db
