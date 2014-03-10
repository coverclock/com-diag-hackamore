"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

class ModelSerializer:
    
    #####
    ##### CTOR/DTOR
    #####

    def __init__(self, model, mutex):
        self.model = model
        self.mutex = mutex

    def __del__(self):
        pass

    def __repr__(self):
        return "ModelSerializer(" + str(self.model) + ")"

    
    #####
    ##### PUBLIC
    #####
    
    def bridge(self, pbx, uniqueid1, uniqueid2):
        with self.mutex:
            return self.model.bridge(pbx, uniqueid1, uniqueid2)

    def confbridgeend(self, pbx, conference):
        with self.mutex:
            return self.model.confbridgeend(pbx, conference)
    
    def confbridgejoin(self, pbx, uniqueid, conference):
        with self.mutex:
            return self.model.confbridgejoin(pbx, uniqueid, conference)
    
    def confbridgeleave(self, pbx, uniqueid, conference):
        with self.mutex:
            return self.model.confbridgeleave(pbx, uniqueid, conference)
    
    def confbridgestart(self, pbx, conference):
        with self.mutex:
            return self.model.confbridgestart(pbx, conference)
    
    def dial(self, pbx, uniqueid, destuniqueid):
        with self.mutex:
            return self.model.dial(pbx, uniqueid, destuniqueid)
    
    def end(self, pbx):
        with self.mutex:
            return self.model.end(pbx)

    def hangup(self, pbx, uniqueid):
        with self.mutex:
            return self.model.hangup(pbx, uniqueid)
    
    def localbridge(self, pbx, uniqueid1, uniqueid2):
        with self.mutex:
            return self.model.localbridge(pbx, uniqueid1, uniqueid2)
    
    def newchannel(self, pbx, uniqueid, channel, calleridnum, channelstate, channelstatedesc):
        with self.mutex:
            return self.model.newchannel(pbx, uniqueid, channel, calleridnum, channelstate, channelstatedesc)
    
    def newstate(self, pbx, uniqueid, channelstate, channelstatedesc):
        with self.mutex:
            return self.model.newstate(pbx, uniqueid, channelstate, channelstatedesc)
    
    def rename(self, pbx, uniqueid, newname):
        with self.mutex:
            return self.model.rename(pbx, uniqueid, newname)

    def sipcallid(self, pbx, uniqueid, value):
        with self.mutex:
            return self.model.sipcallid(pbx, uniqueid, value)
