# -*- test-case-name: twisted.python.logger.test.test_global -*-
# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

"""
Global log publisher.
"""

import sys

from twisted.python.logger._buffer import RingBufferLogObserver
from twisted.python.logger._observer import LogPublisher

class LogStartupBuffer(object):
    """
    Such a publisher is useful, for example, to capture any log messages
    emitted during process startup that may be emitted before a file log
    observer may be initialized.
    """

    def __init__(self, publisher, errorStream):
        self._temporaryObserver = RingBufferLogObserver()
        self._publisher = publisher
        self._publisher.addObserver(self._temporaryObserver)


    def beginLoggingTo(self, observers):
        """
        Begin logging to the given set of observers.

        @param observers: The observers to register.
        @type observers: iterable of L{ILogObserver}s
        """
        if self._temporaryObserver is None:
            raise AssertionError("beginLoggingTo() may only be called once.")
        for observer in observers:
            self._publisher.addObserver(observer)
        self._publisher.removeObserver(self._temporaryObserver)
        self._temporaryObserver.replayTo(self._publisher)
        self._temporaryObserver = None
        self._publisher = None



globalLogPublisher = LogPublisher()
startupBuffer = LogStartupBuffer(globalLogPublisher, sys.stderr)
