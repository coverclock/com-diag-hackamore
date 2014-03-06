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

from com.diag.hackamore.Credentials import USERNAME
from com.diag.hackamore.Credentials import SECRET

from Parameters import LOCALHOST
from Parameters import SAMPLE
from Parameters import TYPESCRIPT

address = ""
port = 0
ready = threading.Condition()

complete = False
done = threading.Condition()

class Producer(threading.Thread):
    
    def __init__(self, path):
        threading.Thread.__init__(self)
        self.path = path
    
    def run(self):
        global address
        global port
        global ready
        global complete
        global done
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(("", 0))
        sock.listen(socket.SOMAXCONN)
        with ready:
            address, port = sock.getsockname()
            print("Producer=" + str(port))
            ready.notifyAll()
        sock2, consumer = sock.accept()
        print("Consumer=" + str(consumer))
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
        with done:
            while not complete:
                done.wait()
        stream.close()
        sock2.close()
        sock.close()

class Test(unittest.TestCase):

    def setUp(self):
        com.diag.hackamore.Logger.logger().setLevel(logging.INFO)

    def tearDown(self):
        pass

    def test010Multiplexing(self):
        global address
        global port
        global ready
        global complete
        global done
        name = self.id()
        complete = False
        port = 0
        thread2 = Producer(SAMPLE)
        thread2.start()
        with ready:
            while port == 0:
                ready.wait()
        port2 = port
        port = 0
        thread4 = Producer(TYPESCRIPT)
        thread4.start()
        with ready:
            while port == 0:
                ready.wait()
        port4 = port
        multiplex = com.diag.hackamore.Multiplex.Multiplex()
        self.assertIsNotNone(multiplex)
        self.assertFalse(multiplex.active())
        print(str(multiplex))
        name1 = name + "-1"
        source1 = com.diag.hackamore.File.File(name1, SAMPLE)
        self.assertIsNotNone(source1)
        self.assertTrue(source1.open())
        multiplex.register(source1)
        self.assertTrue(multiplex.active())
        name2 = name + "-2"
        source2 = com.diag.hackamore.Socket.Socket(name2, USERNAME, SECRET, LOCALHOST, port2)
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
        source4 = com.diag.hackamore.Socket.Socket(name4, USERNAME, SECRET, LOCALHOST, port4)
        self.assertIsNotNone(source4)
        self.assertTrue(source4.open())
        multiplex.register(source4)
        self.assertTrue(multiplex.active())
        print(str(multiplex))
        counter = { }
        counter[name1] = 0
        counter[name2] = 0
        counter[name3] = 0
        counter[name4] = 0
        while multiplex.active():
            messages = multiplex.multiplex()
            for message in messages:
                self.assertIsNotNone(message)
                print(str(message))
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
        print(str(multiplex))
        self.assertEquals(counter[name1], 5)
        self.assertEquals(counter[name2], 5)
        self.assertEquals(counter[name3], 358)
        self.assertEquals(counter[name4], 358)
        with done:
            complete = True
            done.notifyAll()
        thread2.join()
        thread4.join()

if __name__ == "__main__":
    unittest.main()