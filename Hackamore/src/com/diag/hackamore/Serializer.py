"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import logging
import threading

import Event

class Processor(threading.Thread):

    #####
    ##### CTOR/DTOR
    #####

    def __init__(self, serializer):
        threading.Thread.__init__(self)
        self.serializer = serializer

    def __del__(self):
        pass
 
    def __repr__(self):
        return "Thread(" + threading.Thread.__repr__(self) + ").Processor()"

    #####
    ##### PRIVATE
    #####

    def run(self):
        while True:
            with self.serializer.mutex:
                while not self.serializer.queue and not self.serializer.complete:
                    self.serializer.mutex.wait()
                if self.serializer.complete:
                    break
                event = self.serializer.queue.pop(0)
                if self.serializer.logger.isEnabledFor(logging.DEBUG):
                    self.serializer.logger.debug("Processor.run: DEQUEUE. %s", str(self))
                self.serializer.manifold.process(event)

class Serializer:

    #####
    ##### CTOR/DTOR
    #####

    def __init__(self, manifold, logger = None):
        self.manifold = manifold
        self.logger = logger if logger != None else self.manifold.logger
        self.mutex = threading.Condition()
        self.queue = [ ]
        self.processor = Processor(self)
        self.complete = False
        self.processor.start()

    def __del__(self):
        with self.mutex:
            self.complete = True
            self.mutex.notifyAll()
        self.processor.join()

    def __repr__(self):
        return "Serializer(" + str(self.manifold) + "," + str(self.processor) + "," + str(self.backlog()) + ")"

    #####
    ##### PRIVATE
    #####

    def enqueue(self, event):
        with self.mutex:
            self.queue.append(event)
            if self.logger.isEnabledFor(logging.DEBUG):
                self.logger.debug("Serializer.enqueue: ENQUEUE. %s", str(self))
            self.mutex.notifyAll()

    #####
    ##### PUBLIC
    #####

    def backlog(self):
        with self.mutex:
            return len(self.queue)

    def process(self, event):
        if Event.END in event:
            if Event.END in self.manifold.table:
                self.enqueue(event)
        elif Event.EVENT in event:
            name = event[Event.EVENT]
            if name in self.manifold.table:
                self.enqueue(event)
        else:
            pass
