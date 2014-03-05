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
import com.diag.hackamore.End

from Parameters import SAMPLE
from Parameters import TYPESCRIPT

class Test(unittest.TestCase):

    def setUp(self):
        com.diag.hackamore.Logger.logger().setLevel(logging.DEBUG)

    def tearDown(self):
        pass

    def test010Construction(self):
        name = self.id()
        source = com.diag.hackamore.File.File(name, SAMPLE)
        self.assertIsNotNone(source)
        self.assertIsNotNone(source.name)
        self.assertEquals(source.name, name)
        self.assertIsNotNone(source.path)
        self.assertEquals(source.path, SAMPLE)
        self.assertIsNone(source.file)
        self.assertTrue(source.open())
        self.assertFalse(source.open())
        self.assertIsNotNone(source.file)
        self.assertTrue(source.close())
        self.assertFalse(source.close())
        self.assertIsNone(source.file)
        self.assertFalse(source.open())
        self.assertIsNone(source.file)

    def test020Read(self):
        name = self.id()
        source = com.diag.hackamore.File.File(name, SAMPLE)
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
                    self.assertEquals(line, "")
                elif lines == 5:
                    self.assertEquals(line, "TwoOne: BetaAlpha")
                elif lines == 6:
                    self.assertEquals(line, "TwoTwo: BetaBeta")
                elif lines == 7:
                    self.assertEquals(line, "")
                elif lines == 8:
                    self.assertEquals(line, "ThreeOne: GammaAlpha")
                elif lines == 9:
                    self.assertEquals(line, "ThreeTwo: GammaBeta")
                elif lines == 10:
                    self.assertEquals(line, "ThreeThree: GammaGamma")
                elif lines == 11:
                    self.assertEquals(line, "")
                elif lines == 12:
                    self.assertEquals(line, "FourOne: DeltaAlpha")
                elif lines == 13:
                    self.assertEquals(line, "")
                else:
                    self.assertTrue(0 < lines < 14)
            finally:
                pass
        self.assertTrue(lines == 13)
        self.assertTrue(source.close())
 
    def test030Get(self):
        name = self.id()
        source = com.diag.hackamore.File.File(name, SAMPLE)
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
                self.assertEquals(event[com.diag.hackamore.Event.SOURCE], name)
                self.assertIn(com.diag.hackamore.Event.TIME, event)
                self.assertTrue(event[com.diag.hackamore.Event.TIME])
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
                self.assertEquals(event[com.diag.hackamore.Event.SOURCE], name)
                self.assertIn(com.diag.hackamore.Event.TIME, event)
                self.assertTrue(event[com.diag.hackamore.Event.TIME])
                self.assertNotIn(com.diag.hackamore.Event.END, event)
                self.assertIn("TwoOne", event)
                self.assertEquals(event["TwoOne"], "BetaAlpha")
                self.assertIn("TwoTwo", event)
                self.assertEquals(event["TwoTwo"], "BetaBeta")
            elif events == 3:
                self.assertEquals(len(event), 5)
                self.assertIn(com.diag.hackamore.Event.SOURCE, event)
                self.assertEquals(event[com.diag.hackamore.Event.SOURCE], name)
                self.assertIn(com.diag.hackamore.Event.TIME, event)
                self.assertTrue(event[com.diag.hackamore.Event.TIME])
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
                self.assertEquals(event[com.diag.hackamore.Event.SOURCE], name)
                self.assertIn(com.diag.hackamore.Event.TIME, event)
                self.assertTrue(event[com.diag.hackamore.Event.TIME])
                self.assertNotIn(com.diag.hackamore.Event.END, event)
                self.assertIn("FourOne", event)
                self.assertEquals(event["FourOne"], "DeltaAlpha")
            elif events == 5:
                self.assertEquals(len(event), 3)
                self.assertIn(com.diag.hackamore.Event.SOURCE, event)
                self.assertEquals(event[com.diag.hackamore.Event.SOURCE], name)
                self.assertIn(com.diag.hackamore.Event.TIME, event)
                self.assertTrue(event[com.diag.hackamore.Event.TIME])
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
        source = com.diag.hackamore.File.File(name, SAMPLE)
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
                self.assertEquals(event[com.diag.hackamore.Event.SOURCE], name)
                self.assertIn(com.diag.hackamore.Event.TIME, event)
                self.assertTrue(event[com.diag.hackamore.Event.TIME])
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
                self.assertEquals(event[com.diag.hackamore.Event.SOURCE], name)
                self.assertIn(com.diag.hackamore.Event.TIME, event)
                self.assertTrue(event[com.diag.hackamore.Event.TIME])
                self.assertNotIn(com.diag.hackamore.Event.END, event)
                self.assertIn("TwoOne", event)
                self.assertEquals(event["TwoOne"], "BetaAlpha")
                self.assertIn("TwoTwo", event)
                self.assertEquals(event["TwoTwo"], "BetaBeta")
            elif events == 3:
                self.assertEquals(len(event), 5)
                self.assertIn(com.diag.hackamore.Event.SOURCE, event)
                self.assertEquals(event[com.diag.hackamore.Event.SOURCE], name)
                self.assertIn(com.diag.hackamore.Event.TIME, event)
                self.assertTrue(event[com.diag.hackamore.Event.TIME])
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
                self.assertEquals(event[com.diag.hackamore.Event.SOURCE], name)
                self.assertIn(com.diag.hackamore.Event.TIME, event)
                self.assertTrue(event[com.diag.hackamore.Event.TIME])
                self.assertNotIn(com.diag.hackamore.Event.END, event)
                self.assertIn("FourOne", event)
                self.assertEquals(event["FourOne"], "DeltaAlpha")
            elif events == 5:
                self.assertEquals(len(event), 3)
                self.assertIn(com.diag.hackamore.Event.SOURCE, event)
                self.assertEquals(event[com.diag.hackamore.Event.SOURCE], name)
                self.assertIn(com.diag.hackamore.Event.TIME, event)
                self.assertTrue(event[com.diag.hackamore.Event.TIME])
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
        source = com.diag.hackamore.File.File(name, SAMPLE)
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
                self.assertEquals(event[com.diag.hackamore.Event.SOURCE], name)
                self.assertIn(com.diag.hackamore.Event.TIME, event)
                self.assertTrue(event[com.diag.hackamore.Event.TIME])
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
                self.assertEquals(event[com.diag.hackamore.Event.SOURCE], name)
                self.assertIn(com.diag.hackamore.Event.TIME, event)
                self.assertTrue(event[com.diag.hackamore.Event.TIME])
                self.assertNotIn(com.diag.hackamore.Event.END, event)
                self.assertIn("TwoOne", event)
                self.assertEquals(event["TwoOne"], "BetaAlpha")
                self.assertIn("TwoTwo", event)
                self.assertEquals(event["TwoTwo"], "BetaBeta")
            elif events == 3:
                self.assertEquals(len(event), 5)
                self.assertIn(com.diag.hackamore.Event.SOURCE, event)
                self.assertEquals(event[com.diag.hackamore.Event.SOURCE], name)
                self.assertIn(com.diag.hackamore.Event.TIME, event)
                self.assertTrue(event[com.diag.hackamore.Event.TIME])
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
                self.assertEquals(event[com.diag.hackamore.Event.SOURCE], name)
                self.assertIn(com.diag.hackamore.Event.TIME, event)
                self.assertTrue(event[com.diag.hackamore.Event.TIME])
                self.assertNotIn(com.diag.hackamore.Event.END, event)
                self.assertIn("FourOne", event)
                self.assertEquals(event["FourOne"], "DeltaAlpha")
            elif events == 5:
                self.assertEquals(len(event), 3)
                self.assertIn(com.diag.hackamore.Event.SOURCE, event)
                self.assertEquals(event[com.diag.hackamore.Event.SOURCE], name)
                self.assertIn(com.diag.hackamore.Event.TIME, event)
                self.assertTrue(event[com.diag.hackamore.Event.TIME])
                self.assertIn(com.diag.hackamore.Event.END, event)
                self.assertEquals(event[com.diag.hackamore.Event.END], str(5))
            else:
                self.assertTrue(0 < events < 6)
            if com.diag.hackamore.Event.END in event:
                break
        self.assertEquals(events, 5)
        self.assertTrue(source.close())
 
    def test050Typescript(self):
        name = self.id()
        multiplex = com.diag.hackamore.Multiplex.Multiplex()
        self.assertIsNotNone(multiplex)
        multiplex.deregister()
        self.assertFalse(multiplex.active())
        source = com.diag.hackamore.File.File(name, TYPESCRIPT)
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
            self.assertIn(com.diag.hackamore.Event.SOURCE, event)
            self.assertEquals(event[com.diag.hackamore.Event.SOURCE], name)
            self.assertIn(com.diag.hackamore.Event.TIME, event)
            self.assertTrue(event[com.diag.hackamore.Event.TIME])
            if com.diag.hackamore.Event.END in event:
                self.assertEquals(event[com.diag.hackamore.Event.END], str(events))
                break
        self.assertEquals(events, 358) # 1 response, 356 events, 1 end
        self.assertTrue(source.close())

if __name__ == "__main__":
    unittest.main()
