"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import sys

def fprintf(stream, fmt, *args):
    """
    Format and print an argument list to the specified stream.
    @param stream is the output stream.
    @param fmt is the format string.
    @param args is the argument list.
    @return the value returned by write().
    """
    return  stream.write(fmt % args)

def printf(fmt, *args):
    """
    Format and print an argument list to the Standard Output stream.
    @param fmt is the format string.
    @param args is the argument list.
    @return the value returned by write().
    """
    return sys.stdout.write(fmt % args)
