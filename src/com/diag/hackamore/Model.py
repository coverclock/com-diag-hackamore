"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import Logger

class Model:
    """
    Model describes how Events received from one or more AMI Sources affect
    the dynamic call state maintained by Hackamore. Model is not concerned
    with how those Events are received (that's the Controller), nor with how
    they are displayed (that's the View). There can be more than one kind of
    Model. This particular Model is just a container database that is the
    dynamic call state. Its individual methods which represent events and their
    parameters do not change the database; that's up to derived classes.
    """

    #
    # CTOR/DTOR
    #

    def __init__(self, logger = None):
        """
        Constructor.
        @param logger is an optional logger which derived classes may use.
        """
        self.logger = Logger.logger() if logger == None else logger
        self.channels = { }     # Channel = self.channels[pbx][uniqueid]
        self.bridges = { }      # Channel = self.bridges[pbx][conference][uniqueid]
        self.trunks = { }       # Channel = self.trunks[sipcallid]
        self.calls = [ ]        # Channel = self.calls[0:-1][0:-1]
        self.numbers = { }      # calleridnum = self.numbers[pbx][channel]

    def __del__(self):
        pass

    def __repr__(self):
        return "Model(" + hex(id(self)) + ")"
    
    #
    # PUBLIC
    #
    
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

    def hanguprequest(self, pbx, uniqueid):
        pass

    def musiconhold(self, pbx, uniqueid):
        pass

    def musicoffhold(self, pbx, uniqueid):
        pass

    def newcallerid(self, pbx, uniqueid, channel, calleridnum):
        pass

    def softhanguprequest(self, pbx, uniqueid, cause):
        pass

