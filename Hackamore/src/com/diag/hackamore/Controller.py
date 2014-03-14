"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import Logger
import Event

class Controller:

    def __init__(self, multiplex, manifold, logger = None):
        self.logger = Logger.logger() if logger == None else logger
        self.multiplex = multiplex
        self.manifold = manifold
        
    def __del__(self):
        pass

    def __repr__(self):
        return "Controller(" + str(self.multiplex) + "," + str(self.manifold) + ")"

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
