"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import logging
import threading

NAME = "com.diag.hackamore"
LEVEL = logging.INFO

__defaultlogger__ = None
__mutex__ = threading.Condition()

def logger(name = NAME, level = LEVEL, handler = None):
    """
    Return a reference to a common Logger that can be used to log messages.
    If no such Logger already exists, create one to be used by subsequent
    requests.
    @param name is the name of the Logger if the Logger is created.
    @param level is the initial logging level if the Logger is created.
    @param handler is the initial logging handler if the Logger is created.
    @return a Logger.
    """
    global __defaultlogger__
    global __mutex__
    with __mutex__:
        if __defaultlogger__ == None:
            __defaultlogger__ = logging.getLogger(name)
            __defaultlogger__.setLevel(level)
            if handler == None:
                handler = logging.StreamHandler()
            __defaultlogger__.addHandler(handler)
        return __defaultlogger__
