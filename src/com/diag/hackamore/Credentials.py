"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import os

DOTFILE=".com_diag_hackamore"

def credentialfile(path, keyword, default = None):
    """
    Return the value of the specified keyword if it is found in the file on
    the specified path in the platform's file system.
    @return the value of the specified keyword or its default it not found.
    """
    if keyword in os.environ:
        return os.environ[keyword]
    else:
        try:
            for line in open(path):
                pair = line.split("#", 1)[0].split("=", 1)
                if pair[0].strip() == keyword:
                    if len(pair) > 1:
                        return pair[1].strip()
                    else:
                        return ""
        except Exception:
            pass
    return default

def credentialhome(filename, keyword, default = None):
    """
    Return the value of the specified keyword if it is found in the specified
    file in the caller's home directory.
    @return the value of the specified keyword or its default it not found.
    """
    return credentialfile(os.environ["HOME"] + "/" + filename, keyword, default)    

def credential(keyword, default = None):
    """
    Return the value of the specified keyword if it is found in the standard
    dot file (.com_diag_hackamore) in the caller's home directory.
    @return the value of the specified keyword or its default it not found.
    """
    return credentialhome(DOTFILE, keyword, default = default)
