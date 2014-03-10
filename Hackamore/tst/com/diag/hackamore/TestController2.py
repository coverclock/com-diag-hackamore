"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import unittest
import logging
import socket
import threading
import time

import com.diag.hackamore.Logger
import com.diag.hackamore.Socket
import com.diag.hackamore.ModelSerializer
import com.diag.hackamore.ModelStandard
import com.diag.hackamore.ViewCurses
import com.diag.hackamore.Controller

from com.diag.hackamore.Credentials import SERVER
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
DELAY=0.1

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
            ready.notifyAll()
        producers = [ ]
        while self.limit > 0:
            sock2, farend = sock.accept()
            producer = Producer(sock2, TYPESCRIPT, self.delay)
            producer.start()
            producers.append(producer)
            self.limit = self.limit - 1
        for producer in producers:
            producer.join()
            producers.remove(producer)
        sock.close()

class Test(unittest.TestCase):

    def setUp(self):
        com.diag.hackamore.Logger.logger().setLevel(logging.WARNING)

    def tearDown(self):
        pass

    def test010Curses(self):
        global address
        global port
        global ready
        address = ""
        port = 0
        ready = threading.Condition()
        thread = Server(TYPESCRIPT, delay = DELAY)
        self.assertIsNotNone(thread)
        thread.start()
        with ready:
            while port == 0:
                ready.wait()
        source = com.diag.hackamore.Socket.Socket(SERVER, USERNAME, SECRET, LOCALHOST, port)
        self.assertIsNotNone(source)
        sources = [ ]
        sources.append(source)
        self.assertEquals(len(sources), 1)
        model = com.diag.hackamore.ModelStandard.ModelStandard()
        serializedmodel = com.diag.hackamore.ModelSerializer.ModelSerializer(model)
        view = com.diag.hackamore.ViewCurses.ViewCurses(model = model)
        controller = com.diag.hackamore.Controller.Controller(model = serializedmodel, view = view)
        controller.loop(sources, sources)
        self.assertEquals(len(sources), 1)
        thread.join()

if __name__ == "__main__":
    unittest.main()
