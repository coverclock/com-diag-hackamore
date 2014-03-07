"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import logging
import threading

NAME = "com.diag.hackamore"
LEVEL = logging.INFO

defaultlogger = None
mutex = threading.Condition()

def logger(name = NAME, level = LEVEL, handler = None):
    global defaultlogger
    with mutex:
        if defaultlogger == None:
            defaultlogger = logging.getLogger(name)
            defaultlogger.setLevel(level)
            handler = logging.StreamHandler() if handler == None else handler
            defaultlogger.addHandler(handler)
    return defaultlogger
