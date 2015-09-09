#
# pat/core/database.py
#
"""
Defines python interface for leveldb
"""

import leveldb
import os


class LevelDB:
    """
    Class which wraps the leveldb library in a pythonic manner, using methods
    similar to dict access and generators.

    :param path: Directory containing the database files
    :type path: str
    """

    def __init__(self, path, **opts):
        subdir = os.path.join(path, 'leveldb')
        if os.path.exists(subdir):
            path = subdir
        self.db = leveldb.LevelDB(path, **opts)
        self.path = path

    def key_iter(self):
        for x in self.db.RangeIter():
            yield x[0]

    def keys(self):
        return [key for key in self.key_iter()]

    def items(self):
        for k, v in self.db.RangeIter():
            yield (bytes(k), bytes(v))

    def __getitem__(self, key):
        return self.db.Get(key)

    def get(self, key, default=None):
        try:
            return self.db.Get(key)
        except KeyError:
            return default
