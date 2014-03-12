"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

from stdio import printf

IDLE = 0
CALLING = 1
CALLED = 2
TRUNK = 3

ROLE = ( "IDLE", "CALLING", "CALLED", "TRUNK" )

#####
##### PRIVATE
#####

class Channel():
    
    #####
    ##### CTOR/DTOR
    #####

    def __init__(self, pbx, uniqueid, channel, calleridnum, channelstate, channelstatedesc):
        self.pbx = pbx
        self.uniqueid = uniqueid
        self.calleridnum = calleridnum
        self.sipcallid = None
        self.conference = None
        self.channel = channel
        self.channelstate = channelstate
        self.channelstatedesc = channelstatedesc
        self.role = IDLE
        self.call = None
            
    def __del__(self):
        pass

    def __repr__(self):
        return "Channel(" + str(self.pbx) + "," + str(self.uniqueid) + "," + str(self.channel) + "," + str(self.calleridnum) + "," + str(self.sipcallid) + "," + str(self.conference) + "," + str(self.channelstatedesc) + "," + str(ROLE[self.role]) + ")"

    #####
    ##### PUBLIC
    #####

    def newstate(self, channelstate, channelstatedesc):
        self.channelstate = channelstate
        self.channelstatedesc = channelstatedesc

    def rename(self, channel):
        self.channel = channel
        
    def endpoint(self, sipcallid):
        self.sipcallid = sipcallid

    def trunk(self):
        self.role = TRUNK

    def calling(self):
        if self.role == IDLE:
            self.role = CALLING
        elif self.role == CALLED:
            self.role = TRUNK
        else:
            pass
    
    def called(self):
        if self.role == IDLE:
            self.role = CALLED
        elif self.role == CALLING:
            self.role = TRUNK
        else:
            pass

    def dial(self, calleridnum):
        self.calleridnum = calleridnum

    def join(self, conference):
        self.conference = conference

    def leave(self):
        self.conference = None

    def display(self):
        #print "", "", "", "", "CHANNEL", self.pbx, self.uniqueid, self.channel, self.calleridnum if self.calleridnum else None, ROLE[self.role], self.channelstatedesc, self.sipcallid, self.conference, hex(id(self.call)) if self.call != None else self.call
        printf("    CHANNEL %-8s %-16s %-64s %-8s %-8s %-8s %-8s %-10s\n", self.pbx, self.uniqueid, self.channel, self.calleridnum if self.calleridnum else None, ROLE[self.role], self.channelstatedesc, self.conference, hex(id(self.call)) if self.call != None else self.call)
