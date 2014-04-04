"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import logging
import threading

import Event

class Processor(threading.Thread):
    """
    A Processor is a Thread that removes unconsumed Events from the queue in the
    Serializer and passes them to a Manifold for processing. There is one
    Processor (and hence one Thread) per Serializer. Access to the queue in the
    Serializer is serialized by a mutex.  Several Controllers, each receiving
    Events from one or more Sources via its own Multiplex, can feed these
    Events to a common Serializer (and hence a common Manifold, Model, and
    View).
    """

    #
    # CTOR/DTOR
    #

    def __init__(self, serializer):
        """
        Constructor.
        @param serializer is the Serializer that this Processor services.
        """
        threading.Thread.__init__(self)
        self.serializer = serializer

    def __del__(self):
        pass
 
    def __repr__(self):
        return "Thread(" + threading.Thread.__repr__(self) + ").Processor()"

    #
    # PRIVATE
    #

    def run(self):
        while True:
            with self.serializer.mutex:
                while not self.serializer.queue and not self.serializer.complete:
                    self.serializer.mutex.wait()
                if self.serializer.complete:
                    self.serializer.logger.info("Serializer.Processor.run: COMPLETE. %s", str(self))
                    break
                event = self.serializer.queue.pop(0)
                if self.serializer.logger.isEnabledFor(logging.DEBUG):
                    self.serializer.logger.debug("Serializer.Processor.run: DEQUEUE. %s", str(self))
                self.serializer.manifold.process(event)
                self.serializer.mutex.notifyAll()

class Serializer:
    """
    A Serializer receives unconsumed Events from one or more Controllers and
    queues those Events on a queue for asynchronous processing by its Processor.
    There is one Processor (and hence one Thread) per Serializer. Access to the
    queue in the Serializer is serialized by a mutex.  Several Controllers, each
    receiving Events from one or more Sources via its own Multiplex, can feed
    these Events to a common Serializer (and hence a common Manifold, Model, and
    View).
    """

    #
    # CTOR/DTOR
    #

    def __init__(self, manifold, logger = None):
        """
        Constructor.
        @param manifold is the Manifold associated with this Serializer.
        @param logger is an optional Logger.
        """
        self.manifold = manifold
        self.logger = logger if logger != None else self.manifold.logger
        self.mutex = threading.Condition()
        self.queue = [ ]
        self.processor = Processor(self)
        self.complete = False
        self.processor.start()

    def __del__(self):
        self.shutdown()

    def __repr__(self):
        return "Serializer(" + str(self.manifold) + "," + str(self.processor) + "," + str(self.backlog()) + ")"

    #
    # PRIVATE
    #

    def enqueue(self, event):
        with self.mutex:
            self.queue.append(event)
            if self.logger.isEnabledFor(logging.DEBUG):
                self.logger.debug("Serializer.enqueue: ENQUEUE. %s", str(self))
            self.mutex.notifyAll()

    #
    # PUBLIC
    #

    def backlog(self):
        """
        Return the number of Events queued.
        @return the number of Events queued.
        """
        with self.mutex:
            return len(self.queue)
        
    def wait(self):
        """
        Block the caller until the queue is empty or until the Serializer has
        been told to exit.
        """
        with self.mutex:
            while self.queue and not self.complete:
                self.mutex.wait()

    def process(self, event):
        """
        Process an event by enqueueing it on the queue for asynchronous
        processing by the associated Processor.
        """
        if Event.END in event:
            if Event.END in self.manifold.table:
                self.enqueue(event)
        elif Event.EVENT in event:
            name = event[Event.EVENT]
            if name in self.manifold.table:
                self.enqueue(event)
        else:
            pass

    def shutdown(self):
        with self.mutex:
            self.complete = True
            self.mutex.notifyAll()
        self.processor.join()
