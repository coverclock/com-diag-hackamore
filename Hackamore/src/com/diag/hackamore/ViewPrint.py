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

    #
    # CTOR/DTOR
    #

    def __init__(self, model, logger = None):
        View.__init__(self, model, logger = logger)
        self.sn = 0

    def __del__(self):
        pass

    def __repr__(self):
        return View.__repr__(self) + ".ViewPrint()"

    #
    # PRIVATE
    #

    def printline(self, label, pbx, uniqueid, channel, calleridnum, role, channelstatedesc, conference, call):
        printf("%s %-16s %-16s %-64s %-8s %-8s %-8s %-8s %-10s\n", label, pbx, uniqueid, channel, calleridnum, role, channelstatedesc, conference, call)

    def printchannel(self, chan):
        self.printline("    ", chan.pbx, chan.uniqueid, chan.channel, chan.calleridnum if chan.calleridnum else None, ROLE[chan.role], chan.channelstatedesc, chan.conference, hex(id(chan.call)) if chan.call != None else None)

    #
    # PUBLIC
    #
    
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
        self.printline("VIEW", "SOURCE", "UNIQUEID", "CHANNEL", "CALLERID", "ROLE", "STATE", "BRIDGE", "CALL")
        if self.model.channels:
            printf(" CHANNELS\n")
            for pbx in self.model.channels:
                channels = self.model.channels[pbx]
                for channel in channels:
                    chan = channels[channel]
                    self.printchannel(chan)
        if self.model.calls:
            printf(" CALLS\n")
            for call in self.model.calls:
                printf("  CALL\n")
                for chan in call:
                    self.printchannel(chan)
        if self.model.bridges:
            printf(" BRIDGES\n")
            for pbx in self.model.bridges:
                bridges = self.model.bridges[pbx]
                for conference in bridges:
                    printf("   %s\n", conference)
                    bridge = bridges[conference]
                    for uniqueid in bridge:
                        chan = bridge[uniqueid]
                        self.printchannel(chan)
        if self.model.trunks:
            printf(" TRUNKS\n")
            for sipcallid in self.model.trunks:
                printf("  %s\n", sipcallid)
                chan = self.model.trunks[sipcallid]
                self.printchannel(chan)
        if self.model.numbers:
            printf(" NUMBERS\n")
            for pbx in self.model.numbers:
                numbers = self.model.numbers[pbx]
                for channel in numbers:
                    calleridnum = numbers[channel]
                    self.printline("    ", pbx, "", channel, calleridnum, "", "", "", "")
