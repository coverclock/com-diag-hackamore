"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import logging

import Logger
import Event
import Multiplex

from Channel import Channel

channels = { }
conferences = { }
        
def confbridgeend(logger, conference):
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug("Engine.confbridgeend: CONFBRIDGEEND: %s", str(conference))
    if conference in conferences:
        del conferences[conference]

def confbridgejoin(logger, uniqueid, channel, conference):
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug("Engine.confbridgejoin: CONFBRIDGEJOIN: %s %s %s", str(uniqueid), str(channel), str(conference))
    if not conference in conferences:
        pass
    elif not uniqueid in channels:
        pass
    else:
        conf = conferences[conference]
        chan = channels[uniqueid]
        conf[uniqueid] = chan

def confbridgeleave(logger, uniqueid, channel, conference):
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug("Engine.confbridgeleave: CONFBRIDGELEAVE: %s %s %s", str(uniqueid), str(channel), str(conference))
    if not conference in conferences:
        pass
    elif not uniqueid in channels:
        pass
    else:
        conf = conferences[conference]
        del conf[uniqueid]

def confbridgestart(logger, conference):
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug("Engine.confbridgestart: CONFBRIDGESTART: %s", str(conference))
    conferences[conference] = { }

def dial(logger, uniqueid, channel, destuniqueid, destination):
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug("Engine.dial: DIAL: %s %s %s %s", str(uniqueid), str(channel), str(destuniqueid), str(destination))
    if not uniqueid in channels:
        pass
    elif not destuniqueid in channels:
        pass
    else:
        calling = channels[uniqueid]
        called = channels[destuniqueid]
        calling.calling()
        called.called()
        
        
def hangup(logger, uniqueid, channel):
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug("Engine.hangup: HANGUP: %s %s", str(uniqueid), str(channel))

def localbridge(logger, uniqueid1, channel1, uniqueid2, channel2):
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug("Engine.localbridge: LOCALBRIDGE: %s %s %s %s", str(uniqueid1), str(channel1), str(uniqueid2), str(channel2))

def newchannel(logger, uniqueid, channel, channelstate, channelstatedesc):
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug("Engine.newchannel: NEWCHANNEL: %s %s %s %s", str(uniqueid), str(channel), str(channelstate), str(channelstatedesc))
    chan = Channel(uniqueid, channel, channelstate, channelstatedesc)
    channels[uniqueid] = chan

def newstate(logger, uniqueid, channel, channelstate, channelstatedesc):
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug("Engine.newstate: NEWSTATE: %s %s %s %s", str(uniqueid), str(channel), str(channelstate), str(channelstatedesc))
    if uniqueid in channels:
        chan = channels[uniqueid]
        chan.newstate(channelstate, channelstatedesc)

def rename(logger, uniqueid, channel, newname):
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug("Engine.rename: RENAME: %s %s %s", str(uniqueid), str(channel), str(newname))
    if uniqueid in channels:
        chan = channels[uniqueid]
        chan.rename(newname)

def sipcallid(logger, uniqueid, channel, value):
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug("Engine.sipcallid: SIPCALLID: %s %s %s", str(uniqueid), str(channel), str(value))

def close(logger, name):
    pass

