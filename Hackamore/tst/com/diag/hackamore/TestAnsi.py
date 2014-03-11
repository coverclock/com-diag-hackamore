"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import unittest
import os
import curses.ascii
import sys

from com.diag.hackamore.stdio import printf

class Test(unittest.TestCase):

    def setUp(self):
        pass


    def tearDown(self):
        pass

    def testName(self):
        if "TERM" not in os.environ:
            printf("Bypassing test using ANSI escape sequences.\n")
            return
        printf("TERM=%s\n", os.environ["TERM"])
        printf("BEFORE\n")
        clear = chr(curses.ascii.ESC) + "[2J"
        home = chr(curses.ascii.ESC) + "[1;1H"
        sys.stdout.write(clear)
        sys.stdout.write(home)
        sys.stdout.flush()
        printf("AFTER\n")

if __name__ == "__main__":
    unittest.main()