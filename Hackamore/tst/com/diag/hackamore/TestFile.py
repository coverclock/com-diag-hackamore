"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import unittest
import logging

import com.diag.hackamore.Logger
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
        com.diag.hackamore.Multiplex.deregister()
        self.assertFalse(name in com.diag.hackamore.Multiplex.sources)
        source = com.diag.hackamore.File.File(name, SAMPLE)
        self.assertTrue(source != None)
        self.assertTrue(source.name != None)
        self.assertTrue(source.name == name)
        self.assertTrue(source.path != None)
        self.assertTrue(source.path == SAMPLE)
        self.assertFalse(source.name in com.diag.hackamore.Multiplex.sources)
        self.assertTrue(source.file == None)
        self.assertTrue(source.open())
        self.assertFalse(source.open())
        self.assertFalse(source.file == None)
        self.assertTrue(source.name in com.diag.hackamore.Multiplex.sources)
        self.assertTrue(source.close())
        self.assertFalse(source.close())
        self.assertFalse(source.name in com.diag.hackamore.Multiplex.sources)
        self.assertTrue(source.file == None)
        self.assertFalse(source.open())
        self.assertFalse(source.name in com.diag.hackamore.Multiplex.sources)
        self.assertTrue(source.file == None)

    def test020Read(self):
        name = self.id()
        com.diag.hackamore.Multiplex.deregister()
        self.assertFalse(name in com.diag.hackamore.Multiplex.sources)
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
                    self.assertTrue(line == "OneOne: AlphaAlpha")
                elif lines == 2:
                    self.assertTrue(line == "OneTwo: AlphaBeta")
                elif lines == 3:
                    self.assertTrue(line == "OneThree: AlphaGamma")
                elif lines == 4:
                    self.assertTrue(line == "")
                elif lines == 5:
                    self.assertTrue(line == "TwoOne: BetaAlpha")
                elif lines == 6:
                    self.assertTrue(line == "TwoTwo: BetaBeta")
                elif lines == 7:
                    self.assertTrue(line == "")
                elif lines == 8:
                    self.assertTrue(line == "ThreeOne: GammaAlpha")
                elif lines == 9:
                    self.assertTrue(line == "ThreeTwo: GammaBeta")
                elif lines == 10:
                    self.assertTrue(line == "ThreeThree: GammaGamma")
                elif lines == 11:
                    self.assertTrue(line == "")
                elif lines == 12:
                    self.assertTrue(line == "FourOne: DeltaAlpha")
                elif lines == 13:
                    self.assertTrue(line == "")
                else:
                    self.assertTrue(0 < lines < 14)
            finally:
                pass
        self.assertTrue(lines == 13)
        self.assertTrue(source.close())
 
    def test030Get(self):
        name = self.id()
        com.diag.hackamore.Multiplex.deregister()
        self.assertFalse(name in com.diag.hackamore.Multiplex.sources)
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
                self.assertTrue(len(event) == 5)
                self.assertTrue(com.diag.hackamore.Source.SOURCE in event)
                self.assertTrue(event[com.diag.hackamore.Source.SOURCE] == name)
                self.assertTrue(com.diag.hackamore.Source.TIME in event)
                self.assertTrue(event[com.diag.hackamore.Source.TIME])
                self.assertFalse(com.diag.hackamore.Source.END in event)
                self.assertTrue("OneOne" in event)
                self.assertTrue(event["OneOne"] == "AlphaAlpha")
                self.assertTrue("OneTwo" in event)
                self.assertTrue(event["OneTwo"] == "AlphaBeta")
                self.assertTrue("OneThree" in event)
                self.assertTrue(event["OneThree"] == "AlphaGamma")
            elif events == 2:
                self.assertTrue(len(event) == 4)
                self.assertTrue(com.diag.hackamore.Source.SOURCE in event)
                self.assertTrue(event[com.diag.hackamore.Source.SOURCE] == name)
                self.assertTrue(com.diag.hackamore.Source.TIME in event)
                self.assertTrue(event[com.diag.hackamore.Source.TIME])
                self.assertFalse(com.diag.hackamore.Source.END in event)
                self.assertTrue("TwoOne" in event)
                self.assertTrue(event["TwoOne"] == "BetaAlpha")
                self.assertTrue("TwoTwo" in event)
                self.assertTrue(event["TwoTwo"] == "BetaBeta")
            elif events == 3:
                self.assertTrue(len(event) == 5)
                self.assertTrue(com.diag.hackamore.Source.SOURCE in event)
                self.assertTrue(event[com.diag.hackamore.Source.SOURCE] == name)
                self.assertTrue(com.diag.hackamore.Source.TIME in event)
                self.assertTrue(event[com.diag.hackamore.Source.TIME])
                self.assertFalse(com.diag.hackamore.Source.END in event)
                self.assertTrue("ThreeOne" in event)
                self.assertTrue(event["ThreeOne"] == "GammaAlpha")
                self.assertTrue("ThreeTwo" in event)
                self.assertTrue(event["ThreeTwo"] == "GammaBeta")
                self.assertTrue("ThreeThree" in event)
                self.assertTrue(event["ThreeThree"] == "GammaGamma")
            elif events == 4:
                self.assertTrue(len(event) == 3)
                self.assertTrue(com.diag.hackamore.Source.SOURCE in event)
                self.assertTrue(event[com.diag.hackamore.Source.SOURCE] == name)
                self.assertTrue(com.diag.hackamore.Source.TIME in event)
                self.assertTrue(event[com.diag.hackamore.Source.TIME])
                self.assertFalse(com.diag.hackamore.Source.END in event)
                self.assertTrue("FourOne" in event)
                self.assertTrue(event["FourOne"] == "DeltaAlpha")
            elif events == 5:
                self.assertTrue(len(event) == 3)
                self.assertTrue(com.diag.hackamore.Source.SOURCE in event)
                self.assertTrue(event[com.diag.hackamore.Source.SOURCE] == name)
                self.assertTrue(com.diag.hackamore.Source.TIME in event)
                self.assertTrue(event[com.diag.hackamore.Source.TIME])
                self.assertTrue(com.diag.hackamore.Source.END in event)
                self.assertTrue(event[com.diag.hackamore.Source.END] == str(5))
            else:
                self.assertTrue(0 < events < 6)
            if com.diag.hackamore.Source.END in event:
                eof = True
        self.assertTrue(events == 5)
        self.assertTrue(source.close())

    def test040Multiplexer(self):
        name = self.id()
        com.diag.hackamore.Multiplex.deregister()
        self.assertFalse(name in com.diag.hackamore.Multiplex.sources)
        source = com.diag.hackamore.File.File(name, SAMPLE)
        self.assertTrue(source.open())
        events = 0
        for event in com.diag.hackamore.Multiplex.multiplex():
            self.assertFalse(event == None)
            events = events + 1
            self.assertTrue(event)
            if events == 1:
                self.assertTrue(len(event) == 5)
                self.assertTrue(com.diag.hackamore.Source.SOURCE in event)
                self.assertTrue(event[com.diag.hackamore.Source.SOURCE] == name)
                self.assertTrue(com.diag.hackamore.Source.TIME in event)
                self.assertTrue(event[com.diag.hackamore.Source.TIME])
                self.assertFalse(com.diag.hackamore.Source.END in event)
                self.assertTrue("OneOne" in event)
                self.assertTrue(event["OneOne"] == "AlphaAlpha")
                self.assertTrue("OneTwo" in event)
                self.assertTrue(event["OneTwo"] == "AlphaBeta")
                self.assertTrue("OneThree" in event)
                self.assertTrue(event["OneThree"] == "AlphaGamma")
            elif events == 2:
                self.assertTrue(len(event) == 4)
                self.assertTrue(com.diag.hackamore.Source.SOURCE in event)
                self.assertTrue(event[com.diag.hackamore.Source.SOURCE] == name)
                self.assertTrue(com.diag.hackamore.Source.TIME in event)
                self.assertTrue(event[com.diag.hackamore.Source.TIME])
                self.assertFalse(com.diag.hackamore.Source.END in event)
                self.assertTrue("TwoOne" in event)
                self.assertTrue(event["TwoOne"] == "BetaAlpha")
                self.assertTrue("TwoTwo" in event)
                self.assertTrue(event["TwoTwo"] == "BetaBeta")
            elif events == 3:
                self.assertTrue(len(event) == 5)
                self.assertTrue(com.diag.hackamore.Source.SOURCE in event)
                self.assertTrue(event[com.diag.hackamore.Source.SOURCE] == name)
                self.assertTrue(com.diag.hackamore.Source.TIME in event)
                self.assertTrue(event[com.diag.hackamore.Source.TIME])
                self.assertFalse(com.diag.hackamore.Source.END in event)
                self.assertTrue("ThreeOne" in event)
                self.assertTrue(event["ThreeOne"] == "GammaAlpha")
                self.assertTrue("ThreeTwo" in event)
                self.assertTrue(event["ThreeTwo"] == "GammaBeta")
                self.assertTrue("ThreeThree" in event)
                self.assertTrue(event["ThreeThree"] == "GammaGamma")
            elif events == 4:
                self.assertTrue(len(event) == 3)
                self.assertTrue(com.diag.hackamore.Source.SOURCE in event)
                self.assertTrue(event[com.diag.hackamore.Source.SOURCE] == name)
                self.assertTrue(com.diag.hackamore.Source.TIME in event)
                self.assertTrue(event[com.diag.hackamore.Source.TIME])
                self.assertFalse(com.diag.hackamore.Source.END in event)
                self.assertTrue("FourOne" in event)
                self.assertTrue(event["FourOne"] == "DeltaAlpha")
            elif events == 5:
                self.assertTrue(len(event) == 3)
                self.assertTrue(com.diag.hackamore.Source.SOURCE in event)
                self.assertTrue(event[com.diag.hackamore.Source.SOURCE] == name)
                self.assertTrue(com.diag.hackamore.Source.TIME in event)
                self.assertTrue(event[com.diag.hackamore.Source.TIME])
                self.assertTrue(com.diag.hackamore.Source.END in event)
                self.assertTrue(event[com.diag.hackamore.Source.END] == str(5))
            else:
                self.assertTrue(0 < events < 6)
            if com.diag.hackamore.Source.END in event:
                break
        self.assertTrue(events == 5)
        self.assertTrue(source.close())
 
    def test050Typescript(self):
        name = self.id()
        com.diag.hackamore.Multiplex.deregister()
        self.assertFalse(name in com.diag.hackamore.Multiplex.sources)
        source = com.diag.hackamore.File.File(name, TYPESCRIPT)
        self.assertTrue(source.open())
        events = 0
        for event in com.diag.hackamore.Multiplex.multiplex():
            self.assertFalse(event == None)
            events = events + 1
            self.assertTrue(event)
            self.assertTrue(com.diag.hackamore.Source.SOURCE in event)
            self.assertTrue(event[com.diag.hackamore.Source.SOURCE] == name)
            self.assertTrue(com.diag.hackamore.Source.TIME in event)
            self.assertTrue(event[com.diag.hackamore.Source.TIME])
            if com.diag.hackamore.Source.END in event:
                self.assertTrue(event[com.diag.hackamore.Source.END] == str(events))
                break
        self.assertTrue(events == 358) # 1 response, 356 events, 1 end
        self.assertTrue(source.close())

if __name__ == "__main__":
    unittest.main()
