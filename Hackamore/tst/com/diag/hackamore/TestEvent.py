"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import unittest
import logging

import com.diag.hackamore.Logger
import com.diag.hackamore.Event

class Test(unittest.TestCase):

    def setUp(self):
        com.diag.hackamore.Logger.logger().setLevel(logging.WARNING)

    def tearDown(self):
        pass
    
    def test010Construction(self):
        name = self.id()
        actual = None
        message = com.diag.hackamore.Event.Event(actual)
        self.assertIsNotNone(message)
        expected = message.event
        self.assertIsNone(expected)
        self.assertIsNotNone(message.logger)
        actual = { }
        message = com.diag.hackamore.Event.Event(actual)
        self.assertIsNotNone(message)
        expected = message.event
        self.assertIsNotNone(expected)
        self.assertEquals(len(expected), 0)
        self.assertIsNotNone(message.logger)
        actual = { }
        actual[name] = name
        message = com.diag.hackamore.Event.Event(actual)
        self.assertIsNotNone(message)
        expected = message.event
        self.assertIsNotNone(expected)
        self.assertEquals(len(expected), 1)
        self.assertIn(name, expected)
        self.assertEquals(expected[name], name)
        self.assertIsNotNone(message.logger)

if __name__ == "__main__":
    unittest.main()
