#!/usr/bin/env python3
#
# scripts/pat.py
#
"""
Main executable script of the pat-project
"""

import sys
from argparse import ArgumentParser


def parse_args(argv):
    parser = ArgumentParser('pat')
    return parser.parse_args(argv)


def main(argv):
    args = parse_args(argv)



if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
