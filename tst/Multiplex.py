"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import unittest
import logging

import com.diag.hackamore.File
import com.diag.hackamore.Multiplex

PATH = "./typescript.txt"

class Test(unittest.TestCase):

    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)

    def tearDown(self):
        pass

    def test1(self):
        name = "PBXMULTIPLEX1"
        source = com.diag.hackamore.File.File(name, PATH)
        source.open()
        events = 0
        while True:
            for event in com.diag.hackamore.Multiplex.multiplex():
                events = events + 1
                self.assertTrue(len(event) > 0)
                self.assertTrue(com.diag.hackamore.Source.SOURCE in event)
                if com.diag.hackamore.Source.END in event:
                    break
                self.assertTrue(com.diag.hackamore.Source.TIME in event)
                logging.debug(event)
        self.assertTrue(events == 358) # 1 response, 356 events, 1 end
        source.close()

if __name__ == "__main__":
    unittest.main()