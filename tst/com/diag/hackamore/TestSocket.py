"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import unittest
import logging
import socket
import threading

import com.diag.hackamore.Socket
import com.diag.hackamore.Multiplex

ADDRESS = "192.168.1.220"
HOST = "graphite"
PORT = com.diag.hackamore.Socket.PORT
USERNAME = "admin"
SECRET = "85t3r15k"
LOCALHOST = "127.0.0.1"
SAMPLE = "./sample.txt"

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
        with ready:
            address, port2 = sock.getsockname()
            logging.debug("Refuser=" + str(port2))
            sock.close()
            port = port2
            ready.notifyAll()
        with done:
            while not complete:
                done.wait()

class Tardier(threading.Thread):
    
    def run(self):
        global address
        global port
        global ready
        global complete
        global done
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        sock.bind(("", 0))
        with ready:
            address, port = sock.getsockname()
            logging.debug("Tardier=" + str(port))
            ready.notifyAll()
        with done:
            while not complete:
                done.wait()
        sock.close()

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
        with ready:
            address, port = sock.getsockname()
            logging.debug("Nonproducer=" + str(port))
            ready.notifyAll()
        sock.accept()
        with done:
            while not complete:
                done.wait()
        sock.close()

class Producer(threading.Thread):
    
    def run(self):
        global address
        global port
        global ready
        global complete
        global done
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        sock.bind(("", 0))
        sock.listen(socket.SOMAXCONN)
        with ready:
            address, port = sock.getsockname()
            logging.debug("Producer=" + str(port))
            ready.notifyAll()
        sock2, client = sock.accept()
        logging.debug("Consumer=" + str(client))
        stream = open(SAMPLE, "r")
        while True:
            with done:
                if complete:
                    break;
            line = stream.readline(512)
            if line == None:
                break
            elif not line:
                break
            else:
                sock2.sendall(line)
        stream.close()
        sock2.close()
        with done:
            while not complete:
                done.wait()
        sock.close()

