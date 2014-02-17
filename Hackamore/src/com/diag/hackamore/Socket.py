"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import logging
import socket

from Source import Source

HOST = "127.0.0.1"
PORT = 5038
CONNECT = 0.0
MAKEFILE = 1024

class Socket(Source):

    def __init__(self, name, host, port, username, secret):
        Source.__init__(self, name)
        self.host = host
        self.port = port
        self.username = username
        self.secret = secret
        self.socket = None
        
    def __del__(self):
        self.close()

    def __repr__(self):
        return Source.__repr__(self) + ".Socket(\"" + str(self.host) + "\"," + str(self.port) + ")"

    def open(self):
        try:
            self.socket = socket.create_connection((self.host, self.port), CONNECT)
        except Exception as exception:
            logging.error("Socket.open: FAILED!" + str(self) + " " + str(exception))
            self.close()
        else:
            logging.info("Socket.open: CONNECTED. " + str(self))
            try:
                self.file = self.socket.makefile("rwb", MAKEFILE)
            except Exception as exception:
                logging.error("Socket.open: FAILED!" + str(self) + " " + str(exception))
                self.close()
            else:
                logging.info("Socket.open: OPENED. " + str(self))
                self.put( ( ("Action", "Login"), ("Username", str(self.username)), ("Secret", str(self.secret)) ) )
                Source.open(self)
            finally:
                pass
        finally:
            pass

    def close(self):
        closed = False
        if self.file != None:
            try:
                self.file.close()
            except Exception as exception:
                logging.error("Socket.close: FAILED! " + str(self) + " " + str(exception))
            else:
                logging.info("Socket.close: CLOSED. " + str(self))
                closed = True
            finally:
                self.file = None
        if self.socket != None:
            try:
                self.socket.close()
            except Exception as exception:
                logging.error("Socket.close: FAILED! " + str(self) + " " + str(exception))
            else:
                logging.info("Socket.close: DISCONNECTED. " + str(self))
                closed = True
            finally:
                self.socket = None
        if closed:
            Source.close(self)
 
    def fileno(self):
        if (self.socket == None) or (self.file == None):
            self.open()
        return Source.fileno(self)
