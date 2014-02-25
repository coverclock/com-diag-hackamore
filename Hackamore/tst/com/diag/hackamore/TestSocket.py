"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import unittest
import logging
import socket
import threading
import select

import com.diag.hackamore.Socket
import com.diag.hackamore.Multiplex

ADDRESS = "192.168.1.220"
HOST = "graphite"
PORT = com.diag.hackamore.Socket.PORT
USERNAME = "admin"
SECRET = "85t3r15k"
LOCALHOST = "127.0.0.1"

address = ""
port = 0
ready = threading.Condition()

complete = False
done = threading.Condition()

class Refuser(threading.Thread):
    
    def run(self):
        global address
        global port
        global ready
        global complete
        global done
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        sock.bind(("", 0))
        ready.acquire()
        address, port = sock.getsockname()
        logging.debug("Refuser=" + str(port))
        sock.close()
        ready.notify()
        ready.release()
        done.acquire()
        while not complete:
            done.wait()
        done.release()

class Tardier(threading.Thread):
    
    def run(self):
        global address
        global port
        global ready
        global complete
        global done
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        sock.bind(("", 0))
        ready.acquire()
        address, port = sock.getsockname()
        logging.debug("Tardier=" + str(port))
        ready.notify()
        ready.release()
        done.acquire()
        while not complete:
            done.wait()
        done.release()

class Nonproducer(threading.Thread):
    
    def run(self):
        global address
        global port
        global ready
        global complete
        global done
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        sock.bind(("", 0))
        sock.listen(socket.SOMAXCONN)
        ready.acquire()
        address, port = sock.getsockname()
        logging.debug("Nonproducer=" + str(port))
        ready.notify()
        ready.release()
        sock.accept()
        done.acquire()
        while not complete:
            done.wait()
        done.release()

class Test(unittest.TestCase):

    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)

    def tearDown(self):
        pass
    
    def test010(self):
        self.assertFalse(socket.create_connection((ADDRESS, PORT)) == None)
    
    def test020(self):
        self.assertFalse(socket.create_connection((HOST, PORT)) == None)
        
    def test030(self):
        name = "PBXSOCKET030"
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
        
    def test032(self):
        global address
        global port
        global ready
        global complete
        global done
        name = "PBXSOCKET032"
        self.assertFalse(name in com.diag.hackamore.Multiplex.sources)
        port = 0
        complete = False
        thread = Refuser()
        thread.start()
        ready.acquire()
        while port == 0:
            ready.wait()
        ready.release()
        source = com.diag.hackamore.Socket.Socket(name, USERNAME, SECRET, LOCALHOST, port)
        self.assertTrue(source != None)
        self.assertTrue(source.name != None)
        self.assertTrue(source.name == name)
        self.assertTrue(source.host != None)
        self.assertTrue(source.host == LOCALHOST)
        self.assertTrue(source.port != None)
        self.assertTrue(source.port == port)
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
        done.acquire()
        complete = True
        done.notify()
        done.release()
        thread.join()
        
    def test034(self):
        global address
        global port
        global ready
        global complete
        global done
        name = "PBXSOCKET034"
        self.assertFalse(name in com.diag.hackamore.Multiplex.sources)
        port = 0
        complete = False
        thread = Tardier()
        thread.start()
        ready.acquire()
        while port == 0:
            ready.wait()
        ready.release()
        source = com.diag.hackamore.Socket.Socket(name, USERNAME, SECRET, LOCALHOST, port)
        self.assertTrue(source != None)
        self.assertTrue(source.name != None)
        self.assertTrue(source.name == name)
        self.assertTrue(source.host != None)
        self.assertTrue(source.host == LOCALHOST)
        self.assertTrue(source.port != None)
        self.assertTrue(source.port == port)
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
        done.acquire()
        complete = True
        done.notify()
        done.release()
        thread.join()

    def test036(self):
        global address
        global port
        global ready
        global complete
        global done
        name = "PBXSOCKET036"
        self.assertFalse(name in com.diag.hackamore.Multiplex.sources)
        port = 0
        complete = False
        thread = Nonproducer()
        thread.start()
        ready.acquire()
        while port == 0:
            ready.wait()
        ready.release()
        source = com.diag.hackamore.Socket.Socket(name, USERNAME, SECRET, LOCALHOST, port)
        self.assertTrue(source != None)
        self.assertTrue(source.name != None)
        self.assertTrue(source.name == name)
        self.assertTrue(source.host != None)
        self.assertTrue(source.host == LOCALHOST)
        self.assertTrue(source.port != None)
        self.assertTrue(source.port == port)
        self.assertFalse(source.name in com.diag.hackamore.Multiplex.sources)
        self.assertTrue(source.socket == None)
        self.assertTrue(source.file == None)
        source.open()
        self.assertFalse(source.socket == None)
        self.assertFalse(source.file == None)
        self.assertTrue(source.name in com.diag.hackamore.Multiplex.sources)
        line = source.read()
        print("LINE=\"" + str(line) + "\"")
        #self.assertTrue(line == None)
        source.close()
        self.assertFalse(source.name in com.diag.hackamore.Multiplex.sources)
        self.assertTrue(source.file == None)
        self.assertTrue(source.socket == None)
        done.acquire()
        complete = True
        done.notify()
        done.release()
        thread.join()
"""        
    def test036(self):
        name = "PBXSOCKET036"
        try:
            port = socket.getservbyname("echo", "tcp")
        except Exception:
            port = 7
        source = com.diag.hackamore.Socket.Socket(name, USERNAME, SECRET, LOCALHOST, port)
        source.open()
        lines = 0
        while True:
            line = source.read()
            self.assertFalse(line == None)
            logging.debug(line)
            if line == "\r\n":
                break
            self.assertFalse(len(line) < 2)
            self.assertTrue(line[-1] == '\n')
            self.assertTrue(line[-2] == '\r')
            lines = lines + 1
        self.assertTrue(lines == 3)
        source.close()

    def test040(self):
        name = "PBXSOCKET040"
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

    def test050(self):
        name = "PBXSOCKET050"
        source = com.diag.hackamore.Socket.Socket(name, USERNAME, SECRET, HOST, PORT)
        source.open()
        lines = 0
        while True:
            line = source.read()
            self.assertFalse(line == None)
            logging.debug(line)
            if line == "\r\n":
                break
            self.assertFalse(len(line) < 2)
            self.assertTrue(line[-1] == '\n')
            self.assertTrue(line[-2] == '\r')
            lines = lines + 1
        self.assertTrue(lines == 3)
        source.close()

    def test060(self):
        name = "PBXSOCKET060"
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
            self.assertTrue(com.diag.hackamore.Source.TIME in event)
            self.assertTrue(len(event[com.diag.hackamore.Source.TIME]) > 0)
            self.assertFalse(com.diag.hackamore.Source.END in event)
            if "Response" in event:
                break
        self.assertTrue(events == 1) # 1 response
        source.close()

    def test070(self):
        name = "PBXSOCKET070"
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
        self.assertTrue(event[com.diag.hackamore.Source.END] == str(4))
        source.close()

    def test080(self):
        name = "PBXSOCKET080"
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
                self.assertTrue(event[com.diag.hackamore.Source.SOURCE] == name)
                self.assertTrue(com.diag.hackamore.Source.TIME in event)
                self.assertTrue(len(event[com.diag.hackamore.Source.TIME]) > 0)
                if com.diag.hackamore.Source.END in event:
                    self.assertTrue(event[com.diag.hackamore.Source.END] == str(events))
                    eof = True
                    break
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
"""
if __name__ == "__main__":
    unittest.main()
