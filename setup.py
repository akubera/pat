#
# setup.py
#
"""
"""

import pat
from glob import glob
from setuptools import setup, find_packages

REQUIRES = [
]

TESTS_REQUIRE = [
    'pytest',
]

SCRIPTS = glob('scripts/*')

CLASSIFIERS = [
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Natural Language :: English",
]


setup(
    name="pat",
    version=pat.__version__,
    author=pat.__author__,
    author_email=pat.__author_email__,
    license=pat.__licence__,
    install_requires=REQUIRES,
    description=__doc__.strip(),
    tests_require=TESTS_REQUIRE,
    classifiers=CLASSIFIERS,
    platforms='all',
    scripts=SCRIPTS,
)
