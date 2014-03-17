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
        #
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
        #
        #
        #
        model.newchannel("pbx1", "uid01", "chan01", "01", "0", "up")
        #
        self.assertEquals(len(model.channels), 1)
        self.assertEquals(len(model.bridges), 0)
        self.assertEquals(len(model.trunks), 0)
        self.assertEquals(len(model.calls), 0)
        self.assertEquals(len(model.numbers), 1)
        #
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
        #
        self.assertIn("pbx1", model.numbers)
        numbers = model.numbers["pbx1"]
        self.assertIsNotNone(numbers)
        self.assertEquals(len(numbers), 1)
        self.assertIn("chan01", numbers)
        number = numbers["chan01"]
        self.assertIsNotNone(number)
        self.assertEquals(number, "01")
        #
        #
        #
        model.newchannel("pbx1", "uid02", "chan02", "02", "1", "rsvd")
        #
        self.assertEquals(len(model.channels), 1)
        self.assertEquals(len(model.bridges), 0)
        self.assertEquals(len(model.trunks), 0)
        self.assertEquals(len(model.calls), 0)
        self.assertEquals(len(model.numbers), 1)
        #
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
        #
        self.assertIn("pbx1", model.numbers)
        numbers = model.numbers["pbx1"]
        self.assertIsNotNone(numbers)
        self.assertEquals(len(numbers), 2)
        self.assertIn("chan02", numbers)
        number = numbers["chan02"]
        self.assertIsNotNone(number)
        self.assertEquals(number, "02")
        #
        #
        #
        model.newchannel("pbx2", "uid03", "chan03", "03", "3", "down")
        #
        self.assertEquals(len(model.channels), 2)
        self.assertEquals(len(model.bridges), 0)
        self.assertEquals(len(model.trunks), 0)
        self.assertEquals(len(model.calls), 0)
        self.assertEquals(len(model.numbers), 2)
        #
        self.assertIn("pbx2", model.channels)
        channels = model.channels["pbx2"]
        self.assertIsNotNone(channels)
        self.assertEquals(len(channels), 1)
        self.assertIn("uid03", channels)
        chan = channels["uid03"]
        self.assertIsNotNone(chan)
        self.assertIsInstance(chan, com.diag.hackamore.Channel.Channel)
        self.assertEquals(chan.pbx, "pbx2")
        self.assertEquals(chan.uniqueid, "uid03")
        self.assertEquals(chan.calleridnum, "03")
        self.assertIsNone(chan.sipcallid)
        self.assertIsNone(chan.conference)
        self.assertEquals(chan.channel, "chan03")
        self.assertEquals(chan.channelstate, "3")
        self.assertEquals(chan.channelstatedesc, "down")
        self.assertEquals(chan.role, com.diag.hackamore.Channel.IDLE)
        self.assertIsNone(chan.call)
        #
        self.assertIn("pbx2", model.numbers)
        numbers = model.numbers["pbx2"]
        self.assertIsNotNone(numbers)
        self.assertEquals(len(numbers), 1)
        self.assertIn("chan03", numbers)
        number = numbers["chan03"]
        self.assertIsNotNone(number)
        self.assertEquals(number, "03")
        #
        #
        #
        model.dial("pbx1", "uid01", "uid02")
        #
        self.assertEquals(len(model.channels), 2)
        self.assertEquals(len(model.bridges), 0)
        self.assertEquals(len(model.trunks), 0)
        self.assertEquals(len(model.calls), 0)
        self.assertEquals(len(model.numbers), 2)
        #
        self.assertIn("pbx1", model.channels)
        channels = model.channels["pbx1"]
        self.assertIsNotNone(channels)
        self.assertEquals(len(channels), 2)
        self.assertIn("uid01", channels)
        self.assertIn("uid02", channels)
        chan1 = channels["uid01"]
        self.assertIsNotNone(chan1)
        self.assertEquals(chan1.role, com.diag.hackamore.Channel.CALLING)
        self.assertIsNone(chan1.call)
        #
        chan2 = channels["uid02"]
        self.assertIsNotNone(chan2)
        self.assertEquals(chan2.role, com.diag.hackamore.Channel.CALLED)
        self.assertIsNone(chan2.call)
        #
        #
        #
        model.bridge("pbx1", "uid01", "uid02")
        #
        self.assertEquals(len(model.channels), 2)
        self.assertEquals(len(model.bridges), 0)
        self.assertEquals(len(model.trunks), 0)
        self.assertEquals(len(model.calls), 1)
        self.assertEquals(len(model.numbers), 2)
        #
        self.assertIn("pbx1", model.channels)
        channels = model.channels["pbx1"]
        self.assertIsNotNone(channels)
        self.assertEquals(len(channels), 2)
        #
        self.assertIn("uid01", channels)
        chan1 = channels["uid01"]
        self.assertIsNotNone(chan1)
        self.assertEquals(chan1.role, com.diag.hackamore.Channel.CALLING)
        self.assertIsNotNone(chan1.call)
        call1 = chan1.call
        #
        self.assertIn("uid02", channels)
        chan2 = channels["uid02"]
        self.assertIsNotNone(chan2)
        self.assertEquals(chan2.role, com.diag.hackamore.Channel.CALLED)
        self.assertIsNotNone(chan2.call)
        call2 = chan2.call
        #
        self.assertIs(call1, call2)
        for call in model.calls:
            if call is call1:
                self.assertEquals(len(call), 2)
                self.assertIn(chan1, call)
                self.assertIn(chan2, call)
        #
        #
        #
        model.confbridgestart("pbx1", "99")
        #
        self.assertEquals(len(model.channels), 2)
        self.assertEquals(len(model.bridges), 1)
        self.assertEquals(len(model.trunks), 0)
        self.assertEquals(len(model.calls), 1)
        self.assertEquals(len(model.numbers), 2)
        #
        self.assertIn("pbx1", model.bridges)
        bridges = model.bridges["pbx1"]
        self.assertIsNotNone(bridges)
        self.assertEquals(len(bridges), 1)
        self.assertIn("99", bridges)
        bridge = bridges["99"]
        self.assertIsNotNone(bridge)
        self.assertEqual(len(bridge), 0)
        #
        #
        #
        model.confbridgejoin("pbx1", "uid01", "99")
        #
        self.assertEquals(len(model.channels), 2)
        self.assertEquals(len(model.bridges), 1)
        self.assertEquals(len(model.trunks), 0)
        self.assertEquals(len(model.calls), 1)
        self.assertEquals(len(model.numbers), 2)
        #
        self.assertIn("pbx1", model.bridges)
        bridges = model.bridges["pbx1"]
        self.assertIsNotNone(bridges)
        self.assertEquals(len(bridges), 1)
        self.assertIn("99", bridges)
        bridge = bridges["99"]
        self.assertIsNotNone(bridge)
        self.assertEqual(len(bridge), 1)
        self.assertIn("uid01", bridge)
        chan1 = bridge["uid01"]
        self.assertIn("pbx1", model.channels)
        channels = model.channels["pbx1"]
        self.assertIn("uid01", channels)
        chan2 = channels["uid01"]
        self.assertIs(chan1, chan2)
        #
        model.confbridgejoin("pbx1", "uid02", "99")
        #
        self.assertEquals(len(model.channels), 2)
        self.assertEquals(len(model.bridges), 1)
        self.assertEquals(len(model.trunks), 0)
        self.assertEquals(len(model.calls), 1)
        self.assertEquals(len(model.numbers), 2)
        #
        self.assertIn("pbx1", model.bridges)
        bridges = model.bridges["pbx1"]
        self.assertIsNotNone(bridges)
        self.assertEquals(len(bridges), 1)
        self.assertIn("99", bridges)
        bridge = bridges["99"]
        self.assertIsNotNone(bridge)
        self.assertEqual(len(bridge), 2)
        self.assertIn("uid01", bridge)
        chan1 = bridge["uid01"]
        self.assertIn("pbx1", model.channels)
        channels = model.channels["pbx1"]
        self.assertIn("uid01", channels)
        chan2 = channels["uid01"]
        self.assertIs(chan1, chan2)
        self.assertIn("uid02", bridge)
        chan3 = bridge["uid02"]
        self.assertIn("pbx1", model.channels)
        channels = model.channels["pbx1"]
        self.assertIn("uid02", channels)
        chan4 = channels["uid02"]
        self.assertIs(chan3, chan4)
        #
        #
        #
        model.confbridgeleave("pbx1", "uid01", "99")
        #
        self.assertEquals(len(model.channels), 2)
        self.assertEquals(len(model.bridges), 1)
        self.assertEquals(len(model.trunks), 0)
        self.assertEquals(len(model.calls), 1)
        self.assertEquals(len(model.numbers), 2)
        #
        self.assertIn("pbx1", model.bridges)
        bridges = model.bridges["pbx1"]
        self.assertIsNotNone(bridges)
        self.assertEquals(len(bridges), 1)
        self.assertIn("99", bridges)
        bridge = bridges["99"]
        self.assertIsNotNone(bridge)
        self.assertEqual(len(bridge), 1)
        self.assertIn("uid02", bridge)
        chan1 = bridge["uid02"]
        self.assertIn("pbx1", model.channels)
        channels = model.channels["pbx1"]
        self.assertIn("uid02", channels)
        chan2 = channels["uid02"]
        self.assertIs(chan1, chan2)
        #
        #
        #
        model.confbridgeleave("pbx1", "uid02", "99")
        #
        self.assertEquals(len(model.channels), 2)
        self.assertEquals(len(model.bridges), 1)
        self.assertEquals(len(model.trunks), 0)
        self.assertEquals(len(model.calls), 1)
        self.assertEquals(len(model.numbers), 2)
        #
        self.assertIn("pbx1", model.bridges)
        bridges = model.bridges["pbx1"]
        self.assertIsNotNone(bridges)
        self.assertEquals(len(bridges), 1)
        self.assertIn("99", bridges)
        bridge = bridges["99"]
        self.assertIsNotNone(bridge)
        self.assertEqual(len(bridge), 0)
        #
        #
        #
        model.confbridgeend("pbx1", "99")
        #
        self.assertEquals(len(model.channels), 2)
        self.assertEquals(len(model.bridges), 0)
        self.assertEquals(len(model.trunks), 0)
        self.assertEquals(len(model.calls), 1)
        self.assertEquals(len(model.numbers), 2)
        #
        #
        #
        model.hangup("pbx1", "uid01")
        #
        self.assertEquals(len(model.channels), 2)
        self.assertEquals(len(model.bridges), 0)
        self.assertEquals(len(model.trunks), 0)
        self.assertEquals(len(model.calls), 1)
        self.assertEquals(len(model.numbers), 2)
        #
        self.assertIn("pbx1", model.channels)
        channels = model.channels["pbx1"]
        self.assertIsNotNone(channels)
        self.assertEquals(len(channels), 1)
        self.assertIn("uid02", channels)
        #
        self.assertIn("pbx1", model.channels)
        channels = model.channels["pbx1"]
        self.assertIn("uid02", channels)
        chan1 = channels["uid02"]
        self.assertIsNotNone(chan1)
        self.assertIsNotNone(chan1.call)
        call1 = chan1.call
        #
        for call in model.calls:
            if call is call1:
                self.assertEquals(len(call), 1)
                self.assertIn(chan1, call)
        #
        #
        #
        model.hangup("pbx1", "uid02")
        #
        self.assertEquals(len(model.channels), 1)
        self.assertEquals(len(model.bridges), 0)
        self.assertEquals(len(model.trunks), 0)
        self.assertEquals(len(model.calls), 0)
        self.assertEquals(len(model.numbers), 1)
        #
        self.assertNotIn("pbx1", model.channels)
        self.assertIn("pbx2", model.channels)
        #
        #
        #
        model.newchannel("pbx2", "uid04", "chan04", "04", "1", "up")
        #
        self.assertEquals(len(model.channels), 1)
        self.assertEquals(len(model.bridges), 0)
        self.assertEquals(len(model.trunks), 0)
        self.assertEquals(len(model.calls), 0)
        self.assertEquals(len(model.numbers), 1)
        #
        self.assertIn("pbx2", model.channels)
        channels = model.channels["pbx2"]
        self.assertIsNotNone(channels)
        self.assertEquals(len(channels), 2)
        self.assertIn("uid04", channels)
        chan = channels["uid04"]
        self.assertIsNotNone(chan)
        self.assertIsInstance(chan, com.diag.hackamore.Channel.Channel)
        self.assertEquals(chan.pbx, "pbx2")
        self.assertEquals(chan.uniqueid, "uid04")
        self.assertEquals(chan.calleridnum, "04")
        self.assertIsNone(chan.sipcallid)
        self.assertIsNone(chan.conference)
        self.assertEquals(chan.channel, "chan04")
        self.assertEquals(chan.channelstate, "1")
        self.assertEquals(chan.channelstatedesc, "up")
        self.assertEquals(chan.role, com.diag.hackamore.Channel.IDLE)
        self.assertIsNone(chan.call)
        #
        self.assertIn("pbx2", model.numbers)
        numbers = model.numbers["pbx2"]
        self.assertIsNotNone(numbers)
        self.assertEquals(len(numbers), 2)
        self.assertIn("chan04", numbers)
        number = numbers["chan04"]
        self.assertIsNotNone(number)
        self.assertEquals(number, "04")
        #
        #
        #
        model.localbridge("pbx2", "uid03", "uid04")
        #
        self.assertEquals(len(model.channels), 1)
        self.assertEquals(len(model.bridges), 0)
        self.assertEquals(len(model.trunks), 0)
        self.assertEquals(len(model.calls), 1)
        self.assertEquals(len(model.numbers), 1)
        #
        self.assertIn("pbx2", model.channels)
        channels = model.channels["pbx2"]
        self.assertIsNotNone(channels)
        self.assertEquals(len(channels), 2)
        #
        self.assertIn("uid03", channels)
        chan1 = channels["uid03"]
        self.assertIsNotNone(chan1)
        self.assertEquals(chan1.role, com.diag.hackamore.Channel.TRUNK)
        self.assertIsNotNone(chan1.call)
        call1 = chan1.call
        #
        self.assertIn("uid04", channels)
        chan2 = channels["uid04"]
        self.assertIsNotNone(chan2)
        self.assertEquals(chan2.role, com.diag.hackamore.Channel.TRUNK)
        self.assertIsNotNone(chan2.call)
        call2 = chan2.call
        #
        self.assertIs(call1, call2)
        #
        for call in model.calls:
            if call is call1:
                self.assertEquals(len(call), 2)
                self.assertIn(chan1, call)
                self.assertIn(chan2, call)
        #
        #
        #
        model.newstate("pbx2", "uid03", "0", "up")
        #
        self.assertIn("pbx2", model.channels)
        channels = model.channels["pbx2"]
        self.assertIsNotNone(channels)
        self.assertEquals(len(channels), 2)
        self.assertIn("uid03", channels)
        chan = channels["uid03"]
        self.assertIsNotNone(chan)
        self.assertIsInstance(chan, com.diag.hackamore.Channel.Channel)
        self.assertEquals(chan.channelstate, "0")
        self.assertEquals(chan.channelstatedesc, "up")
        #
        self.assertEquals(chan.channel, "chan03")
        #
        #
        #
        model.rename("pbx2", "uid03", "chan13")
        #
        self.assertIn("pbx2", model.channels)
        channels = model.channels["pbx2"]
        self.assertIsNotNone(channels)
        self.assertEquals(len(channels), 2)
        self.assertIn("uid03", channels)
        chan = channels["uid03"]
        self.assertIsNotNone(chan)
        self.assertIsInstance(chan, com.diag.hackamore.Channel.Channel)
        self.assertEquals(chan.channelstate, "0")
        self.assertEquals(chan.channelstatedesc, "up")
        self.assertEquals(chan.channel, "chan13")
        #
        self.assertIn("pbx2", model.numbers)
        numbers = model.numbers["pbx2"]
        self.assertIsNotNone(numbers)
        self.assertEquals(len(numbers), 2)
        self.assertNotIn("chan03", numbers)
        self.assertIn("chan13", numbers)
        number = numbers["chan13"]
        self.assertIsNotNone(number)
        self.assertEquals(number, "03")
        #
        self.assertIsNone(chan.sipcallid)
        self.assertEquals(len(model.trunks), 0)
        #
        #
        #
        model.sipcallid("pbx2", "uid03", "sipcallid03")
        #
        self.assertIn("pbx2", model.channels)
        channels = model.channels["pbx2"]
        self.assertIsNotNone(channels)
        self.assertEquals(len(channels), 2)
        self.assertIn("uid03", channels)
        chan1 = channels["uid03"]
        self.assertIsNotNone(chan1)
        self.assertIsInstance(chan1, com.diag.hackamore.Channel.Channel)
        self.assertEquals(chan1.channelstate, "0")
        self.assertEquals(chan1.channelstatedesc, "up")
        self.assertEquals(chan1.channel, "chan13")
        self.assertIsNotNone(chan1.sipcallid)
        self.assertEquals(chan1.sipcallid, "sipcallid03")
        #
        self.assertEquals(len(model.trunks), 1)
        self.assertIn("sipcallid03", model.trunks)
        chan2 = model.trunks["sipcallid03"]
        self.assertIs(chan1, chan2)
        #
        self.assertEquals(len(model.channels), 1)
        self.assertEquals(len(model.bridges), 0)
        self.assertEquals(len(model.trunks), 1)
        self.assertEquals(len(model.calls), 1)
        self.assertEquals(len(model.numbers), 1)
        #
        #
        #
        model.end("pbx2")
        #
        self.assertEquals(len(model.channels), 0)
        self.assertEquals(len(model.bridges), 0)
        self.assertEquals(len(model.trunks), 0)
        self.assertEquals(len(model.calls), 0)
        self.assertEquals(len(model.numbers), 0)

if __name__ == "__main__":
    unittest.main()
