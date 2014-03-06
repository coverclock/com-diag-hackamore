"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import unittest
import logging
import socket
import threading

import com.diag.hackamore.Logger
import com.diag.hackamore.File
import com.diag.hackamore.Socket
import com.diag.hackamore.Engine

from com.diag.hackamore.Credentials import USERNAME
from com.diag.hackamore.Credentials import SECRET

from Parameters import LOCALHOST
from Parameters import TYPESCRIPT

address = None
port = None
ready = None

READLINE = 512
RECV = 512
LIMIT = 3

class Producer(threading.Thread):
    
    def __init__(self, sock, path):
        threading.Thread.__init__(self)
        self.sock = sock
        self.path = path
        
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
        print("Client=done")  

class Server(threading.Thread):
    
    def __init__(self, path, limit):
        threading.Thread.__init__(self)
        self.path = path
        self.limit = limit
    
    def run(self):
        global address
        global port
        global ready
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(("", 0))
        sock.listen(socket.SOMAXCONN)
        with ready:
            address, port = sock.getsockname()
            print("Server=" + str(port))
            ready.notifyAll()
        producers = [ ]
        while self.limit > 0:
            sock2, farend = sock.accept()
            print("Client=" + str(farend))
            producer = Producer(sock2, TYPESCRIPT)
            producer.start()
            producers.append(producer)
            self.limit = self.limit - 1
        for producer in producers:
            producer.join()
            producers.remove(producer)
        sock.close()
        print("Server=done")

class Test(unittest.TestCase):

    def setUp(self):
        com.diag.hackamore.Logger.logger().setLevel(logging.DEBUG)

    def tearDown(self):
        pass

    def test010Rinse(self):
        name = self.id()
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        console = logging.StreamHandler()
        logger.addHandler(console)
        engine = com.diag.hackamore.Engine.Engine()
        source = com.diag.hackamore.File.File(name, TYPESCRIPT, logger = logger)
        self.assertIsNotNone(source)
        inputs = [ ]
        inputs.append(source)
        outputs = [ ]
        self.assertEquals(len(inputs), 1)
        self.assertEquals(len(outputs), 0)
        engine.engine(inputs, outputs, suppress = True)
        self.assertEquals(len(inputs), 0)
        self.assertEquals(len(outputs), 1)

    def test020Repeat(self):
        name = self.id()
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        console = logging.StreamHandler()
        logger.addHandler(console)
        engine = com.diag.hackamore.Engine.Engine()
        source = com.diag.hackamore.File.File(name, TYPESCRIPT, logger = logger)
        self.assertIsNotNone(source)
        inputs = [ ]
        inputs.append(source)
        self.assertEquals(len(inputs), 1)
        engine.engine(inputs, inputs, suppress = True)
        self.assertEquals(len(inputs), 1)
        
    def test030Passive(self):
        global address
        global port
        global ready
        name = self.id()
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        console = logging.StreamHandler()
        logger.addHandler(console)
        engine = com.diag.hackamore.Engine.Engine()
        address = ""
        port = 0
        ready = threading.Condition()
        thread = Server(TYPESCRIPT, LIMIT)
        self.assertIsNotNone(thread)
        thread.start()
        with ready:
            while port == 0:
                ready.wait()
        source = com.diag.hackamore.Socket.Socket(name, USERNAME, SECRET, LOCALHOST, port, logger = logger)
        self.assertIsNotNone(source)
        sources = [ ]
        sources.append(source)
        self.assertEquals(len(sources), 1)
        engine.engine(sources, sources, suppress = True)
        self.assertEquals(len(sources), 1)
        thread.join()

    def test040Active(self):
        global address
        global port
        global ready
        name = self.id()
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        console = logging.StreamHandler()
        logger.addHandler(console)
        state = com.diag.hackamore.State.State()
        engine = com.diag.hackamore.Engine.Engine(state = state)
        address = ""
        port = 0
        ready = threading.Condition()
        thread = Server(TYPESCRIPT, LIMIT)
        self.assertIsNotNone(thread)
        thread.start()
        with ready:
            while port == 0:
                ready.wait()
        source = com.diag.hackamore.Socket.Socket(name, USERNAME, SECRET, LOCALHOST, port, logger = logger)
        self.assertIsNotNone(source)
        sources = [ ]
        sources.append(source)
        self.assertEquals(len(sources), 1)
        engine.engine(sources, sources, verbose = True)
        self.assertEquals(len(sources), 1)
        state.dump()
        thread.join()

if __name__ == "__main__":
    unittest.main()
