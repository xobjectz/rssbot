# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0212,E0402


"handler"


import queue
import threading
import _thread


from .brokers import Broker
from .objects import Object
from .threads import launch


def __dir__():
    return (
        'Handler',
   ) 


__all__ = __dir__()


class Handler(Object):

    def __init__(self):
        Object.__init__(self)
        self.cbs      = Object()
        self.queue    = queue.Queue()
        self.stopped  = threading.Event()
        self.threaded = True
        Broker.add(self)

    def callback(self, evt):
        func = getattr(self.cbs, evt.type, None)
        if not func:
            evt.ready()
            return
        if self.threaded:
            evt._thr = launch(func, evt)
        else:
            func(evt)
            evt.ready()

    def loop(self):
        while not self.stopped.is_set():
            try:
                evt = self.poll()
                self.callback(evt)
            except (KeyboardInterrupt, EOFError):
                _thread.interrupt_main()

    def poll(self):
        return self.queue.get()

    def put(self, evt):
        self.queue.put_nowait(evt)

    def register(self, typ, cbs):
        setattr(self.cbs, typ, cbs)

    def start(self):
        launch(self.loop)

    def stop(self):
        self.stopped.set()
