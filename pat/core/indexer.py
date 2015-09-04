#
# pat/core/indexer.py
#

import os
from platform import system


class Indexer:
    """
    I have no idea what this does!
    """

    sockpath_default_platform = {
        'Windows': r'\\.\pipe\dat\\',
        'Linux': '.',
    }

    db = None
    db_path = ''
    checkout = None

    data = None
    changes = 0

    main_layer = None
    heads = None
    _pending = None
    _looping = None

    def __init__(self, path='.', db=None, multiprocess=False, backend=None):

        self.db_path = os.path.join(path, 'leveldb')

        self._pending = []

        if db is not None:
            # ready(db, create_log(db), true)
            pass
        elif multiprocess is None and path is None or backend is not None:
            db = levelup(dbpath, {'db': backend})
            # ready(db, create_log(db), true)

        self.multiprocess = multiprocess({
            'sockpath': self.sockpath_default_platform[system()]
        })


    def create_log(self, db):
        meta = sublevel(db, 'meta')

        log = meta.get('log')

        if log and log.split(':')[0:-1].join(':'):
            return on_log()

        log = path + ":" + cuid()

        meta.put('log', log)


        return hyperlog(sublevel(db, 'log'), {'getId': getId})


    def create_db(self):
        return levelup(self.dbpath, {db: self.backend})


    def add(self, links, value):

        node = self.log.add(links, messages.Commit.encode(value))
        (node, layer) = self._flush_node(node)
        if self.checkout and (self.checkout in node.links):
            self.meta.batch([{'type': 'put',
                              'key': 'layer',
                              'value': layer},
                             {'type': 'del',
                              'key': 'checkout'}])
            self.main_layer = layer
        return node, layer

    def get(self, hash_):
        return self.log.get(hash_)

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

        db = sublevel(subleve(self.db, 'log'), 'nodes')

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

        #wtf is loop?
        self.loop(False, self.loop(True))