def engine(inputs, outputs, logger = None):
    logger = Logger.logger() if logger == None else logger
    logger.info("Engine.engine: STARTING.")
    while True:
        for source in inputs:
            if source.open():
                inputs.remove(source)
        if not Multiplex.active():
            logger.info("Engine.engine: STOPPING.")
            break
        events = Multiplex.multiplex()
        for event in events:
            name = event[Event.SOURCE]
            if Event.END in event:
                close(logger, name)
                source = Multiplex.query(name)
                if source == None:
                    pass
                elif not source.close():
                    pass
                elif source.open():
                    pass
                else:
                    outputs.append(source)
                if not Multiplex.active():
                    events.close()
            elif Event.EVENT in event:
                flavor = event[Event.EVENT]
                if flavor == Event.CONFBRIDGEEND:
                    if not Event.CONFERENCE in event:
                        pass
                    else:
                        conference = event[Event.CONFERENCE]
                        confbridgeend(logger, conference)
                elif flavor == Event.CONFBRIDGEJOIN:
                    if not Event.CHANNEL in event:
                        pass
                    elif not Event.CONFERENCE in event:
                        pass
                    elif not Event.UNIQUEIDLC in event:
                        pass
                    else:
                        channel = event[Event.CHANNEL]
                        conference = event[Event.CONFERENCE]
                        uniqueid = ( name, event[Event.UNIQUEIDLC] )
                        confbridgejoin(logger, uniqueid, channel, conference)
                elif flavor == Event.CONFBRIDGELEAVE:
                    if not Event.CHANNEL in event:
                        pass
                    elif not Event.CONFERENCE in event:
                        pass
                    elif not Event.UNIQUEIDLC in event:
                        pass
                    else:
                        channel = event[Event.CHANNEL]
                        conference = event[Event.CONFERENCE]
                        uniqueid = ( name, event[Event.UNIQUEIDLC] )
                        confbridgeleave(logger, uniqueid, channel, conference)
                elif flavor == Event.CONFBRIDGESTART:
                    if not Event.CONFERENCE in event:
                        pass
                    else:
                        conference = event[Event.CONFERENCE]
                        confbridgestart(logger, conference)
                elif flavor == Event.DIAL:
                    if not Event.SUBEVENT in event:
                        pass
                    elif event[Event.SUBEVENT] != Event.BEGIN:
                        pass
                    elif not Event.CHANNEL in event:
                        pass
                    elif not Event.DESTINATION in event:
                        pass
                    elif not Event.DESTUNIQUEID in event:
                        pass
                    elif not Event.UNIQUEIDUC in event:
                        pass
                    else:
                        channel = event[Event.CHANNEL]
                        destination = event[Event.DESTINATION]
                        destuniqueid = ( name, event[Event.DESTUNIQUEID] )
                        uniqueid = ( name, event[Event.UNIQUEIDUC] )
                        dial(logger, uniqueid, channel, destuniqueid, destination)
                elif flavor == Event.HANGUP:
                    if not Event.CHANNEL in event:
                        pass
                    elif not Event.UNIQUEIDLC in event:
                        pass
                    else:
                        channel = event[Event.CHANNEL]
                        uniqueid = ( name, event[Event.UNIQUEIDLC] )
                        hangup(logger, uniqueid, channel)
                elif flavor == Event.LOCALBRIDGE:
                    if not Event.CHANNEL1 in event:
                        pass
                    elif not Event.CHANNEL2 in event:
                        pass
                    elif not Event.UNIQUEID1 in event:
                        pass
                    elif not Event.UNIQUEID2 in event:
                        pass
                    else:
                        channel1 = event[Event.CHANNEL1]
                        channel2 = event[Event.CHANNEL2]
                        uniqueid1 = ( name, event[Event.UNIQUEID1] )
                        uniqueid2 = ( name, event[Event.UNIQUEID2] )
                        localbridge(logger, uniqueid1, channel1, uniqueid2, channel2)
                elif flavor == Event.NEWCHANNEL:
                    if not Event.CHANNEL in event:
                        pass
                    elif not Event.CHANNELSTATE in event:
                        pass
                    elif not Event.CHANNELSTATEDESC in event:
                        pass
                    elif not Event.UNIQUEIDLC in event:
                        pass
                    else:
                        channel = event[Event.CHANNEL]
                        channelstate = event[Event.CHANNELSTATE]
                        channelstatedesc = event[Event.CHANNELSTATEDESC]
                        uniqueid = ( name, event[Event.UNIQUEIDLC] )
                        newchannel(logger, uniqueid, channel, channelstate, channelstatedesc)
                elif flavor == Event.NEWSTATE:
                    if not Event.CHANNEL in event:
                        pass
                    elif not Event.CHANNELSTATE in event:
                        pass
                    elif not Event.CHANNELSTATEDESC in event:
                        pass
                    elif not Event.UNIQUEIDLC in event:
                        pass
                    else:
                        channel = event[Event.CHANNEL]
                        channelstate = event[Event.CHANNELSTATE]
                        channelstatedesc = event[Event.CHANNELSTATEDESC]
                        uniqueid = ( name, event[Event.UNIQUEIDLC] )
                        newstate(logger, uniqueid, channel, channelstate, channelstatedesc)
                elif flavor == Event.RENAME:
                    if not Event.CHANNEL in event:
                        pass
                    elif not Event.NEWNAME in event:
                        pass
                    elif not Event.UNIQUEIDLC in event:
                        pass
                    else:
                        channel = event[Event.CHANNEL]
                        newname = event[Event.NEWNAME]
                        uniqueid = ( name, event[Event.UNIQUEIDLC] )
                        rename(logger, uniqueid, channel, newname)
                elif flavor == Event.VARSET:
                    if not Event.VARIABLE in event:
                        pass
                    elif event[Event.VARIABLE] != Event.SIPCALLID:
                        pass
                    elif not Event.CHANNEL in event:
                        pass
                    elif not Event.UNIQUEIDLC in event:
                        pass
                    elif not Event.VALUE in event:
                        pass
                    else:
                        channel = event[Event.CHANNEL]
                        uniqueid = ( name, event[Event.UNIQUEIDLC] )
                        value = event[Event.VALUE]
                        sipcallid(logger, uniqueid, channel, value)
                else:
                    pass
            else:
                pass
