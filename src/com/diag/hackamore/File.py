"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import logging

from Source import Source

class File(Source):

    def __init__(self, name, path):
        Source.__init__(self, name)
        self.path = path
        self.eof = False

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
        return Source.fileno(self)
