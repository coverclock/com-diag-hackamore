"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import com.diag.hackamore.Socket
import com.diag.hackamore.Credentials

LOCALHOST = "127.0.0.1"
SAMPLE = "sample.txt"
TYPESCRIPT = "typescript.txt"
TRACE = "trace.txt"
TRACELET = "tracelet.txt"

SERVER = com.diag.hackamore.Credentials.credential("COM_DIAG_HACKAMORE_SERVER", "")
PORT = com.diag.hackamore.Credentials.credential("COM_DIAG_HACKAMORE_PORT", str(com.diag.hackamore.Socket.PORT))
USERNAME = com.diag.hackamore.Credentials.credential("COM_DIAG_HACKAMORE_USERNAME", "")
SECRET = com.diag.hackamore.Credentials.credential("COM_DIAG_HACKAMORE_SECRET", "")
