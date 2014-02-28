"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import logging
import time

import Multiplex

SOURCE = "SOURCE"
TIME = "TIME"
END = "END"

class Source:

    def __init__(self, name):
        self.name = name
        self.count = 0
        self.event = { }
        self.event[SOURCE] = self.name
        self.state = False
        
    def __del__(self):
        if self.state:
            self.close()
            self.state = False

    def __repr__(self):
        return "Source(\"" + str(self.name) + "\")"

    def open(self):
        if not self.state:
            self.count = 0
            Multiplex.register(self)
            logging.info("Source.open: OPENED. " + str(self))
            self.state = True

    def close(self):
        if self.state:
            Multiplex.unregister(self)
            logging.info("Source.close: CLOSED. " + str(self))
            self.state = False

    def fileno(self):
        return -1

    def read(self):
        pass

    def write(self, line):
        pass

    def get(self):
        event = None
        try:
            line = self.read()
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
            pass
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
