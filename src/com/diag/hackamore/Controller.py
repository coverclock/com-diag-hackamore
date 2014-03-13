"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import Logger
import Event
import Multiplex
import Manifold
import Model
import View

class Controller:

    def __init__(self, model = None, view = None, manifold = None, multiplex = None, tracer = None, logger = None):
        self.logger = Logger.logger() if logger == None else logger
        self.tracer = tracer
        self.multiplex = Multiplex.Multiplex(logger = self.logger) if multiplex == None else multiplex
        self.model = Model.Model(logger = self.logger) if model == None else model
        self.view = View.View(model = self.model, logger = self.logger) if view == None else view
        self.manifold = Manifold.Manifold(model = self.model, view = self.view, logger = self.logger) if manifold == None else manifold
        
    def __del__(self):
        pass

    def __repr__(self):
        return "Controller(" + str(self.model) + "," + str(self.view) + "," + str(self.manifold) + "," + str(self.multiplex) + ")"

    def loop(self, inputs, outputs):
        self.logger.info("Controller.loop: STARTING. %s", str(self))
        while True:
            for source in inputs:
                if source.open():
                    inputs.remove(source)
                    self.multiplex.register(source)
            if not self.multiplex.active():
                break
            messages = self.multiplex.multiplex()
            for message in messages:
                if self.tracer != None:
                    message.trace(self.tracer)
                event = message.event
                if not Event.END in event:
                    self.manifold.process(event)
                elif not Event.SOURCE in event:
                    pass
                else:
                    events = event[Event.END]
                    if events != "1":
                        # Processing an END event in the model is expensive.
                        # We get an END every time we fail to open an AMI socket
                        # to a PBX. This happens routinely when a PBX reboots.
                        # So we don't process the END event if it's the only
                        # event in the source.
                        self.manifold.process(event)
                    pbx = event[Event.SOURCE]
                    source = self.multiplex.query(pbx)
                    source.close()
                    self.multiplex.unregister(source)
                    outputs.append(source)
                    messages.close()
        self.logger.info("Controller.loop: STOPPING. %s", str(self))
