"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import Event

from View import View
from Channel import ROLE
from stdio import printf

class ViewPrint(View):
    """
    ViewPrint is a kind of View that displays each Event and its effect on the
    associated Model on the Standard Output stream.
    """

    #####
    ##### CTOR/DTOR
    #####

    def __init__(self, model, logger = None):
        View.__init__(self, model, logger = logger)
        self.sn = 0

    def __del__(self):
        pass

    def __repr__(self):
        return View.__repr__(self) + ".ViewPrint()"

    #####
    ##### PRIVATE
    #####

    def channel(self, chan):
        #print "", "", "", "", "CHANNEL", self.pbx, self.uniqueid, self.channel, self.calleridnum if self.calleridnum else None, ROLE[self.role], self.channelstatedesc, self.sipcallid, self.conference, hex(id(self.call)) if self.call != None else self.call
        printf("    CHANNEL %-8s %-16s %-64s %-8s %-8s %-8s %-8s %-10s\n", chan.pbx, chan.uniqueid, chan.channel, chan.calleridnum if chan.calleridnum else None, ROLE[chan.role], chan.channelstatedesc, chan.conference, hex(id(chan.call)) if chan.call != None else None)

    #####
    ##### PUBLIC
    #####
    
    def bridge(self, pbx, uniqueid1, channel1, callerid1, uniqueid2, channel2, callerid2):
        print "EVENT", self.sn, Event.BRIDGE, pbx, uniqueid1, channel1, callerid1, uniqueid2, channel2, callerid2
        self.sn = self.sn + 1

    def confbridgeend(self, pbx, conference):
        print "EVENT", self.sn, Event.CONFBRIDGEEND, pbx, conference
        self.sn = self.sn + 1

    def confbridgejoin(self, pbx, uniqueid, channel, conference):
        print "EVENT", self.sn, Event.CONFBRIDGEJOIN, pbx, uniqueid, channel, conference
        self.sn = self.sn + 1

    def confbridgeleave(self, pbx, uniqueid, channel, conference):        
        print "EVENT", self.sn, Event.CONFBRIDGELEAVE, pbx, uniqueid, channel, conference
        self.sn = self.sn + 1

    def confbridgestart(self, pbx, conference):        
        print "EVENT", self.sn, Event.CONFBRIDGESTART, pbx, conference
        self.sn = self.sn + 1

    def dial(self, pbx, uniqueid, channel, destuniqueid, destination):
        print "EVENT", self.sn, Event.DIAL, pbx, uniqueid, channel, destuniqueid, destination
        self.sn = self.sn + 1

    def end(self, pbx):
        print "EVENT", self.sn, Event.END, pbx
        self.sn = self.sn + 1

    def hangup(self, pbx, uniqueid, channel):
        print "EVENT", self.sn, Event.HANGUP, pbx, uniqueid, channel
        self.sn = self.sn + 1

    def localbridge(self, pbx, uniqueid1, channel1, uniqueid2, channel2):
        print "EVENT", self.sn, Event.LOCALBRIDGE, pbx, uniqueid1, channel1, uniqueid2, channel2
        self.sn = self.sn + 1

    def newchannel(self, pbx, uniqueid, channel, calleridnum, channelstate, channelstatedesc):
        print "EVENT", self.sn, Event.NEWCHANNEL, pbx, uniqueid, channel, calleridnum, channelstate, channelstatedesc
        self.sn = self.sn + 1

    def newstate(self, pbx, uniqueid, channel, channelstate, channelstatedesc):
        print "EVENT", self.sn, Event.NEWSTATE, pbx, uniqueid, channel, channelstate, channelstatedesc
        self.sn = self.sn + 1

    def rename(self, pbx, uniqueid, channel, newname):
        print "EVENT", self.sn, Event.RENAME, pbx, uniqueid, channel, newname
        self.sn = self.sn + 1

    def sipcallid(self, pbx, uniqueid, channel, value):
        print "EVENT", self.sn, Event.SIPCALLID, pbx, uniqueid, channel, value
        self.sn = self.sn + 1

    def display(self):
        printf("VIEW\n")
        if self.model.channels:
            printf(" CHANNELS\n")
            for pbx in self.model.channels:
                printf("  SOURCE %s\n", pbx)
                channels = self.model.channels[pbx]
                for channel in channels:
                    chan = channels[channel]
                    self.channel(chan)
        if self.model.calls:
            printf(" CALLS\n")
            for call in self.model.calls:
                printf("  CALL 0x%x\n", id(call))
                for chan in call:
                    self.channel(chan)
        if self.model.bridges:
            printf(" BRIDGES\n")
            for pbx in self.model.bridges:
                printf("  SOURCE %s\n", pbx)
                bridges = self.model.bridges[pbx]
                for conference in bridges:
                    printf("   BRIDGE %s\n", conference)
                    bridge = bridges[conference]
                    for uniqueid in bridge:
                        chan = bridge[uniqueid]
                        self.channel(chan)
        if self.model.trunks:
            printf(" TRUNKS\n")
            for sipcallid in self.model.trunks:
                printf("  ID %s\n", sipcallid)
                chan = self.model.trunks[sipcallid]
                self.channel(chan)
        if self.model.numbers:
            printf(" NUMBERS\n")
            for pbx in self.model.numbers:
                printf("  SOURCE %s\n", pbx)
                numbers = self.model.numbers[pbx]
                for channel in numbers:
                    calleridnum = numbers[channel]
                    printf("   NUMBER %-8s %-64s\n", calleridnum, channel)
