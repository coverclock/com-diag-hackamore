"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import os

DOTFILE=".com_diag_hackamore"

def credentialfile(path, keyword):
    try:
        return os.environ[keyword].strip()
    except Exception:
        pass
    try:
        for line in open(path):
            pair = line.split("=", 1)
            if pair[0].strip() == keyword:
                return pair[1].strip()
    except Exception:
        pass
    return ""

def credentialhome(path, keyword):
    return credentialfile(os.environ["HOME"] + "/" + path, keyword)    

def credential(keyword):
    return credentialhome(DOTFILE, keyword)

COM_DIAG_HACKAMORE_SERVER = "COM_DIAG_HACKAMORE_SERVER"
COM_DIAG_HACKAMORE_USERNAME = "COM_DIAG_HACKAMORE_USERNAME"
COM_DIAG_HACKAMORE_SECRET = "COM_DIAG_HACKAMORE_SECRET"

SERVER = credential(COM_DIAG_HACKAMORE_SERVER)
USERNAME = credential(COM_DIAG_HACKAMORE_USERNAME)
SECRET = credential(COM_DIAG_HACKAMORE_SECRET)
