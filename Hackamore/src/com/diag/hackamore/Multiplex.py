"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import select

import Logger

from Event import Event

SELECT = 1.0
NONE = ( )

class Multiplex:

    def __init__(self, logger = None):
        self.logger = Logger.logger() if logger == None else logger
        self.sources = { }
        self.logger.info("Multiplex: INIT. %s", str(self))
        
    def __del__(self):
        self.logger.info("Multiplex: FINI. %s", str(self))

    def __repr__(self):
        return "Multiplex(" + str(self.sources) + ")"
    
    def register(self, source):
        if source.fileno() >= 0:
            self.sources[source.pbx] = source
    
    def unregister(self, source):
        if source.pbx in self.sources:
            del self.sources[source.pbx]

    def deregister(self):
        self.sources = { }
    
    def active(self):
        return True if self.sources else False
    
    def query(self, pbx):
        if pbx in self.sources:
            return self.sources[pbx]
        
    def service(self, timeout = SELECT):
        candidates = [ candidate for candidate in self.sources.values() if candidate.fileno() >= 0 ]
        for source in select.select(candidates, NONE, NONE, timeout)[0]:
            source.service()
    
    def multiplex(self, timeout = SELECT):
        candidates = [ candidate for candidate in self.sources.values() if candidate.fileno() >= 0 ]
        effective = 0.0
        while candidates:
            for source in select.select(candidates, NONE, NONE, effective)[0]:
                source.service()
            active = False
            for source in candidates:
                event = source.get(self)
                if event != None:
                    active = True
                    message = Event(event, source.logger)
                    yield message
            effective = 0.0 if active else timeout
