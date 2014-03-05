"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import unittest
import logging

import com.diag.hackamore.Logger
import com.diag.hackamore.Event
import com.diag.hackamore.File
import com.diag.hackamore.Multiplex

from Parameters import TYPESCRIPT

class Test(unittest.TestCase):

    def setUp(self):
        com.diag.hackamore.Logger.logger().setLevel(logging.WARNING)

    def tearDown(self):
        pass
    
    def test010Construction(self):
        name = self.id()
        actual = None
        message = com.diag.hackamore.Event.Event(actual)
        self.assertIsNotNone(message)
        expected = message.event
        self.assertIsNone(expected)
        self.assertIsNotNone(message.logger)
        actual = { }
        message = com.diag.hackamore.Event.Event(actual)
        self.assertIsNotNone(message)
        expected = message.event
        self.assertIsNotNone(expected)
        self.assertEquals(len(expected), 0)
        self.assertIsNotNone(message.logger)
        actual = { }
        actual[name] = name
        message = com.diag.hackamore.Event.Event(actual)
        self.assertIsNotNone(message)
        expected = message.event
        self.assertIsNotNone(expected)
        self.assertEquals(len(expected), 1)
        self.assertIn(name, expected)
        self.assertEquals(expected[name], name)
        self.assertIsNotNone(message.logger)

    def test020Filter(self):
        name = self.id()
        multiplex = com.diag.hackamore.Multiplex.Multiplex(name)
        self.assertIsNotNone(multiplex)
        self.assertFalse(multiplex.active())
        source = com.diag.hackamore.File.File(name, TYPESCRIPT)
        self.assertIsNotNone(source)
        self.assertTrue(source.open())
        self.assertFalse(multiplex.active())
        multiplex.register(source)
        self.assertTrue(multiplex.active())
        counter = { }
        counter[com.diag.hackamore.Event.CONFBRIDGEEND] = 0
        counter[com.diag.hackamore.Event.CONFBRIDGEJOIN] = 0
        counter[com.diag.hackamore.Event.CONFBRIDGELEAVE] = 0
        counter[com.diag.hackamore.Event.CONFBRIDGESTART] = 0
        counter[com.diag.hackamore.Event.DIAL] = 0
        counter[com.diag.hackamore.Event.HANGUP] = 0
        counter[com.diag.hackamore.Event.LOCALBRIDGE] = 0
        counter[com.diag.hackamore.Event.NEWCHANNEL] = 0
        counter[com.diag.hackamore.Event.NEWSTATE] = 0
        counter[com.diag.hackamore.Event.RENAME] = 0
        counter[com.diag.hackamore.Event.SIPCALLID] = 0
        messages = multiplex.multiplex()
        for message in messages:
            self.assertIsNotNone(message)
            event = message.event
            self.assertIsNotNone(event)
            self.assertTrue(event)
            self.assertIn(com.diag.hackamore.Event.SOURCE, event)
            name = event[com.diag.hackamore.Event.SOURCE]
            if com.diag.hackamore.Event.END in event:
                temporary = multiplex.query(name)
                self.assertEquals(temporary.name, name)
                self.assertIsNotNone(temporary)
                self.assertTrue(temporary.close())
                self.assertTrue(multiplex.active())
                self.assertFalse(temporary.open())
                self.assertTrue(multiplex.active())
                multiplex.unregister(source)
                self.assertFalse(multiplex.active())
                messages.close()
            elif com.diag.hackamore.Event.EVENT in event:
                if event[com.diag.hackamore.Event.EVENT] == com.diag.hackamore.Event.CONFBRIDGEEND:
                    if not com.diag.hackamore.Event.CONFERENCE in event:
                        pass
                    else:
                        conference = event[com.diag.hackamore.Event.CONFERENCE]
                        print(com.diag.hackamore.Event.CONFBRIDGEEND, conference)
                        counter[com.diag.hackamore.Event.CONFBRIDGEEND] = counter[com.diag.hackamore.Event.CONFBRIDGEEND] + 1
                elif event[com.diag.hackamore.Event.EVENT] == com.diag.hackamore.Event.CONFBRIDGEJOIN:
                    if not com.diag.hackamore.Event.CHANNEL in event:
                        pass
                    elif not com.diag.hackamore.Event.CONFERENCE in event:
                        pass
                    elif not com.diag.hackamore.Event.UNIQUEIDLC in event:
                        pass
                    else:
                        channel = event[com.diag.hackamore.Event.CHANNEL]
                        conference = event[com.diag.hackamore.Event.CONFERENCE]
                        uniqueid = ( name, event[com.diag.hackamore.Event.UNIQUEIDLC] )
                        print(com.diag.hackamore.Event.CONFBRIDGEJOIN, channel, conference, uniqueid)
                        counter[com.diag.hackamore.Event.CONFBRIDGEJOIN] = counter[com.diag.hackamore.Event.CONFBRIDGEJOIN] + 1
                elif event[com.diag.hackamore.Event.EVENT] == com.diag.hackamore.Event.CONFBRIDGELEAVE:
                    if not com.diag.hackamore.Event.CHANNEL in event:
                        pass
                    elif not com.diag.hackamore.Event.CONFERENCE in event:
                        pass
                    elif not com.diag.hackamore.Event.UNIQUEIDLC in event:
                        pass
                    else:
                        channel = event[com.diag.hackamore.Event.CHANNEL]
                        conference = event[com.diag.hackamore.Event.CONFERENCE]
                        uniqueid = ( name, event[com.diag.hackamore.Event.UNIQUEIDLC] )
                        print(com.diag.hackamore.Event.CONFBRIDGELEAVE, channel, conference, uniqueid)
                        counter[com.diag.hackamore.Event.CONFBRIDGELEAVE] = counter[com.diag.hackamore.Event.CONFBRIDGELEAVE] + 1
                elif event[com.diag.hackamore.Event.EVENT] == com.diag.hackamore.Event.CONFBRIDGESTART:
                    if not com.diag.hackamore.Event.CONFERENCE in event:
                        pass
                    else:
                        conference = event[com.diag.hackamore.Event.CONFERENCE]
                        print(com.diag.hackamore.Event.CONFBRIDGESTART, conference)
                        counter[com.diag.hackamore.Event.CONFBRIDGESTART] = counter[com.diag.hackamore.Event.CONFBRIDGESTART] + 1
                elif event[com.diag.hackamore.Event.EVENT] == com.diag.hackamore.Event.DIAL:
                    if not com.diag.hackamore.Event.SUBEVENT in event:
                        pass
                    elif event[com.diag.hackamore.Event.SUBEVENT] != com.diag.hackamore.Event.BEGIN:
                        pass
                    elif not com.diag.hackamore.Event.CHANNEL in event:
                        pass
                    elif not com.diag.hackamore.Event.DESTINATION in event:
                        pass
                    elif not com.diag.hackamore.Event.DESTUNIQUEID in event:
                        pass
                    elif not com.diag.hackamore.Event.UNIQUEIDUC in event:
                        pass
                    else:
                        channel = event[com.diag.hackamore.Event.CHANNEL]
                        destination = event[com.diag.hackamore.Event.DESTINATION]
                        destuniqueid = ( name, event[com.diag.hackamore.Event.DESTUNIQUEID] )
                        uniqueid = ( name, event[com.diag.hackamore.Event.UNIQUEIDUC] )
                        print(com.diag.hackamore.Event.DIAL, channel, destination, destuniqueid, uniqueid)
                        counter[com.diag.hackamore.Event.DIAL] = counter[com.diag.hackamore.Event.DIAL] + 1
                elif event[com.diag.hackamore.Event.EVENT] == com.diag.hackamore.Event.HANGUP:
                    if not com.diag.hackamore.Event.CHANNEL in event:
                        pass
                    elif not com.diag.hackamore.Event.UNIQUEIDLC in event:
                        pass
                    else:
                        channel = event[com.diag.hackamore.Event.CHANNEL]
                        uniqueid = ( name, event[com.diag.hackamore.Event.UNIQUEIDLC] )
                        print(com.diag.hackamore.Event.HANGUP, channel, uniqueid)
                        counter[com.diag.hackamore.Event.HANGUP] = counter[com.diag.hackamore.Event.HANGUP] + 1
                elif event[com.diag.hackamore.Event.EVENT] == com.diag.hackamore.Event.LOCALBRIDGE:
                    if not com.diag.hackamore.Event.CHANNEL1 in event:
                        pass
                    elif not com.diag.hackamore.Event.CHANNEL2 in event:
                        pass
                    elif not com.diag.hackamore.Event.UNIQUEID1 in event:
                        pass
                    elif not com.diag.hackamore.Event.UNIQUEID2 in event:
                        pass
                    else:
                        channel1 = event[com.diag.hackamore.Event.CHANNEL1]
                        channel2 = event[com.diag.hackamore.Event.CHANNEL2]
                        uniqueid1 = ( name, event[com.diag.hackamore.Event.UNIQUEID1] )
                        uniqueid2 = ( name, event[com.diag.hackamore.Event.UNIQUEID2] )
                        print(com.diag.hackamore.Event.LOCALBRIDGE, channel1, channel2, uniqueid1, uniqueid2)
                        counter[com.diag.hackamore.Event.LOCALBRIDGE] = counter[com.diag.hackamore.Event.LOCALBRIDGE] + 1
                elif event[com.diag.hackamore.Event.EVENT] == com.diag.hackamore.Event.NEWCHANNEL:
                    if not com.diag.hackamore.Event.CHANNEL in event:
                        pass
                    elif not com.diag.hackamore.Event.CHANNELSTATE in event:
                        pass
                    elif not com.diag.hackamore.Event.CHANNELSTATEDESC in event:
                        pass
                    elif not com.diag.hackamore.Event.UNIQUEIDLC in event:
                        pass
                    else:
                        channel = event[com.diag.hackamore.Event.CHANNEL]
                        channelstate = event[com.diag.hackamore.Event.CHANNELSTATE]
                        channelstatedesc = event[com.diag.hackamore.Event.CHANNELSTATEDESC]
                        uniqueid = ( name, event[com.diag.hackamore.Event.UNIQUEIDLC] )
                        print(com.diag.hackamore.Event.NEWCHANNEL, channel, channelstate, channelstatedesc, uniqueid)
                        counter[com.diag.hackamore.Event.NEWCHANNEL] = counter[com.diag.hackamore.Event.NEWCHANNEL] + 1
                elif event[com.diag.hackamore.Event.EVENT] == com.diag.hackamore.Event.NEWSTATE:
                    if not com.diag.hackamore.Event.CHANNEL in event:
                        pass
                    elif not com.diag.hackamore.Event.CHANNELSTATE in event:
                        pass
                    elif not com.diag.hackamore.Event.CHANNELSTATEDESC in event:
                        pass
                    elif not com.diag.hackamore.Event.UNIQUEIDLC in event:
                        pass
                    else:
                        channel = event[com.diag.hackamore.Event.CHANNEL]
                        channelstate = event[com.diag.hackamore.Event.CHANNELSTATE]
                        channelstatedesc = event[com.diag.hackamore.Event.CHANNELSTATEDESC]
                        uniqueid = ( name, event[com.diag.hackamore.Event.UNIQUEIDLC] )
                        print(com.diag.hackamore.Event.NEWSTATE, channel, channelstate, channelstatedesc, uniqueid)
                        counter[com.diag.hackamore.Event.NEWSTATE] = counter[com.diag.hackamore.Event.NEWSTATE] + 1
                elif event[com.diag.hackamore.Event.EVENT] == com.diag.hackamore.Event.RENAME:
                    if not com.diag.hackamore.Event.CHANNEL in event:
                        pass
                    elif not com.diag.hackamore.Event.NEWNAME in event:
                        pass
                    elif not com.diag.hackamore.Event.UNIQUEIDLC in event:
                        pass
                    else:
                        channel = event[com.diag.hackamore.Event.CHANNEL]
                        newname = event[com.diag.hackamore.Event.NEWNAME]
                        uniqueid = ( name, event[com.diag.hackamore.Event.UNIQUEIDLC] )
                        print(com.diag.hackamore.Event.RENAME, channel, newname, destuniqueid, uniqueid)
                        counter[com.diag.hackamore.Event.RENAME] = counter[com.diag.hackamore.Event.RENAME] + 1
                elif event[com.diag.hackamore.Event.EVENT] == com.diag.hackamore.Event.VARSET:
                    if not com.diag.hackamore.Event.VARIABLE in event:
                        pass
                    elif event[com.diag.hackamore.Event.VARIABLE] != com.diag.hackamore.Event.SIPCALLID:
                        pass
                    elif not com.diag.hackamore.Event.CHANNEL in event:
                        pass
                    elif not com.diag.hackamore.Event.UNIQUEIDLC in event:
                        pass
                    elif not com.diag.hackamore.Event.VALUE in event:
                        pass
                    else:
                        channel = event[com.diag.hackamore.Event.CHANNEL]
                        uniqueid = ( name, event[com.diag.hackamore.Event.UNIQUEIDLC] )
                        value = event[com.diag.hackamore.Event.VALUE]
                        print(com.diag.hackamore.Event.SIPCALLID, channel, uniqueid, value)
                        counter[com.diag.hackamore.Event.SIPCALLID] = counter[com.diag.hackamore.Event.SIPCALLID] + 1
                else:
                    pass
            else:
                pass
        self.assertFalse(multiplex.active())
        self.assertTrue(counter[com.diag.hackamore.Event.CONFBRIDGEEND])
        self.assertTrue(counter[com.diag.hackamore.Event.CONFBRIDGEJOIN])
        self.assertTrue(counter[com.diag.hackamore.Event.CONFBRIDGELEAVE])
        self.assertTrue(counter[com.diag.hackamore.Event.CONFBRIDGESTART])
        self.assertTrue(counter[com.diag.hackamore.Event.DIAL])
        self.assertTrue(counter[com.diag.hackamore.Event.HANGUP])
        self.assertTrue(counter[com.diag.hackamore.Event.LOCALBRIDGE])
        self.assertTrue(counter[com.diag.hackamore.Event.NEWCHANNEL])
        self.assertTrue(counter[com.diag.hackamore.Event.NEWSTATE])
        self.assertTrue(counter[com.diag.hackamore.Event.RENAME])
        self.assertTrue(counter[com.diag.hackamore.Event.SIPCALLID])    

if __name__ == "__main__":
    unittest.main()
