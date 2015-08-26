#
# pat/pat.py
#
"""
Pat module providing the 'main' pat repo-accessor-class, Pat
"""

import os


class Pat:
    """
    The main class of the pat project - providing the abstraction and interface
    around pat/dat repositories.
    """

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

        opts.get()

        if path:
            self.open(path)

    def open(self, path):
        """
        Opens the pat container located at path
        """

        path = os.path.absdir(path)
