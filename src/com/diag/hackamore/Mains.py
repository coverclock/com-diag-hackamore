"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import time
import threading
import os

import Logger
import Configure
import ModelStandard
import ViewPrint
import ViewCurses
import Controller
import Manifold
import Serializer
import Multiplex
    
PREFIX = "COM_DIAG_HACKAMORE_"
TIMEOUT = 1.0

class Producer(threading.Thread):
    
    def __init__(self, inputs, outputs, controller, logger):
        threading.Thread.__init__(self)
        self.logger = logger
        self.controller = controller
        self.inputs = inputs
        self.outputs = outputs

    def __del__(self):
        pass
 
    def __repr__(self):
        return "Thread(" + threading.Thread.__repr__(self) + ").Producer()"
    
    def run(self):
        self.logger.info("Mains.Producer.run: STARTING. %s", str(self))
        while self.inputs:
            self.controller.loop(self.inputs, self.outputs)
            time.sleep(2.0)
            self.logger.info("Mains.Producer.run: RESTARTING. %s", str(self))
        self.logger.info("Mains.Producer.run: STOPPING. %s", str(self))

def body(manifold, inputs, outputs, logger = None):
    if logger == None:
        logger = Logger.logger()
    serializer = Serializer.Serializer(manifold)
    producers = [ ]
    while inputs:
        source = inputs.pop(0)
        multiplex = Multiplex.Multiplex()
        controller = Controller.Controller(multiplex, serializer)
        sources = [ source ]
        if id(inputs) == id(outputs):
            sinks = sources
        else:
            sinks = [ ]
        producer = Producer(sources, sinks, controller, logger)
        producers.append(producer)
    for producer in producers:
        producer.start()
    while producers:
        threads = [ producer for producer in producers ]
        for producer in threads:
            producer.join(TIMEOUT)
            if not producer.isAlive():
                producers.remove(producer)
                for source in producer.outputs:
                    outputs.append(source)
    serializer.shutdown()

def main():
    logger = Logger.logger()
    sources = Configure.servers(logger)
    model = ModelStandard.ModelStandard()
    view = ViewCurses.ViewCurses(model) if "TERM" in os.environ else ViewPrint.ViewPrint(model)
    manifold = Manifold.Manifold(model, view)
    body(manifold, sources, sources)

if __name__ == "__main__":
    main()
