"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import unittest
import logging

import com.diag.hackamore.File
import com.diag.hackamore.Multiplex

PATH = "./tst/typescript.txt"

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
            # print line[0:-2]
            lines = lines + 1
        self.assertTrue(lines == 3041)
        source.close()

if __name__ == "__main__":
    unittest.main()
