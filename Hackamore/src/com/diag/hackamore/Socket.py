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

    def __init__(self, name, username, secret, host = HOST, port = PORT, timeout = CONNECT, bufsize = RECV, logger = None):
        Source.__init__(self, name, username, secret, logger = logger)
        self.host = host
        self.port = port
        self.timeout = timeout
        self.bufsize = bufsize
        self.eof = False
        self.prefix = ""
        self.partial = [ ]
        self.queue = [ ]
        self.socket = None
        self.logger.info("Socket: INIT. %s", str(self))

    def __del__(self):
        self.close()
        self.logger.info("Socket: FINI. %s", str(self))

    def __repr__(self):
        return Source.__repr__(self) + ".Socket(" + str(self.host) + "," + str(self.port) + ")"
 
    def open(self):
        result = False
        if self.socket == None:
            try:
                self.socket = socket.create_connection((self.host, self.port), self.timeout)
            except Exception as exception:
                self.logger.error("Socket.open: FAILED! %s %s", str(self), str(exception))
            else:
                self.eof = False
                self.logger.info("Socket.open: CONNECTED. %s", str(self))
                self.login()
                Source.open(self)
                result = True
            finally:
                pass
        return result

    def close(self):
        result = False
        if self.socket != None:
            try:
                self.socket.close()
            except Exception as exception:
                self.logger.error("Socket.close: FAILED! %s %s", str(self), str(exception))
            else:
                self.logger.info("Socket.close: DISCONNECTED. %s", str(self))
            finally:
                self.socket = None
                Source.close(self)
                result = True
        return result
 
    def fileno(self):
        return self.socket.fileno() if self.socket != None else -1
    
    def assemble(self, fragment):
        # This is really inefficient. When I finally move from Python 2.7
        # I'll replace this with something like memory views. But for now,
        # fragments that split the "\r\n" pair don't happen that often.
        if fragment[0] == "\n":
            fragment = self.prefix + fragment
            self.prefix = ""
        if fragment[-1] == "\r":
            self.prefix = self.prefix + fragment
            fragment = None
        if fragment == None:
            pass
        elif "\r\n" in fragment:
            sequence = fragment.split("\r\n")
            self.partial.append(sequence.pop(0))
            self.queue.append("".join(self.partial))
            self.partial = [ sequence.pop(-1) ]
            for piece in sequence:
                self.queue.append(piece)
        else:
            self.partial.append(fragment)
        #self.logger.debug("Socket.assemble:PARTIAL=" + str(self.partial))
        #self.logger.debug("Socket.assemble:QUEUE=" + str(self.queue))

    def service(self):
        if self.socket == None:
            pass
        elif self.eof:
            pass
        else:
            try:
                fragment = self.socket.recv(self.bufsize)
            except Exception as exception:
                self.logger.error("Socket.read: FAILED! %s %s", str(self), str(exception))
            else:
                if fragment == None:
                    pass
                elif not fragment:
                    self.eof = True
                    self.logger.info("Socket.read: END. %s", str(self))
                else:
                    self.assemble(fragment)
            finally:
                pass

    def read(self, multiplex = None):
        if multiplex == None:
            self.service()
        line = None
        if self.queue:
            line = self.queue.pop(0)
            if self.logger.isEnabledFor(logging.DEBUG):
                self.logger.debug("Socket.read: READ: %s \"%s\"", str(self), str(line))
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
                self.logger.error("Socket.write: FAILED! %s %s", str(self), str(exception))
            else:
                result = True
                if self.logger.isEnabledFor(logging.DEBUG):
                    self.logger.debug("Socket.write: WRITE: %s \"%s\"", str(self), str(line))
            finally:
                pass
        return result
