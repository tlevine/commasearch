from io import StringIO
from traceback import print_exc

def traceback():
    not_file = StringIO()
    print_exc(file = not_file)
    return not_file.getvalue()
