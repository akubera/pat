#
# pat/core/sublevel.py
#

END = 0xff


class SubLevel:

    db = None

    def __init__(self, db, prefix='', separator='!', **opts):
        self.name = prefix
        prefix.strip(separator)
        self.prefix = ("{0}{1}".format(separator, prefix)).encode()
        self.delim = separator.encode()
        self.db = db

    def close(self, *args):
        self.leveldown.close(*args)

    def set_db(self, *args):
        self.leveldown.close(*args)

    def put(self, *args):
        self.leveldown.put(b"%s%s")

    def __getitem__(self, key):
        prefixed_key = self.delim.join((self.prefix, key.encode()))
        for k, v in self.db.items():
            if k.startswith(prefixed_key):
                return v
        raise KeyError("No such key '%s' in sublevel '%s'" % (key, self.name))

    def items(self):
        for key, val in self.db.items():
            if key.startswith(self.prefix):
                yield (key, val)

    def matching(self, key):
        prefixed_key = self.delim.join((self.prefix, key.encode()))
        for k, v in self.db.items():
            if k.startswith(prefixed_key):
                yield (k, v)
