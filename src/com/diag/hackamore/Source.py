"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import time

import Logger
import Multiplex

from AMI import SOURCE
from AMI import TIME
from AMI import END
from AMI import RESPONSE
from AMI import MESSAGE
from AMI import SUCCESS
from AMI import GOODBYE
from AMI import AUTHENTICATEDACCEPTED

USERNAME = ""
SECRET = ""

class Source:

    def __init__(self, name, username = USERNAME, secret = SECRET, logger = None):
        self.logger = Logger.logger() if logger == None else logger
        self.name = name
        self.username = username
        self.secret = secret
        self.count = 0
        self.event = { }
        self.event[SOURCE] = self.name
        self.state = False
        self.authenticated = False
        
    def __del__(self):
        if self.state:
            self.close()

    def __repr__(self):
        return "Source(\"" + str(self.name) + "\")"

    def open(self):
        if not self.state:
            self.count = 0
            Multiplex.register(self)
            self.logger.info("Source.open: OPENED. %s", str(self))
            self.state = True
            self.authenticated = False

    def close(self):
        if self.state:
            Multiplex.unregister(self)
            self.logger.info("Source.close: CLOSED. %s", str(self))
            self.state = False

    def fileno(self):
        return -1
    
    def service(self):
        pass

    def read(self, multiplexing = False):
        pass

    def write(self, line):
        pass
    
    def authentication(self, event):
        if not RESPONSE in event:
            pass
        elif not self.authenticated:
            if event[RESPONSE] != SUCCESS:
                pass
            elif not MESSAGE in event:
                pass
            elif event[MESSAGE] != AUTHENTICATEDACCEPTED:
                pass
            else:
                self.authenticated = True
                self.logger.info("Source:authentication: AUTHENTICATED. %s", str(self))
        else:
            if event[RESPONSE] != GOODBYE:
                pass
            else:
                self.authenticated = False
                self.logger.info("Source:authentication: DEAUTHENTICATED. %s", str(self))

    def get(self, multiplexing = False):
        event = None
        try:
            line = self.read(multiplexing)
        except Exception:
            self.close()
            self.count = self.count + 1
            self.event[TIME] = str(time.time())
            self.event[END] = str(self.count)
            event = self.event
            self.event = { }
            self.event[SOURCE] = self.name          
        else:
            if line == None:
                pass
            elif not line:
                self.count = self.count + 1
                self.event[TIME] = str(time.time())
                event = self.event
                self.event = { }
                self.event[SOURCE] = self.name
            else:
                data = line.split(": ", 1)
                if not data:
                    pass
                elif len(data) == 1:
                    self.event[data[0]] = ""
                else:
                    self.event[data[0]] = data[1]
        finally:
            if event != None:
                self.logger.debug("Source.get: %s", str(event))
                self.authentication(event)
        return event

    def put(self, command):
        result = False
        for pair in command:
            line = pair[0] + ": " + pair[1]
            if not self.write(line):
                break
        else:
            result = True
        if not self.write(""):
            result = False
        return result

    def login(self):
        return self.put( ( ("Action", "Login"), ("Username", str(self.username)), ("Secret", str(self.secret)) ) )

    def logout(self):
        return self.put( ( ("Action", "Logoff"), ) )
