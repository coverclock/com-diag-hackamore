"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
If you want to run any of the unit tests that execute against a live Asterisk
server, the unit test needs to know your server's hostname or IP address and the
username and secret that you administered in your

    /etc/asterisk/manager.conf

file. You can either define these in your environment as the values of the
variables
    
    COM_DIAG_HACKAMORE_SERVER,
    COM_DIAG_HACKAMORE_USERNAME, and
    COM_DIAG_HACKAMORE_SECRET
    
respectively, or, you can define them in a file in your home directory named

    .com_diag_hackamore

and the unit test will extract them from successive lines encoded in

    keyword=value
    
form. Note that this capability is not part of the unit test modules but part
of the Hackamore framework itself so that you can use this in your own Hackamore
application. If COM_DIAG_HACKAMORE_SERVER is not defined or is an empty string,
the unit tests which run against a live server will be bypassed.
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
