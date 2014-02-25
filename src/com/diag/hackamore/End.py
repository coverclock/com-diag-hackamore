"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

class End(Exception):

    def __init__(self, payload):
        self.payload = payload
        
    def __del__(self):
        pass

    def __repr__(self):
        return "End(\"" + str(self.payload) + "\")"
