"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import unittest
import logging

import com.diag.hackamore.Logger
import com.diag.hackamore.File
import com.diag.hackamore.Machine

from Parameters import TYPESCRIPT

class Test(unittest.TestCase):

    def setUp(self):
        com.diag.hackamore.Logger.logger().setLevel(logging.DEBUG)

    def tearDown(self):
        pass

    def test010Machine(self):
        name = self.id()
        com.diag.hackamore.Multiplex.deregister()
        source = com.diag.hackamore.File.File(name, TYPESCRIPT)
        self.assertIsNotNone(source)
        self.assertTrue(source.open())
        self.assertIn(source.name, com.diag.hackamore.Multiplex.sources)
        self.assertTrue(com.diag.hackamore.Multiplex.active())
        com.diag.hackamore.Machine.machine()

if __name__ == "__main__":
    unittest.main()