#
# pat/__init__.py
#
# flake8: noqa
#
"""
Pat module file.
"""

from .__meta__ import (
    version as __version__,
    date as __date__,
    author as __author__,
    author_email as __contact__,
    license as __license__
)


from . import core
from .pat import Pat

# get rid of pat.pat.Pat as that just looks silly/confusing
del pat
