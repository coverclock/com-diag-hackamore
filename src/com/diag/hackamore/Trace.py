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

class Trace(Source):
    """
    Trace describes a Source that is like a File. But unlike a File, a Trace
    can be closed and reopened to pick up reading where it left off. Also,
    Traces already contain the SOURCE and TIME entries for each event, and an
    END event, and so these are not generated as the Trace is processed. 
    """
    
    #####
    ##### CTOR/DTOR
    #####

    def __init__(self, pbx, path, bufsize = READLINE, logger = None):
        """
        Constructor.
        @param pbx is the name of the source.
        @param path is the pathname to the file in the file system.
        @param bufsize is an optional read buffer size in bytes.
        @param logger is an optional Logger used to log messages.
        """
        Source.__init__(self, pbx, logger = logger)
        self.path = path
        self.active = False
        self.eof = False
        self.file = None
        self.bufsize = bufsize

    def __del__(self):
        self.force()

    def __repr__(self):
        return Source.__repr__(self) + ".Trace(" + str(self.path) + ")"

    #####
    ##### PROTECTED
    #####

    def initialize(self):
        pass       
    
    def finalize(self):
        pass
        
    def terminate(self):
        pass

    #####
    ##### PUBLIC
    #####

    def open(self):
        result = False
        if self.active:
            pass
        elif self.eof:
            pass
        elif self.file != None:
            self.active = True
            result = True
        else:
            try:
                self.file = open(self.path, OPEN)
            except Exception as exception:
                self.logger.error("Trace.open: FAILED! %s %s", str(self), str(exception))
            else:
                self.logger.info("Trace.open: OPENED. %s", str(self))
                Source.open(self)
                self.active = True
                self.eof = False
                result = True
            finally:
                pass
        return result
                
    def close(self):
        result = False
        if not self.active:
            pass
        elif self.file == None:
            pass
        elif not self.eof:
            self.active = False
            result = True
        else:
            try:
                self.file.close()
            except Exception as exception:
                self.logger.error("File.close: FAILED! %s %s", str(self), str(exception))
            else:
                self.logger.info("File.close: CLOSED. %s", str(self))
            finally:
                self.active = False
                self.eof = True
                self.file = None
                Source.close(self)
                result = True
        return result
 
    def fileno(self):
        return self.file.fileno() if (self.file != None) and self.active else -1

    def read(self, multiplex = None):
        line = None
        if not self.active:
            pass
        elif self.file == None:
            pass
        else:
            try:
                line = self.file.readline(self.bufsize)
            except Exception as exception:
                self.logger.error("Trace.read: FAILED! %s %s", str(self), str(exception))
                self.eof = True
                raise exception
            else:
                if line == None:
                    pass
                elif not line:
                    self.logger.info("Trace.read: END. %s", str(self))
                    self.eof = True
                    exception = End
                    raise exception
                elif len(line) < 2:
                    self.logger.warning("Trace.read: SHORT? %s", str(self))
                    line = None
                elif line[-1] != '\n':
                    self.logger.warning("Trace.read: LINEFEED? %s", str(self))
                    line = None
                elif line[-2] != '\r':
                    self.logger.warning("Trace.read: CARRIAGERETURN? %s", str(self))
                    line = None
                else:
                    line = line[0:-2]
                    if self.logger.isEnabledFor(logging.DEBUG):
                        self.logger.debug("Trace.read: READ: %s \"%s\"", str(self), str(line))
            finally:
                pass
        return line

    def force(self):
        """
        Force a real close (whatever that means on the underlying platform).
        @return True is successful, False otherwise.
        """
        self.active = True
        self.eof = True
        return self.close()
