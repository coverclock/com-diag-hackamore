"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import sys

import Event

from View import View
from Channel import ROLE
from Channel import ACTIVITY
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

    def printline(self, label, pbx, uniqueid, channel, calleridnum, role, activity, channelstatedesc, conference, call, sipcallid):
        printf("%s %-16s %-16s %-64s %-16s %-8s %-8s %-8s %-8s %-12s %s\n", label, pbx, uniqueid, channel, calleridnum, role, activity, channelstatedesc, conference, call, sipcallid)

    def printchannel(self, chan):
        self.printline("    ", chan.pbx, chan.uniqueid, chan.channel, chan.calleridnum if chan.calleridnum else None, ROLE[chan.role], ACTIVITY[chan.activity], chan.channelstatedesc, chan.conference, hex(id(chan.call)) if chan.call != None else None, chan.sipcallid.split("@", 1)[0] if chan.sipcallid != None else None)
    
    #
    # PROTECTED
    #
        
    def preevent(self):
        """
        Do whatever needs to be done before viewing an event.
        The default is to do nothing.
        """
        pass

    def postevent(self):
        """
        Do whatever needs to be done after viewing an event.
        The default is to flush the event view to the display.
        """
        sys.stdout.flush()

    def predisplay(self):
        """
        Do whatever needs to be done before viewing the model.
        The default is to do nothing.
        """
        pass

    def postdisplay(self):
        """
        Do whatever needs to be done after viewing the model.
        The default is to flush the model view to the display.
        """
        sys.stdout.flush()

    #
    # PUBLIC
    #
    
    def bridge(self, pbx, uniqueid1, channel1, callerid1, uniqueid2, channel2, callerid2):
        self.preevent()
        print "EVENT", self.sn, Event.BRIDGE, pbx, uniqueid1, channel1, callerid1, uniqueid2, channel2, callerid2
        self.sn = self.sn + 1
        self.postevent()

    def confbridgeend(self, pbx, conference):
        self.preevent()
        print "EVENT", self.sn, Event.CONFBRIDGEEND, pbx, conference
        self.sn = self.sn + 1
        self.postevent()

    def confbridgejoin(self, pbx, uniqueid, channel, conference):
        self.preevent()
        print "EVENT", self.sn, Event.CONFBRIDGEJOIN, pbx, uniqueid, channel, conference
        self.sn = self.sn + 1
        self.postevent()

    def confbridgeleave(self, pbx, uniqueid, channel, conference):        
        self.preevent()
        print "EVENT", self.sn, Event.CONFBRIDGELEAVE, pbx, uniqueid, channel, conference
        self.sn = self.sn + 1
        self.postevent()

    def confbridgestart(self, pbx, conference):        
        self.preevent()
        print "EVENT", self.sn, Event.CONFBRIDGESTART, pbx, conference
        self.sn = self.sn + 1
        self.postevent()

    def dial(self, pbx, uniqueid, channel, destuniqueid, destination):
        self.preevent()
        print "EVENT", self.sn, Event.DIAL, pbx, uniqueid, channel, destuniqueid, destination
        self.sn = self.sn + 1
        self.postevent()

    def end(self, pbx):
        self.preevent()
        print "EVENT", self.sn, Event.END, pbx
        self.sn = self.sn + 1
        self.postevent()

    def hangup(self, pbx, uniqueid, channel):
        self.preevent()
        print "EVENT", self.sn, Event.HANGUP, pbx, uniqueid, channel
        self.sn = self.sn + 1
        self.postevent()

    def localbridge(self, pbx, uniqueid1, channel1, uniqueid2, channel2):
        self.preevent()
        print "EVENT", self.sn, Event.LOCALBRIDGE, pbx, uniqueid1, channel1, uniqueid2, channel2
        self.sn = self.sn + 1
        self.postevent()

    def newchannel(self, pbx, uniqueid, channel, calleridnum, channelstate, channelstatedesc):
        self.preevent()
        print "EVENT", self.sn, Event.NEWCHANNEL, pbx, uniqueid, channel, calleridnum, channelstate, channelstatedesc
        self.sn = self.sn + 1
        self.postevent()

    def newstate(self, pbx, uniqueid, channel, channelstate, channelstatedesc):
        self.preevent()
        print "EVENT", self.sn, Event.NEWSTATE, pbx, uniqueid, channel, channelstate, channelstatedesc
        self.sn = self.sn + 1
        self.postevent()

    def rename(self, pbx, uniqueid, channel, newname):
        self.preevent()
        print "EVENT", self.sn, Event.RENAME, pbx, uniqueid, channel, newname
        self.sn = self.sn + 1
        self.postevent()

    def sipcallid(self, pbx, uniqueid, channel, value):
        self.preevent()
        print "EVENT", self.sn, Event.SIPCALLID, pbx, uniqueid, channel, value
        self.sn = self.sn + 1
        self.postevent()

    def hanguprequest(self, pbx, uniqueid, channel):
        self.preevent()
        print "EVENT", self.sn, Event.HANGUPREQUEST, pbx, uniqueid, channel
        self.sn = self.sn + 1
        self.postevent()

    def musiconhold(self, pbx, uniqueid, channel):
        self.preevent()
        print "EVENT", self.sn, Event.MUSICONHOLD, pbx, uniqueid, channel, Event.START
        self.sn = self.sn + 1
        self.postevent()

    def musicoffhold(self, pbx, uniqueid, channel):
        self.preevent()
        print "EVENT", self.sn, Event.MUSICONHOLD, pbx, uniqueid, channel, Event.STOP
        self.sn = self.sn + 1

    def newcallerid(self, pbx, uniqueid, channel, calleridnum):
        self.preevent()
        print "EVENT", self.sn, Event.NEWCALLERID, pbx, uniqueid, channel, calleridnum
        self.sn = self.sn + 1
        self.postevent()

    def softhanguprequest(self, pbx, uniqueid, channel, cause):
        self.preevent()
        print "EVENT", self.sn, Event.SOFTHANGUPREQUEST, pbx, uniqueid, channel, cause
        self.sn = self.sn + 1
        self.postevent()

    def display(self):
        self.predisplay()
        self.printline("VIEW", "SOURCE", "UNIQUEID", "CHANNEL", "CALLERID", "ROLE", "ACTIVITY", "STATE", "BRIDGE", "CALL", "SIPCALLID")
        if self.model.channels:
            printf(" CHANNELS\n")
            for pbx in self.model.channels:
                channels = self.model.channels[pbx]
                for channel in channels:
                    chan = channels[channel]
                    self.printchannel(chan)
        if self.model.calls:
            for call in self.model.calls:
                printf(" CALL\n")
                for chan in call:
                    self.printchannel(chan)
        if self.model.bridges:
            printf(" BRIDGES\n")
            for pbx in self.model.bridges:
                bridges = self.model.bridges[pbx]
                for conference in bridges:
                    bridge = bridges[conference]
                    for uniqueid in bridge:
                        chan = bridge[uniqueid]
                        self.printchannel(chan)
        if self.model.trunks:
            printf(" TRUNKS\n")
            for sipcallid in self.model.trunks:
                chan = self.model.trunks[sipcallid]
                self.printchannel(chan)
        if self.model.numbers:
            printf(" NUMBERS\n")
            for pbx in self.model.numbers:
                numbers = self.model.numbers[pbx]
                for channel in numbers:
                    calleridnum = numbers[channel]
                    self.printline("    ", pbx, "", channel, calleridnum, "", "", "", "", "", "")
        self.postdisplay()
