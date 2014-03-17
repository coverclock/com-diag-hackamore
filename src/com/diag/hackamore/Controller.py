"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import Logger
import Event

class Controller:
    """
    Controller uses a Multiplex to receive AMI Events from Sources, and a
    Manifold to deliver those Events to the Model and View associated with
    the Manifold. The Controller is not concerned with how the Events alter
    the dynamic call state (that's the Model), nor with how those Events or
    the dynamic call state is displayed (that's the View). The Controller isn't
    even concerned with what parameters are extracted from the Event and given
    to the Model and View (that's the Manifold). The Controller just wants to
    keep Events from Sources humming along to the Model and View.
    """

    #
    # CTOR/DTOR
    #

    def __init__(self, multiplex, manifold, logger = None):
        """
        Constructor.
        @param multiplex is the Multiplex used to multiplex Sources.
        @param manifold is the Manifold used to feed the Model and View.
        @param logger is an optional Logger used to log messages.
        """
        self.logger = Logger.logger() if logger == None else logger
        self.multiplex = multiplex
        self.manifold = manifold
        
    def __del__(self):
        pass

    def __repr__(self):
        return "Controller(" + str(self.multiplex) + "," + str(self.manifold) + ")"

    #
    # PUBLIC
    #

    def loop(self, inputs, outputs):
        """
        Given a list of input Sources, continuously try to open() each Source,
        and for each open Source, use the Multiplex to get Events from the
        Source to provide to a Model and View via the Manifold. If an END
        event occurs on an open Source, close() the source and place it on
        the list of output Sources. If the caller passes the same list as both
        the input and output Sources, then a Source that is closed will be
        reopened, and if that open is successful, it will be subject to further
        processing. This function continues to run until the list of open
        Sources is empty. If the caller considers this to be a temporary
        condition (for example, PBXes are being restarted), it can just call
        this function again.
        @param inputs is a list initially populated with unopened Sources.
        @param outputs is a list initially empty but returned with closed Sources.
        """
        self.logger.info("Controller.loop: STARTING. %s", str(self))
        while True:
            if inputs:
                sources = [ source for source in inputs ]
                for source in sources:
                    if source.open():
                        self.multiplex.register(source)
                        inputs.remove(source)
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
                    outputs.append(source)
                    self.multiplex.unregister(source)
                    messages.close()
        self.logger.info("Controller.loop: STOPPING. %s", str(self))
