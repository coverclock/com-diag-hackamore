"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import Logger
import Event

from stdio import fprintf

class Manifold:
    """
    A Manifold maps each Event to the individual functions calls in a Model
    and View. There may be more than one kind of Manifold, each kind handling
    the specific kinds of Models and Views for which it was designed.
    """

    #
    # CTOR/DTOR
    #

    def __init__(self, model, view, tracer = None, logger = None):
        """
        Constructor.
        @param model is the Model associated with this Manifold.
        @param view is the View associated with this Manifold.
        @param tracer is an optional writeable object to which a Trace is generated.
        @param logger is an optional Logger.
        """
        self.logger = Logger.logger() if logger == None else logger
        self.tracer = tracer
        self.model = model
        self.view = view
        self.table = { }
        self.table[Event.BRIDGE]            = self.bridge
        self.table[Event.CONFBRIDGEEND]     = self.confbridgeend
        self.table[Event.CONFBRIDGEJOIN]    = self.confbridgejoin
        self.table[Event.CONFBRIDGELEAVE]   = self.confbridgeleave
        self.table[Event.CONFBRIDGESTART]   = self.confbridgestart
        self.table[Event.DIAL]              = self.dial
        self.table[Event.END]               = self.end
        self.table[Event.HANGUP]            = self.hangup
        self.table[Event.HANGUPREQUEST]     = self.hanguprequest
        self.table[Event.LOCALBRIDGE]       = self.localbridge
        self.table[Event.MUSICONHOLD]       = self.musiconhold
        self.table[Event.NEWCALLERID]       = self.newcallerid
        self.table[Event.NEWCHANNEL]        = self.newchannel
        self.table[Event.NEWSTATE]          = self.newstate
        self.table[Event.RENAME]            = self.rename
        self.table[Event.SOFTHANGUPREQUEST] = self.softhanguprequest
        self.table[Event.VARSET]            = self.varset

    def __del__(self):
        pass

    def __repr__(self):
        return "Manifold(" + str(self.model) + "," + str(self.view) + ")"

    #
    # PRIVATE
    #
    
    def bridge(self, event):
        if not Event.SOURCE in event:
            pass
        elif not Event.CALLERID1 in event:
            pass
        elif not Event.CALLERID2 in event:
            pass
        elif not Event.CHANNEL1 in event:
            pass
        elif not Event.CHANNEL2 in event:
            pass
        elif not Event.UNIQUEID1 in event:
            pass
        elif not Event.UNIQUEID2 in event:
            pass
        else:
            pbx = event[Event.SOURCE]
            callerid1 = event[Event.CALLERID1]
            callerid2 = event[Event.CALLERID2]
            channel1 = event[Event.CHANNEL1]
            channel2 = event[Event.CHANNEL2]
            uniqueid1 = event[Event.UNIQUEID1]
            uniqueid2 = event[Event.UNIQUEID2]
            self.view.bridge(pbx, uniqueid1, channel1, callerid1, uniqueid2, channel2, callerid2)
            self.model.bridge(pbx, uniqueid1, uniqueid2)
            self.view.display()

    def confbridgeend(self, event):
        if not Event.SOURCE in event:
            pass
        elif not Event.CONFERENCE in event:
            pass
        else:
            pbx = event[Event.SOURCE]
            conference = event[Event.CONFERENCE]
            self.view.confbridgeend(pbx, conference)
            self.model.confbridgeend(pbx, conference)
            self.view.display()
    
    def confbridgejoin(self, event):
        if not Event.SOURCE in event:
            pass
        elif not Event.CHANNEL in event:
            pass
        elif not Event.CONFERENCE in event:
            pass
        elif not Event.UNIQUEIDLC in event:
            pass
        else:
            pbx = event[Event.SOURCE]
            channel = event[Event.CHANNEL]
            conference = event[Event.CONFERENCE]
            uniqueid = event[Event.UNIQUEIDLC]
            self.view.confbridgejoin(pbx, uniqueid, channel, conference)
            self.model.confbridgejoin(pbx, uniqueid, conference)
            self.view.display()
    
    def confbridgeleave(self, event):
        if not Event.SOURCE in event:
            pass
        elif not Event.CHANNEL in event:
            pass
        elif not Event.CONFERENCE in event:
            pass
        elif not Event.UNIQUEIDLC in event:
            pass
        else:
            pbx = event[Event.SOURCE]
            channel = event[Event.CHANNEL]
            conference = event[Event.CONFERENCE]
            uniqueid = event[Event.UNIQUEIDLC]
            self.view.confbridgeleave(pbx, uniqueid, channel, conference)
            self.model.confbridgeleave(pbx, uniqueid, conference)
            self.view.display()
    
    def confbridgestart(self, event):
        if not Event.SOURCE in event:
            pass
        elif not Event.CONFERENCE in event:
            pass
        else:
            pbx = event[Event.SOURCE]
            conference = event[Event.CONFERENCE]
            self.view.confbridgestart(pbx, conference)
            self.model.confbridgestart(pbx, conference)
            self.view.display()
    
    def dial(self, event):
        if not Event.SOURCE in event:
            pass
        elif not Event.SUBEVENT in event:
            pass
        elif event[Event.SUBEVENT] != Event.BEGIN:
            pass
        elif not Event.CHANNEL in event:
            pass
        elif not Event.DESTINATION in event:
            pass
        elif not Event.DESTUNIQUEID in event:
            pass
        elif not Event.UNIQUEIDUC in event:
            pass
        else:
            pbx = event[Event.SOURCE]
            channel = event[Event.CHANNEL]
            destination = event[Event.DESTINATION]
            destuniqueid = event[Event.DESTUNIQUEID]
            uniqueid = event[Event.UNIQUEIDUC]
            self.view.dial(pbx, uniqueid, channel, destuniqueid, destination)
            self.model.dial(pbx, uniqueid, destuniqueid)
            self.view.display()
    
    def end(self, event):
        if not Event.SOURCE in event:
            pass
        else:
            pbx = event[Event.SOURCE]
            self.view.end(pbx)
            self.model.end(pbx)
            self.view.display()

    def hangup(self, event):
        if not Event.SOURCE in event:
            pass
        elif not Event.CHANNEL in event:
            pass
        elif not Event.UNIQUEIDLC in event:
            pass
        else:
            pbx = event[Event.SOURCE]
            channel = event[Event.CHANNEL]
            uniqueid = event[Event.UNIQUEIDLC]
            self.view.hangup(pbx, uniqueid, channel)
            self.model.hangup(pbx, uniqueid)
            self.view.display()

    def hanguprequest(self, event):
        if not Event.SOURCE in event:
            pass
        elif not Event.CHANNEL in event:
            pass
        elif not Event.UNIQUEIDLC in event:
            pass
        else:
            pbx = event[Event.SOURCE]
            channel = event[Event.CHANNEL]
            uniqueid = event[Event.UNIQUEIDLC]
            self.view.hanguprequest(pbx, uniqueid, channel)
            self.model.hanguprequest(pbx, uniqueid)
            self.view.display()

    def localbridge(self, event):
        if not Event.SOURCE in event:
            pass
        elif not Event.CHANNEL1 in event:
            pass
        elif not Event.CHANNEL2 in event:
            pass
        elif not Event.UNIQUEID1 in event:
            pass
        elif not Event.UNIQUEID2 in event:
            pass
        else:
            pbx = event[Event.SOURCE]
            channel1 = event[Event.CHANNEL1]
            channel2 = event[Event.CHANNEL2]
            uniqueid1 = event[Event.UNIQUEID1]
            uniqueid2 = event[Event.UNIQUEID2]
            self.view.localbridge(pbx, uniqueid1, channel1, uniqueid2, channel2)
            self.model.localbridge(pbx, uniqueid1, uniqueid2)
            self.view.display()

    def musiconhold(self, event):
        if not Event.SOURCE in event:
            pass
        elif not Event.CHANNEL in event:
            pass
        elif not Event.STATE in event:
            pass
        elif not Event.UNIQUEIDUC in event:
            pass
        else:
            pbx = event[Event.SOURCE]
            channel = event[Event.CHANNEL]
            state = event[Event.STATE]
            uniqueid  = event[Event.UNIQUEIDUC]
            if state == Event.START:
                self.view.musiconhold(pbx, uniqueid, channel)
                self.model.musiconhold(pbx, uniqueid)
                self.view.display()
            elif state == Event.STOP:
                self.view.musicoffhold(pbx, uniqueid, channel)
                self.model.musicoffhold(pbx, uniqueid)
                self.view.display()
            else:
                pass

    def newcallerid(self, event):
        if not Event.SOURCE in event:
            pass
        elif not Event.CALLERIDNUM in event:
            pass
        elif not Event.CHANNEL in event:
            pass
        elif not Event.UNIQUEIDLC in event:
            pass
        else:
            pbx = event[Event.SOURCE]
            calleridnum = event[Event.CALLERIDNUM]
            channel = event[Event.CHANNEL]
            uniqueid = event[Event.UNIQUEIDLC]
            self.view.newcallerid(pbx, uniqueid, channel, calleridnum)
            self.model.newcallerid(pbx, uniqueid, channel, calleridnum)
            self.view.display()

    def newchannel(self, event):
        if not Event.SOURCE in event:
            pass
        elif not Event.CALLERIDNUM in event:
            pass
        elif not Event.CHANNEL in event:
            pass
        elif not Event.CHANNELSTATE in event:
            pass
        elif not Event.CHANNELSTATEDESC in event:
            pass
        elif not Event.UNIQUEIDLC in event:
            pass
        else:
            pbx = event[Event.SOURCE]
            calleridnum = event[Event.CALLERIDNUM]
            channel = event[Event.CHANNEL]
            channelstate = event[Event.CHANNELSTATE]
            channelstatedesc = event[Event.CHANNELSTATEDESC]
            uniqueid = event[Event.UNIQUEIDLC]
            self.view.newchannel(pbx, uniqueid, channel, calleridnum, channelstate, channelstatedesc)
            self.model.newchannel(pbx, uniqueid, channel, calleridnum, channelstate, channelstatedesc)
            self.view.display()
    
    def newstate(self, event):
        if not Event.SOURCE in event:
            pass
        elif not Event.CHANNEL in event:
            pass
        elif not Event.CHANNELSTATE in event:
            pass
        elif not Event.CHANNELSTATEDESC in event:
            pass
        elif not Event.UNIQUEIDLC in event:
            pass
        else:
            pbx = event[Event.SOURCE]
            channel = event[Event.CHANNEL]
            channelstate = event[Event.CHANNELSTATE]
            channelstatedesc = event[Event.CHANNELSTATEDESC]
            uniqueid = event[Event.UNIQUEIDLC]
            self.view.newstate(pbx, uniqueid, channel, channelstate, channelstatedesc)
            self.model.newstate(pbx, uniqueid, channelstate, channelstatedesc)
            self.view.display()
    
    def rename(self, event):
        if not Event.SOURCE in event:
            pass
        elif not Event.CHANNEL in event:
            pass
        elif not Event.NEWNAME in event:
            pass
        elif not Event.UNIQUEIDLC in event:
            pass
        else:
            pbx = event[Event.SOURCE]
            channel = event[Event.CHANNEL]
            newname = event[Event.NEWNAME]
            uniqueid = event[Event.UNIQUEIDLC]
            self.view.rename(pbx, uniqueid, channel, newname)
            self.model.rename(pbx, uniqueid, newname)
            self.view.display()

    def softhanguprequest(self, event):
        if not Event.SOURCE in event:
            pass
        elif not Event.CAUSE in event:
            pass
        elif not Event.CHANNEL in event:
            pass
        elif not Event.UNIQUEIDLC in event:
            pass
        else:
            pbx = event[Event.SOURCE]
            cause = event[Event.CAUSE]
            channel = event[Event.CHANNEL]
            uniqueid = event[Event.UNIQUEIDLC]
            self.view.softhanguprequest(pbx, uniqueid, channel, cause)
            self.model.softhanguprequest(pbx, uniqueid, cause)
            self.view.display()

    def varset(self, event):
        if not Event.SOURCE in event:
            pass
        elif not Event.VARIABLE in event:
            pass
        elif event[Event.VARIABLE] != Event.SIPCALLID:
            pass
        elif not Event.CHANNEL in event:
            pass
        elif not Event.UNIQUEIDLC in event:
            pass
        elif not Event.VALUE in event:
            pass
        else:
            pbx = event[Event.SOURCE]
            channel = event[Event.CHANNEL]
            uniqueid = event[Event.UNIQUEIDLC]
            value = event[Event.VALUE]
            self.view.sipcallid(pbx, uniqueid, channel, value)
            self.model.sipcallid(pbx, uniqueid, value)
            self.view.display()

    def trace(self, event):
        for keyword in event:
            value = event[keyword]
            fprintf(self.tracer, "%s: %s\r\n", keyword, value)
        fprintf(self.tracer, "\r\n")

    #
    # PUBLIC
    #

    def process(self, event):
        """
        Process a dictionary from an Event by extracting the necessary
        keyword:value pairs from the dictionary for those Events that are
        supported and passing them along to the Model and the View.
        """
        if Event.END in event:
            if Event.END in self.table:
                if self.tracer != None:
                    self.trace(event)
                self.table[Event.END](event)
        elif Event.EVENT in event:
            name = event[Event.EVENT]
            if name in self.table:
                if self.tracer != None:
                    self.trace(event)
                self.table[name](event)
        else:
            pass
