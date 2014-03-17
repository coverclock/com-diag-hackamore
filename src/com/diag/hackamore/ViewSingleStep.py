"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import sys

from ViewCurses import ViewCurses

class ViewSingleStep(ViewCurses):
    """
    ViewSingleStep is a kind of ViewPrint (even though it derives from
    ViewCurses) that waits for the user to hit the return key before proceeding
    to the next display of an Event and its associated changes to the Model.
    """

    #
    # CTOR/DTOR
    #

    def __init__(self, model, logger = None):
        ViewCurses.__init__(self, model, logger = logger)

    def __del__(self):
        pass

    def __repr__(self):
        return ViewCurses.__repr__(self) + ".ViewSingleStep()"
         
    #
    # PRIVATE
    #
        
    def before(self):
        pass

    def during(self):
        sys.stdout.write(">")
        sys.stdout.flush()
        sys.stdin.readline()

    def after(self):
        sys.stdout.write(">")
        sys.stdout.flush()
        sys.stdin.readline()
