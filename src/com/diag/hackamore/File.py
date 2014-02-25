"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import logging

from Source import Source

READLINE = 512

class File(Source):

    def __init__(self, name, path, bufsize = READLINE):
        Source.__init__(self, name)
        self.path = path
        self.eof = False
        self.file = None
        self.bufsize = bufsize

    def __del__(self):
        self.close()

    def __repr__(self):
        return Source.__repr__(self) + ".File(\"" + str(self.path) + "\")"

    def open(self):
        try:
            self.file = open(self.path, "rb")
        except Exception as exception:
            logging.error("File.open: FAILED! " + str(self) + " " + str(exception))
            self.close()
        else:
            logging.info("File.open: OPENED. " + str(self))
            Source.open(self)
        finally:
            pass
                
    def close(self):
        self.eof = True
        if self.file != None:
            try:
                self.file.close()
            except Exception as exception:
                logging.error("File.close: FAILED! " + str(self) + " " + str(exception))
            else:
                logging.info("File.close: CLOSED. " + str(self))
            finally:
                self.file = None
                Source.close(self)
 
    def fileno(self):
        if (self.file == None) and (not self.eof):
            self.open()
        return self.file.fileno()

    def read(self):
        line = None
        if self.file != None:
            try:
                line = self.file.readline(self.bufsize)
            except Exception as exception:
                logging.error("File.read: FAILED! " + str(self) + " " + str(exception))
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
                logging.error("File.write: FAILED! " + str(self) + " " + str(exception))
            else:
                result = True
            finally:
                pass
        return result
