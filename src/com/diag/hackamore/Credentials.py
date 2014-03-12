"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import os

DOTFILE=".com_diag_hackamore"

def credentialfile(path, keyword, default = None):
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
    return default

def credentialhome(filename, keyword, default = None):
    return credentialfile(os.environ["HOME"] + "/" + filename, keyword, default)    

def credential(keyword, default = None):
    return credentialhome(DOTFILE, keyword, default = default)
