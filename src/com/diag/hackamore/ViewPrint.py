"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

from View import View

import Event

class ViewPrint(View):

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

    def refresh(self):
        print "VIEW"
        if self.model.channels:
            print "", "CHANNELS"
            for pbx in self.model.channels:
                print "", "", "SOURCE", pbx
                channels = self.model.channels[pbx]
                for channel in channels:
                    chan = channels[channel]
                    chan.dump()
        if self.model.calls:
            print "", "CALLS"
            for call in self.model.calls:
                print "", "", "CALL", hex(id(call))
                for chan in call:
                    chan.dump()
        if self.model.bridges:
            print "", "BRIDGES"
            for pbx in self.model.bridges:
                print "", "", "SOURCE", pbx
                bridges = self.model.bridges[pbx]
                for conference in bridges:
                    print "", "", "", "BRIDGE", conference
                    bridge = bridges[conference]
                    for uniqueid in bridge:
                        chan = bridge[uniqueid]
                        chan.dump()
        if self.model.trunks:
            print "", "TRUNKS"
            for sipcallid in self.model.trunks:
                print "", "", "ID", sipcallid
                chan = self.model.trunks[sipcallid]
                chan.dump()
        if self.model.numbers:
            print "", "NUMBERS"
            for channel in self.model.numbers:
                calleridnum = self.model.numbers[channel]
                print "", "", "NUMBER", calleridnum, channel
