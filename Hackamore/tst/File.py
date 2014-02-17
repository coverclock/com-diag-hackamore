"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import unittest

import com.diag.hackamore.File
import com.diag.hackamore.Multiplex

PATH = "./tst/typescript.txt"

class Test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    def testOne(self):
        self.assertFalse(open(PATH, "r") == None)

    def testTwo(self):
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

if __name__ == "__main__":
    unittest.main()