class Test(unittest.TestCase):

    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)

    def tearDown(self):
        pass
    
    def test002(self):
        source = com.diag.hackamore.Socket.Socket("", "", "", "", 0)
        logging.debug("PARTIAL=" + str(source.partial))
        logging.debug("QUEUE=" + str(source.queue))
        self.assertTrue(len(source.partial) == 0)
        self.assertTrue(len(source.queue) == 0)
        source.assemble("OneOne: ")
        logging.debug("PARTIAL=" + str(source.partial))
        logging.debug("QUEUE=" + str(source.queue))
        self.assertTrue(len(source.partial) == 1)
        self.assertTrue(len(source.queue) == 0)
        source.assemble("AlphaAlpha")
        logging.debug("PARTIAL=" + str(source.partial))
        logging.debug("QUEUE=" + str(source.queue))
        self.assertTrue(len(source.partial) == 2)
        self.assertTrue(len(source.queue) == 0)
        source.assemble("\r\n")
        logging.debug("PARTIAL=" + str(source.partial))
        logging.debug("QUEUE=" + str(source.queue))
        self.assertTrue(len(source.partial) == 1)
        self.assertTrue(len(source.queue) == 1)
        source.assemble("OneTwo: ")
        logging.debug("PARTIAL=" + str(source.partial))
        logging.debug("QUEUE=" + str(source.queue))
        self.assertTrue(len(source.partial) == 2)
        self.assertTrue(len(source.queue) == 1)
        source.assemble("AlphaBeta\r\n")
        logging.debug("PARTIAL=" + str(source.partial))
        logging.debug("QUEUE=" + str(source.queue))
        self.assertTrue(len(source.partial) == 1)
        self.assertTrue(len(source.queue) == 2)
        source.assemble("OneThree: AlphaGamma\r\n")
        logging.debug("PARTIAL=" + str(source.partial))
        logging.debug("QUEUE=" + str(source.queue))
        self.assertTrue(len(source.partial) == 1)
        self.assertTrue(len(source.queue) == 3)
        source.assemble("\r\n")
        logging.debug("PARTIAL=" + str(source.partial))
        logging.debug("QUEUE=" + str(source.queue))
        self.assertTrue(len(source.partial) == 1)
        self.assertTrue(len(source.queue) == 4)
        event = source.get()
        logging.debug("EVENT=" + str(event))

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
        with ready:
            while port == 0:
                ready.wait()
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
        source.open()
        self.assertTrue(source.socket == None)
        self.assertFalse(source.name in com.diag.hackamore.Multiplex.sources)
        source.close()
        self.assertFalse(source.name in com.diag.hackamore.Multiplex.sources)
        self.assertTrue(source.socket == None)
        with done:
            complete = True
            done.notifyAll()
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
        with ready:
            while port == 0:
                ready.wait()
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
        source.open()
        self.assertTrue(source.socket == None)
        self.assertFalse(source.name in com.diag.hackamore.Multiplex.sources)
        source.close()
        self.assertFalse(source.name in com.diag.hackamore.Multiplex.sources)
        self.assertTrue(source.socket == None)
        with done:
            complete = True
            done.notifyAll()
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
        with ready:
            while port == 0:
                ready.wait()
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
        source.open()
        self.assertFalse(source.socket == None)
        self.assertTrue(source.name in com.diag.hackamore.Multiplex.sources)
        lines = 0
        while True:
            try:
                line = source.read()
            except Exception as exception:
                print exception
                self.assertTrue(isinstance(exception, com.diag.hackamore.End.End))
                break
            else:
                self.assertFalse(line == None)
                logging.debug(line)
                lines = lines + 1
            finally:
                pass
        self.assertTrue(lines == 0)
        source.close()
        self.assertFalse(source.name in com.diag.hackamore.Multiplex.sources)
        self.assertTrue(source.socket == None)
        with done:
            complete = True
            done.notifyAll()
        thread.join()

    def test037(self):
        global address
        global port
        global ready
        global complete
        global done
        name = "PBXSOCKET037"
        self.assertFalse(name in com.diag.hackamore.Multiplex.sources)
        port = 0
        complete = False
        thread = Producer()
        thread.start()
        with ready:
            while port == 0:
                ready.wait()
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
        source.open()
        self.assertFalse(source.socket == None)
        self.assertTrue(source.name in com.diag.hackamore.Multiplex.sources)
        events = 0
        eof = False
        while not eof:
            for event in com.diag.hackamore.Multiplex.multiplex():
                self.assertFalse(event == None)
                events = events + 1
                self.assertTrue(event)
                logging.debug(event)
                if events == 1:
                    self.assertTrue(len(event) == 5)
                    self.assertTrue(com.diag.hackamore.Source.SOURCE in event)
                    self.assertTrue(event[com.diag.hackamore.Source.SOURCE] == name)
                    self.assertTrue(com.diag.hackamore.Source.TIME in event)
                    self.assertTrue(event[com.diag.hackamore.Source.TIME])
                    self.assertFalse(com.diag.hackamore.Source.END in event)
                    self.assertTrue("OneOne" in event)
                    self.assertTrue(event["OneOne"] == "AlphaAlpha")
                    self.assertTrue("OneTwo" in event)
                    self.assertTrue(event["OneTwo"] == "AlphaBeta")
                    self.assertTrue("OneThree" in event)
                    self.assertTrue(event["OneThree"] == "AlphaGamma")
                elif events == 2:
                    self.assertTrue(len(event) == 4)
                    self.assertTrue(com.diag.hackamore.Source.SOURCE in event)
                    self.assertTrue(event[com.diag.hackamore.Source.SOURCE] == name)
                    self.assertTrue(com.diag.hackamore.Source.TIME in event)
                    self.assertTrue(event[com.diag.hackamore.Source.TIME])
                    self.assertFalse(com.diag.hackamore.Source.END in event)
                    self.assertTrue("TwoOne" in event)
                    self.assertTrue(event["TwoOne"] == "BetaAlpha")
                    self.assertTrue("TwoTwo" in event)
                    self.assertTrue(event["TwoTwo"] == "BetaBeta")
                elif events == 3:
                    self.assertTrue(len(event) == 5)
                    self.assertTrue(com.diag.hackamore.Source.SOURCE in event)
                    self.assertTrue(event[com.diag.hackamore.Source.SOURCE] == name)
                    self.assertTrue(com.diag.hackamore.Source.TIME in event)
                    self.assertTrue(event[com.diag.hackamore.Source.TIME])
                    self.assertFalse(com.diag.hackamore.Source.END in event)
                    self.assertTrue("ThreeOne" in event)
                    self.assertTrue(event["ThreeOne"] == "GammaAlpha")
                    self.assertTrue("ThreeTwo" in event)
                    self.assertTrue(event["ThreeTwo"] == "GammaBeta")
                    self.assertTrue("ThreeThree" in event)
                    self.assertTrue(event["ThreeThree"] == "GammaGamma")
                elif events == 4:
                    self.assertTrue(len(event) == 3)
                    self.assertTrue(com.diag.hackamore.Source.SOURCE in event)
                    self.assertTrue(event[com.diag.hackamore.Source.SOURCE] == name)
                    self.assertTrue(com.diag.hackamore.Source.TIME in event)
                    self.assertTrue(event[com.diag.hackamore.Source.TIME])
                    self.assertFalse(com.diag.hackamore.Source.END in event)
                    self.assertTrue("FourOne" in event)
                    self.assertTrue(event["FourOne"] == "DeltaAlpha")
                elif events == 5:
                    self.assertTrue(len(event) == 3)
                    self.assertTrue(com.diag.hackamore.Source.SOURCE in event)
                    self.assertTrue(event[com.diag.hackamore.Source.SOURCE] == name)
                    self.assertTrue(com.diag.hackamore.Source.TIME in event)
                    self.assertTrue(event[com.diag.hackamore.Source.TIME])
                    self.assertTrue(com.diag.hackamore.Source.END in event)
                    self.assertTrue(event[com.diag.hackamore.Source.END] == str(5))
                    eof = True
                else:
                    self.assertTrue(0 < events < 5)
        source.close()
        self.assertFalse(source.name in com.diag.hackamore.Multiplex.sources)
        self.assertTrue(source.socket == None)
        with done:
            complete = True
            done.notifyAll()
        thread.join()

