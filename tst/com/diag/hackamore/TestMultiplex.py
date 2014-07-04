"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import unittest
import logging
import threading
import socket

import com.diag.hackamore.Logger
import com.diag.hackamore.Socket
import com.diag.hackamore.File
import com.diag.hackamore.Multiplex
import com.diag.hackamore.Event

from com.diag.hackamore.stdio import printf

from Parameters import USERNAME
from Parameters import SECRET
from Parameters import LOCALHOST
from Parameters import SAMPLE
from Parameters import TYPESCRIPT

class Producer(threading.Thread):
    
    def __init__(self, path):
        threading.Thread.__init__(self)
        self.path = path
        self.address = None
        self.port = None
        self.ready = threading.Condition()
        self.complete = False
        self.done = threading.Condition()
    
    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(("", 0))
        sock.listen(socket.SOMAXCONN)
        with self.ready:
            self.address, self.port = sock.getsockname()
            printf("Producer=%s\n", str(self.port))
            self.ready.notifyAll()
        sock2, consumer = sock.accept()
        printf("Consumer=%s\n", str(consumer))
        stream = open(self.path, "r")
        if stream != None:
            while True:
                line = stream.readline(512)
                if line == None:
                    break
                elif not line:
                    break
                else:
                    sock2.sendall(line)
        sock2.shutdown(socket.SHUT_WR)
        with self.done:
            while not self.complete:
                self.done.wait()
        stream.close()
        sock2.close()
        sock.close()

class Test(unittest.TestCase):

    def setUp(self):
        com.diag.hackamore.Logger.logger().setLevel(logging.INFO)

    def tearDown(self):
        pass

    def test010Multiplexing(self):
        name = self.id()
        thread2 = Producer(SAMPLE)
        thread2.start()
        with thread2.ready:
            while thread2.port == None:
                thread2.ready.wait()
        thread4 = Producer(TYPESCRIPT)
        thread4.start()
        with thread4.ready:
            while thread4.port == None:
                thread4.ready.wait()
        multiplex = com.diag.hackamore.Multiplex.Multiplex()
        self.assertIsNotNone(multiplex)
        self.assertFalse(multiplex.active())
        printf("%s\n", str(multiplex))
        name1 = name + "-1"
        source1 = com.diag.hackamore.File.File(name1, SAMPLE)
        self.assertIsNotNone(source1)
        self.assertTrue(source1.open())
        multiplex.register(source1)
        self.assertTrue(multiplex.active())
        name2 = name + "-2"
        source2 = com.diag.hackamore.Socket.Socket(name2, USERNAME, SECRET, LOCALHOST, thread2.port)
        self.assertIsNotNone(source2)
        self.assertTrue(source2.open())
        multiplex.register(source2)
        self.assertTrue(multiplex.active())
        name3 = name + "-3"
        source3 = com.diag.hackamore.File.File(name3, TYPESCRIPT)
        self.assertIsNotNone(source3)
        self.assertTrue(source3.open())
        multiplex.register(source3)
        self.assertTrue(multiplex.active())
        name4 = name + "-4"
        source4 = com.diag.hackamore.Socket.Socket(name4, USERNAME, SECRET, LOCALHOST, thread4.port)
        self.assertIsNotNone(source4)
        self.assertTrue(source4.open())
        multiplex.register(source4)
        self.assertTrue(multiplex.active())
        printf("%s\n", str(multiplex))
        counter = { }
        counter[name1] = 0
        counter[name2] = 0
        counter[name3] = 0
        counter[name4] = 0
        while multiplex.active():
            messages = multiplex.multiplex()
            for message in messages:
                self.assertIsNotNone(message)
                printf("%s\n", str(message))
                event = message.event
                self.assertIsNotNone(event)
                self.assertTrue(event)
                self.assertIn(com.diag.hackamore.Event.SOURCE, event)
                name = event[com.diag.hackamore.Event.SOURCE]
                self.assertIsNotNone(name)
                self.assertIn(name, counter)
                counter[name] = counter[name] + 1
                if com.diag.hackamore.Event.END in event:
                    source = multiplex.query(name)
                    self.assertIsNotNone(source)
                    self.assertTrue(source.close())
                    multiplex.unregister(source)
                    messages.close()
        self.assertFalse(multiplex.active())
        printf("%s\n", str(multiplex))
        self.assertEquals(counter[name1], 5)
        self.assertEquals(counter[name2], 5)
        self.assertEquals(counter[name3], 358)
        self.assertEquals(counter[name4], 358)
        with thread2.done:
            thread2.complete = True
            thread2.done.notifyAll()
        thread2.join()
        with thread4.done:
            thread4.complete = True
            thread4.done.notifyAll()
        thread4.join()

if __name__ == "__main__":
    unittest.main()