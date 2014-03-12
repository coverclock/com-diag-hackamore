"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import unittest
import logging

import com.diag.hackamore.Logger
import com.diag.hackamore.ModelStandard
import com.diag.hackamore.Channel

class Test(unittest.TestCase):

    def setUp(self):
        com.diag.hackamore.Logger.logger().setLevel(logging.DEBUG)

    def tearDown(self):
        pass

    # Channel = model.channels[pbx][uniqueid]
    # Channel = model.bridges[pbx][conference][uniqueid]
    # Channel = model.trunks[sipcallid]
    # Channel = model.calls[0:-1][0:-1]
    # calleridnum = model.numbers[pbx][channel]

    # channel.pbx = pbx
    # channel.uniqueid = uniqueid
    # channel.calleridnum = calleridnum
    # channel.sipcallid = None
    # channel.conference = None
    # channel.channel = channel
    # channel.channelstate = channelstate
    # channel.channelstatedesc = channelstatedesc
    # channel.role = IDLE
    # channel.call = None

    def testSanity(self):
        model = com.diag.hackamore.ModelStandard.ModelStandard()
        self.assertIsNotNone(model.channels)
        self.assertIsNotNone(model.bridges)
        self.assertIsNotNone(model.trunks)
        self.assertIsNotNone(model.calls)
        self.assertIsNotNone(model.numbers)
        self.assertEquals(len(model.channels), 0)
        self.assertEquals(len(model.bridges), 0)
        self.assertEquals(len(model.trunks), 0)
        self.assertEquals(len(model.calls), 0)
        self.assertEquals(len(model.numbers), 0)
        #####
        #####
        #####
        model.newchannel("pbx1", "uid01", "chan01", "01", "0", "up")
        #####
        self.assertEquals(len(model.channels), 1)
        self.assertEquals(len(model.bridges), 0)
        self.assertEquals(len(model.trunks), 0)
        self.assertEquals(len(model.calls), 0)
        self.assertEquals(len(model.numbers), 1)
        #####
        self.assertIn("pbx1", model.channels)
        channels = model.channels["pbx1"]
        self.assertIsNotNone(channels)
        self.assertEquals(len(channels), 1)
        self.assertIn("uid01", channels)
        chan = channels["uid01"]
        self.assertIsNotNone(chan)
        self.assertIsInstance(chan, com.diag.hackamore.Channel.Channel)
        self.assertEquals(chan.pbx, "pbx1")
        self.assertEquals(chan.uniqueid, "uid01")
        self.assertEquals(chan.calleridnum, "01")
        self.assertIsNone(chan.sipcallid)
        self.assertIsNone(chan.conference)
        self.assertEquals(chan.channel, "chan01")
        self.assertEquals(chan.channelstate, "0")
        self.assertEquals(chan.channelstatedesc, "up")
        self.assertEquals(chan.role, com.diag.hackamore.Channel.IDLE)
        self.assertEquals(chan.call, None)
        #####
        self.assertIn("pbx1", model.numbers)
        numbers = model.numbers["pbx1"]
        self.assertIsNotNone(numbers)
        self.assertEquals(len(numbers), 1)
        self.assertIn("chan01", numbers)
        number = numbers["chan01"]
        self.assertIsNotNone(number)
        self.assertEquals(number, "01")
        #####
        #####
        #####
        model.newchannel("pbx1", "uid02", "chan02", "02", "1", "rsvd")
        #####
        self.assertEquals(len(model.channels), 1)
        self.assertEquals(len(model.bridges), 0)
        self.assertEquals(len(model.trunks), 0)
        self.assertEquals(len(model.calls), 0)
        self.assertEquals(len(model.numbers), 1)
        #####
        self.assertIn("pbx1", model.channels)
        channels = model.channels["pbx1"]
        self.assertIsNotNone(channels)
        self.assertEquals(len(channels), 2)
        self.assertIn("uid02", channels)
        chan = channels["uid02"]
        self.assertIsNotNone(chan)
        self.assertIsInstance(chan, com.diag.hackamore.Channel.Channel)
        self.assertEquals(chan.pbx, "pbx1")
        self.assertEquals(chan.uniqueid, "uid02")
        self.assertEquals(chan.calleridnum, "02")
        self.assertIsNone(chan.sipcallid)
        self.assertIsNone(chan.conference)
        self.assertEquals(chan.channel, "chan02")
        self.assertEquals(chan.channelstate, "1")
        self.assertEquals(chan.channelstatedesc, "rsvd")
        self.assertEquals(chan.role, com.diag.hackamore.Channel.IDLE)
        self.assertEquals(chan.call, None)
        #####
        self.assertIn("pbx1", model.numbers)
        numbers = model.numbers["pbx1"]
        self.assertIsNotNone(numbers)
        self.assertEquals(len(numbers), 2)
        self.assertIn("chan02", numbers)
        number = numbers["chan02"]
        self.assertIsNotNone(number)
        self.assertEquals(number, "02")

if __name__ == "__main__":
    unittest.main()
