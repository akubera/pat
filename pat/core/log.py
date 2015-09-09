#
# pat/core/log.py
#

from cuid import cuid
from .sublevel import SubLevel
from .hyperlog_pb import (
    Node,
)


class Log:
    """
    Replacement for the nodejs hyperlog 'class'
    """

    ID = '!!id'
    CHANGES = '!changes!'
    NODES = '!nodes!'
    HEADS = '!heads!'

    def __init__(self, db):
        self.db = db
        self.log = SubLevel(self.db, 'log')
        self.meta = SubLevel(self.db, 'meta')

    def get_id(self):
        log = self.meta.get('log')
        if log:
            split_log = log.split(":")
            path = ':'.join(split_log[:-1])

            if (not path and not self.db.path) or path == self.db.path:
                return log.split(':')
        log = '%s:%s' % (self.db.path, cuid())

    def get(self, key, **opts):
        buf = bytes(self.log[self.NODES + key])
        node = Node.FromString(buf)
        return node

    def items(self, **opts):
        # since = opts.pop('since', 0)
        # until = opts.pop('until', 0)

        for key, val in self.log.items():
            yield key, val

    def nodes(self):
        for k, v in self.log.matching(self.NODES):
            node = Node.FromString(v)
            yield node
