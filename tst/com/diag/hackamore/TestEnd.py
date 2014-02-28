"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import unittest
import logging

import com.diag.hackamore.Logger
import com.diag.hackamore.End

def succeeder():
    pass
    
def failer():
    exception = com.diag.hackamore.End.End()
    raise exception

class Test(unittest.TestCase):

    def setUp(self):
        com.diag.hackamore.Logger.logger().setLevel(logging.DEBUG)

    def tearDown(self):
        pass

    def test010NoException(self):
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

    def test020Exception(self):
        didtry = False
        didexcept = False
        didfinally = False
        try:
            didtry = True
            failer()
        except Exception as exception:
            self.assertTrue(isinstance(exception, com.diag.hackamore.End.End))
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
