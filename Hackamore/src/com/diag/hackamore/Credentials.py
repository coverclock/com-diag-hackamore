"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import os

DOTFILE=".com_diag_hackamore"

def credential(keyword):
    try:
        return os.environ[keyword].strip()
    except Exception:
        pass
    try:
        for line in open(os.environ["HOME"] + "/" + DOTFILE):
            pair = line.split("=", 1)
            if pair[0].strip() == keyword:
                return pair[1].strip()
    except Exception:
        pass
    return ""

SERVER = credential("COM_DIAG_HACKAMORE_SERVER")
USERNAME = credential("COM_DIAG_HACKAMORE_USERNAME")
SECRET = credential("COM_DIAG_HACKAMORE_SECRET")
