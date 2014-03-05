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

    def __del__(self):
        pass

    def __repr__(self):
        return "State()"
        
    def confbridgeend(self, conference):
        with self.mutex:
            if conference in self.conferences:
                del self.conferences[conference]
    
    def confbridgejoin(self, uniqueid, conference):
        with self.mutex:
            if not conference in self.conferences:
                pass
            elif not uniqueid in self.channels:
                pass
            else:
                conf = self.conferences[conference]
                chan = self.channels[uniqueid]
                conf[uniqueid] = chan
    
    def confbridgeleave(self, uniqueid, conference):
        with self.mutex:
            if not conference in self.conferences:
                pass
            elif not uniqueid in self.channels:
                pass
            else:
                conf = self.conferences[conference]
                del conf[uniqueid]
    
    def confbridgestart(self, conference):
        with self.mutex:
            self.conferences[conference] = { }
    
    def dial(self, uniqueid, destuniqueid):
        with self.mutex:
            return
            if not uniqueid in self.channels:
                pass
            elif not destuniqueid in self.channels:
                pass
            else:
                calling = self.channels[uniqueid]
                called = self.channels[destuniqueid]
                calling.calling()
                called.called()
            
    def hangup(self, uniqueid):
        with self.mutex:
            pass
    
    def localbridge(self, uniqueid1, channel1, uniqueid2, channel2):
        with self.mutex:
            pass
    
    def newchannel(self, uniqueid, channel, channelstate, channelstatedesc):
        with self.mutex:
            chan = Channel.Channel(uniqueid, channel, channelstate, channelstatedesc)
            self.channels[uniqueid] = chan
    
    def newstate(self, uniqueid, channelstate, channelstatedesc):
        with self.mutex:
            if uniqueid in self.channels:
                chan = self.channels[uniqueid]
                chan.newstate(channelstate, channelstatedesc)
    
    def rename(self, uniqueid, newname):
        with self.mutex:
            if uniqueid in self.channels:
                chan = self.channels[uniqueid]
                chan.rename(newname)
    
    def sipcallid(self, uniqueid, channel, value):
        with self.mutex:
            pass
    
    def close(self, name):
        with self.mutex:
            pass

    def dump(self):
        with self.mutex:
            pass
