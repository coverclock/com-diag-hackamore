"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import unittest

import com.diag.hackamore.Credentials

class Test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test010Sanity(self):
        self.assertIsNotNone(com.diag.hackamore.Credentials.credential("HOME"))
        self.assertNotEqual(com.diag.hackamore.Credentials.credential("HOME"), "")
        self.assertIsNotNone(com.diag.hackamore.Credentials.credential("PATH"))
        self.assertNotEqual(com.diag.hackamore.Credentials.credential("PATH"), "")
        self.assertIsNone(com.diag.hackamore.Credentials.credential("COM_DIAG_HACKAMORE_FOO"))
        self.assertIsNotNone(com.diag.hackamore.Credentials.credential("COM_DIAG_HACKAMORE_FOO", "COM_DIAG_HACKAMORE_BAR"))
        self.assertEquals(com.diag.hackamore.Credentials.credential("COM_DIAG_HACKAMORE_FOO", "COM_DIAG_HACKAMORE_BAR"), "COM_DIAG_HACKAMORE_BAR")

if __name__ == "__main__":
    unittest.main()