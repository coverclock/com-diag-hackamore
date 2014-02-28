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

def multiplex(timeout = SELECT):
    global sources
    for source in select.select(sources.values(), EMPTY, EMPTY, timeout)[0]:
        event = source.get()
        if event != None:
            yield event
