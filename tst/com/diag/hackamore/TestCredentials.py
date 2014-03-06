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
        self.assertIsNotNone(com.diag.hackamore.Credentials.SERVER)
        self.assertIsNotNone(com.diag.hackamore.Credentials.USERNAME)
        self.assertIsNotNone(com.diag.hackamore.Credentials.SERVER)

if __name__ == "__main__":
    unittest.main()