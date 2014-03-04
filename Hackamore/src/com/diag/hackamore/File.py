"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import logging

from Source import Source
from End import End

READLINE = 512
OPEN = "rb"

class File(Source):

    def __init__(self, name, path, bufsize = READLINE, logger = None):
        Source.__init__(self, name, logger = logger)
        self.path = path
        self.eof = False
        self.file = None
        self.bufsize = bufsize
        self.logger.info("File: INIT. %s", str(self))

    def __del__(self):
        self.close()

    def __repr__(self):
        return Source.__repr__(self) + ".File(\"" + str(self.path) + "\")"

    def open(self):
        result = False
        if self.eof:
            pass
        elif self.file != None:
            pass
        else:
            try:
                self.file = open(self.path, OPEN)
            except Exception as exception:
                self.logger.error("File.open: FAILED! %s %s", str(self), str(exception))
            else:
                self.logger.info("File.open: OPENED. %s", str(self))
                Source.open(self)
                result = True
            finally:
                pass
        return result
                
    def close(self):
        result = False
        if self.file != None:
            try:
                self.file.close()
            except Exception as exception:
                self.logger.error("File.close: FAILED! %s %s", str(self), str(exception))
            else:
                self.logger.info("File.close: CLOSED. %s", str(self))
            finally:
                self.eof = True
                self.file = None
                Source.close(self)
                result = True
        return result
 
    def fileno(self):
        return self.file.fileno()

    def read(self, multiplexing = False):
        line = None
        if self.file != None:
            try:
                line = self.file.readline(self.bufsize)
            except Exception as exception:
                self.logger.error("File.read: FAILED! %s %s", str(self), str(exception))
                raise exception
            else:
                if line == None:
                    pass
                elif not line:
                    self.logger.info("File.read: END. %s", str(self))
                    exception = End
                    raise exception
                elif len(line) < 2:
                    self.logger.warning("File.read: SHORT? %s", str(self))
                    line = None
                elif line[-1] != '\n':
                    self.logger.warning("File.read: LINEFEED? %s", str(self))
                    line = None
                elif line[-2] != '\r':
                    self.logger.warning("File.read: CARRIAGERETURN? %s", str(self))
                    line = None
                else:
                    line = line[0:-2]
                    if self.logger.isEnabledFor(logging.DEBUG):
                        self.logger.debug("File.read: READ: %s \"%s\"", str(self), str(line))
            finally:
                pass
        return line
