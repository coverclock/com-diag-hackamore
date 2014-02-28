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

    def test010Filter(self):
        name = self.id()
        com.diag.hackamore.Multiplex.deregister()
        source = com.diag.hackamore.File.File(name, TYPESCRIPT)
        self.assertIsNotNone(source)
        self.assertTrue(source.open())
        self.assertIn(source.name, com.diag.hackamore.Multiplex.sources)
        self.assertTrue(com.diag.hackamore.Multiplex.active())
        for event in com.diag.hackamore.Multiplex.multiplex():
            self.assertIsNotNone(event)
            self.assertTrue(event)
            self.assertIn(com.diag.hackamore.Event.SOURCE, event)
            name = event[com.diag.hackamore.Event.SOURCE]
            if com.diag.hackamore.Event.END in event:
                temporary = com.diag.hackamore.Multiplex.query(name)
                self.assertEquals(temporary.name, name)
                self.assertIsNotNone(temporary)
                self.assertTrue(temporary.close())
                self.assertFalse(temporary.open())
                if not com.diag.hackamore.Multiplex.active():
                    break
            elif com.diag.hackamore.Event.EVENT in event:
                if event[com.diag.hackamore.Event.EVENT] == com.diag.hackamore.Event.DIAL:
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
                elif event[com.diag.hackamore.Event.EVENT] == com.diag.hackamore.Event.HANGUP:
                    if not com.diag.hackamore.Event.CHANNEL in event:
                        pass
                    elif not com.diag.hackamore.Event.UNIQUEIDLC in event:
                        pass
                    else:
                        channel = event[com.diag.hackamore.Event.CHANNEL]
                        uniqueid = ( name, event[com.diag.hackamore.Event.UNIQUEIDLC] )
                        print(com.diag.hackamore.Event.HANGUP, channel, uniqueid)
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
                elif event[com.diag.hackamore.Event.EVENT] == com.diag.hackamore.Event.VARSET:
                    if not com.diag.hackamore.Event.VARIABLE in event:
                        pass
                    elif event[com.diag.hackamore.Event.VARIABLE] != com.diag.hackamore.Event.SIPCALLID:
                        pass
                    elif not com.diag.hackamore.Event.CHANNEL not in event:
                        pass
                    elif not com.diag.hackamore.Event.UNIQUEIDLC not in event:
                        pass
                    elif not com.diag.hackamore.Event.VALUE in event:
                        pass
                    else:
                        channel = event[com.diag.hackamore.Event.CHANNEL]
                        uniqueid = ( name, event[com.diag.hackamore.Event.UNIQUEIDLC] )
                        value = event[com.diag.hackamore.Event.VALUE]
                        print(com.diag.hackamore.Event.SIPCALLID, channel, uniqueid, value)
                else:
                    pass
            else:
                pass
        self.assertNotIn(source.name, com.diag.hackamore.Multiplex.sources)
        self.assertFalse(com.diag.hackamore.Multiplex.active())

if __name__ == "__main__":
    unittest.main()
