from io import StringIO

import nose.tools as n

import commasearch.indexer.dsv as dsv

def test_guess_dialect():
    empty = StringIO('')
    n.assert_equal(dsv.guess_dialect(empty), 'excel')

    interesting = StringIO('a;b;c\r\n3;";";8\r\n')
    dialect = dsv.guess_dialect(interesting)
    observed = tuple(getattr(dialect, attr) for attr in ('delimiter', 'doublequote', 'escapechar', 'lineterminator', 'quotechar', 'quoting', 'skipinitialspace'))
    expected = (';', False, None, '\r\n', '"', 0, False)
    n.assert_tuple_equal(observed, expected)


