"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import logging

import Logger
import Event
import Multiplex

def engine(inputs, outputs, logger = None):
    global complete
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
                source = Multiplex.query(name)
                if source != None:
                    if not source.close():
                        pass
                    elif source.open():
                        pass
                    else:
                        outputs.append(source)
                    if not Multiplex.active():
                        events.close()
            elif Event.EVENT in event:
                if event[Event.EVENT] == Event.DIAL:
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
                        if logger.isEnabledFor(logging.DEBUG):
                            logger.debug("Engine.engine: EVENT: %s %s %s %s %s", Event.DIAL, str(uniqueid), channel, str(destuniqueid), destination)
                elif event[Event.EVENT] == Event.HANGUP:
                    if not Event.CHANNEL in event:
                        pass
                    elif not Event.UNIQUEIDLC in event:
                        pass
                    else:
                        channel = event[Event.CHANNEL]
                        uniqueid = ( name, event[Event.UNIQUEIDLC] )
                        if logger.isEnabledFor(logging.DEBUG):
                            logger.debug("Engine.engine: EVENT: %s %s %s", Event.HANGUP, str(uniqueid), channel)
                elif event[Event.EVENT] == Event.LOCALBRIDGE:
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
                        if logger.isEnabledFor(logging.DEBUG):
                            logger.debug("Engine.engine: EVENT: %s %s %s %s %s", Event.LOCALBRIDGE, str(uniqueid1), channel1, str(uniqueid2), channel2)
                elif event[Event.EVENT] == Event.NEWCHANNEL:
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
                        if logger.isEnabledFor(logging.DEBUG):
                            logger.debug("Engine.engine: EVENT: %s %s %s %s %s", Event.NEWCHANNEL, str(uniqueid), channel, channelstate, channelstatedesc)
                elif event[Event.EVENT] == Event.NEWSTATE:
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
                        if logger.isEnabledFor(logging.DEBUG):
                            logger.debug("Engine.engine: EVENT: %s %s %s %s %s", Event.NEWSTATE, str(uniqueid), channel, channelstate, channelstatedesc)
                elif event[Event.EVENT] == Event.RENAME:
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
                        if logger.isEnabledFor(logging.DEBUG):
                            logger.debug("Engine.engine: %s %s %s %s", Event.RENAME, str(uniqueid), channel, newname)
                elif event[Event.EVENT] == Event.VARSET:
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
                        if logger.isEnabledFor(logging.DEBUG):
                            logger.debug("Engine.engine: EVENT: %s %s %s %s", Event.SIPCALLID, str(uniqueid), channel, value)
                else:
                    pass
            else:
                pass
