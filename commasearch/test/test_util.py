import nose.tools as n

import commasearch.util as u

def test_column_combinations():
    colnames = ('b', 'a', 'c')
    observed = set(u.column_combinations(colnames))
    expected = {('a',),('b',),('c',),('a','b',),('b','c',),('a','c'),('a','b','c')}
    n.assert_set_equal(observed, expected)
