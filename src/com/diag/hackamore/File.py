"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import logging

from Source import Source
from End import End

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
        if self.file == None:
            try:
                self.file = open(self.path, "rb")
            except Exception as exception:
                logging.error("File.open: FAILED! " + str(self) + " " + str(exception))
            else:
                logging.info("File.open: OPENED. " + str(self))
                Source.open(self)
            finally:
                pass
                
    def close(self):
        if self.file != None:
            try:
                self.file.close()
            except Exception as exception:
                logging.error("File.close: FAILED! " + str(self) + " " + str(exception))
            else:
                logging.info("File.close: CLOSED. " + str(self))
            finally:
                self.eof = True
                self.file = None
                Source.close(self)
 
    def fileno(self):
        if (self.file == None) and (not self.eof):
            self.open()
        return self.file.fileno()

    def read(self, multiplexing = False):
        line = None
        if self.file != None:
            try:
                line = self.file.readline(self.bufsize)
            except Exception as exception:
                logging.error("File.read: FAILED! " + str(self) + " " + str(exception))
                raise exception
            else:
                if line == None:
                    pass
                elif not line:
                    logging.info("File.read: END. " + str(self))
                    exception = End
                    raise exception
                elif len(line) < 2:
                    logging.warning("File.read: SHORT? " + str(self) + " \"" + str(line) + "\"")
                    line = None
                elif line[-1] != '\n':
                    logging.warning("File.read: LINEFEED? " + str(self) + " \"" + str(line) + "\"")
                    line = None
                elif line[-2] != '\r':
                    logging.warning("File.read: CARRIAGERETURN? " + str(self) + " \"" + str(line) + "\"")
                    line = None
                else:
                    line = line[0:-2]
                    logging.debug("File.read: \"" + str(line) + "\"")
            finally:
                pass
        return line

    def write(self, line):
        result = False
        if self.file != None:
            try:
                self.file.write(str(line))
                self.file.write("\r\n")
                self.file.flush()
            except Exception as exception:
                logging.error("File.write: FAILED! " + str(self) + " " + str(exception))
                raise exception
            else:
                result = True
                logging.debug("File.write: \"" + str(line) + "\"")
            finally:
                pass
        return result
