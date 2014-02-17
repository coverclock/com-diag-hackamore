"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import sys
import socket
import Source

HOST = "127.0.0.1"
PORT = 5038
CONNECT = 0.0
MAKEFILE = 1024

class Socket(Source):

    def __init__(self, name, host, port, username, secret):
        super.__init__(name)
        self.host = host
        self.port = port
        self.username = username
        self.secret = secret
        self.socket = None
        
    def __del__(self):
        self.close()

    def __repr__(self):
        return super.__repr__() + ".Socket(\"" + str(self.host) + "\"," + str(self.port) + ")"

    def open(self):
        try:
            self.socket = socket.create_connection((self.host, self.port), CONNECT)
            self.file = self.socket.makefile("rwb", MAKEFILE)
        except Exception as exception:
            sys.stderr.write("Socket.open: \"" + str(self.host) + "\" " + str(self.port) + " failed! \"" + str(exception) + "\"\n")
            self.close()
        else:
            super.open()
            self.put( ( ("Action", "Login"), ("Username", str(self.username)), ("Secret", str(self.secret)) ) )
        finally:
            pass
                
    def close(self):
        if self.socket != None:
            try:
                self.socket.close()
            except Exception as exception:
                sys.stderr.write("Socket.close: failed! error=\"" + str(exception) + "\"\n")
            else:
                pass
            finally:
                self.socket = None
        if self.file != None:
            try:
                self.file.close()
            except Exception as exception:
                sys.stderr.write("Socket.close: failed! error=\"" + str(exception) + "\"\n")
            else:
                pass
            finally:
                self.file = None
        super.close()
 
    def fileno(self):
        if (self.socket == None) or (self.file == None):
            self.open()
        return super.fileno()
