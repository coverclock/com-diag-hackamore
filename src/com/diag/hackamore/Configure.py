"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import Logger
import Credentials
import Socket

def servers(logger = None):
    logger = Logger.logger() if logger == None else logger
    sources = [ ]
    prefix = "COM_DIAG_HACKAMORE_"
    index = 1
    while True:
        names = prefix + "NAME" + str(index)
        name = Credentials.credential(names)
        if name == None:
            break
        servers = prefix + "SERVER" + str(index)
        server = Credentials.credential(servers, Socket.HOST)
        ports = prefix + "PORT" + str(index)
        port = int(Credentials.credential(ports, str(Socket.PORT)))
        usernames = prefix + "USERNAME" + str(index)
        username = Credentials.credential(usernames, "")
        secrets = prefix + "SECRET" + str(index)
        secret = Credentials.credential(secrets, "")
        logger.info("Configure.servers: %s=\"%s\" %s=\"%s\" %s=%d %s=\"%s\" %s=\"%s\"", names, name, servers, server, ports, port, usernames, username, secrets, secret)
        source = Socket.Socket(name, username, secret, server, port)
        sources.append(source)
        index = index + 1
    return sources
