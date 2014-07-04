"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import unittest
import logging

import com.diag.hackamore.Logger
import com.diag.hackamore.Event
import com.diag.hackamore.Source

class Test(unittest.TestCase):

    def setUp(self):
        com.diag.hackamore.Logger.logger().setLevel(logging.DEBUG)

    def tearDown(self):
        pass

    def test010Construction(self):
        name = self.id()
        source = com.diag.hackamore.Source.Source(name)
        self.assertIsNotNone(source)
        self.assertIsNotNone(source.pbx)
        self.assertEquals(source.pbx, name)
        self.assertEqual(len(source.event), 1)
        self.assertTrue(com.diag.hackamore.Event.SOURCE in source.event)
        self.assertTrue(source.open())
        self.assertFalse(source.open())
        self.assertIsNone(source.read())
        self.assertFalse(source.write(""))
        self.assertIsNone(source.get())
        self.assertFalse(source.put((())))
        self.assertTrue(source.close())
        self.assertFalse(source.close())
        self.assertTrue(source.open())
        self.assertFalse(source.open())
        self.assertIsNone(source.read())
        self.assertFalse(source.write(""))
        self.assertIsNone(source.get())
        self.assertFalse(source.put((())))
        self.assertTrue(source.close())
        self.assertFalse(source.close())

if __name__ == "__main__":
    unittest.main()
