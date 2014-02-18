"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import unittest
import logging
import socket

import com.diag.hackamore.Socket
import com.diag.hackamore.Multiplex

ADDRESS = "192.168.1.220"
HOST = "graphite"
PORT = com.diag.hackamore.Socket.PORT
USERNAME = "admin"
SECRET = "85t3r15k"
REFUSED = 0xffff

class Test(unittest.TestCase):

    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)

    def tearDown(self):
        pass
    
    def test1(self):
        self.assertFalse(socket.create_connection((ADDRESS, PORT)) == None)
    
    def test2(self):
        self.assertFalse(socket.create_connection((HOST, PORT)) == None)

    def test3(self):
        name = "PBXSOCKET3"
        self.assertFalse(name in com.diag.hackamore.Multiplex.sources)
        source = com.diag.hackamore.Socket.Socket(name, USERNAME, SECRET, HOST, PORT)
        self.assertTrue(source != None)
        self.assertTrue(source.name != None)
        self.assertTrue(source.name == name)
        self.assertTrue(source.host != None)
        self.assertTrue(source.host == HOST)
        self.assertTrue(source.port != None)
        self.assertTrue(source.port == PORT)
        self.assertFalse(source.name in com.diag.hackamore.Multiplex.sources)
        self.assertTrue(source.socket == None)
        self.assertTrue(source.file == None)
        source.open()
        self.assertFalse(source.socket == None)
        self.assertFalse(source.file == None)
        self.assertTrue(source.name in com.diag.hackamore.Multiplex.sources)
        source.close()
        self.assertFalse(source.name in com.diag.hackamore.Multiplex.sources)
        self.assertTrue(source.file == None)
        self.assertTrue(source.socket == None)
        
    def test4(self):
        name = "PBXSOCKET4"
        self.assertFalse(name in com.diag.hackamore.Multiplex.sources)
        source = com.diag.hackamore.Socket.Socket(name, USERNAME, SECRET, HOST, REFUSED)
        self.assertTrue(source != None)
        self.assertTrue(source.name != None)
        self.assertTrue(source.name == name)
        self.assertTrue(source.host != None)
        self.assertTrue(source.host == HOST)
        self.assertTrue(source.port != None)
        self.assertTrue(source.port == REFUSED)
        self.assertFalse(source.name in com.diag.hackamore.Multiplex.sources)
        self.assertTrue(source.socket == None)
        self.assertTrue(source.file == None)
        source.open()
        self.assertTrue(source.socket == None)
        self.assertTrue(source.file == None)
        self.assertFalse(source.name in com.diag.hackamore.Multiplex.sources)
        source.close()
        self.assertFalse(source.name in com.diag.hackamore.Multiplex.sources)
        self.assertTrue(source.file == None)
        self.assertTrue(source.socket == None)

    def test5(self):
        name = "PBXSOCKET5"
        source = com.diag.hackamore.Socket.Socket(name, USERNAME, SECRET, HOST, PORT)
        source.open()
        lines = 0
        while True:
            line = source.read()
            self.assertFalse(line == None)
            if line == "\r\n":
                break
            self.assertFalse(len(line) < 2)
            self.assertTrue(line[-1] == '\n')
            self.assertTrue(line[-2] == '\r')
            logging.debug(line[0:-2])
            lines = lines + 1
        self.assertTrue(lines == 3)
        source.close()

    def test6(self):
        name = "PBXSOCKET6"
        source = com.diag.hackamore.Socket.Socket(name, USERNAME, SECRET, HOST, PORT)
        source.open()
        events = 0
        while True:
            event = source.get()
            if event == None:
                continue
            events = events + 1
            self.assertTrue(len(event) > 0)
            logging.debug(event)
            self.assertTrue(com.diag.hackamore.Source.SOURCE in event)
            self.assertTrue(event[com.diag.hackamore.Source.SOURCE] == name)
            if com.diag.hackamore.Source.END in event:
                break
            self.assertTrue(com.diag.hackamore.Source.TIME in event)
            self.assertTrue(len(event[com.diag.hackamore.Source.TIME]) > 0)
            if "Response" in event:
                break
        self.assertTrue(events == 1) # 1 response
        source.close()

    def test7(self):
        name = "PBXSOCKET7"
        source = com.diag.hackamore.Socket.Socket(name, USERNAME, SECRET, HOST, PORT)
        source.open()
        while True:
            event = source.get()
            if event != None:
                break       
        self.assertTrue(len(event) > 0)
        logging.debug(event)
        self.assertTrue(com.diag.hackamore.Source.SOURCE in event)
        self.assertTrue(event[com.diag.hackamore.Source.SOURCE] == name)
        self.assertTrue(com.diag.hackamore.Source.TIME in event)
        self.assertTrue(len(event[com.diag.hackamore.Source.TIME]) > 0)
        self.assertTrue("Response" in event)
        self.assertTrue(event["Response"] == "Success")
        self.assertTrue("Message" in event)
        self.assertTrue(event["Message"] == "Authentication accepted")
        while True:
            event = source.get()
            if event != None:
                break
        self.assertTrue(len(event) > 0)
        logging.debug(event)
        self.assertTrue(com.diag.hackamore.Source.SOURCE in event)
        self.assertTrue(event[com.diag.hackamore.Source.SOURCE] == name)
        self.assertTrue(com.diag.hackamore.Source.TIME in event)
        self.assertTrue(len(event[com.diag.hackamore.Source.TIME]) > 0)
        self.assertTrue("Event" in event)
        self.assertTrue(event["Event"] == "FullyBooted")
        self.assertTrue("Status" in event)
        self.assertTrue(event["Status"] == "Fully Booted")
        self.assertTrue(source.logout())
        while True:
            event = source.get()
            if event != None:
                break
        self.assertTrue(len(event) > 0)
        logging.debug(event)
        self.assertTrue(com.diag.hackamore.Source.SOURCE in event)
        self.assertTrue(event[com.diag.hackamore.Source.SOURCE] == name)
        self.assertTrue(com.diag.hackamore.Source.TIME in event)
        self.assertTrue(len(event[com.diag.hackamore.Source.TIME]) > 0)
        self.assertTrue("Response" in event)
        self.assertTrue(event["Response"] == "Goodbye")
        while True:
            event = source.get()
            if event != None:
                break
        self.assertTrue(len(event) > 0)
        logging.debug(event)
        self.assertTrue(com.diag.hackamore.Source.SOURCE in event)
        self.assertTrue(event[com.diag.hackamore.Source.SOURCE] == name)
        self.assertTrue(com.diag.hackamore.Source.END in event)
        self.assertTrue(len(event[com.diag.hackamore.Source.END]) > 0)
        source.close()

    def test8(self):
        self.test7()
        self.test7()

    def test9(self):
        name = "PBXSOCKET9"
        source = com.diag.hackamore.Socket.Socket(name, USERNAME, SECRET, HOST, PORT)
        source.open()
        events = 0
        eof = False
        while not eof:
            for event in com.diag.hackamore.Multiplex.multiplex():
                events = events + 1
                self.assertTrue(len(event) > 0)
                logging.debug(event)
                self.assertTrue(com.diag.hackamore.Source.SOURCE in event)
                if com.diag.hackamore.Source.END in event:
                    self.assertTrue(len(event[com.diag.hackamore.Source.END]) > 0)
                    eof = True
                    break
                self.assertTrue(com.diag.hackamore.Source.TIME in event)
                self.assertTrue(len(event[com.diag.hackamore.Source.TIME]) > 0)
                if not "Response" in event:
                    pass
                elif event["Response"] != "Success":
                    pass
                elif not "Message" in event:
                    pass
                elif event["Message"] != "Authentication accepted":
                    pass
                else:
                    self.assertTrue(source.logout())
        self.assertTrue(events == 4) # 2 responses, 1 events, 1 end
        source.close()

if __name__ == "__main__":
    unittest.main()
