"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import unittest
import logging

from com.diag.hackamore.End import End

def succeeder():
    pass
    
def failer():
    exception = End()
    raise exception

class Test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test010(self):
        didtry = False
        didelse = False
        didfinally = False
        try:
            didtry = True
            succeeder()
        except Exception:
            self.fail()
        else:
            didelse = True
        finally:
            didfinally = True
        self.assertTrue(didtry)
        self.assertTrue(didelse)
        self.assertTrue(didfinally)

    def test020(self):
        didtry = False
        didexcept = False
        didfinally = False
        try:
            didtry = True
            failer()
        except Exception as exception:
            self.assertTrue(isinstance(exception, End))
            didexcept = True
        else:
            self.fail()
        finally:
            didfinally = True
        self.assertTrue(didtry)
        self.assertTrue(didexcept)
        self.assertTrue(didfinally)

if __name__ == "__main__":
    unittest.main()
