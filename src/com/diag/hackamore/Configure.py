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
    Parse the .com_diag_hackamore file for the a list of serverkeyword in the form
    of keyword=value pairs with variable namekeyword COM_DIAG_HACKAMORE_NAMEn (the
    human-readable PBX name), COM_DIAG_HACKAMORE_SERVERn (the PBX IP address,
    host name, or domain name, which defaults to the local host),
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
        namekeyword = prefix + "NAME" + str(index)
        name = Credentials.credential(namekeyword)
        if name == None:
            break
        serverkeyword = prefix + "SERVER" + str(index)
        server = Credentials.credential(serverkeyword, Socket.HOST)
        portkeyword = prefix + "PORT" + str(index)
        port = int(Credentials.credential(portkeyword, str(Socket.PORT)))
        usernamekeyword = prefix + "USERNAME" + str(index)
        username = Credentials.credential(usernamekeyword, "")
        secretkeyword = prefix + "SECRET" + str(index)
        secret = Credentials.credential(secretkeyword, "")
        logger.info("Configure.serverkeyword: %s=\"%s\" %s=\"%s\" %s=%d %s=\"%s\" %s=\"%s\"", namekeyword, name, serverkeyword, server, portkeyword, port, usernamekeyword, username, secretkeyword, secret)
        source = Socket.Socket(name, username, secret, server, port)
        sources.append(source)
        index = index + 1
    return sources
