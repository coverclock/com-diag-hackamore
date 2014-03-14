"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import time
import threading

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
    
    def __init__(self, sources, controller, logger):
        threading.Thread.__init__(self)
        self.logger = logger
        self.controller = controller
        self.sources = sources

    def __del__(self):
        pass
 
    def __repr__(self):
        return "Thread(" + threading.Thread.__repr__(self) + ").Producer()"
    
    def run(self):
        self.logger.info("Producer.run: STARTING. %s", str(self))
        while self.sources:
            self.controller.loop(self.sources, self.sources)
            time.sleep(2.0)
            self.logger.info("Producer.run: RESTARTING. %s", str(self))
        self.logger.info("Producer.run: STOPPING. %s", str(self))

def main():
    logger = com.diag.hackamore.Logger.logger()
    model = com.diag.hackamore.ModelStandard.ModelStandard()
    view = com.diag.hackamore.ViewCurses.ViewCurses(model)
    manifold = com.diag.hackamore.Manifold.Manifold(model, view)
    serializer = com.diag.hackamore.Serializer.Serializer(manifold)
    producers = [ ]
    index = 1
    while True:
        names = PREFIX + "NAME" + str(index)
        name = com.diag.hackamore.Credentials.credential(names)
        if name == None:
            break
        servers = PREFIX + "SERVER" + str(index)
        server = com.diag.hackamore.Credentials.credential(servers, com.diag.hackamore.Socket.HOST)
        ports = PREFIX + "PORT" + str(index)
        port = int(com.diag.hackamore.Credentials.credential(ports, str(com.diag.hackamore.Socket.PORT)))
        usernames = PREFIX + "USERNAME" + str(index)
        username = com.diag.hackamore.Credentials.credential(usernames, "")
        secrets = PREFIX + "SECRET" + str(index)
        secret = com.diag.hackamore.Credentials.credential(secrets, "")
        logger.info("Mains.main: %s=\"%s\" %s=\"%s\" %s=\"%s\" %s=\"%s\"", names, name, servers, server, usernames, username, secrets, secret)
        source = com.diag.hackamore.Socket.Socket(name, username, secret, server, port)
        sources = [ source ]
        multiplex = com.diag.hackamore.Multiplex.Multiplex()
        controller = com.diag.hackamore.Controller.Controller(multiplex, serializer)
        producer = Producer(sources, controller, logger)
        producers.append(producer)
        index = index + 1
    for producer in producers:
        producer.start()
    while producers:
        for producer in producers:
            producer.join(TIMEOUT)
            if not producer.isAlive():
                producers.remove(producer)
                break

if __name__ == "__main__":
    main()
