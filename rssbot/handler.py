# This file is placed in the Public Domain.


"handler"


import queue
import threading
import _thread


from .object import Default, Object
from .thread import launch


rpr = object.__repr__


class Handler:

    "Handler"

    def __init__(self):
        self.cbs      = Object()
        self.queue    = queue.Queue()
        self.stopped  = threading.Event()
        self.threaded = True

    def callback(self, evt):
        "call callback based on event type."
        func = getattr(self.cbs, evt.type, None)
        if not func:
            evt.ready()
            return
        evt._thr = launch(func, self, evt) # pylint: disable=W0212

    def loop(self):
        "proces events until interrupted."
        while not self.stopped.is_set():
            try:
                evt = self.poll()
                self.callback(evt)
            except (KeyboardInterrupt, EOFError):
                _thread.interrupt_main()

    def poll(self):
        "function to return event."
        return self.queue.get()

    def put(self, evt):
        "put event into the queue."
        self.queue.put_nowait(evt)

    def register(self, typ, cbs):
        "register callback for a type."
        setattr(self.cbs, typ, cbs)

    def start(self):
        "start the event loop."
        launch(self.loop)

    def stop(self):
        "stop the event loop."
        self.stopped.set()


class Event(Default): # pylint: disable=R0902

    "Event"

    def __init__(self):
        Default.__init__(self)
        self._thr    = None
        self._ready  = threading.Event()
        self.done    = False
        self.orig    = None
        self.result  = []
        self.txt     = ""
        self.type    = "event"

    def ready(self):
        "event is ready."
        self._ready.set()

    def reply(self, txt):
        "add text to the result"
        self.result.append(txt)

    def wait(self):
        "wait for event to be ready."
        if self._thr:
            self._thr.join()
        self._ready.wait()
        return self.result


def __dir__():
    return (
        'Event',
        'Handler'
    )
