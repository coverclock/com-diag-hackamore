"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import select

SELECT = 0.0

sources = { }

def get():
    global sources
    for source in select.select(sources.values(), None, None, SELECT)[0]:
        event = source.get()
        if event != None:
            yield event
