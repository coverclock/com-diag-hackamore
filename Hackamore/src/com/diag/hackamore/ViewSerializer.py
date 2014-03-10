"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

class ViewSerializer:

    #####
    ##### CTOR/DTOR
    #####

    def __init__(self, view, mutex, logger = None):
        self.view = view
        self.mutex = mutex

    def __del__(self):
        pass

    def __repr__(self):
        return "ViewSerializer(" + str(self.view) + ")"

    #####
    ##### PUBLIC
    #####
    
    def bridge(self, pbx, uniqueid1, channel1, callerid1, uniqueid2, channel2, callerid2):
        return self.view.bridge(pbx, uniqueid1, channel1, callerid1, uniqueid2, channel2, callerid2)

    def confbridgeend(self, pbx, conference):
        return self.view.confbridgeend(pbx, conference)

    def confbridgejoin(self, pbx, uniqueid, channel, conference):
        return self.view.confbridgejoin(pbx, uniqueid, channel, conference)

    def confbridgeleave(self, pbx, uniqueid, channel, conference):        
        return self.view.confbridgejoin(pbx, uniqueid, channel, conference)

    def confbridgestart(self, pbx, conference):        
        return self.view.confbridgestart(pbx, conference)

    def dial(self, pbx, uniqueid, channel, destuniqueid, destination):
        return self.view.dial(pbx, uniqueid, channel, destuniqueid, destination)

    def end(self, pbx):
        return self.view.end(pbx)

    def hangup(self, pbx, uniqueid, channel):
        return self.view.hangup(pbx, uniqueid, channel)

    def localbridge(self, pbx, uniqueid1, channel1, uniqueid2, channel2):
        return self.view.localbridge(pbx, uniqueid1, channel1, uniqueid2, channel2)

    def newchannel(self, pbx, uniqueid, channel, calleridnum, channelstate, channelstatedesc):
        return self.view.newchannel(pbx, uniqueid, channel, calleridnum, channelstate, channelstatedesc)

    def newstate(self, pbx, uniqueid, channel, channelstate, channelstatedesc):
        return self.view.newstate(pbx, uniqueid, channel, channelstate, channelstatedesc)

    def rename(self, pbx, uniqueid, channel, newname):
        return self.view.rename(pbx, uniqueid, channel, newname)

    def sipcallid(self, pbx, uniqueid, channel, value):
        return self.view.sipcallid(pbx, uniqueid, channel, value)

    def display(self):
        with self.mutex:
            return self.view.display()
