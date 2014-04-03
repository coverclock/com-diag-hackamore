"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import select

import Logger

from Event import Event

SELECT = 1.0
EMPTY = ( )

class Multiplex:
    """
    Multiplex is a container for a dynamically changing list of open Sources.
    This list is initially empty upon construction, but Sources are registered
    and unregistered with a Multiplex as they are opened and closed (by, for
    example, a Controller)  respectively. Multiplex uses the select(2) system
    call to multiplex I/O across its list of open Sources. It services each open
    Source by providing a generator function that returns an iterable list
    of Sources who have Events ready to be received.
    """

    #
    # CTOR/DTOR
    #

    def __init__(self, logger = None):
        self.logger = Logger.logger() if logger == None else logger
        self.sources = { }
        self.effective = 0.0

    def __del__(self):
        pass

    def __repr__(self):
        return "Multiplex(" + str(self.sources) + ")"

    #
    #  PUBLIC
    #
    
    def register(self, source):
        """
        Register a Source on the list of open Sources. The Source must return
        a valid file number usable by select(2).
        @param source is the open Source.
        """
        if source.fileno() >= 0:
            self.sources[source.pbx] = source
    
    def unregister(self, source):
        """
        Unregister a Source from the list of open Sources. The Source must be
        on the list indexed by the name of the Source (its "PBX").
        """
        if source.pbx in self.sources:
            del self.sources[source.pbx]

    def deregister(self):
        """
        Unregister all Sources from the list of open Sources. The list of open
        Sources will be empty after this call returns.
        """
        self.sources = { }
    
    def active(self):
        """
        Return True if there are Sources on the list of open Sources, False
        otherwise.
        @return True if there are open Sources, False otherwise.
        """
        return True if self.sources else False
    
    def query(self, pbx):
        """
        Return the Source identified by the specified PBX on the list of open
        Sources, or None if it does not exist.
        @param pbx is the name of the Source.
        @return an open Source named by the pbx or None.
        """
        if pbx in self.sources:
            return self.sources[pbx]
        
    def service(self, timeout = SELECT):
        """
        For each Source on the list of open Sources which has a valid file
        number (generally indicating it represents an open input/output resource
        in the underlying platform), service any pending I/O on that Source.
        It is only necessary to call this function if the caller is not using
        the Multiplex in the usual manner (for example, in unit testing).
        @param timeout is an optional select(2) timeout value in seconds.
        """
        candidates = [ candidate for candidate in self.sources.values() if candidate.fileno() >= 0 ]
        for source in select.select(candidates, EMPTY, EMPTY, timeout)[0]:
            source.service()
    
    def multiplex(self, timeout = SELECT):
        """
        For each Source on the list of open Sources which has a valid file
        number (generally indicating it represents an open input/output resource
        in the underlying platform), service any pending I/O on that Source,
        and then return the next available Event from that same list of Sources.
        Because Sources may have a backlog of unconsumed Events when they are
        terminated (for Sockets, when the far end closes the underlying platform
        socket), Sources should not be closed on the near end until the END
        Event is consumed. The END Event is automatically placed at the end of
        the queue of unconsumed Events when the far end closes the Socket. Note
        that this is a generator function whose state is maintained between
        its yielding of results to the caller.
        @param timeout is an optional select(2) timeout value in seconds.
        """
        # Note that the relative ordering of Events between Sources cannot
        # be guaranteed. Even if we could guarantee that we consumed all
        # Events in the same order that they were given to us, latency in
        # each producer Source itself prevents any strict ordering of
        # Events in real-time. That's not a problem for an Event stream from
        # a single Source (which arrives serialized over a single Socket)
        # but is a problem when we are trying to draw conclusions about
        # how multiple Sources interact with one another (for example in
        # the setup of inter-PBX SIP trunks). I don't believe this is
        # solvable in the general case. Hence our implementation of the
        # model must be robust enough to at least not go off the rails if
        # inter-PBX Events sometimes fail to correlate. 
        candidates = [ candidate for candidate in self.sources.values() if candidate.fileno() >= 0 ]
        effective = 0.0
        while candidates:
            # Service all pending I/O on every open Socket. Our goal here
            # is to consume data in the platform buffers as quickly as possible.
            for source in select.select(candidates, EMPTY, EMPTY, effective)[0]:
                source.service()
            active = False
            # Process queued events on every open socket. Should we process all
            # Events on each Source before moving onto the next one, or should
            # we round robin? There's probably no answer that will be right
            # every time. The code below does the former. Mostly we want to
            # stimulate the Model with each Event as quickly as possible
            # regardless of the Source.
            for source in candidates:
                while True:
                    event = source.get(self)
                    if event == None:
                        break
                    active = True
                    message = Event(event, source.logger)
                    yield message
            effective = 0.0 if active else timeout
            if effective > self.effective:
                self.logger.debug("Multiplex.multiplex: WAITING. %s", str(self))
            self.effective = effective
