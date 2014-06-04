from collections import Counter
from io import StringIO

import nose.tools as n

import commasearch.dsv as dsv
from commasearch.test.mockdb import mockdb

def test_guess_dialect():
    empty = StringIO('')
    n.assert_equal(dsv.guess_dialect(empty), 'excel')

    interesting = StringIO('a;b;c\r\n3;";";8\r\n')
    dialect = dsv.guess_dialect(interesting)
    observed = tuple(getattr(dialect, attr) for attr in ('delimiter', 'doublequote', 'escapechar', 'lineterminator', 'quotechar', 'quoting', 'skipinitialspace'))
    expected = (';', False, None, '\r\n', '"', 0, False)
    n.assert_tuple_equal(observed, expected)

def test_receive_csv():
    url = 'wumbo://spongebob:squarepants@sea/pineapple'
    observed = dsv.retrieve_csv(url, transporters = {'wumbo': lambda _: 88})
    n.assert_equal(observed, 88)

    with n.assert_raises(ValueError):
        dsv.retrieve_csv(url, transporters = {})

def test_index_csv():
    db = mockdb()
    fp = StringIO('Chick,Time\r\n1,1\r\n1,2\r\n1,3\r\n')
    url = 'http://big.dada.pink/ChickWeight.csv'

    dsv._index(db, fp, url)

    expected_index = ('Time',)
    n.assert_dict_equal(db.indices, {url: {expected_index}})
    n.assert_dict_equal(db.values(expected_index), {url: set(map(hash, [('1',),('2',),('3',)]))})
