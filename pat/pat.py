#
# pat/pat.py
#
"""
Pat module providing the 'main' pat repo-accessor-class, Pat
"""

import os
import asyncio

from datetime import datetime
from .core.indexer import Indexer
from .core.database import LevelDB


class Pat:
    """
    The main class of the pat project - providing the abstraction and interface
    around pat/dat repositories.
    """

    FOLDER_NAME = 'data.dat'

    head = None

    opened = False

    in_checkout = False

    def __init__(self, path=None, db=None, **opts):
        """
        Constructor

        :param path: If specified, this will automatically open the pat
                     repository located in this directory
        :type path: str

        :param opts: extra options to
        """

        self.value_encoding = opts.pop('value_encoding', 'utf-8')
        self.head = None

        self._layers = []
        self._layer_change = 0
        self._layer_key = None
        self._lock = asyncio.Lock()
        self._index = None

        path = os.path.abspath(path)

        should_create = opts.get('create_if_missing', False)

        if db:
            self.db = db
            self._index = Indexer(db=db)
        elif path:
            self.open(path, create_if_missing=should_create)
        else:
            raise ValueError("Invalid path '%s'" % (path))

        # checkout = self._index.expand(opts['checkout'])

        # if opts['persistent']:
        #     self._index.changeCheckout(checkout)
        #
        # checkout = checkout or self._index.checkout
        # if checkout:
        #     checkout = self._index.expand(checkout)
        #     self.in_checkout = True
        #     layers = self._get_layers(self._index, checkout)
        #     self.head = checkout
        #     self._layers = layers
        #     self._layer_change = layers[0][0]
        #     self._layer_key = layers[0][1]
        #
        # elif 'layer' in opts:
        #     self.in_checkout = True
        # elif self._index.main_layer:
        #     pass

    def open(self, path, create_if_missing=False, **opts):
        """
        Opens the pat container located at 'path'
        """
        print("Path", path)
        dat_path = os.path.join(path, self.FOLDER_NAME)
        print("dat_path", dat_path)

        # create the database
        self.db = LevelDB(dat_path, create_if_missing=create_if_missing, **opts)

        if not os.path.exists(dat_path):
            if not create_if_missing:
                err_msg = "File does not exist : %s" % (dat_path)
                raise Exception(err_msg)
            # TODO: Make datpath

        self._index = Indexer(db=self.db)
        print("DONE")

    def _get_layers(self, index, head):
        pass

    def changes(self):
        for key, val in self._index.meta.matching('status'):
            commit_key = key.split(b'!')[-1].decode()
            commit = self._index.commit[commit_key]
            print(commit)
            yield {
                'id': commit_key,
                'modified': datetime.fromtimestamp(val.modified // 1000),
                'puts': val.puts,
                'deletes': val.deletes,
                'rows': val.rows,
                'files': val.files,
                'type': val.type,
            }

    def open_file(self, key):
        result = self.get(key)
        if result.content != 'file':
            raise ValueError("Key is not a file")
        elif not self._index.blobs:
            raise Exception("No blob store attached")
        return self._index.blobs.read(result.value.key)

    def open_writable_file(self, key):
        raise NotImplementedError()
