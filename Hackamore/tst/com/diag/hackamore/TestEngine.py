"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import unittest
import logging

import com.diag.hackamore.Logger
import com.diag.hackamore.File
import com.diag.hackamore.Engine

from Parameters import TYPESCRIPT

class Test(unittest.TestCase):

    def setUp(self):
        com.diag.hackamore.Logger.logger().setLevel(logging.DEBUG)

    def tearDown(self):
        pass

    def test010Rinse(self):
        name = self.id()
        com.diag.hackamore.Multiplex.deregister()
        source = com.diag.hackamore.File.File(name, TYPESCRIPT)
        self.assertIsNotNone(source)
        inputs = [ ]
        inputs.append(source)
        outputs = [ ]
        self.assertEquals(len(inputs), 1)
        self.assertEquals(len(outputs), 0)
        com.diag.hackamore.Engine.engine(inputs, outputs)
        self.assertEquals(len(inputs), 0)
        self.assertEquals(len(outputs), 1)

    def test020Repeat(self):
        name = self.id()
        com.diag.hackamore.Multiplex.deregister()
        source = com.diag.hackamore.File.File(name, TYPESCRIPT)
        self.assertIsNotNone(source)
        inputs = [ ]
        inputs.append(source)
        self.assertEquals(len(inputs), 1)
        com.diag.hackamore.Engine.engine(inputs, inputs)
        self.assertEquals(len(inputs), 1)

if __name__ == "__main__":
    unittest.main()
