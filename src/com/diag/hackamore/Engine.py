"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import logging
import sys
#import curses

import Logger
import Event
import Multiplex
import State

class Engine:

    def __init__(self, state = None, multiplex = None, logger = None):
        self.logger = Logger.logger() if logger == None else logger
        self.multiplex = Multiplex.Multiplex(self.logger) if multiplex == None else multiplex
        self.state = State.State(self.logger) if state == None else state
        self.window = None
        self.logger.info("Engine: INIT. %s", str(self))
        
    def __del__(self):
        self.logger.info("Engine: FINI. %s", str(self))

    def __repr__(self):
        return "Engine(" + str(self.multiplex) + ")"
    
    def initscr(self):
        self.window = True
        #self.window = curses.initscr()
        #curses.nl()
        #curses.nocbreak()
    
    def erase(self):
        if self.window != None:
            #self.window.erase()
            print chr(0x1b) + "[2J"
            print chr(0x1b) + "[;H"

    def flush(self):
        if self.window != None:
            sys.stdout.flush()

    def endwin(self):
        #if self.window != None:
        #    self.window.endwin()
        pass

    def engine(self, inputs, outputs, suppress = False, verbose = False, clear = False):
        self.logger.info("Engine.engine: STARTING. %s", str(self))
        debug = self.logger.isEnabledFor(logging.DEBUG)
        if verbose and clear:
            self.initscr()
            self.erase()
        sn = 0
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
                    if debug:
                        self.logger.debug("Engine.engine: EVENT: %s %s", str(Event.END), str(pbx))
                    if not suppress:
                        if verbose:
                            self.erase()
                            print "EVENT", sn, Event.END, pbx
                        self.state.close(pbx)
                        if verbose:
                            self.state.dump()  
                            self.flush()
                    source = self.multiplex.query(pbx)
                    source.close()
                    self.multiplex.unregister(source)
                    outputs.append(source)
                    messages.close()
                elif Event.EVENT in event:
                    flavor = event[Event.EVENT]
                    if flavor == Event.BRIDGE:
                        if not Event.CALLERID1 in event:
                            pass
                        elif not Event.CALLERID2 in event:
                            pass
                        elif not Event.CHANNEL1 in event:
                            pass
                        elif not Event.CHANNEL2 in event:
                            pass
                        elif not Event.UNIQUEID1 in event:
                            pass
                        elif not Event.UNIQUEID2 in event:
                            pass
                        else:
                            callerid1 = event[Event.CALLERID1]
                            callerid2 = event[Event.CALLERID2]
                            channel1 = event[Event.CHANNEL1]
                            channel2 = event[Event.CHANNEL2]
                            uniqueid1 = event[Event.UNIQUEID1]
                            uniqueid2 = event[Event.UNIQUEID2]
                            if debug:
                                self.logger.debug("Engine.engine: EVENT: %s %s %s %s %s %s %s %s", str(Event.BRIDGE), str(pbx), str(uniqueid1), str(channel1), str(callerid1), str(uniqueid2), str(channel2), str(callerid2))
                            if not suppress:
                                if verbose:
                                    self.erase()
                                    print "EVENT", sn, Event.BRIDGE, pbx, uniqueid1, channel1, callerid1, uniqueid2, channel2, callerid2
                                self.state.bridge(pbx, uniqueid1, uniqueid2)
                                if verbose:
                                    self.state.dump()
                                    self.flush()
                    elif flavor == Event.CONFBRIDGEEND:
                        if not Event.CONFERENCE in event:
                            pass
                        else:
                            conference = event[Event.CONFERENCE]
                            if debug:
                                self.logger.debug("Engine.engine: EVENT: %s %s %s", str(Event.CONFBRIDGEEND), str(pbx), str(conference))
                            if not suppress:
                                if verbose:
                                    self.erase()
                                    print "EVENT", sn, Event.CONFBRIDGEEND, pbx, conference
                                self.state.confbridgeend(pbx, conference)
                                if verbose:
                                    self.state.dump()
                                    self.flush()
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
                            if debug:
                                self.logger.debug("Engine.engine: EVENT: %s %s %s %s %s", str(Event.CONFBRIDGEJOIN), str(pbx), str(uniqueid), str(channel), str(conference))
                            if not suppress:
                                if verbose:
                                    self.erase()
                                    print "EVENT", sn, Event.CONFBRIDGEJOIN, pbx, uniqueid, channel, conference
                                self.state.confbridgejoin(pbx, uniqueid, conference)
                                if verbose:
                                    self.state.dump()
                                    self.flush()
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
                            if debug:
                                self.logger.debug("Engine.engine: EVENT: %s %s %s %s %s", str(Event.CONFBRIDGELEAVE), str(pbx), str(uniqueid), str(channel), str(conference))
                            if not suppress:
                                if verbose:
                                    self.erase()
                                    print "EVENT", sn, Event.CONFBRIDGELEAVE, pbx, uniqueid, channel, conference
                                self.state.confbridgeleave(pbx, uniqueid, conference)
                                if verbose:
                                    self.state.dump()
                                    self.flush()
                    elif flavor == Event.CONFBRIDGESTART:
                        if not Event.CONFERENCE in event:
                            pass
                        else:
                            conference = event[Event.CONFERENCE]
                            if debug:
                                self.logger.debug("Engine.engine: EVENT: %s %s %s", str(Event.CONFBRIDGESTART), str(pbx), str(conference))
                            if not suppress:
                                if verbose:
                                    self.erase()
                                    print "EVENT", sn, Event.CONFBRIDGESTART, pbx, conference
                                self.state.confbridgestart(pbx, conference)
                                if verbose:
                                    self.state.dump()
                                    self.flush()
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
                            if debug:
                                self.logger.debug("Engine.engine: %s %s %s %s %s %s", str(Event.DIAL), str(pbx), str(uniqueid), str(channel), str(destuniqueid), str(destination))
                            if not suppress:
                                if verbose:
                                    self.erase()
                                    print "EVENT", sn, Event.DIAL, pbx, uniqueid, channel, destuniqueid, destination
                                self.state.dial(pbx, uniqueid, destuniqueid)
                                if verbose:
                                    self.state.dump()
                                    self.flush()
                    elif flavor == Event.HANGUP:
                        if not Event.CHANNEL in event:
                            pass
                        elif not Event.UNIQUEIDLC in event:
                            pass
                        else:
                            channel = event[Event.CHANNEL]
                            uniqueid = event[Event.UNIQUEIDLC]
                            if debug:
                                self.logger.debug("Engine.engine: EVENT: %s %s %s %s", str(Event.HANGUP), str(pbx), str(uniqueid), str(channel))
                            if not suppress:
                                if verbose:
                                    self.erase()
                                    print "EVENT", sn, Event.HANGUP, pbx, uniqueid, channel
                                self.state.hangup(pbx, uniqueid)
                                if verbose:
                                    self.state.dump()
                                    self.flush()
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
                            uniqueid1 = event[Event.UNIQUEID1]
                            uniqueid2 = event[Event.UNIQUEID2]
                            if debug:
                                self.logger.debug("Engine.engine: EVENT: %s %s %s %s %s %s", str(Event.LOCALBRIDGE), str(pbx), str(uniqueid1), str(channel1), str(uniqueid2), str(channel2))
                            if not suppress:
                                if verbose:
                                    self.erase()
                                    print "EVENT", sn, Event.LOCALBRIDGE, pbx, uniqueid1, channel1, uniqueid2, channel2
                                self.state.localbridge(pbx, uniqueid1, uniqueid2)
                                if verbose:
                                    self.state.dump()
                                    self.flush()
                    elif flavor == Event.NEWCHANNEL:
                        if not Event.CALLERIDNUM in event:
                            pass
                        elif not Event.CHANNEL in event:
                            pass
                        elif not Event.CHANNELSTATE in event:
                            pass
                        elif not Event.CHANNELSTATEDESC in event:
                            pass
                        elif not Event.UNIQUEIDLC in event:
                            pass
                        else:
                            calleridnum = event[Event.CALLERIDNUM]
                            channel = event[Event.CHANNEL]
                            channelstate = event[Event.CHANNELSTATE]
                            channelstatedesc = event[Event.CHANNELSTATEDESC]
                            uniqueid = event[Event.UNIQUEIDLC]
                            if debug:
                                self.logger.debug("Engine.engine: EVENT: %s %s %s %s %s %s %s", str(Event.NEWCHANNEL), str(pbx), str(uniqueid), str(channel), str(calleridnum), str(channelstate), str(channelstatedesc))
                            if not suppress:
                                if verbose:
                                    self.erase()
                                    print "EVENT", sn, Event.NEWCHANNEL, pbx, uniqueid, channel, calleridnum, channelstate, channelstatedesc
                                self.state.newchannel(pbx, uniqueid, channel, calleridnum, channelstate, channelstatedesc)
                                if verbose:
                                    self.state.dump()
                                    self.flush()
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
                            if debug:
                                self.logger.debug("Engine.engine: EVENT: %s %s %s %s %s %s", str(Event.NEWSTATE), str(pbx), str(uniqueid), str(channel), str(channelstate), str(channelstatedesc))
                            if not suppress:
                                if verbose:
                                    self.erase()
                                    print "EVENT", sn, Event.NEWSTATE, pbx, uniqueid, channel, channelstate, channelstatedesc
                                self.state.newstate(pbx, uniqueid, channelstate, channelstatedesc)
                                if verbose:
                                    self.state.dump()
                                    self.flush()
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
                            if debug:
                                self.logger.debug("Engine.engine: EVENT: %s %s %s %s %s", str(Event.RENAME), str(pbx), str(uniqueid), str(channel), str(newname))
                            if not suppress:
                                if verbose:
                                    self.erase()
                                    print "EVENT", sn, Event.RENAME, pbx, uniqueid, channel, newname
                                self.state.rename(pbx, uniqueid, newname)
                                if verbose:
                                    self.state.dump()
                                    self.flush()
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
                            if debug:
                                self.logger.debug("Engine.engine: EVENT: %s %s %s %s %s", str(Event.SIPCALLID), str(pbx), str(uniqueid), str(channel), str(value))
                            if not suppress:
                                if verbose:
                                    self.erase()
                                    print "EVENT", sn, Event.SIPCALLID, pbx, uniqueid, channel, value
                                self.state.sipcallid(pbx, uniqueid, value)
                                if verbose:
                                    self.state.dump()
                                    self.flush()
                    else:
                        pass
                else:
                    pass
                sn = sn + 1
        self.endwin()
        self.logger.info("Engine.engine: STOPPING. %s", str(self))
