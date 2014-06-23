import os
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

def test_hashcells():
    cells1 = ['aoeu','aoeuaeu','hnthrth']
    cells2 = ['aoeuaoeuaeu','hnthrth']
    n.assert_equal(dsv.hashcells(cells1), '0e1eeef622197ea61b636dd764200e14')
    n.assert_equal(dsv.hashcells(cells1), dsv.hashcells(cells2))

def test_explode():
    columns = [
        'aaatoml',
        'aacaaac',
        'ggguuua',
        'zgaoeub',
    ]
    expected = [Counter({
        '04cc5c04ee96b97f7ebd31d900d4048b': 1,
        '1c277f8972b086747c4737802dd2df18': 1,
        '2da392699470ab19e730fa58783c4acf': 1,
        '4a1655ec6fbe9bfff38e6aebd73f5894': 1,
        '68088f1de36dd961badf175e8d836a56': 1,
        'a0ecacbdd2a98a50ac163c0398fe5bf2': 1,
        'a1598b7898ce80bc8d403960b63dfb55': 1,
    })]
    observed = dsv.explode(lambda x,n: [x,x], columns, n)
    n.assert_equal(len(observed), 2)
    n.assert_equal(len(observed[0]), 7)
    n.assert_list_equal(observed, expected * 2)
