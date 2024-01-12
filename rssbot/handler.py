# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0212,E0402


"""event handler

This event handler uses callbacks to react to events put to the handler.
Every callback gets run in it's own thread just to escape the "it must not
block" problem async coding delivers. It does deferred exception handling to
not have the main loop exiting on an raised exception and uses a bus (called
 fleet) to do the output to.

"""


import queue
import threading
import _thread


from .brokers import Fleet
from .objects import Default, Object
from .threads import launch


def __dir__():
    return (
        'Event',
        'Handler'
   ) 


__all__ = __dir__()


class Handler(Object):

    "event handler"

    def __init__(self):
        Object.__init__(self)
        self.cbs      = Object()
        self.queue    = queue.Queue()
        self.stopped  = threading.Event()

    def callback(self, evt) -> None:
        "run function based on event type."
        func = getattr(self.cbs, evt.type, None)
        if not func:
            evt.ready()
            return
        evt._thr = launch(func, evt)
 
    def loop(self) -> None:
        "poll for event, run callback loop." 
        while not self.stopped.is_set():
            try:
                self.callback(self.poll())
            except (KeyboardInterrupt, EOFError):
                _thread.interrupt_main()

    def poll(self):
        "poll the queue for an event."
        return self.queue.get()

    def put(self, evt) -> None:
        "put and event on the queue."
        self.queue.put_nowait(evt)

    def register(self, typ, cbs) -> None:
        "register function as callback."
        setattr(self.cbs, typ, cbs)

    def start(self) -> None:
        "start event handler loop."
        launch(self.loop)

    def stop(self) -> None:
        "stop event handler loop."
        self.stopped.set()


class Event(Default):

    "event to handle."

    def __init__(self):
        Default.__init__(self)
        self._ready  = threading.Event()
        self._thr    = None
        self.done    = False
        self.orig    = None
        self.result  = []
        self.txt     = ""

    def ready(self):
        "flag as ready."
        self._ready.set()

    def reply(self, txt) -> None:
        "add to result list."
        self.result.append(txt)

    def show(self) -> None:
        "print result."
        for txt in self.result:
            bot = Fleet.byorig(self.orig) or Fleet.first()
            if bot:
                bot.say(self.channel, txt)

    def wait(self):
        "wait until event is finished."
        if self._thr:
            self._thr.join()
        self._ready.wait()
        return self.result
