"""
@file
Copyright 2014 by the Digital Aggregates Corporation, Colorado, USA.
Licensed under the terms in the README.txt file.
"""

import unittest
import logging

import com.diag.hackamore.Logger
import com.diag.hackamore.Event
import com.diag.hackamore.File
import com.diag.hackamore.Multiplex

from Parameters import TYPESCRIPT

class Test(unittest.TestCase):

    def setUp(self):
        com.diag.hackamore.Logger.logger().setLevel(logging.WARNING)

    def tearDown(self):
        pass

    def test010Filter(self):
        name = self.id()
        com.diag.hackamore.Multiplex.deregister()
        source = com.diag.hackamore.File.File(name, TYPESCRIPT)
        source.open()
        for event in com.diag.hackamore.Multiplex.multiplex():
            if com.diag.hackamore.Event.END in event:
                break
            elif com.diag.hackamore.Event.EVENT in event:
                if event[com.diag.hackamore.Event.EVENT] == com.diag.hackamore.Event.DIAL:
                    if not com.diag.hackamore.Event.SUBEVENT in event:
                        pass
                    elif event[com.diag.hackamore.Event.SUBEVENT] != com.diag.hackamore.Event.BEGIN:
                        pass
                    elif not com.diag.hackamore.Event.CHANNEL in event:
                        pass
                    elif not com.diag.hackamore.Event.DESTINATION in event:
                        pass
                    elif not com.diag.hackamore.Event.DESTUNIQUEID in event:
                        pass
                    elif not com.diag.hackamore.Event.UNIQUEIDUC in event:
                        pass
                    else:
                        print("DIAL=" + str(event))
                elif event[com.diag.hackamore.Event.EVENT] == com.diag.hackamore.Event.HANGUP:
                    if not com.diag.hackamore.Event.CHANNEL in event:
                        pass
                    elif not com.diag.hackamore.Event.UNIQUEIDLC in event:
                        pass
                    else:
                        print("HANGUP=" + str(event))
                elif event[com.diag.hackamore.Event.EVENT] == com.diag.hackamore.Event.LOCALBRIDGE:
                    if not com.diag.hackamore.Event.CHANNEL1 in event:
                        pass
                    elif not com.diag.hackamore.Event.CHANNEL2 in event:
                        pass
                    elif not com.diag.hackamore.Event.UNIQUEID1 in event:
                        pass
                    elif not com.diag.hackamore.Event.UNIQUEID2 in event:
                        pass
                    else:
                        print("LOCALBRIDGE=" + str(event))
                elif event[com.diag.hackamore.Event.EVENT] == com.diag.hackamore.Event.NEWCHANNEL:
                    if not com.diag.hackamore.Event.CHANNEL in event:
                        pass
                    elif not com.diag.hackamore.Event.CHANNELSTATE in event:
                        pass
                    elif not com.diag.hackamore.Event.CHANNELSTATEDESC in event:
                        pass
                    elif not com.diag.hackamore.Event.UNIQUEIDLC in event:
                        pass
                    else:
                        print("NEWCHANNEL=" + str(event))
                elif event[com.diag.hackamore.Event.EVENT] == com.diag.hackamore.Event.NEWSTATE:
                    if not com.diag.hackamore.Event.CHANNEL in event:
                        pass
                    elif not com.diag.hackamore.Event.CHANNELSTATE in event:
                        pass
                    elif not com.diag.hackamore.Event.CHANNELSTATEDESC in event:
                        pass
                    elif not com.diag.hackamore.Event.UNIQUEIDLC in event:
                        pass
                    else:
                        print("NEWSTATE=" + str(event))
                elif event[com.diag.hackamore.Event.EVENT] == com.diag.hackamore.Event.RENAME:
                    if not com.diag.hackamore.Event.CHANNEL in event:
                        pass
                    elif not com.diag.hackamore.Event.NEWNAME in event:
                        pass
                    elif not com.diag.hackamore.Event.UNIQUEIDLC in event:
                        pass
                    else:
                        print("RENAME=" + str(event))
                elif event[com.diag.hackamore.Event.EVENT] == com.diag.hackamore.Event.VARSET:
                    if not com.diag.hackamore.Event.VARIABLE in event:
                        pass
                    elif not com.diag.hackamore.Event.VALUE in event:
                        pass
                    else:
                        if not event[com.diag.hackamore.Event.VARIABLE] == com.diag.hackamore.Event.SIPCALLID:
                            pass
                        else:
                            print("SIPCALLID=" + str(event))
                else:
                    pass
            else:
                pass
        source.close()

if __name__ == "__main__":
    unittest.main()
