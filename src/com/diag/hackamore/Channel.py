"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

IDLE = 0
CALLING = 1
CALLED = 2
TRUNK = 3

ROLE = ( "IDLE", "CALLING", "CALLED", "TRUNK" )

#####
##### PRIVATE
#####

class Channel():
    """
    Channel describes an Asterisk channel. Channels are abstract communication
    paths in Asterisk which may or may not represent actual platform
    telecommunications resources. Asterisk creates channels as necessary and
    connects them together to achieve an end-to-end call.
    """
    
    #####
    ##### CTOR/DTOR
    #####

    def __init__(self, pbx, uniqueid, channel, calleridnum, channelstate, channelstatedesc):
        """
        Constructor.
        @param pbx is the name of the Source on which the channel was created.
        @param uniqueid is a unique channel identifier that Asterisk uses.
        @param channel is the non-unique channel name that Asterisk uses.
        @param calleridnum is the caller identification number of the channel.
        @param channelstate is a number representing the initial channel state.
        @param channelstatedesc is a human-readable channel state description.
        """
        self.pbx = pbx
        self.uniqueid = uniqueid
        self.calleridnum = calleridnum
        self.sipcallid = None
        self.conference = None
        self.channel = channel
        self.channelstate = channelstate
        self.channelstatedesc = channelstatedesc
        self.role = IDLE
        self.call = None
            
    def __del__(self):
        pass

    def __repr__(self):
        return "Channel(" + str(self.pbx) + "," + str(self.uniqueid) + "," + str(self.channel) + "," + str(self.calleridnum) + "," + str(self.sipcallid) + "," + str(self.conference) + "," + str(self.channelstatedesc) + "," + str(ROLE[self.role]) + ")"

    #####
    ##### PUBLIC
    #####

    def newstate(self, channelstate, channelstatedesc):
        """
        Transition this Channel to a new state.
        @param channelstate is the new channel state.
        @param channelstatedesc is the new channel state description.
        """
        self.channelstate = channelstate
        self.channelstatedesc = channelstatedesc

    def rename(self, channel):
        """
        Rename this Channel.
        @param channel is the new channel name.
        """
        self.channel = channel
        
    def endpoint(self, sipcallid):
        """
        Identify this Channel as a SIP end point. Not all Asterisk channels are
        SIP end points. But if they are, SIP end point identifiers can cross PBX
        boundaries. So if two Channels on different PBXes have the same SIP
        call identifier, they are connected to one another end-to-end.
        @param sipcallid is the SIP call identifier.
        """
        self.sipcallid = sipcallid

    def trunk(self):
        """
        Specify that this Channel is acting in the role of a trunk, as opposed
        to a calling party or a called party. Trunks are intermediate Asterisk
        channels that do not represent either end of a call.
        """
        self.role = TRUNK

    def calling(self):
        """
        Specify that this Channel is a calling party. The calling party is that
        party on the call that initiated the call by dialing the called party.
        If this Channel was already a called party, than it is now a trunk.
        """
        if self.role == IDLE:
            self.role = CALLING
        elif self.role == CALLED:
            self.role = TRUNK
        else:
            pass
    
    def called(self):
        """
        Specify that this Channel is a called party. The called party is that
        party on the call that terminated the call by being dialed by the
        calling party. If this Channel was already a calling party, then it is
        now a trunk.
        """
        if self.role == IDLE:
            self.role = CALLED
        elif self.role == CALLING:
            self.role = TRUNK
        else:
            pass

    def dial(self, calleridnum):
        """
        Associate this Channel with a specific caller identification number.
        Generally this is the number the dial plan uses to dial this Channel,
        but (alas) not necessarily.
        @param calleridnum is a caller identification number.
        """
        self.calleridnum = calleridnum

    def join(self, conference):
        """
        Associate this Channel with a conference bridge identified by a
        conference bridge number.
        @param conference is a conference bridge number.
        """
        self.conference = conference

    def leave(self):
        """
        Disassociate this Channel from any conference bridge it may have been
        on.
        """
        self.conference = None
