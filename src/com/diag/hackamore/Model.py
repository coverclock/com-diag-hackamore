"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import Logger

class Model:
    
    #####
    ##### CTOR/DTOR
    #####

    def __init__(self, logger = None):
        self.logger = Logger.logger() if logger == None else logger
        self.channels = { }     # Channel = self.channels[pbx][uniqueid]
        self.bridges = { }      # Channel = self.bridges[pbx][conference][uniqueid]
        self.trunks = { }       # Channel = self.trunks[sipcallid]
        self.calls = [ ]        # Channel = self.calls[0:-1][0:-1]
        self.numbers = { }      # calleridnum = self.numbers[channel]

    def __del__(self):
        pass

    def __repr__(self):
        return "Model()"
    
    #####
    ##### PUBLIC
    #####
    
    def bridge(self, pbx, uniqueid1, uniqueid2):
        pass

    def confbridgeend(self, pbx, conference):
        pass
    
    def confbridgejoin(self, pbx, uniqueid, conference):
        pass
    
    def confbridgeleave(self, pbx, uniqueid, conference):
        pass
    
    def confbridgestart(self, pbx, conference):
        pass
    
    def dial(self, pbx, uniqueid, destuniqueid):
        pass
    
    def end(self, pbx):
        pass

    def hangup(self, pbx, uniqueid):
        pass
    
    def localbridge(self, pbx, uniqueid1, uniqueid2):
        pass
    
    def newchannel(self, pbx, uniqueid, channel, calleridnum, channelstate, channelstatedesc):
        pass
    
    def newstate(self, pbx, uniqueid, channelstate, channelstatedesc):
        pass
    
    def rename(self, pbx, uniqueid, newname):
        pass

    def sipcallid(self, pbx, uniqueid, value):
        pass
