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
CONNECT = 5.0
MAKEFILE = 1024

class Socket(Source):

    def __init__(self, name, username, secret, host = HOST, port = PORT):
        Source.__init__(self, name)
        self.username = username
        self.secret = secret
        self.host = host
        self.port = port
        self.socket = None
        
    def __del__(self):
        self.close()

    def __repr__(self):
        return Source.__repr__(self) + ".Socket(\"" + str(self.host) + "\"," + str(self.port) + ")"

    def login(self):
        return self.put( ( ("Action", "Login"), ("Username", str(self.username)), ("Secret", str(self.secret)) ) )

    def logout(self):
        return self.put( ( ("Action", "Logoff"), ) )

    def open(self):
        try:
            self.socket = socket.create_connection((self.host, self.port), CONNECT)
        except Exception as exception:
            logging.error("Socket.open: FAILED! " + str(self) + " " + str(exception))
            self.close()
        else:
            logging.info("Socket.open: CONNECTED. " + str(self))
            try:
                self.file = self.socket.makefile("rwb", MAKEFILE)
            except Exception as exception:
                logging.error("Socket.open: FAILED! " + str(self) + " " + str(exception))
                self.close()
            else:
                logging.info("Socket.open: OPENED. " + str(self))
                self.login()
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

    def get(self):
        event = Source.get(self)
        if event == None:
            pass
        elif not "Response" in event:
            pass
        elif event["Response"] != "Success":
            pass
        elif not "Message" in event:
            pass
        elif event["Message"] != "Authentication accepted":
            pass
        else:
            logging.info("Socket:get: AUTHENTICATED. " + str(self))
        return event