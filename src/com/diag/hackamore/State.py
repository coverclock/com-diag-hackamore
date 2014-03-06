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

    def __del__(self):
        pass

    def __repr__(self):
        return "State()"
    
    #####
    ##### PRIVATE
    #####

    def remove(self, pbx, uniqueid):
        if pbx in self.channels:
            channels = self.channels[pbx]
            if uniqueid in channels:
                chan = channels[uniqueid]
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
    
    def connect(self, pbx, uniqueid, destuniqueid):
        if pbx in self.channels:
            channels = self.channels[pbx]
            if uniqueid in channels:
                chan = channels[uniqueid]
                chan.calling()
                if destuniqueid in channels:
                    dest = channels[destuniqueid]
                    dest.called()
                    if (chan.call != None) and (dest.call != None):
                        calls = [ ]
                        for channel in chan.call:
                            calls.append(channel)
                        for channel in dest.call:
                            calls.append(channel)
                        self.calls.remove(chan.call)
                        self.calls.remove(dest.call)
                        chan.call = calls
                        dest.call = calls
                        self.calls.append(calls)
                    elif chan.call != None:
                        chan.call.append(dest)
                        dest.call = chan.call
                    elif dest.call != None:
                        dest.call.insert(0, chan)
                        chan.call = dest.call
                    else:
                        calls = [ chan, dest ]
                        chan.call = calls
                        dest.call = calls
                        self.calls.append(calls)

    #####
    ##### DEBUG
    #####

    def dump(self):
        with self.mutex:
            print("CHANNELS")
            for pbx in self.channels:
                print(str(pbx))
                channels = self.channels[pbx]
                for channel in channels:
                    chan = channels[channel]
                    print(str(chan))
            for pbx in self.bridges:
                bridges = self.bridges[pbx]
                for conference in bridges:
                    bridge = bridges[conference]
                    print("BRIDGE")
                    for uniqueid in bridge:
                        chan = bridge[uniqueid]
                        print(str(chan))
            print("TRUNKS")
            for sipcallid in self.trunks:
                chan = self.trunks[sipcallid]
                print(str(chan))
            for calls in self.calls:
                print("CALL")
                for chan in calls:
                    print(str(chan)) 

    def audit(self):
        with self.mutex:
            pass
    
    #####
    ##### PUBLIC
    #####
    
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
        with self.mutex:
            self.connect(pbx, uniqueid, destuniqueid)

    def hangup(self, pbx, uniqueid):
        with self.mutex:
            self.remove(pbx, uniqueid)
    
    def localbridge(self, pbx, uniqueid1, uniqueid2):
        with self.mutex:
            self.connect(pbx, uniqueid1, uniqueid2)
    
    def newchannel(self, pbx, uniqueid, channel, channelstate, channelstatedesc):
        with self.mutex:
            chan = Channel.Channel(pbx, uniqueid, channel, channelstate, channelstatedesc)
            if not pbx in self.channels:
                self.channels[pbx] = { }
            channels = self.channels[pbx]
            channels[uniqueid] = chan
    
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
                        if (chan.call != None) and (dest.call != None):
                            calls = [ ]
                            for channel in chan.call:
                                calls.append(channel)
                            for channel in dest.call:
                                calls.append(channel)
                            self.calls.remove(chan.call)
                            self.calls.remove(dest.call)
                            chan.call = calls
                            dest.call = calls
                            self.calls.append(calls)
                        elif chan.call != None:
                            chan.call.append(dest)
                            dest.call = chan.call
                        elif dest.call != None:
                            dest.call.insert(0, chan)
                            chan.call = dest.call
                        else:
                            calls = [ chan, dest ]
                            chan.call = calls
                            dest.call = calls
                            self.calls.append(calls)
