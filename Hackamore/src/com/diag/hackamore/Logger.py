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
    """
    Return a reference to a common Logger that can be used to log messages.
    If no such Logger already exists, create one to be used by subsequent
    requests.
    @param name is the name of the Logger if the Logger is created.
    @param level is the initial logging level if the Logger is created.
    @param handler is the initial logging handler if the Logger is created.
    @return a Logger.
    """
    global defaultlogger
    with mutex:
        if defaultlogger == None:
            defaultlogger = logging.getLogger(name)
            defaultlogger.setLevel(level)
            handler = logging.StreamHandler() if handler == None else handler
            defaultlogger.addHandler(handler)
        return defaultlogger
