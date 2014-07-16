"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import socket
import threading
import time

from com.diag.hackamore.Socket import Socket
from com.diag.hackamore.ModelStandard import ModelStandard
from com.diag.hackamore.ViewSingleStep import ViewSingleStep
from com.diag.hackamore.Manifold import Manifold
from com.diag.hackamore.Multiplex import Multiplex
from com.diag.hackamore.Controller import Controller

from Parameters import SERVER
from Parameters import USERNAME
from Parameters import SECRET
from Parameters import LOCALHOST
from Parameters import TYPESCRIPT

READLINE = 512
RECV = 512
LIMIT = 3

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

def main():
        thread = Server(TYPESCRIPT)
        thread.start()
        with thread.ready:
            while thread.port == None:
                thread.ready.wait()
        source = Socket(SERVER, USERNAME, SECRET, LOCALHOST, thread.port)
        sources = [ source ]
        model = ModelStandard()
        view = ViewSingleStep(model)
        manifold = Manifold(model, view)
        multiplex = Multiplex()
        controller = Controller(multiplex, manifold)
        controller.loop(sources, sources)
        thread.join()

if __name__ == "__main__":
    main()
