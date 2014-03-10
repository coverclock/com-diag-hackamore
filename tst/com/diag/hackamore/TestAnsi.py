"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import unittest
import os
import curses.ascii
import sys

class Test(unittest.TestCase):

    def setUp(self):
        pass


    def tearDown(self):
        pass

    def testName(self):
        if "TERM" not in os.environ:
            print("Bypassing test using ANSI escape sequences.")
            return
        print "TERM=" + os.environ["TERM"]
        print "BEFORE"
        clear = chr(curses.ascii.ESC) + "[2J"
        home = chr(curses.ascii.ESC) + "[1;1H"
        sys.stdout.write(clear)
        sys.stdout.write(home)
        sys.stdout.flush()
        print "AFTER"

if __name__ == "__main__":
    unittest.main()