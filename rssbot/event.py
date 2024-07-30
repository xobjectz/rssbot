# This file is placed in the Public Domain.
# pylint: disable=R0902


"event"


import threading


from .dft import Default


class Event(Default):

    "Event"

    def __init__(self):
        Default.__init__(self)
        self._ready  = threading.Event()
        self._thr    = None
        self.orig    = ""
        self.result  = []
        self.txt     = ""
        self.type    = "command"

    def ready(self):
        "event is ready."
        self._ready.set()

    def reply(self, txt):
        "add text to the result"
        self.result.append(txt)

    def wait(self, timeout=None):
        "wait for event to be ready."
        self._ready.wait(timeout)
        if self._thr:
            self._thr.join()
        return self.result


def __dir__():
    return (
        'Event',
    )
