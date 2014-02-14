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
MULTIPLEX = 0.0

sources = { }

connections = { }

sessions = { }

def multiplex():
    for source in sources:
        source.connect(CONNECT)
    for connection in connections:
        connection.authenticate()
    for session in select.select(sessions.values(), None, None, MULTIPLEX)[0]:
        pass
    for connection in select.select(connections.values(), None, None, MULTIPLEX)[0]:
        pass

class Source:
    """
    This class manages a socket object that is an OS client socket connections
    to an OS server socket that exposes an Asterisk Management Interface (AMI)
    presumably provided by an Asterisk PBX.
    """

    #
    # BOOKKEEPING LAYER
    #

    def __init__(self, name, host, port, username, secret, timeout):
        self.socket = None
        self.name = name
        self.host = host
        self.port = port
        self.username = username
        self.secret = secret
        self.fileno = -1
        self.error = None
        sources[self.name] = self
        
    def __del__(self):
        if (self.name in connections) or (self.name in sessions):
            self.disconnect()
        if self.name in sources:
            del sources[self.name]

    def __repr__(self):
        return "Source(\"" + str(self.name) + "\",\"" + str(self.host) + "\"," + str(self.port) + ",\"" + str(self.username) + "\",\"" + str(self.secret) + "\"," + str(self.fileno) + ",\"" + str(self.error) + "," + str(self.authenticated) + "\")"
        
    #
    # CONNECTION LAYER
    #
        
    def disconnect(self):
        try:
            self.socket.close()
        except socket.error as self.error:
            sys.stderr.write("Source.disconnect: socket.close() FAILED! error=\"" + str(self.error) + "\"\n")
        else:
            pass
        finally:
            self.socket = None
            self.fileno = -1
            if self.name in sessions:
                del sessions[self.name]
            if self.name in connections:
                del connections[self.name]
            sources[self.name] = self

    def connect(self, timeout):
        try:
            self.socket = socket.create_connection((self.host, self.port), timeout)
        except socket.error as self.error:
            sys.stderr.write("Source.connect: socket.create_connection() FAILED! error=\"" + str(self.error) + "\"\n")
            self.socket = None
        else:
            self.fileno = self.socket.fileno();
            del sources[self.name]
            connections[self.name] = self
        finally:
            pass

    def fileno(self):
        return self.fileno
    
    #
    # AUTHENTICATION LAYER
    #
    
    def authenticated(self):
        del connections[self.name]
        sessions[self.name] = self

    def deauthenticated(self):
        del sessions[self.name]
        connections[self.name] = self

    def authenticate(self):
        self.write("Action: Login\r\nUsername: " + str(self.username) + "\r\nSecret: " + str(self.secret) + "\r\n\r\n")

    def deauthenticate(self):
        self.write("Action: Logoff\r\n\r\n")

    #
    # INPUT/OUTPUT LAYER
    #

    def write(self, stuff):
        try:
            self.socket.sendall(stuff)
        except socket.error as self.error:
            sys.stderr.write("Source.write: socket.sendall() FAILED! error=\"" + str(self.error) + "\"\n")
            self.disconnect()
        else:
            self.error = None
        finally:
            pass
    
    def read(self, limit):
        try:
            data = self.socket.recv(limit)
        except socket.error as self.error:
            sys.stderr.write("Source.read: socket.recv() FAILED! error=\"" + str(self.error) + "\"\n")
            self.disconnect()
            data = ""
        else:
            pass
        finally:
            return data
