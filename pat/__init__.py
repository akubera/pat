#
# pat/__init__.py
#
# flake8: noqa
#
"""
Pat module file.
"""


__version__ = '0.0.0'
__date__ = 'Aug 17, 2015'
__author__ = 'Andrew Kubera'
__author_email__ = 'andrewkubera@gmail.com'
__license__ = '???'

from . import core
from .pat import Pat

# get rid of pat.pat.Pat as that just looks silly/confusing
del pat
