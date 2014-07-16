"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

from Model import Model

import Channel

class ModelStandard(Model):
    """
    ModelStandard is a kind of Model that implements the default modifications
    to the dynamic call state in the base class for every Event that it is
    given. It tries hard to be forgiving about being given Events that apply to
    Channels that were created before it was instantiated. (It generally ignores
    such Events.)
    """
    
    #
    # CTOR/DTOR
    #

    def __init__(self, logger = None):
        Model.__init__(self, logger)

    def __del__(self):
        pass

    def __repr__(self):
        return Model.__repr__(self) + ".ModelStandard()"

    #
    # PRIVATE
    #

    def remove(self, pbx, uniqueid):
        if pbx in self.channels:
            channels = self.channels[pbx]
            if uniqueid in channels:
                chan = channels[uniqueid]
                if chan.calleridnum != None:
                    if pbx in self.numbers:
                        numbers = self.numbers[pbx]
                        if chan.channel in numbers:
                            del numbers[chan.channel]
                        if not numbers:
                            del self.numbers[pbx]
                if chan.call != None:
                    if chan in chan.call:
                        chan.call.remove(chan)
                    if not chan.call:
                        if chan.call in self.calls:
                            self.calls.remove(chan.call)
                if chan.conference != None:
                    if pbx in self.bridges:
                        bridges = self.bridges[pbx]
                        if chan.conference in bridges:
                            bridge = bridges[chan.conference]
                            if uniqueid in bridge:
                                del bridge[uniqueid]
                                if not bridge:
                                    del bridges[chan.conference]
                                    if not bridges:
                                        del self.bridges[pbx]                       
                if chan.sipcallid in self.trunks:
                    del self.trunks[chan.sipcallid]
                del channels[uniqueid]
                if not channels:
                    del self.channels[pbx]
    
    def merge(self, chan1, chan2):
        if (chan1.call == None) and (chan2.call == None):
            calls = [ chan1, chan2 ]
            chan1.call = calls
            chan2.call = calls
            self.calls.append(calls)
        elif chan1.call == None:
            chan2.call.insert(0, chan1)
            chan1.call = chan2.call
        elif chan2.call == None:
            chan1.call.append(chan2)
            chan2.call = chan1.call
        elif id(chan1.call) != id(chan2.call):
            calls = [ ]
            for channel in chan1.call:
                calls.append(channel)
            for channel in chan2.call:
                calls.append(channel)
            if chan1.call in self.calls:
                self.calls.remove(chan1.call)
            if chan2.call in self.calls:
                self.calls.remove(chan2.call)
            chan1.call = calls
            chan2.call = calls
            self.calls.append(calls)
        else:
            pass # Typically a re-Bridge.
    
    #
    # PUBLIC
    #
    
    def bridge(self, pbx, uniqueid1, uniqueid2):
        if pbx in self.channels:
            channels = self.channels[pbx]
            if uniqueid1 in channels:
                chan1 = channels[uniqueid1]
                chan1.idled()
                if uniqueid2 in channels:
                    chan2 = channels[uniqueid2]
                    self.merge(chan1, chan2)

    def confbridgeend(self, pbx, conference):
        if pbx in self.bridges:
            bridges = self.bridges[pbx]
            if conference in bridges:
                bridge = bridges[conference]
                for uniqueid in bridge:
                    chan = bridge[uniqueid]
                    chan.leave()
                del bridges[conference]
                if not bridges:
                    del self.bridges[pbx]
    
    def confbridgejoin(self, pbx, uniqueid, conference):
        if pbx in self.channels:
            channels = self.channels[pbx]
            if pbx in self.bridges:
                bridges = self.bridges[pbx]
                if uniqueid in channels:
                    chan = channels[uniqueid]
                    if conference in bridges:
                        bridge = bridges[conference]
                        bridge[uniqueid] = chan
                        chan.join(conference)
    
    def confbridgeleave(self, pbx, uniqueid, conference):
        if pbx in self.bridges:
            bridges = self.bridges[pbx]
            if conference in bridges:
                bridge = bridges[conference]
                if uniqueid in bridge:
                    chan = bridge[uniqueid]
                    chan.leave()
                    del bridge[uniqueid]
    
    def confbridgestart(self, pbx, conference):
        if not pbx in self.bridges:
            self.bridges[pbx] = { }
        bridges = self.bridges[pbx]
        bridges[conference] = { }
    
    def dial(self, pbx, uniqueid, destuniqueid):
        channels = self.channels[pbx]
        if uniqueid in channels:
            chan = channels[uniqueid]
            chan.calling()
            chan.dialing()
            if destuniqueid in channels:
                dest = channels[destuniqueid]
                dest.called()
    
    def end(self, pbx):
        if pbx in self.channels:
            channels = self.channels[pbx]
            uniqueids = channels.keys()
            for uniqueid in uniqueids:
                self.remove(pbx, uniqueid)

    def hangup(self, pbx, uniqueid):
        self.remove(pbx, uniqueid)
    
    def localbridge(self, pbx, uniqueid1, uniqueid2):
        if pbx in self.channels:
            channels = self.channels[pbx]
            if uniqueid1 in channels:
                chan1 = channels[uniqueid1]
                if uniqueid2 in channels:
                    chan2 = channels[uniqueid2]
                    chan1.trunk()
                    chan2.trunk()
                    self.merge(chan1, chan2)
    
    def newchannel(self, pbx, uniqueid, channel, calleridnum, channelstate, channelstatedesc):
        chan = Channel.Channel(pbx, uniqueid, channel, calleridnum, channelstate, channelstatedesc)
        if not pbx in self.channels:
            self.channels[pbx] = { }
        channels = self.channels[pbx]
        channels[uniqueid] = chan
        if calleridnum == None:
            pass
        elif not calleridnum:
            pass
        else:
            if not pbx in self.numbers:
                self.numbers[pbx] = { }
            numbers = self.numbers[pbx]
            numbers[channel] = calleridnum
    
    def newstate(self, pbx, uniqueid, channelstate, channelstatedesc):
        if pbx in self.channels:
            channels = self.channels[pbx]
            if uniqueid in channels:
                chan = channels[uniqueid]
                chan.newstate(channelstate, channelstatedesc)
    
    def rename(self, pbx, uniqueid, newname):
        if pbx in self.channels:
            channels = self.channels[pbx]
            if uniqueid in channels:
                chan = channels[uniqueid]
                oldname = chan.channel
                chan.rename(newname)
                if chan.calleridnum == None or not chan.calleridnum:
                    if pbx in self.numbers:
                        numbers = self.numbers[pbx]
                        if newname in numbers:
                            calleridnum = numbers[newname]
                            chan.dial(calleridnum)
                else:
                    if pbx in self.numbers:
                        numbers = self.numbers[pbx]
                        if oldname in numbers:
                            calleridnum = numbers[oldname]
                            del numbers[oldname]
                            numbers[newname] = calleridnum                   

    def sipcallid(self, pbx, uniqueid, value):
        if pbx in self.channels:
            channels = self.channels[pbx]
            if uniqueid in channels:
                chan = channels[uniqueid]
                chan.endpoint(value)
                if not value in self.trunks:
                    self.trunks[value] = chan
                else:
                    dest = self.trunks[value]
                    del self.trunks[value]
                    chan.trunk()
                    dest.trunk()
                    self.merge(chan, dest)

    def hanguprequest(self, pbx, uniqueid):
        if pbx in self.channels:
            channels = self.channels[pbx]
            if uniqueid in channels:
                chan = channels[uniqueid]
                chan.hungup()

    def musiconhold(self, pbx, uniqueid):
        if pbx in self.channels:
            channels = self.channels[pbx]
            if uniqueid in channels:
                chan = channels[uniqueid]
                chan.held()

    def musicoffhold(self, pbx, uniqueid):
        if pbx in self.channels:
            channels = self.channels[pbx]
            if uniqueid in channels:
                chan = channels[uniqueid]
                chan.idled()

    def newcallerid(self, pbx, uniqueid, channel, calleridnum):
        if pbx in self.channels:
            channels = self.channels[pbx]
            if uniqueid in channels:
                chan = channels[uniqueid]
                chan.dial(calleridnum)
                if not pbx in self.numbers:
                    self.numbers[pbx] = { }
                numbers = self.numbers[pbx]
                numbers[channel] = calleridnum

    def softhanguprequest(self, pbx, uniqueid, cause):
        if pbx in self.channels:
            channels = self.channels[pbx]
            if uniqueid in channels:
                chan = channels[uniqueid]
                chan.caused()
