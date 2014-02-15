"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import sys
import socket
import select

HOST = "127.0.0.1"
PORT = 5038
CONNECT = 0.0
SELECT = 0.0
MAKEFILE = 1024
READLINE = 512
EOF = ""

sources = { }

connections = { }

sessions = { }

def producer():
    for source in sources:
        source.connect()
    for connection in connections:
        connection.authenticate()
    for session in select.select(sessions.values(), None, None, SELECT)[0]:
        session.read()
    for connection in select.select(connections.values(), None, None, SELECT)[0]:
        connection.read()

def consumer():
    for connection in connections:
        if connection.queue.length() > 0:
            datum = connection.queue[0]
            del connection.queue[0]
            yield ( connection.name, datum )
    for session in sessions:
        if session.queue.length() > 0:
            datum = session.queue[0]
            del session.queue[0]
            yield ( session.name, datum )

class Source:
    """
    This class manages a socket object that is an OS client socket connections
    to an OS server socket that exposes an Asterisk Management Interface (AMI)
    presumably provided by an Asterisk PBX.
    """

    #
    # BOOKKEEPING LAYER
    #

    def __init__(self, name, host, port, username, secret):
        self.name = name
        self.host = host
        self.port = port
        self.username = username
        self.secret = secret
        self.socket = None
        self.file = None
        self.queue = [ ]
        sources[self.name] = self
        
    def __del__(self):
        if (self.name in connections) or (self.name in sessions):
            self.disconnect()
        if self.name in sources:
            del sources[self.name]

    def __repr__(self):
        return "Source(\"" + str(self.name) + "," + str(self.host) + "," + str(self.port) + "," + str(self.username) + "," + ("authenticated" if self.name in sessions else "connected" if self.name in connections else "defined" if self.name in sources else "orphaned")  + ")"
        
    #
    # CONNECTION LAYER
    #
        
    def disconnect(self):
        if self.file != None:
            try:
                self.file.close()
            except Exception as exception:
                sys.stderr.write("Source.disconnect: file.close() failed! error=\"" + str(exception) + "\"\n")
            else:
                sys.stderr.write("Source: " + self.name + " closed.\n")
            finally:
                self.file = None
        if self.socket != None:
            try:
                self.socket.close()
            except Exception as exception:
                sys.stderr.write("Source.disconnect: socket.close() failed! error=\"" + str(exception) + "\"\n")
            else:
                sys.stderr.write("Source: " + self.name + " disconnected.\n")
            finally:
                self.socket = None
        self.queue.append(EOF)
        if self.name in sessions:
            del sessions[self.name]
        if self.name in connections:
            del connections[self.name]
        sources[self.name] = self

    def open(self):
        try:
            self.file = open(self.path, "r")
        except Exception as exception:
            sys.stderr.write("Source.open: file.open(\"" + self.path + "\") failed! \"" + str(exception) + "\"\n")
            self.disconnect()
        else:
            sys.stderr.write("Source: " + self.name + " opened.\n")
            del sources[self.name]
            connections[self.name] = self
        finally:
            pass

    def connect(self):
        try:
            self.socket = socket.create_connection((self.host, self.port), CONNECT)
        except Exception as exception:
            sys.stderr.write("Source.connect: socket.create_connection((\"" + str(self.host) + "\"," + str(self.port) + ")) failed! \"" + str(exception) + "\"\n")
            self.disconnect()
        else:
            sys.stderr.write("Source: " + self.name + " connected.\n")
            try:
                self.file = self.makefile("rwb", MAKEFILE)
            except Exception as exception:
                sys.stderr.write("Source.connect: socket.create_connection() failed! \"" + str(exception) + "\"\n")
                self.disconnect()
            else:
                sys.stderr.write("Source: " + self.name + " opened.\n")
                del sources[self.name]
                connections[self.name] = self
            finally:
                pass
        finally:
            pass

    def fileno(self):
        return self.file.fileno() if True else self.socket.fileno()
    
    #
    # AUTHENTICATION LAYER
    #

    def disauthenticate(self):
        self.write("Action: Logoff\r\n\r\n")

    def authenticate(self):
        self.write("Action: Login\r\nUsername: " + str(self.username) + "\r\nSecret: " + str(self.secret) + "\r\n\r\n")

    def disauthenticated(self):
        sys.stderr.write("Source: " + self.name + " disauthenticated.\n")
        del sessions[self.name]
        connections[self.name] = self
    
    def authenticated(self):
        sys.stderr.write("Source: " + self.name + " authenticated.\n")
        del connections[self.name]
        sessions[self.name] = self

    #
    # INPUT/OUTPUT LAYER
    #

    def write(self, stuff):
        try:
            self.file.write(stuff)
        except Exception as exception:
            sys.stderr.write("Source.write: file.write() failed! \"" + str(exception) + "\"\n")
            self.disconnect()
        else:
            self.file.flush()
        finally:
            pass
    
    def read(self):
        try:
            line = self.file.readline(READLINE)
        except Exception as exception:
            sys.stderr.write("Source.read: file.readline() failed! \"" + str(exception) + "\"\n")
            self.disconnect()
        else:
            if line.length() == 0:
                self.disconnect()
            else:
                self.queue.append(line)
        finally:
            pass

