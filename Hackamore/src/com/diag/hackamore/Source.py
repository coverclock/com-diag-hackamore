"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import logging
import time

import Logger
import Event

USERNAME = ""
SECRET = ""

class Source:
    """
    Source describes an object that provides a complete AMI message in the form
    of a dictionary. AMI messages are in the form of successive keywords
    ("Event:") and values ("Dial") which map conveniently to the dictionary
    container. Source relies on a derived class to deliver complete lines
    from the message with the terminating carriage return and line feed
    stripped off.
    """

    #
    # CTOR/DTOR
    #

    def __init__(self, pbx, username = USERNAME, secret = SECRET, logger = None):
        """
        Constructor.
        @param pbx is the name of the source.
        @param username is the username used to authenticate with the source.
        @param secret is the secret used to authenticate with the source.
        @param logger is an optional Logger used to log messages.
        """
        self.logger = Logger.logger() if logger == None else logger
        self.pbx = pbx
        self.username = username
        self.secret = secret
        self.count = 0
        self.state = False
        self.authenticated = False
        self.event = { }
        self.initialize()
        
    def __del__(self):
        if self.state:
            self.close()

    def __repr__(self):
        return "Source(" + str(self.pbx) + ")"
    
    #
    # PROTECTED
    #

    def read(self, multiplexing = False):
        """
        Return a single line from the underlying platform input/output resource.
        If no line is yet available, return None.
        @param multiplexing is True if the caller is handling calling service().
        @return a single line from the resource or None.
        """
        pass

    def write(self, line):
        """
        Emit a single line to the underlying platform input/output resource.
        The line provided by the caller is assumed not to be terminated by a
        carriage return and line feed. Those characters are added as the line
        is written to the resource. Passing an empty line causes just the two
        terminating chararacters to be written, which signals the end of the
        AMI request in progress.
        @param line is the unterminated line to be written.
        @return True if successful or none if not.
        """
        pass
    
    def authentication(self, event):
        """
        Examine a dictionary containing a complete AMI message to see if it is
        an authentication or deauthentication response. If so, process it.
        @param event is a dictionary containing a complete AMI message.
        """
        if not Event.RESPONSE in event:
            pass
        elif not self.authenticated:
            if event[Event.RESPONSE] != Event.SUCCESS:
                pass
            elif not Event.MESSAGE in event:
                pass
            elif event[Event.MESSAGE] != Event.AUTHENTICATEDACCEPTED:
                pass
            else:
                self.authenticated = True
                self.logger.info("Source:authentication: AUTHENTICATED. %s", str(self))
        else:
            if event[Event.RESPONSE] != Event.GOODBYE:
                pass
            else:
                self.authenticated = False
                self.logger.info("Source:authentication: DEAUTHENTICATED. %s", str(self))
                
    def initialize(self):
        """
        Do whatever initialization is necessary for the accumulated AMI message
        cached in this object when a new message is being started.
        """
        self.event[Event.SOURCE] = self.pbx          
    
    def finalize(self):
        """
        Do whatever finalization is necessary for the accumulated AMI message
        cached in this object when the message is being completed.
        """
        self.event[Event.TIME] = str(time.time())
        
    def terminate(self):
        """
        Do whatever termination is necessary for the accumulated AMI message
        cached in this object when the underlying platform input/output resource
        indicates that it is terminated (end of file, far end closed socket,
        etc.).
        """
        self.event[Event.END] = str(self.count)

    #
    # PUBLIC
    #

    def open(self):
        """
        Open the Source. This is generally overridden, and then called, by the
        derived class.
        @return true if successful, false otherwise.
        """
        result = False
        if not self.state:
            self.count = 0
            self.logger.info("Source.open: OPENED. %s", str(self))
            self.state = True
            self.authenticated = False
            result = True
        return result

    def close(self):
        """
        Close the Source. This is generally overridden, and then called, by the
        derived class.
        @return true if successful, false otherwise.
        """
        result = False
        if self.state:
            self.logger.info("Source.close: CLOSED. %s", str(self))
            self.state = False
            result = True
        return result

    def fileno(self):
        """
        Return a file number that can be used in the underlying platform with
        a select(2) system call. On Linux this is a file descriptor integer.
        On Windows it is a socket descriptor.
        @return a file number usable with the select(2) system call.
        """
        return -1
    
    def service(self):
        """
        Service the underlying platform input/output resource when the select(2)
        system call indicates that it requires servicing. This function has no
        return value. If the resource has provided a complete line from the
        AMI message, it will be made available by a subsequent read() function
        call.
        """
        pass

    def get(self, multiplex = None):
        """
        Return a complete AMI message in the form of a dictionary, or None
        if no such message is yet available.
        @param multiplexing is True if the caller is handling calling service().
        @return a complete AMI message or None.
        """
        event = None
        while event == None:
            try:
                line = self.read(multiplex)
            except Exception:
                self.count = self.count + 1
                self.terminate()
                self.finalize()
                event = self.event
                if self.logger.isEnabledFor(logging.DEBUG):
                    self.logger.debug("Source.get: GET: %s %s", str(self), str(event))
                if self.logger.isEnabledFor(logging.INFO):
                    self.logger.info("Source.get: END: %s %d", str(self), self.count)
                self.event = { }
                self.initialize()
            else:
                if line == None:
                    break
                elif not line:
                    self.count = self.count + 1
                    self.finalize()
                    event = self.event
                    if self.logger.isEnabledFor(logging.DEBUG):
                        self.logger.debug("Source.get: GET: %s %s", str(self), str(event))
                    self.authentication(event)
                    self.event = { }
                    self.initialize()
                else:
                    data = line.split(": ", 1)
                    if not data:
                        pass
                    elif len(data) == 1:
                        self.event[data[0]] = ""
                    else:
                        self.event[data[0]] = data[1]
            finally:
                pass
        #if event != None:
            #event[Event.TIME] = "DUMMY"
            #sorted(event, key=event.get)
        return event

    def put(self, request):
        """
        Emit a complete AMI message. The final empty line consisting of just
        a carriage return and line feed is generated automatically to signal the
        end of the message.
        @param request is the dictionary containing the message to be emitted.
        @return True if successful, False otherwise.
        """
        result = False
        for pair in request:
            line = pair[0] + ": " + pair[1]
            if not self.write(line):
                break
        else:
            result = True
        if not self.write(""):
            result = False
        return result

    def login(self):
        """
        Send an AMI message to request authentication. The message will contain
        the username and secret specified at construction.
        @return True is successfully sent, false otherwise.
        """
        return self.put( ( ("Action", "Login"), ("Username", str(self.username)), ("Secret", str(self.secret)) ) )

    def logout(self):
        """
        Send an AMI message to request deauthentication. For some Sources, like
        Sockets to actual Asterisk PBXes, this will cause the far end to close
        the Socket. For other Sources, like Files and Traces, this may have no
        effect.
        @return True is successfully sent, false otherwise.
        """
        return self.put( ( ("Action", "Logoff"), ) )
