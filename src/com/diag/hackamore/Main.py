"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import threading

import com.diag.hackamore.Credentials
import com.diag.hackamore.Socket
import com.diag.hackamore.ModelStandard
import com.diag.hackamore.ModelSerializer
import com.diag.hackamore.ViewCurses
import com.diag.hackamore.ViewSerializer
import com.diag.hackamore.Controller

def main():
    sources = [ ]
    #####
    name1 = com.diag.hackamore.Credentials.credential(com.diag.hackamore.Credentials.COM_DIAG_HACKAMORE_SERVER)
    server1 = com.diag.hackamore.Credentials.credential(com.diag.hackamore.Credentials.COM_DIAG_HACKAMORE_SERVER)
    username1 = com.diag.hackamore.Credentials.credential(com.diag.hackamore.Credentials.COM_DIAG_HACKAMORE_USERNAME)
    secret1 = com.diag.hackamore.Credentials.credential(com.diag.hackamore.Credentials.COM_DIAG_HACKAMORE_SECRET)
    source1 = com.diag.hackamore.Socket.Socket(name1, username1, secret1, server1)
    sources.append(source1)
    #####
    model = com.diag.hackamore.ModelStandard.ModelStandard()
    mutex = threading.Condition()
    serializedmodel = com.diag.hackamore.ModelSerializer.ModelSerializer(model, mutex)
    view = com.diag.hackamore.ViewCurses.ViewCurses(model)
    serializedview = com.diag.hackamore.ViewSerializer.ViewSerializer(view, mutex)
    controller = com.diag.hackamore.Controller.Controller(serializedmodel, serializedview)
    controller.loop(sources, sources)

if __name__ == "__main__":
    main()
