from io import StringIO

import nose.tools as n

def test_guess_dialect():
    empty = StringIO('')
    n.assert_equal(guess_dialect(empty), 'excel')
