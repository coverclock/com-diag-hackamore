"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import sys
import Source

class File(Source):

    def __init__(self, name, path):
        super.__init__(name)
        self.path = path
        self.eof = False

    def __del__(self):
        self.close()

    def __repr__(self):
        return super.__repr__() + ".File(\"" + str(self.path) + "\")"

    def open(self):
        try:
            self.file = open(self.path, "rb")
        except Exception as exception:
            sys.stderr.write("File.open: \"" + str(self.path) + "\" failed! \"" + str(exception) + "\"\n")
            self.close()
        else:
            super.open()
        finally:
            pass
                
    def close(self):
        self.eof = True
        if self.file != None:
            try:
                self.file.close()
            except Exception as exception:
                sys.stderr.write("File.close: failed! error=\"" + str(exception) + "\"\n")
            else:
                pass
            finally:
                self.file = None
        super.close()
 
    def fileno(self):
        if (self.file == None) and (not self.eof):
            self.open()
        return super.fileno()
