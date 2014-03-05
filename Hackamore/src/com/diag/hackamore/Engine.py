"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import logging

import Logger
import Event
import Multiplex
import State

class Engine:

    def __init__(self, state = None, multiplex = None, logger = None):
        self.logger = Logger.logger() if logger == None else logger
        self.multiplex = Multiplex.Multiplex(self.logger) if multiplex == None else multiplex
        self.state = State.State() if state == None else state
        self.logger.info("Engine: INIT. %s", str(self))
        
    def __del__(self):
        self.logger.info("Engine: FINI. %s", str(self))

    def __repr__(self):
        return "Engine(" + str(self.multiplex) + ")"

    def engine(self, inputs, outputs, debug = False):
        self.logger.info("Engine.engine: STARTING. %s", str(self))
        enabled = self.logger.isEnabledFor(logging.DEBUG)
        while True:
            for source in inputs:
                if source.open():
                    inputs.remove(source)
                    self.multiplex.register(source)
            if not self.multiplex.active():
                break
            messages = self.multiplex.multiplex()
            for message in messages:
                event = message.event
                pbx = event[Event.SOURCE]
                if Event.END in event:
                    self.state.close(pbx)
                    source = self.multiplex.query(pbx)
                    source.close()
                    self.multiplex.unregister(source)
                    outputs.append(source)
                    messages.close()
                elif Event.EVENT in event:
                    flavor = event[Event.EVENT]
                    if flavor == Event.CONFBRIDGEEND:
                        if not Event.CONFERENCE in event:
                            pass
                        else:
                            conference = event[Event.CONFERENCE]
                            if enabled:
                                self.logger.debug("Engine.engine: %s %s %s", str(Event.CONFBRIDGEEND), str(pbx), str(conference))
                            if not debug:
                                self.state.confbridgeend(pbx, conference)
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
                            uniqueid = event[Event.UNIQUEIDLC]
                            if enabled:
                                self.logger.debug("Engine.engine: %s %s %s %s %s", str(Event.CONFBRIDGEJOIN), str(pbx), str(uniqueid), str(channel), str(conference))
                            if not debug:
                                self.state.confbridgejoin(pbx, uniqueid, conference)
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
                            uniqueid = event[Event.UNIQUEIDLC]
                            if enabled:
                                self.logger.debug("Engine.engine: %s %s %s %s %s", str(Event.CONFBRIDGELEAVE), str(pbx), str(uniqueid), str(channel), str(conference))
                            if not debug:
                                self.state.confbridgeleave(pbx, uniqueid, conference)
                    elif flavor == Event.CONFBRIDGESTART:
                        if not Event.CONFERENCE in event:
                            pass
                        else:
                            conference = event[Event.CONFERENCE]
                            if enabled:
                                self.logger.debug("Engine.engine: %s %s %s", str(Event.CONFBRIDGESTART), str(pbx), str(conference))
                            if not debug:
                                self.state.confbridgestart(pbx, conference)
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
                            destuniqueid = event[Event.DESTUNIQUEID]
                            uniqueid = event[Event.UNIQUEIDUC]
                            if enabled:
                                self.logger.debug("Engine.engine: %s %s %s %s %s %s", str(Event.DIAL), str(pbx), str(uniqueid), str(channel), str(destuniqueid), str(destination))
                            if not debug:
                                self.state.dial(pbx, uniqueid, destuniqueid)
                    elif flavor == Event.HANGUP:
                        if not Event.CHANNEL in event:
                            pass
                        elif not Event.UNIQUEIDLC in event:
                            pass
                        else:
                            channel = event[Event.CHANNEL]
                            uniqueid = event[Event.UNIQUEIDLC]
                            if enabled:
                                self.logger.debug("Engine.engine: %s %s %s %s", str(Event.HANGUP), str(pbx), str(uniqueid), str(channel))
                            if not debug:
                                self.state.hangup(pbx, uniqueid)
                    elif flavor == Event.HANGUP:
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
                            uniqueid1 = event[Event.UNIQUEID1]
                            uniqueid2 = event[Event.UNIQUEID2]
                            if enabled:
                                self.logger.debug("Engine.engine: %s %s %s %s %s %s", str(Event.HANGUP), str(pbx), str(uniqueid1), str(channel1), str(uniqueid2), str(channel2))
                            if not debug:
                                self.state.localbridge(pbx, uniqueid1, channel1, uniqueid2, channel2)
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
                            uniqueid = event[Event.UNIQUEIDLC]
                            if enabled:
                                self.logger.debug("Engine.engine: %s %s %s %s %s %s", str(Event.NEWCHANNEL), str(pbx), str(uniqueid), str(channel), str(channelstate), str(channelstatedesc))
                            if not debug:
                                self.state.newchannel(pbx, uniqueid, channel, channelstate, channelstatedesc)
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
                            uniqueid = event[Event.UNIQUEIDLC]
                            if enabled:
                                self.logger.debug("Engine.engine: %s %s %s %s %s %s", str(Event.NEWSTATE), str(pbx), str(uniqueid), str(channel), str(channelstate), str(channelstatedesc))
                            if not debug:
                                self.state.newstate(pbx, uniqueid, channelstate, channelstatedesc)
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
                            uniqueid = event[Event.UNIQUEIDLC]
                            if enabled:
                                self.logger.debug("Engine.engine: %s %s %s %s %s", str(Event.RENAME), str(pbx), str(uniqueid), str(channel), str(newname))
                            if not debug:
                                self.state.rename(pbx, uniqueid, newname)
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
                            uniqueid = event[Event.UNIQUEIDLC]
                            value = event[Event.VALUE]
                            if enabled:
                                self.logger.debug("Engine.engine: %s %s %s %s %s", str(Event.SIPCALLID), str(pbx), str(uniqueid), str(channel), str(value))
                            if not debug:
                                self.state.sipcallid(pbx, uniqueid, channel, value)
                    else:
                        pass
                else:
                    pass
        self.logger.info("Engine.engine: STOPPING. %s", str(self))
