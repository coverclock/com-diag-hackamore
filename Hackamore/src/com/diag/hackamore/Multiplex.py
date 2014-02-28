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

def multiplex(timeout = SELECT):
    global sources
    candidates = sources.values()
    for source in select.select(candidates, EMPTY, EMPTY, timeout)[0]:
        source.service()
    for source in candidates:
        event = source.get(True)
        if event != None:
            yield event
