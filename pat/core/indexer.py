#
# pat/core/indexer.py
#

import os
from platform import system
from .database import LevelDB
from .sublevel import SubLevel
from .log import Log
from .messages import (
    Commit,
)


class Indexer:
    """
    I have no idea what this does!
    """

    sockpath_default_platform = {
        'Windows': '\\\\.\\pipe\\dat\\',
        'Linux': 'dat.sock',
        'Darwin': 'dat.sock',
    }

    sockpath = sockpath_default_platform[system()]

    db = None
    db_path = ''
    checkout = None

    data = None
    changes = 0

    main_layer = None
    heads = None
    _pending = None
    _looping = None

    def __init__(self, path='.', db=None, multiprocess=False):

        self._pending = []

        if db is not None:
            self.db = db
        else:
            db_path = os.path.join(path, 'leveldb')
            self.db = LevelDB(db_path)

        self.meta = SubLevel(self.db, 'meta')
        self.data = SubLevel(self.db, 'data')
        self.commit = SubLevel(self.db, 'commit')
        self.operations = SubLevel(self.db, 'operations')

        self.log = Log(self.db)

        self.mainlayer = self.meta['layer']
        # print(self.mainlayer)
        changes = int(self.meta['changes'], 10)
        # print('changes:', changes)

        try:
            self.checkout = self.meta['checkout']
        except KeyError:
            self.checkout = None


    def add(self, links, value):

        node = self.log.add(links, Commit.encode(value))
        (node, layer) = self._flush_node(node)
        if self.checkout and (self.checkout in node.links):
            self.meta.batch([{'type': 'put',
                              'key': 'layer',
                              'value': layer},
                             {'type': 'del',
                              'key': 'checkout'}])
            self.main_layer = layer
        return node, layer

    def get(self, hsh):
        node = self.log.get(hsh)
        return node, Commit.FromString(node.value)

    def flush(self):
        if self.changes < self.log.changes:
            self._pending.append([self.log.changes, None])

    def _flush_node(self, node):
        if self.changes < node.change:
            self._pending.append([node.change, node])
        else:
            layer = self.layers.get(node.key)
            return node, layer

    def change_checkout(self, head):

        if head:
            self.meta.put('checkout', head)
        else:
            self.meta.delete('checkout')

        self.checkout = head or None

    def expand(self, hash_):

        if len(hash_) < 16:
            raise ValueError("Checkout hash must be at least 16 characters")
        elif len(hash_) >= 64:
            return self.get(hash_)

        db = sublevel(sublevel(self.db, 'log'), 'nodes')

        keys = db.create_key_stream({
            'gt': hash_,
            'lt': hash_ + '\xff',
            'limit': 1
        })

        result = keys()

        if not result:
            raise Exception("Could not expand the hash")
        return self.get(result)

    def start(self):
        layer = self.meta.get('layer')
        if layer:
            self.mainlayer = layer

        # wtf is loop?
        self.loop(False, self.loop(True))

    @property
    def db_path(self):
        return self.db.path
