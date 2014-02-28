"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import select

SELECT = 1.0
EMPTY = ( )

sources = { }

def register(source):
    global sources
    if source.fileno() >= 0:
        sources[source.name] = source

def unregister(source):
    global sources
    if source.name in sources:
        del sources[source.name]
        
def deregister():
    global sources
    sources = { }

def active():
    return True if sources else False

def query(name):
    global sources
    if name in sources:
        return sources[name]
    
def service(timeout = SELECT):
    global sources
    candidates = sources.values()
    for source in select.select(candidates, EMPTY, EMPTY, timeout)[0]:
        source.service()

def multiplex(timeout = SELECT):
    global sources
    candidates = sources.values()
    delay = 0.0
    while candidates:
        for source in select.select(candidates, EMPTY, EMPTY, delay)[0]:
            source.service()
        active = False
        for source in candidates:
            event = source.get(True)
            if event != None:
                active = True
                yield event
        delay = 0.0 if active else timeout
