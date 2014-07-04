"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import unittest
import os
import tempfile

import com.diag.hackamore.Credentials

class Test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test010Sanity(self):
        name = self.id()
        self.assertIsNotNone(com.diag.hackamore.Credentials.credential("HOME"))
        self.assertNotEqual(com.diag.hackamore.Credentials.credential("HOME"), "")
        self.assertIsNotNone(com.diag.hackamore.Credentials.credential("PATH"))
        self.assertNotEqual(com.diag.hackamore.Credentials.credential("PATH"), "")
        keyword = name + "_FOO"
        value = name + "_BAR"
        self.assertIsNone(com.diag.hackamore.Credentials.credential(keyword))
        self.assertIsNotNone(com.diag.hackamore.Credentials.credential(keyword, value))
        self.assertEquals(com.diag.hackamore.Credentials.credential(keyword, value), value)
        value = name + "_WTF"
        os.environ[keyword] = value
        self.assertIsNotNone(com.diag.hackamore.Credentials.credential(keyword))
        self.assertEquals(com.diag.hackamore.Credentials.credential(keyword), value)
        keyword = name + "_CAT"
        value = name + "_LOL"
        fd, path = tempfile.mkstemp()
        dot = open(path, "w")
        dot.write("# Test!\n")
        dot.write(" " + keyword + " = " + value + " # Cheezburger?\n")
        dot.flush()
        dot.close()  
        self.assertIsNotNone(com.diag.hackamore.Credentials.credentialfile(path, keyword))
        self.assertEquals(com.diag.hackamore.Credentials.credentialfile(path, keyword), value)
        dot = open(path, "w")
        dot.write(" # Test!\n")
        dot.write(" " + keyword + " =\n")
        dot.flush()
        dot.close()  
        self.assertIsNotNone(com.diag.hackamore.Credentials.credentialfile(path, keyword))
        self.assertEquals(com.diag.hackamore.Credentials.credentialfile(path, keyword), "")
        os.remove(path)

if __name__ == "__main__":
    unittest.main()