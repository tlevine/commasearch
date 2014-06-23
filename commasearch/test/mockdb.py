import collections

class _values:
    def __init__(self):
        self.values = collections.defaultdict(lambda: {})
    def __call__(self, index):
        return self.values[index]

class mockdb:
    'Create an in-memory dict database that acts like the disk-backed database.'
    def __init__(self):
        self.indices = {}
        self.combinations = _values()
        self.permutations = _values()
        self.colnames = {}
        self.errors = {}
