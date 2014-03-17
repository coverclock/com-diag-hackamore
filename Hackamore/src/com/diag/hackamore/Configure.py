"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import Logger
import Credentials
import Socket

def servers(logger = None):
    """
    Parse the .com_diag_hackamore file for the a list of servers in the form
    of keyword=value pairs with variable names COM_DIAG_HACKAMORE_NAMEn (the
    human-readable PBX name), COM_DIAG_HACKAMORE_SERVERn (the PBX IP address,
    host name, or domain name, which defaults ot the local host),
    COM_DIAG_HACKAMORE_PORTn (the AMI port number which defaults to the standard
    AMI port), COM_DIAG_HACKAMORE_USERNAMEn (the authentication user name from
    /etc/asterisk/manager.conf), and COM_DIAG_HACKAMORE_SECRETn (the
    authentication secret or password from /etc/asterisk_manager.conf), where
    "n" starts with "1" and increments for successive PBXes.
    @return a list of Sources each of which is an unopened Socket.
    """
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
