"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import unittest
import logging
import tempfile
import os

import com.diag.hackamore.Logger
import com.diag.hackamore.Event
import com.diag.hackamore.File
import com.diag.hackamore.Model
import com.diag.hackamore.View
import com.diag.hackamore.Manifold
import com.diag.hackamore.Multiplex
import com.diag.hackamore.Controller
import com.diag.hackamore.Trace
import com.diag.hackamore.End

from Parameters import TRACELET
from Parameters import TRACE
from Parameters import TYPESCRIPT

class Test(unittest.TestCase):

    def setUp(self):
        com.diag.hackamore.Logger.logger().setLevel(logging.DEBUG)

    def tearDown(self):
        pass

    def test010Construction(self):
        name = self.id()
        source = com.diag.hackamore.Trace.Trace(name, TRACELET)
        self.assertIsNotNone(source)
        self.assertIsNotNone(source.pbx)
        self.assertEquals(source.pbx, name)
        self.assertIsNotNone(source.path)
        self.assertEquals(source.path, TRACELET)
        self.assertIsNone(source.file)
        self.assertTrue(source.open())
        self.assertFalse(source.open())
        self.assertIsNotNone(source.file)
        self.assertTrue(source.close())
        self.assertFalse(source.close())
        self.assertIsNotNone(source.file)
        self.assertTrue(source.open())
        self.assertFalse(source.open())
        self.assertIsNotNone(source.file)
        self.assertTrue(source.close())
        self.assertFalse(source.close())
        self.assertIsNotNone(source.file)
        self.assertTrue(source.open())
        self.assertFalse(source.open())
        self.assertIsNotNone(source.file)
        self.assertTrue(source.force())
        self.assertFalse(source.force())
        self.assertIsNone(source.file)

    def test020Read(self):
        name = self.id()
        source = com.diag.hackamore.Trace.Trace(name, TRACELET)
        self.assertTrue(source.open())
        lines = 0
        eof = False
        while not eof:
            try:
                line = source.read()
            except com.diag.hackamore.End.End:
                eof = True
            else:
                if line == None:
                    continue
                lines = lines + 1
                if lines == 1:
                    self.assertEquals(line, "OneOne: AlphaAlpha")
                elif lines == 2:
                    self.assertEquals(line, "OneTwo: AlphaBeta")
                elif lines == 3:
                    self.assertEquals(line, "OneThree: AlphaGamma")
                elif lines == 4:
                    self.assertEquals(line, "SOURCE: PBX")
                elif lines == 5:
                    self.assertEquals(line, "TIME: 1234567890.01")
                elif lines == 6:
                    self.assertEquals(line, "")
                elif lines == 7:
                    self.assertEquals(line, "TwoOne: BetaAlpha")
                elif lines == 8:
                    self.assertEquals(line, "TwoTwo: BetaBeta")
                elif lines == 9:
                    self.assertEquals(line, "SOURCE: PBX")
                elif lines == 10:
                    self.assertEquals(line, "TIME: 1234567890.02")
                elif lines == 11:
                    self.assertEquals(line, "")
                elif lines == 12:
                    self.assertEquals(line, "ThreeOne: GammaAlpha")
                elif lines == 13:
                    self.assertEquals(line, "ThreeTwo: GammaBeta")
                elif lines == 14:
                    self.assertEquals(line, "ThreeThree: GammaGamma")
                elif lines == 15:
                    self.assertEquals(line, "SOURCE: PBX")
                elif lines == 16:
                    self.assertEquals(line, "TIME: 1234567890.03")
                elif lines == 17:
                    self.assertEquals(line, "")
                elif lines == 18:
                    self.assertEquals(line, "FourOne: DeltaAlpha")
                elif lines == 19:
                    self.assertEquals(line, "SOURCE: PBX")
                elif lines == 20:
                    self.assertEquals(line, "TIME: 1234567890.04")
                elif lines == 21:
                    self.assertEquals(line, "")
                elif lines == 22:
                    self.assertEquals(line, "END: 5")
                elif lines == 23:
                    self.assertEquals(line, "SOURCE: PBX")
                elif lines == 24:
                    self.assertEquals(line, "TIME: 1234567890.05")
                elif lines == 25:
                    self.assertEquals(line, "")
                else:
                    self.assertTrue(0 < lines < 26)
            finally:
                pass
        self.assertEqual(lines, 25)
        self.assertTrue(source.close())
 
    def test030Get(self):
        name = self.id()
        source = com.diag.hackamore.Trace.Trace(name, TRACELET)
        self.assertTrue(source.open())
        events = 0
        eof = False
        while not eof:
            event = source.get()
            if event == None:
                continue
            events = events + 1
            self.assertTrue(event)
            if events == 1:
                self.assertEquals(len(event), 5)
                self.assertIn(com.diag.hackamore.Event.SOURCE, event)
                self.assertEquals(event[com.diag.hackamore.Event.SOURCE], "PBX")
                self.assertIn(com.diag.hackamore.Event.TIME, event)
                self.assertEquals(event[com.diag.hackamore.Event.TIME], "1234567890.01")
                self.assertNotIn(com.diag.hackamore.Event.END, event)
                self.assertIn("OneOne", event)
                self.assertEquals(event["OneOne"], "AlphaAlpha")
                self.assertIn("OneTwo", event)
                self.assertEquals(event["OneTwo"], "AlphaBeta")
                self.assertIn("OneThree", event)
                self.assertEquals(event["OneThree"], "AlphaGamma")
            elif events == 2:
                self.assertEquals(len(event), 4)
                self.assertIn(com.diag.hackamore.Event.SOURCE, event)
                self.assertEquals(event[com.diag.hackamore.Event.SOURCE], "PBX")
                self.assertIn(com.diag.hackamore.Event.TIME, event)
                self.assertEquals(event[com.diag.hackamore.Event.TIME], "1234567890.02")
                self.assertNotIn(com.diag.hackamore.Event.END, event)
                self.assertIn("TwoOne", event)
                self.assertEquals(event["TwoOne"], "BetaAlpha")
                self.assertIn("TwoTwo", event)
                self.assertEquals(event["TwoTwo"], "BetaBeta")
            elif events == 3:
                self.assertEquals(len(event), 5)
                self.assertIn(com.diag.hackamore.Event.SOURCE, event)
                self.assertEquals(event[com.diag.hackamore.Event.SOURCE], "PBX")
                self.assertIn(com.diag.hackamore.Event.TIME, event)
                self.assertEquals(event[com.diag.hackamore.Event.TIME], "1234567890.03")
                self.assertNotIn(com.diag.hackamore.Event.END, event)
                self.assertIn("ThreeOne", event)
                self.assertEquals(event["ThreeOne"], "GammaAlpha")
                self.assertIn("ThreeTwo", event)
                self.assertEquals(event["ThreeTwo"], "GammaBeta")
                self.assertIn("ThreeThree", event)
                self.assertEquals(event["ThreeThree"], "GammaGamma")
            elif events == 4:
                self.assertEquals(len(event), 3)
                self.assertIn(com.diag.hackamore.Event.SOURCE, event)
                self.assertEquals(event[com.diag.hackamore.Event.SOURCE], "PBX")
                self.assertIn(com.diag.hackamore.Event.TIME, event)
                self.assertEquals(event[com.diag.hackamore.Event.TIME], "1234567890.04")
                self.assertNotIn(com.diag.hackamore.Event.END, event)
                self.assertIn("FourOne", event)
                self.assertEquals(event["FourOne"], "DeltaAlpha")
            elif events == 5:
                self.assertEquals(len(event), 3)
                self.assertIn(com.diag.hackamore.Event.SOURCE, event)
                self.assertEquals(event[com.diag.hackamore.Event.SOURCE], "PBX")
                self.assertIn(com.diag.hackamore.Event.TIME, event)
                self.assertEquals(event[com.diag.hackamore.Event.TIME], "1234567890.05")
                self.assertIn(com.diag.hackamore.Event.END, event)
                self.assertEquals(event[com.diag.hackamore.Event.END], str(5))
            else:
                self.assertTrue(0 < events < 6)
            if com.diag.hackamore.Event.END in event:
                eof = True
        self.assertEquals(events, 5)
        self.assertTrue(source.close())
 
    def test035Service(self):
        name = self.id()
        multiplex = com.diag.hackamore.Multiplex.Multiplex()
        self.assertIsNotNone(multiplex)
        self.assertFalse(multiplex.active())
        source = com.diag.hackamore.Trace.Trace(name, TRACELET)
        self.assertFalse(multiplex.active())
        self.assertTrue(source.open())
        self.assertFalse(multiplex.active())
        multiplex.register(source)
        self.assertTrue(multiplex.active())
        events = 0
        eof = False
        while not eof:
            multiplex.service()
            event = source.get(multiplex)
            if event == None:
                continue
            events = events + 1
            self.assertTrue(event)
            if events == 1:
                self.assertEquals(len(event), 5)
                self.assertIn(com.diag.hackamore.Event.SOURCE, event)
                self.assertEquals(event[com.diag.hackamore.Event.SOURCE], "PBX")
                self.assertIn(com.diag.hackamore.Event.TIME, event)
                self.assertEquals(event[com.diag.hackamore.Event.TIME], "1234567890.01")
                self.assertNotIn(com.diag.hackamore.Event.END, event)
                self.assertIn("OneOne", event)
                self.assertEquals(event["OneOne"], "AlphaAlpha")
                self.assertIn("OneTwo", event)
                self.assertEquals(event["OneTwo"], "AlphaBeta")
                self.assertIn("OneThree", event)
                self.assertEquals(event["OneThree"], "AlphaGamma")
            elif events == 2:
                self.assertEquals(len(event), 4)
                self.assertIn(com.diag.hackamore.Event.SOURCE, event)
                self.assertEquals(event[com.diag.hackamore.Event.SOURCE], "PBX")
                self.assertIn(com.diag.hackamore.Event.TIME, event)
                self.assertEquals(event[com.diag.hackamore.Event.TIME], "1234567890.02")
                self.assertNotIn(com.diag.hackamore.Event.END, event)
                self.assertIn("TwoOne", event)
                self.assertEquals(event["TwoOne"], "BetaAlpha")
                self.assertIn("TwoTwo", event)
                self.assertEquals(event["TwoTwo"], "BetaBeta")
            elif events == 3:
                self.assertEquals(len(event), 5)
                self.assertIn(com.diag.hackamore.Event.SOURCE, event)
                self.assertEquals(event[com.diag.hackamore.Event.SOURCE], "PBX")
                self.assertIn(com.diag.hackamore.Event.TIME, event)
                self.assertEquals(event[com.diag.hackamore.Event.TIME], "1234567890.03")
                self.assertNotIn(com.diag.hackamore.Event.END, event)
                self.assertIn("ThreeOne", event)
                self.assertEquals(event["ThreeOne"], "GammaAlpha")
                self.assertIn("ThreeTwo", event)
                self.assertEquals(event["ThreeTwo"], "GammaBeta")
                self.assertIn("ThreeThree", event)
                self.assertEquals(event["ThreeThree"], "GammaGamma")
            elif events == 4:
                self.assertEquals(len(event), 3)
                self.assertIn(com.diag.hackamore.Event.SOURCE, event)
                self.assertEquals(event[com.diag.hackamore.Event.SOURCE], "PBX")
                self.assertEquals(event[com.diag.hackamore.Event.TIME], "1234567890.04")
                self.assertTrue(event[com.diag.hackamore.Event.TIME])
                self.assertNotIn(com.diag.hackamore.Event.END, event)
                self.assertIn("FourOne", event)
                self.assertEquals(event["FourOne"], "DeltaAlpha")
            elif events == 5:
                self.assertEquals(len(event), 3)
                self.assertIn(com.diag.hackamore.Event.SOURCE, event)
                self.assertEquals(event[com.diag.hackamore.Event.SOURCE], "PBX")
                self.assertIn(com.diag.hackamore.Event.TIME, event)
                self.assertEquals(event[com.diag.hackamore.Event.TIME], "1234567890.05")
                self.assertIn(com.diag.hackamore.Event.END, event)
                self.assertEquals(event[com.diag.hackamore.Event.END], str(5))
            else:
                self.assertTrue(0 < events < 6)
            if com.diag.hackamore.Event.END in event:
                eof = True
        self.assertEquals(events, 5)
        self.assertTrue(source.close())

    def test040Multiplexer(self):
        name = self.id()
        multiplex = com.diag.hackamore.Multiplex.Multiplex()
        self.assertIsNotNone(multiplex)
        multiplex.deregister()
        self.assertFalse(multiplex.active())
        source = com.diag.hackamore.Trace.Trace(name, TRACELET)
        self.assertFalse(multiplex.active())
        self.assertTrue(source.open())
        self.assertFalse(multiplex.active())
        multiplex.register(source)
        self.assertTrue(multiplex.active())
        events = 0
        for message in multiplex.multiplex():
            self.assertIsNotNone(message)
            event = message.event
            self.assertIsNotNone(event)
            events = events + 1
            self.assertTrue(event)
            if events == 1:
                self.assertEquals(len(event), 5)
                self.assertIn(com.diag.hackamore.Event.SOURCE, event)
                self.assertEquals(event[com.diag.hackamore.Event.SOURCE], "PBX")
                self.assertIn(com.diag.hackamore.Event.TIME, event)
                self.assertEquals(event[com.diag.hackamore.Event.TIME], "1234567890.01")
                self.assertNotIn(com.diag.hackamore.Event.END, event)
                self.assertIn("OneOne", event)
                self.assertEquals(event["OneOne"], "AlphaAlpha")
                self.assertIn("OneTwo", event)
                self.assertEquals(event["OneTwo"], "AlphaBeta")
                self.assertIn("OneThree", event)
                self.assertEquals(event["OneThree"], "AlphaGamma")
            elif events == 2:
                self.assertEquals(len(event), 4)
                self.assertIn(com.diag.hackamore.Event.SOURCE, event)
                self.assertEquals(event[com.diag.hackamore.Event.SOURCE], "PBX")
                self.assertIn(com.diag.hackamore.Event.TIME, event)
                self.assertEquals(event[com.diag.hackamore.Event.TIME], "1234567890.02")
                self.assertNotIn(com.diag.hackamore.Event.END, event)
                self.assertIn("TwoOne", event)
                self.assertEquals(event["TwoOne"], "BetaAlpha")
                self.assertIn("TwoTwo", event)
                self.assertEquals(event["TwoTwo"], "BetaBeta")
            elif events == 3:
                self.assertEquals(len(event), 5)
                self.assertIn(com.diag.hackamore.Event.SOURCE, event)
                self.assertEquals(event[com.diag.hackamore.Event.SOURCE], "PBX")
                self.assertIn(com.diag.hackamore.Event.TIME, event)
                self.assertEquals(event[com.diag.hackamore.Event.TIME], "1234567890.03")
                self.assertNotIn(com.diag.hackamore.Event.END, event)
                self.assertIn("ThreeOne", event)
                self.assertEquals(event["ThreeOne"], "GammaAlpha")
                self.assertIn("ThreeTwo", event)
                self.assertEquals(event["ThreeTwo"], "GammaBeta")
                self.assertIn("ThreeThree", event)
                self.assertEquals(event["ThreeThree"], "GammaGamma")
            elif events == 4:
                self.assertEquals(len(event), 3)
                self.assertIn(com.diag.hackamore.Event.SOURCE, event)
                self.assertEquals(event[com.diag.hackamore.Event.SOURCE], "PBX")
                self.assertIn(com.diag.hackamore.Event.TIME, event)
                self.assertEquals(event[com.diag.hackamore.Event.TIME], "1234567890.04")
                self.assertNotIn(com.diag.hackamore.Event.END, event)
                self.assertIn("FourOne", event)
                self.assertEquals(event["FourOne"], "DeltaAlpha")
            elif events == 5:
                self.assertEquals(len(event), 3)
                self.assertIn(com.diag.hackamore.Event.SOURCE, event)
                self.assertEquals(event[com.diag.hackamore.Event.SOURCE], "PBX")
                self.assertIn(com.diag.hackamore.Event.TIME, event)
                self.assertEquals(event[com.diag.hackamore.Event.TIME], "1234567890.05")
                self.assertIn(com.diag.hackamore.Event.END, event)
                self.assertEquals(event[com.diag.hackamore.Event.END], str(5))
            else:
                self.assertTrue(0 < events < 6)
            if com.diag.hackamore.Event.END in event:
                break
        self.assertEquals(events, 5)
        self.assertTrue(source.close())
 
    def test050Trace(self):
        name = self.id()
        events = 0
        multiplex = com.diag.hackamore.Multiplex.Multiplex()
        self.assertIsNotNone(multiplex)
        multiplex.deregister()
        self.assertFalse(multiplex.active())
        source = com.diag.hackamore.Trace.Trace(name, TRACE)
        self.assertFalse(multiplex.active())
        self.assertTrue(source.open())
        self.assertFalse(multiplex.active())
        multiplex.register(source)
        self.assertTrue(multiplex.active())
        for message in multiplex.multiplex():
            self.assertIsNotNone(message)
            event = message.event
            self.assertIsNotNone(event)
            events = events + 1
            self.assertTrue(event)
            self.assertIn(com.diag.hackamore.Event.SOURCE, event)
            self.assertTrue(event[com.diag.hackamore.Event.SOURCE])
            self.assertIn(com.diag.hackamore.Event.TIME, event)
            self.assertTrue(event[com.diag.hackamore.Event.TIME])
            if com.diag.hackamore.Event.END in event:
                self.assertEquals(event[com.diag.hackamore.Event.END], str(events))
                break
        self.assertEquals(events, 358) # 1 response, 356 events, 1 end
        self.assertTrue(source.close())
        self.assertTrue(multiplex.active())
        self.assertTrue(source.open())
        self.assertTrue(multiplex.active())
        for message in multiplex.multiplex():
            self.assertIsNotNone(message)
            event = message.event
            self.assertIsNotNone(event)
            events = events + 1
            self.assertTrue(event)
            self.assertIn(com.diag.hackamore.Event.SOURCE, event)
            self.assertTrue(event[com.diag.hackamore.Event.SOURCE])
            self.assertIn(com.diag.hackamore.Event.TIME, event)
            self.assertTrue(event[com.diag.hackamore.Event.TIME])
            if com.diag.hackamore.Event.END in event:
                self.assertEquals(event[com.diag.hackamore.Event.END], str(events))
                break
        self.assertEquals(events, 716) # 1 response, 356 events, 1 end
        self.assertTrue(source.close())
 
    def test050WriteRead(self):
        name = self.id()
        source = com.diag.hackamore.File.File(name, TYPESCRIPT)
        self.assertIsNotNone(source)
        inputs = [ ]
        inputs.append(source)
        outputs = [ ]
        self.assertEquals(len(inputs), 1)
        self.assertEquals(len(outputs), 0)
        fd, trace = tempfile.mkstemp()
        tracer = open(trace, "w")
        self.assertIsNotNone(tracer)
        multiplex = com.diag.hackamore.Multiplex.Multiplex()
        model = com.diag.hackamore.Model.Model()
        view = com.diag.hackamore.View.View(model)
        manifold = com.diag.hackamore.Manifold.Manifold(model, view, tracer = tracer)
        controller = com.diag.hackamore.Controller.Controller(multiplex, manifold)
        controller.loop(inputs, outputs)
        self.assertEquals(len(inputs), 0)
        self.assertEquals(len(outputs), 1)
        tracer.close()
        events = 0
        multiplex = com.diag.hackamore.Multiplex.Multiplex()
        self.assertIsNotNone(multiplex)
        multiplex.deregister()
        self.assertFalse(multiplex.active())
        source = com.diag.hackamore.Trace.Trace(name, trace)
        self.assertFalse(multiplex.active())
        self.assertTrue(source.open())
        self.assertFalse(multiplex.active())
        multiplex.register(source)
        self.assertTrue(multiplex.active())
        for message in multiplex.multiplex():
            self.assertIsNotNone(message)
            event = message.event
            self.assertIsNotNone(event)
            events = events + 1
            self.assertTrue(event)
            self.assertIn(com.diag.hackamore.Event.SOURCE, event)
            self.assertTrue(event[com.diag.hackamore.Event.SOURCE])
            self.assertIn(com.diag.hackamore.Event.TIME, event)
            self.assertTrue(event[com.diag.hackamore.Event.TIME])
            if com.diag.hackamore.Event.END in event:
                break
        self.assertEquals(events, 235) # 234 manifold events, 1 manifold end
        self.assertTrue(source.close())
        os.remove(trace)

if __name__ == "__main__":
    unittest.main()
