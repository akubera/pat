#
# setup.py
#
"""
"""

from glob import glob
from imp import load_source
from setuptools import setup

PACKAGES = [
    'pat',
    'pat.core',
]

REQUIRES = [
    'python3-protobuf',
    'leveldb',
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

# load metadata from __meta__ file
metadata = load_source("metadata", "pat/__meta__.py")

setup(
    name="pat",
    packages=PACKAGES,
    version=metadata.version,
    author=metadata.author,
    author_email=metadata.author_email,
    license=metadata.license,
    install_requires=REQUIRES,
    description=__doc__.strip(),
    tests_require=TESTS_REQUIRE,
    classifiers=CLASSIFIERS,
    platforms='all',
    scripts=SCRIPTS,
)
