"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import sys
import logging
import socket
import threading
import time
import os

import Logger
import Socket
import ModelStandard
import ViewPrint
import ViewCurses
import Controller
import Manifold
import Multiplex

READLINE = 512
RECV = 512
LIMIT = 1
DELAY = 0.0

class Producer(threading.Thread):
    
    def __init__(self, sock, path, delay = 0):
        threading.Thread.__init__(self)
        self.sock = sock
        self.path = path
        self.delay = delay
        
    def run(self):
        stream = open(self.path, "r")
        if stream != None:
            while True:
                line = stream.readline(READLINE)
                if line == None:
                    break
                elif not line:
                    break
                else:
                    self.sock.sendall(line)
                    if line != "\r\n":
                        pass
                    if not self.delay:
                        pass
                    else:
                        time.sleep(self.delay)
        stream.close()
        self.sock.shutdown(socket.SHUT_WR)
        while True:
            fragment = self.sock.recv(RECV)
            if fragment == None:
                pass
            elif not fragment:
                break
            else:
                pass
        self.sock.close()

class Server(threading.Thread):
    
    def __init__(self, path, limit = 1, delay = 0):
        threading.Thread.__init__(self)
        self.path = path
        self.limit = limit
        self.delay = delay
        self.address = None
        self.port = None
        self.ready = threading.Condition()
    
    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(("", 0))
        sock.listen(socket.SOMAXCONN)
        with self.ready:
            self.address, self.port = sock.getsockname()
            self.ready.notifyAll()
        producers = [ ]
        while self.limit > 0:
            sock2 = sock.accept()[0]
            producer = Producer(sock2, self.path, self.delay)
            producer.start()
            producers.append(producer)
            self.limit = self.limit - 1
        for producer in producers:
            producer.join()
        sock.close()

def body(manifold, inputs, outputs, logger = None):
    if logger == None:
        logger = Logger.logger()
    multiplex = Multiplex.Multiplex()
    controller = Controller.Controller(multiplex, manifold)
    logger.info("Main.body: STARTING.")
    controller.loop(inputs, outputs)
    logger.info("Main.body: STOPPING.")

def play(path):
    logger = Logger.logger()
    logger.setLevel(logging.DEBUG)
    thread = Server(path, limit = LIMIT, delay = DELAY)
    thread.start()
    with thread.ready:
        while thread.port == None:
            thread.ready.wait()
    source = Socket.Socket("", "", "", "", thread.port)
    sources = [ source ]
    model = ModelStandard.ModelStandard()
    view = ViewCurses.ViewCurses(model) if "TERM" in os.environ else ViewPrint.ViewPrint(model)
    manifold = Manifold.Manifold(model, view)
    body(manifold, sources, sources, logger)

def main():
    path = "/Volumes/Silver/src/Hackamore/hackamore-GTA/hackamore-GTA-x200-5037.txt";
    path = "/Volumes/Silver/src/Hackamore/hackamore-GTA/hackamore-GTA-x200-5036.txt";
    path = "/Volumes/Silver/src/Hackamore/hackamore-GTA/hackamore-GTA-4wire-x51-5037.txt";
    path = "/Volumes/Silver/src/Hackamore/hackamore-GTA/hackamore-GTA-4wire-x51-5036.txt";
    play(path)

if __name__ == "__main__":
    main()
