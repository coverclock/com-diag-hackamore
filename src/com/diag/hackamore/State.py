"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import threading

import Logger
import Channel

class State:
    
    #####
    ##### CTOR/DTOR
    #####

    def __init__(self, logger = None):
        self.logger = Logger.logger() if logger == None else logger
        self.mutex = threading.Condition()
        self.channels = { }     # Channel = self.channels[pbx][uniqueid]
        self.bridges = { }      # Channel = self.bridges[pbx][conference][uniqueid]
        self.trunks = { }       # Channel = self.trunks[sipcallid]
        self.calls = [ ]        # Channel = self.calls[0:-1][0:-1]
        self.numbers = { }      # calleridnum = self.numbers[channel]

    def __del__(self):
        pass

    def __repr__(self):
        return "State(" + hex(id(self)) + ")"

    #####
    ##### PRIVATE
    #####

    def remove(self, pbx, uniqueid):
        if pbx in self.channels:
            channels = self.channels[pbx]
            if uniqueid in channels:
                chan = channels[uniqueid]
                if chan.calleridnum != None:
                    if chan.channel in self.numbers:
                        del self.numbers[chan.channel]
                if chan.call != None:
                    chan.call.remove(chan)
                    if not chan.call:
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
            self.calls.remove(chan1.call)
            self.calls.remove(chan2.call)
            chan1.call = calls
            chan2.call = calls
            self.calls.append(calls)
        else:
            pass # Typically a re-Bridge.
    
    def connect(self, pbx, uniqueid1, uniqueid2):
        if pbx in self.channels:
            channels = self.channels[pbx]
            if uniqueid1 in channels:
                chan1 = channels[uniqueid1]
                if uniqueid2 in channels:
                    chan2 = channels[uniqueid2]
                    self.merge(chan1, chan2)

    #####
    ##### DEBUG
    #####

    def dump(self):
        with self.mutex:
            print "STATE"
            if self.channels:
                print "", "CHANNELS"
                for pbx in self.channels:
                    print "", "", "SOURCE", pbx
                    channels = self.channels[pbx]
                    for channel in channels:
                        chan = channels[channel]
                        chan.dump()
            if self.bridges:
                print "", "BRIDGES"
                for pbx in self.bridges:
                    print "", "", "SOURCE", pbx
                    bridges = self.bridges[pbx]
                    for conference in bridges:
                        print "", "", "", "BRIDGE", conference
                        bridge = bridges[conference]
                        for uniqueid in bridge:
                            chan = bridge[uniqueid]
                            chan.dump()
            if self.trunks:
                print "", "TRUNKS"
                for sipcallid in self.trunks:
                    print "", "", "ID", sipcallid
                    chan = self.trunks[sipcallid]
                    chan.dump()
            if self.calls:
                print "", "CALLS"
                for call in self.calls:
                    print "", "", "CALL", hex(id(call))
                    for chan in call:
                        chan.dump()
            if self.numbers:
                print "", "NUMBERS"
                for channel in self.numbers:
                    calleridnum = self.numbers[channel]
                    print "", "", "NUMBER", calleridnum, channel

    def audit(self):
        with self.mutex:
            pass
    
    #####
    ##### PUBLIC
    #####
    
    def bridge(self, pbx, uniqueid1, uniqueid2):
        with self.mutex:
            self.connect(pbx, uniqueid1, uniqueid2)
    
    def close(self, pbx):
        with self.mutex:
            if pbx in self.channels:
                channels = self.channels[pbx]
                for uniqueid in channels:
                    self.remove(pbx, uniqueid)

    def confbridgeend(self, pbx, conference):
        with self.mutex:
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
        with self.mutex:
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
        with self.mutex:
            if pbx in self.bridges:
                bridges = self.bridges[pbx]
                if conference in bridges:
                    bridge = bridges[conference]
                    if uniqueid in bridge:
                        chan = bridge[uniqueid]
                        chan.leave(conference)
                        del bridge[uniqueid]
    
    def confbridgestart(self, pbx, conference):
        with self.mutex:
            if not pbx in self.bridges:
                self.bridges[pbx] = { }
            bridges = self.bridges[pbx]
            bridges[conference] = { }
    
    def dial(self, pbx, uniqueid, destuniqueid):
        if pbx in self.channels:
            channels = self.channels[pbx]
            if uniqueid in channels:
                chan = channels[uniqueid]
                chan.calling()
                if destuniqueid in channels:
                    dest = channels[destuniqueid]
                    dest.called()

    def hangup(self, pbx, uniqueid):
        with self.mutex:
            self.remove(pbx, uniqueid)
    
    def localbridge(self, pbx, uniqueid1, uniqueid2):
        with self.mutex:
            self.connect(pbx, uniqueid1, uniqueid2)
    
    def newchannel(self, pbx, uniqueid, channel, calleridnum, channelstate, channelstatedesc):
        with self.mutex:
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
                self.numbers[channel] = calleridnum
    
    def newstate(self, pbx, uniqueid, channelstate, channelstatedesc):
        with self.mutex:
            if pbx in self.channels:
                channels = self.channels[pbx]
                if uniqueid in channels:
                    chan = channels[uniqueid]
                    chan.newstate(channelstate, channelstatedesc)
    
    def rename(self, pbx, uniqueid, newname):
        with self.mutex:
            if pbx in self.channels:
                channels = self.channels[pbx]
                if uniqueid in channels:
                    chan = channels[uniqueid]
                    chan.rename(newname)
                    if chan.calleridnum == None or not chan.calleridnum:
                        if chan.channel in self.numbers:
                            calleridnum = self.numbers[chan.channel]
                            chan.dial(calleridnum)

    def sipcallid(self, pbx, uniqueid, value):
        with self.mutex:
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
