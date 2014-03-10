"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import curses.ascii
import sys

from ViewPrint import ViewPrint

class ViewCurses(ViewPrint):

    #####
    ##### CTOR/DTOR
    #####

    def __init__(self, model, logger = None):
        ViewPrint.__init__(self, model, logger = logger)
        self.erase = chr(curses.ascii.ESC) + "[2J"
        self.home = chr(curses.ascii.ESC) + "[1;1H"

    def __del__(self):
        pass

    def __repr__(self):
        return ViewPrint.__repr__(self) + ".ViewCurses()"
    
    #####
    ##### PRIVATE
    #####
        
    def before(self):
        sys.stdout.write(self.erase)
        sys.stdout.write(self.home)
        sys.stdout.flush()
    
    def during(self):
        sys.stdout.flush()

    def after(self):
        sys.stdout.flush()

    #####
    ##### PUBLIC
    #####
    
    def bridge(self, pbx, uniqueid1, channel1, callerid1, uniqueid2, channel2, callerid2):
        self.before()
        ViewPrint.bridge(self, pbx, uniqueid1, channel1, callerid1, uniqueid2, channel2, callerid2)
        self.during()

    def confbridgeend(self, pbx, conference):
        self.before()
        ViewPrint.confbridgeend(self, pbx, conference)
        self.during()

    def confbridgejoin(self, pbx, uniqueid, channel, conference):
        self.before()
        ViewPrint.confbridgejoin(self, pbx, uniqueid, channel, conference)
        self.during()

    def confbridgeleave(self, pbx, uniqueid, channel, conference):        
        self.before()
        ViewPrint.confbridgeleave(self, pbx, uniqueid, channel, conference)
        self.during()

    def confbridgestart(self, pbx, conference):        
        self.before()
        ViewPrint.confbridgestart(self, pbx, conference)
        self.during()

    def dial(self, pbx, uniqueid, channel, destuniqueid, destination):
        self.before()
        ViewPrint.dial(self, pbx, uniqueid, channel, destuniqueid, destination)
        self.during()

    def end(self, pbx):
        self.before()
        ViewPrint.end(self, pbx)
        self.during()
        pass

    def hangup(self, pbx, uniqueid, channel):
        self.before()
        ViewPrint.hangup(self, pbx, uniqueid, channel)
        self.during()

    def localbridge(self, pbx, uniqueid1, channel1, uniqueid2, channel2):
        self.before()
        ViewPrint.localbridge(self, pbx, uniqueid1, channel1, uniqueid2, channel2)
        self.during()

    def newchannel(self, pbx, uniqueid, channel, calleridnum, channelstate, channelstatedesc):
        self.before()
        ViewPrint.newchannel(self, pbx, uniqueid, channel, calleridnum, channelstate, channelstatedesc)
        self.during()

    def newstate(self, pbx, uniqueid, channel, channelstate, channelstatedesc):
        self.before()
        ViewPrint.newstate(self, pbx, uniqueid, channel, channelstate, channelstatedesc)
        self.during()

    def rename(self, pbx, uniqueid, channel, newname):
        self.before()
        ViewPrint.rename(self, pbx, uniqueid, channel, newname)
        self.during()

    def sipcallid(self, pbx, uniqueid, channel, value):
        self.before()
        ViewPrint.sipcallid(self, pbx, uniqueid, channel, value)
        self.during()

    def display(self):
        ViewPrint.display(self)
        self.after()
