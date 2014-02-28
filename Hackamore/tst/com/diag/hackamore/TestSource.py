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
import com.diag.hackamore.Multiplex

class Test(unittest.TestCase):

    def setUp(self):
        com.diag.hackamore.Logger.logger().setLevel(logging.DEBUG)

    def tearDown(self):
        pass

    def test010Construction(self):
        name = self.id()
        self.assertFalse(name in com.diag.hackamore.Multiplex.sources)
        source = com.diag.hackamore.Source.Source(name)
        self.assertIsNotNone(source)
        self.assertIsNotNone(source.name)
        self.assertEquals(source.name, name)
        self.assertNotIn(source.name, com.diag.hackamore.Multiplex.sources)
        self.assertEqual(len(source.event), 1)
        self.assertTrue(com.diag.hackamore.Event.SOURCE in source.event)
        self.assertTrue(source.open())
        self.assertFalse(source.open())
        self.assertNotIn(source.name, com.diag.hackamore.Multiplex.sources)
        self.assertIsNone(source.read())
        self.assertFalse(source.write(""))
        self.assertIsNone(source.get())
        self.assertFalse(source.put((())))
        self.assertTrue(source.close())
        self.assertFalse(source.close())
        self.assertNotIn(source.name, com.diag.hackamore.Multiplex.sources)
        self.assertTrue(source.open())
        self.assertFalse(source.open())
        self.assertNotIn(source.name, com.diag.hackamore.Multiplex.sources)
        self.assertIsNone(source.read())
        self.assertFalse(source.write(""))
        self.assertIsNone(source.get())
        self.assertFalse(source.put((())))
        self.assertTrue(source.close())
        self.assertFalse(source.close())
        self.assertNotIn(source.name, com.diag.hackamore.Multiplex.sources)

if __name__ == "__main__":
    unittest.main()
