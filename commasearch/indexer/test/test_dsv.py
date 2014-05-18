from io import StringIO

import nose.tools as n

def test_guess_dialect():
    empty = StringIO('')
    n.assert_equal(guess_dialect(empty), 'excel')

    interesting = StringIO('a;b;c\r\n3;";";8\r\n')
    n.assert_equal(guess_dialect(interesting), 8)
