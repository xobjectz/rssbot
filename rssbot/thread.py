# This file is placed in the Public Domain.
# pylint: disable=R0902,W0718


"threads"


import queue
import threading
import time


from .errors import later
from .event  import Event
from .utils  import named


rpr = object.__repr__


class Thread(threading.Thread):

    "Thread"

    def __init__(self, func, thrname, *args, daemon=True, **kwargs):
        super().__init__(None, self.run, thrname, (), {}, daemon=daemon)
        self._result   = None
        self.name      = thrname or (func and named(func)) or named(self).split(".")[-1]
        self.out       = None
        self.queue     = queue.Queue()
        self.sleep     = None
        self.starttime = time.time()
        self.throttle  = 0.002
        if func:
            self.queue.put_nowait((func, args))

    def __iter__(self):
        return self

    def __next__(self):
        yield from dir(self)

    def size(self):
        "return qsize"
        return self.queue.qsize()

    def join(self, timeout=1.0):
        "join this thread."
        super().join(timeout)
        return self._result

    def run(self):
        "run this thread's payload."
        func, args = self.queue.get()
        time.sleep(self.throttle)
        try:
            self._result = func(*args)
        except Exception as ex:
            later(ex)
            for arg in args:
                if isinstance(arg, Event):
                    arg.ready()


def launch(func, *args, **kwargs):
    "launch a thread."
    nme = kwargs.get("name", named(func))
    thread = Thread(func, nme, *args, **kwargs)
    thread.start()
    return thread


def __dir__():
    return (
        'Thread',
        'launch'
    )
