"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import unittest
import logging

import com.diag.hackamore.Source
import com.diag.hackamore.Multiplex

class Test(unittest.TestCase):

    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)

    def tearDown(self):
        pass

    def test010(self):
        name = "PBXSOURCE010"
        self.assertFalse(name in com.diag.hackamore.Multiplex.sources)
        source = com.diag.hackamore.Source.Source(name)
        self.assertTrue(source != None)
        self.assertTrue(source.name != None)
        self.assertTrue(source.name == name)
        self.assertFalse(source.name in com.diag.hackamore.Multiplex.sources)
        self.assertTrue(len(source.event) == 1)
        self.assertTrue(com.diag.hackamore.Source.SOURCE in source.event)
        source.open()
        self.assertFalse(source.name in com.diag.hackamore.Multiplex.sources)
        self.assertTrue(source.read() == None)
        self.assertFalse(source.write(""))
        self.assertTrue(source.get() == None)
        self.assertFalse(source.put((())))
        source.close()
        self.assertFalse(source.name in com.diag.hackamore.Multiplex.sources)

if __name__ == "__main__":
    unittest.main()
