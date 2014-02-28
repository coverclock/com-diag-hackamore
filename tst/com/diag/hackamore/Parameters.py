"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
These are unit test parameters, some of which are likely to be specific to a
particular installation. At the very least you will need to change SERVER,
USERNAME, and SECRET to match your network and what you have administered in
your /etc/asterisk/manager.conf file.
"""

SERVER = "192.168.1.220"
USERNAME = "admin"
SECRET = "85t3r15k"

import com.diag.hackamore.Socket

PORT = com.diag.hackamore.Socket.PORT
LOCALHOST = "127.0.0.1"
SAMPLE = "sample.txt"
TYPESCRIPT = "typescript.txt"
