"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import unittest
import socket
import threading
import logging

import com.diag.hackamore.Logger
import com.diag.hackamore.Socket
import com.diag.hackamore.ModelCounter
import com.diag.hackamore.View
import com.diag.hackamore.Manifold
import com.diag.hackamore.Main

from Parameters import USERNAME
from Parameters import SECRET
from Parameters import LOCALHOST
from Parameters import TYPESCRIPT

READLINE = 512
RECV = 512
LIMIT = 3
DELAY=0.1

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

class Server(threading.Thread):
    
    def __init__(self, path, limit = 1):
        threading.Thread.__init__(self)
        self.path = path
        self.limit = limit
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
            producer = Producer(sock2, self.path)
            producer.start()
            producers.append(producer)
            self.limit = self.limit - 1
        for producer in producers:
            producer.join()
        sock.close()

class Test(unittest.TestCase):

    def setUp(self):
        com.diag.hackamore.Logger.logger().setLevel(logging.INFO)

    def tearDown(self):
        pass

    def testMain(self):
        inputs = [ ]
        outputs = [ ]
        thread1 = Server(TYPESCRIPT)
        self.assertIsNotNone(thread1)
        thread1.start()
        with thread1.ready:
            while thread1.port == None:
                thread1.ready.wait()
        thread2 = Server(TYPESCRIPT)
        self.assertIsNotNone(thread2)
        thread2.start()
        with thread2.ready:
            while thread2.port == None:
                thread2.ready.wait()
        thread3 = Server(TYPESCRIPT)
        self.assertIsNotNone(thread3)
        thread3.start()
        with thread3.ready:
            while thread3.port == None:
                thread3.ready.wait()
        source1 = com.diag.hackamore.Socket.Socket("PBX1", USERNAME, SECRET, LOCALHOST, thread1.port)
        self.assertIsNotNone(source1)
        inputs.append(source1)
        source2 = com.diag.hackamore.Socket.Socket("PBX2", USERNAME, SECRET, LOCALHOST, thread2.port)
        self.assertIsNotNone(source2)
        inputs.append(source2)
        source3 = com.diag.hackamore.Socket.Socket("PBX3", USERNAME, SECRET, LOCALHOST, thread3.port)
        self.assertIsNotNone(source3)
        inputs.append(source3)
        model = com.diag.hackamore.ModelCounter.ModelCounter()
        view = com.diag.hackamore.View.View(model)
        manifold = com.diag.hackamore.Manifold.Manifold(model, view)
        self.assertEquals(len(inputs), 3)
        self.assertEquals(len(outputs), 0)
        com.diag.hackamore.Main.body(manifold, inputs, outputs)
        self.assertEquals(len(inputs), 0)
        self.assertEquals(len(outputs), 3)
        self.assertEquals(model.counter[com.diag.hackamore.Event.END], 3)

if __name__ == "__main__":
    unittest.main()