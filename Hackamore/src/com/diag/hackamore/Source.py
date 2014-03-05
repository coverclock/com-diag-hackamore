"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import logging
import time

import Logger
import Event

USERNAME = ""
SECRET = ""

class Source:

    def __init__(self, pbx, username = USERNAME, secret = SECRET, logger = None):
        self.logger = Logger.logger() if logger == None else logger
        self.pbx = pbx
        self.username = username
        self.secret = secret
        self.count = 0
        self.event = { }
        self.event[Event.SOURCE] = self.pbx
        self.state = False
        self.authenticated = False
        
    def __del__(self):
        if self.state:
            self.close()

    def __repr__(self):
        return "Source(" + str(self.pbx) + ")"

    def open(self):
        result = False
        if not self.state:
            self.count = 0
            self.logger.info("Source.open: OPENED. %s", str(self))
            self.state = True
            self.authenticated = False
            result = True
        return result

    def close(self):
        result = False
        if self.state:
            self.logger.info("Source.close: CLOSED. %s", str(self))
            self.state = False
            result = True
        return result

    def fileno(self):
        return -1
    
    def service(self):
        pass

    def read(self, multiplexing = False):
        pass

    def write(self, line):
        pass
    
    def authentication(self, event):
        if not Event.RESPONSE in event:
            pass
        elif not self.authenticated:
            if event[Event.RESPONSE] != Event.SUCCESS:
                pass
            elif not Event.MESSAGE in event:
                pass
            elif event[Event.MESSAGE] != Event.AUTHENTICATEDACCEPTED:
                pass
            else:
                self.authenticated = True
                self.logger.info("Source:authentication: AUTHENTICATED. %s", str(self))
        else:
            if event[Event.RESPONSE] != Event.GOODBYE:
                pass
            else:
                self.authenticated = False
                self.logger.info("Source:authentication: DEAUTHENTICATED. %s", str(self))

    def get(self, multiplex = None):
        event = None
        while event == None:
            try:
                line = self.read(multiplex)
            except Exception:
                self.count = self.count + 1
                self.event[Event.TIME] = str(time.time())
                self.event[Event.END] = str(self.count)
                event = self.event
                if self.logger.isEnabledFor(logging.DEBUG):
                    self.logger.debug("Source.get: GET: %s %s", str(self), str(event))
                if self.logger.isEnabledFor(logging.INFO):
                    self.logger.info("Source.get: END: %s %d", str(self), self.count)
                self.event = { }
                self.event[Event.SOURCE] = self.pbx          
            else:
                if line == None:
                    break
                elif not line:
                    self.count = self.count + 1
                    self.event[Event.TIME] = str(time.time())
                    event = self.event
                    if self.logger.isEnabledFor(logging.DEBUG):
                        self.logger.debug("Source.get: GET: %s %s", str(self), str(event))
                    self.authentication(event)
                    self.event = { }
                    self.event[Event.SOURCE] = self.pbx
                else:
                    data = line.split(": ", 1)
                    if not data:
                        pass
                    elif len(data) == 1:
                        self.event[data[0]] = ""
                    else:
                        self.event[data[0]] = data[1]
            finally:
                pass
        #if event != None:
            #event[Event.TIME] = "DUMMY"
            #sorted(event, key=event.get)
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
