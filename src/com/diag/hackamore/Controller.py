"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import Logger
import Event
import Multiplex
import Model
import View

class Controller:

    def __init__(self, model = None, view = None, multiplex = None, tracer = None, logger = None):
        self.logger = Logger.logger() if logger == None else logger
        self.tracer = tracer
        self.model = Model.Model(logger = self.logger) if model == None else model
        self.view = View.View(model = self.model, logger = self.logger) if view == None else view
        self.multiplex = Multiplex.Multiplex(logger = self.logger) if multiplex == None else multiplex
        
    def __del__(self):
        pass

    def __repr__(self):
        return "Controller(" + str(self.multiplex) + ")"

    def loop(self, inputs, outputs):
        self.logger.info("Controller.loop: STARTING. %s", str(self))
        while True:
            for source in inputs:
                if source.open():
                    inputs.remove(source)
                    self.multiplex.register(source)
            if not self.multiplex.active():
                break
            messages = self.multiplex.multiplex()
            for message in messages:
                if self.tracer != None:
                    message.trace(self.tracer)
                event = message.event
                pbx = event[Event.SOURCE]
                if Event.END in event:
                    events = event[Event.END]
                    if events == "1":
                        self.view.end(pbx)
                        self.model.end(pbx)
                        self.view.display()
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
                            self.view.bridge(pbx, uniqueid1, channel1, callerid1, uniqueid2, channel2, callerid2)
                            self.model.bridge(pbx, uniqueid1, uniqueid2)
                            self.view.display()
                    elif flavor == Event.CONFBRIDGEEND:
                        if not Event.CONFERENCE in event:
                            pass
                        else:
                            conference = event[Event.CONFERENCE]
                            self.view.confbridgeend(pbx, conference)
                            self.model.confbridgeend(pbx, conference)
                            self.view.display()
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
                            self.view.confbridgejoin(pbx, uniqueid, channel, conference)
                            self.model.confbridgejoin(pbx, uniqueid, conference)
                            self.view.display()
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
                            self.view.confbridgeleave(pbx, uniqueid, channel, conference)
                            self.model.confbridgeleave(pbx, uniqueid, conference)
                            self.view.display()
                    elif flavor == Event.CONFBRIDGESTART:
                        if not Event.CONFERENCE in event:
                            pass
                        else:
                            conference = event[Event.CONFERENCE]
                            self.view.confbridgestart(pbx, conference)
                            self.model.confbridgestart(pbx, conference)
                            self.view.display()
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
                            self.view.dial(pbx, uniqueid, channel, destuniqueid, destination)
                            self.model.dial(pbx, uniqueid, destuniqueid)
                            self.view.display()
                    elif flavor == Event.HANGUP:
                        if not Event.CHANNEL in event:
                            pass
                        elif not Event.UNIQUEIDLC in event:
                            pass
                        else:
                            channel = event[Event.CHANNEL]
                            uniqueid = event[Event.UNIQUEIDLC]
                            self.view.hangup(pbx, uniqueid, channel)
                            self.model.hangup(pbx, uniqueid)
                            self.view.display()
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
                            self.view.localbridge(pbx, uniqueid1, channel1, uniqueid2, channel2)
                            self.model.localbridge(pbx, uniqueid1, uniqueid2)
                            self.view.display()
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
                            self.view.newchannel(pbx, uniqueid, channel, calleridnum, channelstate, channelstatedesc)
                            self.model.newchannel(pbx, uniqueid, channel, calleridnum, channelstate, channelstatedesc)
                            self.view.display()
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
                            self.view.newstate(pbx, uniqueid, channel, channelstate, channelstatedesc)
                            self.model.newstate(pbx, uniqueid, channelstate, channelstatedesc)
                            self.view.display()
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
                            self.view.rename(pbx, uniqueid, channel, newname)
                            self.model.rename(pbx, uniqueid, newname)
                            self.view.display()
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
                            self.view.sipcallid(pbx, uniqueid, channel, value)
                            self.model.sipcallid(pbx, uniqueid, value)
                            self.view.display()
                    else:
                        pass
                else:
                    pass
        self.logger.info("Controller.loop: STOPPING. %s", str(self))
