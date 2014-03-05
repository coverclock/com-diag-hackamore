"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import threading

import Logger
import Channel

class State:

    def __init__(self, logger = None):
        self.logger = Logger.logger() if logger == None else logger
        self.mutex = threading.Condition()
        self.channels = { }
        self.conferences = { }
        self.calls = { }

    def __del__(self):
        pass

    def __repr__(self):
        return "State()"

    def confbridgeend(self, pbx, conference):
        with self.mutex:
            if pbx in self.conferences:
                conferences = self.conferences[pbx]
                if conference in conferences:
                    del conferences[conference]
    
    def confbridgejoin(self, pbx, uniqueid, conference):
        with self.mutex:
            if pbx in self.channels:
                channels = self.channels[pbx]
                if pbx in self.conferences:
                    conferences = self.conferences[pbx]
                    if uniqueid in channels:
                        chan = channels[uniqueid]
                        if conference in conferences:
                            conf = conferences[conference]
                            conf[uniqueid] = chan
    
    def confbridgeleave(self, pbx, uniqueid, conference):
        with self.mutex:
            if pbx in self.conferences:
                conferences = self.conferences[pbx]
                if conference in conferences:
                    conf = conferences[conference]
                    if uniqueid in conf:
                        del conf[uniqueid]
    
    def confbridgestart(self, pbx, conference):
        with self.mutex:
            if not pbx in self.conferences:
                self.conferences[pbx] = { }
            conferences = self.conferences[pbx]
            conferences[conference] = { }
    
    def dial(self, pbx, uniqueid, destuniqueid):
        with self.mutex:
            if pbx in self.channels:
                channels = self.channels[pbx]
                if uniqueid in channels:
                    chan = channels[uniqueid]
                    chan.calling()
                    if destuniqueid in channels:
                        destchan = channels[destuniqueid]
                        destchan.called()
                        

    def hangup(self, pbx, uniqueid):
        with self.mutex:
            pass
    
    def localbridge(self, pbx, uniqueid1, channel1, uniqueid2, channel2):
        with self.mutex:
            pass
    
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
    
    def sipcallid(self, pbx, uniqueid, channel, value):
        with self.mutex:
            pass
    
    def close(self, name):
        with self.mutex:
            for pbx in self.channels:
                channels = self.channels[pbx]
                for uniqueid in channels:
                    self.hangup(pbx, uniqueid)

    def dump(self):
        with self.mutex:
            print("CHANNELS")
            for pbx in self.channels:
                print(str(pbx))
                channels = self.channels[pbx]
                for channel in channels:
                    chan = channels[channel]
                    print(str(chan))
            print("CONFERENCES")
            for pbx in self.conferences:
                print(str(pbx))
                conferences = self.conferences[pbx]
                for conference in conferences:
                    conf = conferences[conference]
                    print(str(conf))

    def audit(self):
        pass