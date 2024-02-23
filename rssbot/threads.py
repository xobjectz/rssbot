# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0718,E0402


"threads"


import queue
import threading
import time


from .excepts import Error
from .utility import name


def __dir__():
    return (
       'Thread',
       'launch'
    )


__all__ = __dir__()


class Thread(threading.Thread):

    def __init__(self, func, thrname, *args, daemon=True, **kwargs):
        super().__init__(None, self.run, thrname, (), {}, daemon=daemon)
        self._result   = None
        self.name      = thrname or name(func)
        self.queue     = queue.Queue()
        self.sleep     = None
        self.starttime = time.time()
        self.queue.put_nowait((func, args))

    def __iter__(self):
        return self

    def __next__(self):
        for k in dir(self):
            yield k

    def join(self, timeout=None):
        super().join(timeout)
        return self._result

    def run(self):
        func, args = self.queue.get()
        try:
            self._result = func(*args)
        except Exception as exc:
            Error.add(exc)
            if args and "ready" in dir(args[0]):
                args[0].ready()


def launch(func, *args, **kwargs):
    nme = kwargs.get("name", name(func))
    thread = Thread(func, nme, *args, **kwargs)
    thread.start()
    return thread
