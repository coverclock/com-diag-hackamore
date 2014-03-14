"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import time

import com.diag.hackamore.Logger
import com.diag.hackamore.Credentials
import com.diag.hackamore.Socket
import com.diag.hackamore.ModelStandard
import com.diag.hackamore.ViewCurses
import com.diag.hackamore.Controller

def main():
    logger = com.diag.hackamore.Logger.logger()
    sources = [ ]
    prefix = "COM_DIAG_HACKAMORE_"
    index = 1
    while True:
        names = prefix + "NAME" + str(index)
        name = com.diag.hackamore.Credentials.credential(names)
        if name == None:
            break
        servers = prefix + "SERVER" + str(index)
        server = com.diag.hackamore.Credentials.credential(servers, com.diag.hackamore.Socket.HOST)
        ports = prefix + "PORT" + str(index)
        port = int(com.diag.hackamore.Credentials.credential(ports, str(com.diag.hackamore.Socket.PORT)))
        usernames = prefix + "USERNAME" + str(index)
        username = com.diag.hackamore.Credentials.credential(usernames, "")
        secrets = prefix + "SECRET" + str(index)
        secret = com.diag.hackamore.Credentials.credential(secrets, "")
        logger.info("Main.main: %s=\"%s\" %s=\"%s\" %s=\"%s\" %s=\"%s\"", names, name, servers, server, usernames, username, secrets, secret)
        source = com.diag.hackamore.Socket.Socket(name, username, secret, server, port)
        sources.append(source)
        index = index + 1
    model = com.diag.hackamore.ModelStandard.ModelStandard()
    view = com.diag.hackamore.ViewCurses.ViewCurses(model)
    controller = com.diag.hackamore.Controller.Controller(model, view)
    logger.info("Main.main: STARTING.")
    while sources:
        controller.loop(sources, sources)
        time.sleep(2.0)
        logger.info("Main.main: RESTARTING.")
    logger.info("Main.main: STOPPING.")

if __name__ == "__main__":
    main()
