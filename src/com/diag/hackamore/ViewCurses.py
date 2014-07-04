"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import curses.ascii
import sys

from ViewPrint import ViewPrint

class ViewCurses(ViewPrint):
    """
    ViewCurses is a kind of ViewPrint that clears the display and rehomes its
    cursor using standard ANSI escape sequence just before displaying an Event
    and its effect on the Model.
    """

    #
    # CTOR/DTOR
    #

    def __init__(self, model, logger = None):
        ViewPrint.__init__(self, model, logger = logger)
        self.erase = chr(curses.ascii.ESC) + "[2J"
        self.home = chr(curses.ascii.ESC) + "[1;1H"

    def __del__(self):
        pass

    def __repr__(self):
        return ViewPrint.__repr__(self) + ".ViewCurses()"
    
    #
    # PROTECTED
    #
        
    def preevent(self):
        """
        Erase the display before viewing an event.
        """
        sys.stdout.write(self.erase)
        sys.stdout.write(self.home)
