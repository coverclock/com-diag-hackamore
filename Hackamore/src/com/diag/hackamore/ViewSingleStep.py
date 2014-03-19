"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import sys

from ViewPrint import ViewPrint

class ViewSingleStep(ViewPrint):
    """
    ViewSingleStep is a kind of ViewPrint that waits for the user to hit the
    return key before proceeding to the next display of an Event and its
    associated changes to the Model.
    """

    #
    # CTOR/DTOR
    #

    def __init__(self, model, logger = None):
        ViewPrint.__init__(self, model, logger = logger)

    def __del__(self):
        pass

    def __repr__(self):
        return ViewPrint.__repr__(self) + ".ViewSingleStep()"
         
    #
    # PRIVATE
    #
        
    def postevent(self):
        sys.stdout.write(">")
        sys.stdout.flush()
        sys.stdin.readline()

    def postdisplay(self):
        sys.stdout.write(">")
        sys.stdout.flush()
        sys.stdin.readline()
