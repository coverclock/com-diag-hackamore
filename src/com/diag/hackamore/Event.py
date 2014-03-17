"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import Logger

# These symbols are keywords specific to the Hackamore application.

END = "END"
SOURCE = "SOURCE"
TIME = "TIME"

# These symbols are keywords used by the Asterisk Management Interface.

BRIDGE = "Bridge"
CALLERID1 = "CallerID1"
CALLERID2 = "CallerID2"
CALLERIDNUM = "CallerIDNum"
CHANNEL = "Channel"
CHANNEL1 = "Channel1"
CHANNEL2 = "Channel2"
CHANNELSTATE = "ChannelState"
CHANNELSTATEDESC = "ChannelStateDesc"
CONFBRIDGEEND = "ConfbridgeEnd"
CONFBRIDGEJOIN = "ConfbridgeJoin"
CONFBRIDGELEAVE = "ConfbridgeLeave"
CONFBRIDGESTART = "ConfbridgeStart"
CONFERENCE = "Conference"
DESTINATION = "Destination"
DESTUNIQUEID = "DestUniqueID"
EVENT = "Event"
MESSAGE = "Message"
NEWNAME = "Newname"
RESPONSE = "Response"
SUBEVENT = "SubEvent"
UNIQUEID1 = "Uniqueid1"
UNIQUEID2 = "Uniqueid2"
UNIQUEIDLC = "Uniqueid"
UNIQUEIDUC = "UniqueID"
VALUE = "Value"
VARIABLE = "Variable"
VARSET = "VarSet"

# These symbols are values used by the Asterisk Management Interface.

AUTHENTICATEDACCEPTED = "Authentication accepted"
BEGIN = "Begin"
DIAL = "Dial"
ERROR = "Error"
GOODBYE = "Goodbye"
HANGUP = "Hangup"
LOCALBRIDGE = "LocalBridge"
NEWCHANNEL = "Newchannel"
NEWSTATE = "Newstate"
RENAME = "Rename"
SIPCALLID = "SIPCALLID"
SUCCESS = "Success"

class Event:
    """
    Event describes a message from an AMI Source. It contains the dictionary
    containing the keyword:value pairs from the message itself, and a
    reference to the logger that may be associated with the Source of the
    message. This latter  field is provided so that different Sources may have
    different logging levels that are inherited by the Events that they
    generate.
    """

    #
    # CTOR/DTOR
    #

    def __init__(self, event, logger = None):
        """
        Constructor.
        @param event is the dictionary containing the AMI message.
        @param logger is an optional Logger.
        """
        self.logger = Logger.logger() if logger == None else logger
        self.event = event

    def __del__(self):
        pass

    def __repr__(self):
        return "Event(" + str(self.event) + ")"
