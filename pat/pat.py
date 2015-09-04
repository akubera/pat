#
# pat/pat.py
#
"""
Pat module providing the 'main' pat repo-accessor-class, Pat
"""

import os
import asyncio
import leveldb
from .core.indexer import Indexer

class Pat:
    """
    The main class of the pat project - providing the abstraction and interface
    around pat/dat repositories.
    """

    FOLDER_NAME = 'data.dat'

    head = None

    opened = False

    in_checkout = False

    def __init__(self, path=None, **opts):
        """
        Constructor

        :param path: If specified, this will automatically open the pat
                    repository located in this directory
        :type path: str

        """

        self.value_encoding = opts.pop('value_encoding', 'binary')
        self.head = None

        self._layers = []
        self._layer_change = 0
        self._layer_key = None
        self._lock = asyncio.Lock()
        self._index = None

        path = os.path.abspath(path)

        should_create = opts.get('create_if_missing', False)

        if 'db' in opts:
            self._index = Indexer({
                'db': opts['db'],
                'path': os.path.join(path, FOLDER_NAME)
            })
        elif path:
            self.open(path, create_if_missing=should_create)
        else:
            raise ValueError("Invalid path")

        checkout = self._index.expand(opts['checkout'])

        if opts['persistent']:
            self._index.changeCheckout(checkout)

        checkout = checkout or self._index.checkout
        if checkout:
            checkout = self._index.expand(checkout)
            self.in_checkout = True
            layers = self._get_layers(self._index, checkout)
            self.head = checkout
            self._layers = layers
            self._layer_change = layers[0][0]
            self._layer_key = layers[0][1]

        elif 'layer' in opts:
            self.in_checkout = True
        elif self._index.main_layer:
            pass

    def open(self, path, create_if_missing=False):
        """
        Opens the pat container located at path
        """
        dat_path = os.path.join(path, FOLDER_NAME)
        if not os.path.exists(dat_path):
            if not create_if_missing:
                raise Exception("File does not exist : %s" % (dat_path))
            # TODO: Make datpath

        self._index = Indexer({
            'path': dat_path,
            'backend': leveldb,
            'blobs': None,
            'multiprocess': False
        })

    def _get_layers(self, index, head):
        pass
