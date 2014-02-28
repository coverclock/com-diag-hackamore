"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import logging
import socket

from Source import Source
from End import End

HOST = "127.0.0.1"
PORT = 5038
CONNECT = 5.0
RECV = 512

class Socket(Source):

    def __init__(self, name, username, secret, host = HOST, port = PORT, timeout = CONNECT, bufsize = RECV):
        Source.__init__(self, name)
        self.username = username
        self.secret = secret
        self.host = host
        self.port = port
        self.timeout = timeout
        self.bufsize = bufsize
        self.authenticated = False
        self.eof = False
        self.partial = [ ]
        self.queue = [ ]
        self.socket = None

    def __del__(self):
        self.close()

    def __repr__(self):
        return Source.__repr__(self) + ".Socket(\"" + str(self.host) + "\"," + str(self.port) + ")"

    def login(self):
        return self.put( ( ("Action", "Login"), ("Username", str(self.username)), ("Secret", str(self.secret)) ) )

    def logout(self):
        self.authenticated = False
        return self.put( ( ("Action", "Logoff"), ) )

    def open(self):
        if self.socket == None:
            try:
                self.socket = socket.create_connection((self.host, self.port), self.timeout)
            except Exception as exception:
                logging.error("Socket.open: FAILED! " + str(self) + " " + str(exception))
            else:
                self.authenticated = False
                self.eof = False
                logging.info("Socket.open: CONNECTED. " + str(self))
                self.login()
                Source.open(self)
            finally:
                pass

    def close(self):
        if self.socket != None:
            try:
                self.socket.close()
            except Exception as exception:
                logging.error("Socket.close: FAILED! " + str(self) + " " + str(exception))
            else:
                logging.info("Socket.close: DISCONNECTED. " + str(self))
            finally:
                self.authenticated = False
                self.socket = None
                Source.close(self)
 
    def fileno(self):
        if self.socket == None:
            self.open()
        return self.socket.fileno()
    
    def assemble(self, fragment):
        if "\r\n" in fragment:
            sequence = fragment.split("\r\n")
            self.partial.append(sequence.pop(0))
            self.queue.append("".join(self.partial))
            self.partial = [ sequence.pop(-1) ]
            for piece in sequence:
                self.queue.append(piece) 
        else:
            self.partial.append(fragment)
        #logging.debug("Socket.assemble:PARTIAL=" + str(self.partial))
        #logging.debug("Socket.assemble:QUEUE=" + str(self.queue))

    def read(self):
        line = None
        if self.socket != None:
            if not self.eof:
                try:
                    fragment = self.socket.recv(self.bufsize)
                except Exception as exception:
                    logging.error("Socket.read: FAILED! " + str(self) + " " + str(exception))
                else:
                    if fragment == None:
                        pass
                    elif not fragment:
                        self.eof = True
                        logging.info("Socket.read: END. " + str(self))
                    else:
                        self.assemble(fragment)
                finally:
                    pass
            if self.queue:
                line = self.queue.pop(0)
                logging.debug("Socket.read: \"" + str(line) + "\"")
            elif self.eof:
                exception = End
                raise exception
            else:
                pass
        return line

    def write(self, line):
        result = False
        if self.socket != None:
            try:
                self.socket.sendall(line)
                self.socket.sendall("\r\n")
            except Exception as exception:
                logging.error("Socket.write: FAILED! " + str(self) + " " + str(exception))
            else:
                result = True
                logging.debug("Socket.write: \"" + str(line) + "\"")
            finally:
                pass
        return result

    def get(self):
        event = Source.get(self)
        if event == None:
            pass
        else:
            if not self.authenticated:
                if not "Response" in event:
                    pass
                elif event["Response"] != "Success":
                    pass
                else:
                    self.authenticated = True
                    logging.info("Socket:get: AUTHENTICATED. " + str(self))
            else:
                if not "Response" in event:
                    pass
                elif event["Response"] != "Goodbye":
                    pass
                else:
                    self.authenticated = False
                    logging.info("Socket:get: UNAUTHENTICATED. " + str(self))
        return event