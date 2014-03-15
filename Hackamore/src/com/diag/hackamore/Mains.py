"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import time
import threading
import os

import com.diag.hackamore.Logger
import com.diag.hackamore.Credentials
import com.diag.hackamore.Socket
import com.diag.hackamore.ModelStandard
import com.diag.hackamore.ViewCurses
import com.diag.hackamore.Controller
import com.diag.hackamore.Manifold
import com.diag.hackamore.Serializer
import com.diag.hackamore.Multiplex
    
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
        self.logger.info("Producer.run: STARTING. %s", str(self))
        while self.inputs:
            self.controller.loop(self.inputs, self.outputs)
            time.sleep(2.0)
            self.logger.info("Producer.run: RESTARTING. %s", str(self))
        self.logger.info("Producer.run: STOPPING. %s", str(self))

def body(manifold, inputs, outputs, logger = None):
    logger = com.diag.hackamore.Logger.logger() if logger == None else logger
    serializer = com.diag.hackamore.Serializer.Serializer(manifold)
    producers = [ ]
    while inputs:
        source = inputs.pop(0)
        multiplex = com.diag.hackamore.Multiplex.Multiplex()
        controller = com.diag.hackamore.Controller.Controller(multiplex, serializer)
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

def main():
    logger = com.diag.hackamore.Logger.logger()
    sources = [ ]
    prefix = "COM_DIAG_HACKAMORE_"
    index = 1
    while True:
        names = prefix + "NAME" + str(index)
        name = com.diag.hackamore.Credentials.credential(names)
        if name == None:
            break
        servers = prefix + "SERVER" + str(index)
        server = com.diag.hackamore.Credentials.credential(servers, com.diag.hackamore.Socket.HOST)
        ports = prefix + "PORT" + str(index)
        port = int(com.diag.hackamore.Credentials.credential(ports, str(com.diag.hackamore.Socket.PORT)))
        usernames = prefix + "USERNAME" + str(index)
        username = com.diag.hackamore.Credentials.credential(usernames, "")
        secrets = prefix + "SECRET" + str(index)
        secret = com.diag.hackamore.Credentials.credential(secrets, "")
        logger.info("Mains.main: %s=\"%s\" %s=\"%s\" %s=%d %s=\"%s\" %s=\"%s\"", names, name, servers, server, ports, port, usernames, username, secrets, secret)
        source = com.diag.hackamore.Socket.Socket(name, username, secret, server, port)
        sources.append(source)
        index = index + 1
    model = com.diag.hackamore.ModelStandard.ModelStandard()
    view = com.diag.hackamore.ViewCurses.ViewCurses(model) if "TERM" in os.environ else com.diag.hackamore.ViewPrint.ViewPrint(model)
    manifold = com.diag.hackamore.Manifold.Manifold(model, view)
    body(manifold, sources, sources)

if __name__ == "__main__":
    main()
