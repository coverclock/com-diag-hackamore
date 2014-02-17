"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import unittest
import logging

import com.diag.hackamore.File
import com.diag.hackamore.Multiplex

PATH = "./typescript.txt"

class Test(unittest.TestCase):

    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)

    def tearDown(self):
        pass
    
    def test1(self):
        self.assertFalse(open(PATH, "r") == None)

    def test2(self):
        name = "PBXFILE2"
        self.assertFalse(name in com.diag.hackamore.Multiplex.sources)
        source = com.diag.hackamore.File.File(name, PATH)
        self.assertTrue(source != None)
        self.assertTrue(source.name != None)
        self.assertTrue(source.name == name)
        self.assertTrue(source.path != None)
        self.assertTrue(source.path == PATH)
        self.assertFalse(source.name in com.diag.hackamore.Multiplex.sources)
        self.assertTrue(source.file == None)
        source.open()
        self.assertFalse(source.file == None)
        self.assertTrue(source.name in com.diag.hackamore.Multiplex.sources)
        source.close()
        self.assertFalse(source.name in com.diag.hackamore.Multiplex.sources)
        self.assertTrue(source.file == None)

    def test3(self):
        name = "PBXFILE3"
        source = com.diag.hackamore.File.File(name, PATH)
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

    def test4(self):
        name = "PBXFILE4"
        source = com.diag.hackamore.File.File(name, PATH)
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

if __name__ == "__main__":
    unittest.main()
