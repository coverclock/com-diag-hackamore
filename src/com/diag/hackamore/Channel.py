"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

IDLE = 0
CALLING = 1
CALLED = 2
BRIDGE = 3

ROLE = ( "IDLE", "CALLING", "CALLED", "BRIDGE" )

class Channel():

    def __init__(self, uniqueid, channel, channelstate, channelstatedesc):
        self.uniqueid = uniqueid
        self.channel = channel
        self.channelstate = channelstate
        self.channelstatedesc = channelstatedesc
        self.role = IDLE
            
    def __del__(self):
        pass

    def __repr__(self):
        return "Channel(" + str(self.uniqueid) + "," + str(self.channel) + "," + str(self.channelstatedesc) + "," + str(ROLE[self.role]) + ")"

    def name(self):
        return self.uniqueid[0]

    def id(self):
        return self.uniqueid[1]

    def newstate(self, channelstate, channelstatedesc):
        self.channelstate = channelstate
        self.channelstatedesc = channelstatedesc

    def rename(self, channel):
        self.channel = channel

    def calling(self):
        if self.role == IDLE:
            self.role = CALLING
        elif self.role == CALLED:
            self.role = BRIDGE
        else:
            pass
    
    def called(self):
        if self.role == IDLE:
            self.role = CALLED
        elif self.role == CALLING:
            self.role = BRIDGE
        else:
            pass
