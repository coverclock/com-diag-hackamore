"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import unittest
import logging
import time

import com.diag.hackamore.Logger
import com.diag.hackamore.Event
import com.diag.hackamore.File
import com.diag.hackamore.Multiplex
import com.diag.hackamore.Manifold
import com.diag.hackamore.Serializer
import com.diag.hackamore.ModelCounter
import com.diag.hackamore.View

from Parameters import TYPESCRIPT

class Test(unittest.TestCase):

    def setUp(self):
        com.diag.hackamore.Logger.logger().setLevel(logging.DEBUG)

    def tearDown(self):
        pass

    def test010Sanity(self):
        name = self.id()
        multiplex = com.diag.hackamore.Multiplex.Multiplex()
        self.assertIsNotNone(multiplex)
        self.assertFalse(multiplex.active())
        source = com.diag.hackamore.File.File(name, TYPESCRIPT)
        self.assertIsNotNone(source)
        self.assertTrue(source.open())
        self.assertFalse(multiplex.active())
        multiplex.register(source)
        self.assertTrue(multiplex.active())
        model = com.diag.hackamore.ModelCounter.ModelCounter()
        view = com.diag.hackamore.View.View(model)
        manifold = com.diag.hackamore.Manifold.Manifold(model, view)
        serializer = com.diag.hackamore.Serializer.Serializer(manifold)
        messages = multiplex.multiplex()
        for message in messages:
            self.assertIsNotNone(message)
            event = message.event
            self.assertIsNotNone(event)
            self.assertTrue(event)
            serializer.process(event)
            if not com.diag.hackamore.Event.END in event:
                pass
            elif not com.diag.hackamore.Event.SOURCE in event:
                pass
            else:
                pbx = event[com.diag.hackamore.Event.SOURCE]
                temporary = multiplex.query(pbx)
                self.assertEquals(temporary.pbx, pbx)
                self.assertIsNotNone(temporary)
                self.assertTrue(temporary.close())
                self.assertTrue(multiplex.active())
                self.assertFalse(temporary.open())
                self.assertTrue(multiplex.active())
                multiplex.unregister(source)
                self.assertFalse(multiplex.active())
                messages.close()
        serializer.wait()
        self.assertFalse(multiplex.active())
        self.assertTrue(model.counter[com.diag.hackamore.Event.BRIDGE])
        self.assertTrue(model.counter[com.diag.hackamore.Event.CONFBRIDGEEND])
        self.assertTrue(model.counter[com.diag.hackamore.Event.CONFBRIDGEJOIN])
        self.assertTrue(model.counter[com.diag.hackamore.Event.CONFBRIDGELEAVE])
        self.assertTrue(model.counter[com.diag.hackamore.Event.CONFBRIDGESTART])
        self.assertTrue(model.counter[com.diag.hackamore.Event.DIAL])
        self.assertTrue(model.counter[com.diag.hackamore.Event.END])
        self.assertTrue(model.counter[com.diag.hackamore.Event.HANGUP])
        self.assertTrue(model.counter[com.diag.hackamore.Event.LOCALBRIDGE])
        self.assertTrue(model.counter[com.diag.hackamore.Event.NEWCHANNEL])
        self.assertTrue(model.counter[com.diag.hackamore.Event.NEWSTATE])
        self.assertTrue(model.counter[com.diag.hackamore.Event.RENAME])
        self.assertTrue(model.counter[com.diag.hackamore.Event.SIPCALLID])    

if __name__ == "__main__":
    unittest.main()
