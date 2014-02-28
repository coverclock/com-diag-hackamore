"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import logging

NAME = "com.diag.hackamore"
LEVEL = logging.INFO

defaultlogger = None

def logger(name = NAME, level = LEVEL):
    global defaultlogger
    if defaultlogger == None:
        defaultlogger = logging.getLogger(name)
        defaultlogger.setLevel(level)
        console = logging.StreamHandler()
        defaultlogger.addHandler(console)
    return defaultlogger
