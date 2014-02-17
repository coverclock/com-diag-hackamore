"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import logging
import time

import Multiplex

READLINE = 512
SOURCE = "SOURCE"
TIME = "TIME"
END = "END"

class Source:

    def __init__(self, name):
        self.name = name
        self.file = None
        self.event = { }
        self.event[SOURCE] = self.name
        
    def __del__(self):
        pass

    def __repr__(self):
        return "Source(\"" + str(self.name) + "\")"

    def open(self):
        if self.file != None:
            Multiplex.sources[self.name] = self
        logging.info("Source.open: OPENED. " + str(self))

    def close(self):
        if self.name in Multiplex.sources:
            del Multiplex.sources[self.name]
        logging.info("Source.close: CLOSED. " + str(self))

    def fileno(self):
        return self.file.fileno() if self.file != None else None

    def read(self):
        line = None
        if self.file != None:
            try:
                line = self.file.readline(READLINE)
            except Exception as exception:
                logging.error("Source.read: FAILED! " + str(self) + " " + str(exception))
            else:
                pass
            finally:
                pass
        return line

    def write(self, line):
        result = False
        if self.file != None:
            try:
                self.file.write(line)
                self.file.write("\r\n")
                self.file.flush()
            except Exception as exception:
                logging.error("Source.write: FAILED! " + str(self) + " " + str(exception))
            else:
                result = True
            finally:
                pass
        return result

    def get(self):
        event = None
        line = self.read()
        if line == None:
            pass
        elif len(line) == 0:
            self.close()
            self.event[END] = time.time()
            event = self.event
            self.event = { }
            self.event[SOURCE] = self.name        
        elif len(line) < 2: 
            pass
        elif (line[-1] != '\n') and (line[-2] != '\r'):
            pass
        elif len(line) == 2:
            self.event[TIME] = time.time()
            event = self.event
            self.event = { }
            self.event[SOURCE] = self.name
        else:
            data = line.split(": ", 1)
            if len(data) == 0:
                pass
            elif len(data) == 1:
                self.event[data[0]] = ""
            else:
                self.event[data[0]] = data[1][0:-2]
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
