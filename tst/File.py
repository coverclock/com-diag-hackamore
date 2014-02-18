"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import unittest
import logging

import com.diag.hackamore.File
import com.diag.hackamore.Multiplex

SAMPLE = "./sample.txt"
TYPESCRIPT = "./typescript.txt"

class Test(unittest.TestCase):

    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)

    def tearDown(self):
        pass
     
    def test1(self):
        self.assertFalse(open(SAMPLE, "r") == None)
   
    def test2(self):
        self.assertFalse(open(TYPESCRIPT, "r") == None)

    def test3(self):
        name = "PBXFILE3"
        self.assertFalse(name in com.diag.hackamore.Multiplex.sources)
        source = com.diag.hackamore.File.File(name, TYPESCRIPT)
        self.assertTrue(source != None)
        self.assertTrue(source.name != None)
        self.assertTrue(source.name == name)
        self.assertTrue(source.path != None)
        self.assertTrue(source.path == TYPESCRIPT)
        self.assertFalse(source.name in com.diag.hackamore.Multiplex.sources)
        self.assertTrue(source.file == None)
        source.open()
        self.assertFalse(source.file == None)
        self.assertTrue(source.name in com.diag.hackamore.Multiplex.sources)
        source.close()
        self.assertFalse(source.name in com.diag.hackamore.Multiplex.sources)
        self.assertTrue(source.file == None)

    def test4(self):
        name = "PBXFILE4"
        source = com.diag.hackamore.File.File(name, TYPESCRIPT)
        source.open()
        lines = 0
        while True:
            line = source.read()
            self.assertFalse(line == None)
            if line == "":
                break
            self.assertFalse(len(line) < 2)
            self.assertTrue(line[-1] == '\n')
            self.assertTrue(line[-2] == '\r')
            logging.debug(line[0:-2])
            lines = lines + 1
        self.assertTrue(lines == 3034)
        source.close()

    def test5(self):
        name = "PBXFILE5"
        source = com.diag.hackamore.File.File(name, TYPESCRIPT)
        source.open()
        events = 0
        while True:
            event = source.get()
            if event == None:
                continue
            events = events + 1
            self.assertTrue(len(event) > 0)
            self.assertTrue(com.diag.hackamore.Source.SOURCE in event)
            if com.diag.hackamore.Source.END in event:
                break
            self.assertTrue(com.diag.hackamore.Source.TIME in event)
            logging.debug(event)
        self.assertTrue(events == 358) # 1 response, 356 events, 1 end
        source.close()

    def test6(self):
        name = "PBXFILE6"
        source = com.diag.hackamore.File.File(name, SAMPLE)
        source.open()        
        event = source.get()
        self.assertTrue(event == None)
        event = source.get()
        self.assertTrue(event == None)
        event = source.get()
        self.assertTrue(event == None)
        event = source.get()
        self.assertFalse(event == None)
        logging.debug(event)
        self.assertTrue(len(event) == 5)
        self.assertTrue(com.diag.hackamore.Source.SOURCE in event)
        self.assertTrue(event[com.diag.hackamore.Source.SOURCE] == name)
        self.assertTrue(com.diag.hackamore.Source.TIME in event)
        self.assertFalse(com.diag.hackamore.Source.END in event)
        self.assertTrue("OneOne" in event)
        self.assertTrue(event["OneOne"] == "AlphaAlpha")
        self.assertTrue("OneTwo" in event)
        self.assertTrue(event["OneTwo"] == "AlphaBeta")
        self.assertTrue("OneThree" in event)
        self.assertTrue(event["OneThree"] == "AlphaGamma")
        event = source.get()
        self.assertTrue(event == None)
        event = source.get()
        self.assertTrue(event == None)
        event = source.get()
        self.assertFalse(event == None)
        logging.debug(event)
        self.assertTrue(len(event) == 4)
        self.assertTrue(com.diag.hackamore.Source.SOURCE in event)
        self.assertTrue(event[com.diag.hackamore.Source.SOURCE] == name)
        self.assertTrue(com.diag.hackamore.Source.TIME in event)
        self.assertTrue(len(event[com.diag.hackamore.Source.TIME]) > 0)
        self.assertFalse(com.diag.hackamore.Source.END in event)
        self.assertTrue("TwoOne" in event)
        self.assertTrue(event["TwoOne"] == "BetaAlpha")
        self.assertTrue("TwoTwo" in event)
        self.assertTrue(event["TwoTwo"] == "BetaBeta")
        event = source.get()
        self.assertTrue(event == None)
        event = source.get()
        self.assertTrue(event == None)
        event = source.get()
        self.assertTrue(event == None)
        event = source.get()
        self.assertFalse(event == None)
        logging.debug(event)
        self.assertTrue(len(event) == 5)
        self.assertTrue(com.diag.hackamore.Source.SOURCE in event)
        self.assertTrue(event[com.diag.hackamore.Source.SOURCE] == name)
        self.assertTrue(com.diag.hackamore.Source.TIME in event)
        self.assertTrue(len(event[com.diag.hackamore.Source.TIME]) > 0)
        self.assertFalse(com.diag.hackamore.Source.END in event)
        self.assertTrue("ThreeOne" in event)
        self.assertTrue(event["ThreeOne"] == "GammaAlpha")
        self.assertTrue("ThreeTwo" in event)
        self.assertTrue(event["ThreeTwo"] == "GammaBeta")
        self.assertTrue("ThreeThree" in event)
        self.assertTrue(event["ThreeThree"] == "GammaGamma")
        event = source.get()
        self.assertTrue(event == None)
        event = source.get()
        self.assertFalse(event == None)
        logging.debug(event)
        self.assertTrue(len(event) == 3)
        self.assertTrue(com.diag.hackamore.Source.SOURCE in event)
        self.assertTrue(event[com.diag.hackamore.Source.SOURCE] == name)
        self.assertTrue(com.diag.hackamore.Source.TIME in event)
        self.assertTrue(len(event[com.diag.hackamore.Source.TIME]) > 0)
        self.assertFalse(com.diag.hackamore.Source.END in event)
        self.assertTrue("FourOne" in event)
        self.assertTrue(event["FourOne"] == "DeltaAlpha")
        event = source.get()
        self.assertFalse(event == None)
        logging.debug(event)
        self.assertTrue(len(event) == 2)
        self.assertTrue(com.diag.hackamore.Source.SOURCE in event)
        self.assertTrue(event[com.diag.hackamore.Source.SOURCE] == name)
        self.assertFalse(com.diag.hackamore.Source.TIME in event)
        self.assertTrue(com.diag.hackamore.Source.END in event)
        self.assertTrue(len(event[com.diag.hackamore.Source.END]) > 0)
        source.close()

    def test7(self):
        name = "PBXFILE7"
        source = com.diag.hackamore.File.File(name, TYPESCRIPT)
        source.open()
        events = 0
        while True:
            for event in com.diag.hackamore.Multiplex.multiplex():
                events = events + 1
                self.assertTrue(len(event) > 0)
                self.assertTrue(com.diag.hackamore.Source.SOURCE in event)
                if com.diag.hackamore.Source.END in event:
                    break
                self.assertTrue(com.diag.hackamore.Source.TIME in event)
                logging.debug(event)
        self.assertTrue(events == 358) # 1 response, 356 events, 1 end
        source.close()

if __name__ == "__main__":
    unittest.main()
