"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import sys

def printf(fmt, *args):
    sys.stdout.write(fmt % args)
