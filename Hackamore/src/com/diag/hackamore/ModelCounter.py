"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import Event

from Model import Model

class ModelCounter(Model):
    """
    ModelCounter is a kind of Model that just counts how many of each Event
    occurs. It does not make any changes to the dynamic call state in the base
    class. It is mostly used for unit testing.
    """
    
    #####
    ##### CTOR/DTOR
    #####

    def __init__(self, logger = None):
        Model.__init__(self, logger)
        self.counter = { }
        self.counter[Event.BRIDGE] = 0
        self.counter[Event.CONFBRIDGEEND] = 0
        self.counter[Event.CONFBRIDGEJOIN] = 0
        self.counter[Event.CONFBRIDGELEAVE] = 0
        self.counter[Event.CONFBRIDGESTART] = 0
        self.counter[Event.DIAL] = 0
        self.counter[Event.END] = 0
        self.counter[Event.HANGUP] = 0
        self.counter[Event.LOCALBRIDGE] = 0
        self.counter[Event.NEWCHANNEL] = 0
        self.counter[Event.NEWSTATE] = 0
        self.counter[Event.RENAME] = 0
        self.counter[Event.SIPCALLID] = 0

    def __del__(self):
        pass

    def __repr__(self):
        return Model.__repr__(self) + ".ModelCounter()"
    
    #####
    ##### PUBLIC
    #####
    
    def bridge(self, pbx, uniqueid1, uniqueid2):
        self.counter[Event.BRIDGE] = self.counter[Event.BRIDGE] + 1

    def confbridgeend(self, pbx, conference):
        self.counter[Event.CONFBRIDGEEND] = self.counter[Event.CONFBRIDGEEND] + 1
    
    def confbridgejoin(self, pbx, uniqueid, conference):
        self.counter[Event.CONFBRIDGEJOIN] = self.counter[Event.CONFBRIDGEJOIN] + 1
    
    def confbridgeleave(self, pbx, uniqueid, conference):
        self.counter[Event.CONFBRIDGELEAVE] = self.counter[Event.CONFBRIDGELEAVE] + 1
    
    def confbridgestart(self, pbx, conference):
        self.counter[Event.CONFBRIDGESTART] = self.counter[Event.CONFBRIDGESTART] + 1
    
    def dial(self, pbx, uniqueid, destuniqueid):
        self.counter[Event.DIAL] = self.counter[Event.DIAL] + 1
    
    def end(self, pbx):
        self.counter[Event.END] = self.counter[Event.END] + 1

    def hangup(self, pbx, uniqueid):
        self.counter[Event.HANGUP] = self.counter[Event.HANGUP] + 1
    
    def localbridge(self, pbx, uniqueid1, uniqueid2):
        self.counter[Event.LOCALBRIDGE] = self.counter[Event.LOCALBRIDGE] + 1
    
    def newchannel(self, pbx, uniqueid, channel, calleridnum, channelstate, channelstatedesc):
        self.counter[Event.NEWCHANNEL] = self.counter[Event.NEWCHANNEL] + 1
    
    def newstate(self, pbx, uniqueid, channelstate, channelstatedesc):
        self.counter[Event.NEWSTATE] = self.counter[Event.NEWSTATE] + 1
    
    def rename(self, pbx, uniqueid, newname):
        self.counter[Event.RENAME] = self.counter[Event.RENAME] + 1

    def sipcallid(self, pbx, uniqueid, value):
        self.counter[Event.SIPCALLID] = self.counter[Event.SIPCALLID] + 1