"""

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
        source.open()
        self.assertFalse(source.socket == None)
        self.assertTrue(source.name in com.diag.hackamore.Multiplex.sources)
        source.close()
        self.assertFalse(source.name in com.diag.hackamore.Multiplex.sources)
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
            self.assertTrue(event)
            logging.debug(event)
            self.assertTrue(com.diag.hackamore.Source.SOURCE in event)
            self.assertTrue(event[com.diag.hackamore.Source.SOURCE] == name)
            self.assertTrue(com.diag.hackamore.Source.TIME in event)
            self.assertTrue(event[com.diag.hackamore.Source.TIME])
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
        self.assertTrue(event)
        logging.debug(event)
        self.assertTrue(com.diag.hackamore.Source.SOURCE in event)
        self.assertTrue(event[com.diag.hackamore.Source.SOURCE] == name)
        self.assertTrue(com.diag.hackamore.Source.TIME in event)
        self.assertTrue(event[com.diag.hackamore.Source.TIME])
        self.assertTrue("Response" in event)
        self.assertTrue(event["Response"] == "Success")
        self.assertTrue("Message" in event)
        self.assertTrue(event["Message"] == "Authentication accepted")
        while True:
            event = source.get()
            if event != None:
                break
        self.assertTrue(event)
        logging.debug(event)
        self.assertTrue(com.diag.hackamore.Source.SOURCE in event)
        self.assertTrue(event[com.diag.hackamore.Source.SOURCE] == name)
        self.assertTrue(com.diag.hackamore.Source.TIME in event)
        self.assertTrue(event[com.diag.hackamore.Source.TIME])
        self.assertTrue("Event" in event)
        self.assertTrue(event["Event"] == "FullyBooted")
        self.assertTrue("Status" in event)
        self.assertTrue(event["Status"] == "Fully Booted")
        self.assertTrue(source.logout())
        while True:
            event = source.get()
            if event != None:
                break
        self.assertTrue(event)
        logging.debug(event)
        self.assertTrue(com.diag.hackamore.Source.SOURCE in event)
        self.assertTrue(event[com.diag.hackamore.Source.SOURCE] == name)
        self.assertTrue(com.diag.hackamore.Source.TIME in event)
        self.assertTrue(event[com.diag.hackamore.Source.TIME])
        self.assertTrue("Response" in event)
        self.assertTrue(event["Response"] == "Goodbye")
        while True:
            event = source.get()
            if event != None:
                break
        self.assertTrue(event)
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
                self.assertTrue(event)
                logging.debug(event)
                self.assertTrue(com.diag.hackamore.Source.SOURCE in event)
                self.assertTrue(event[com.diag.hackamore.Source.SOURCE] == name)
                self.assertTrue(com.diag.hackamore.Source.TIME in event)
                self.assertTrue(event[com.diag.hackamore.Source.TIME])
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
