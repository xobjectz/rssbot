# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0718,E0402


"threads"


import queue
import threading
import time
import types


from .excepts import Error
from .objects import Object


def __dir__():
    return (
       'Repeater',
       'Thread',
       'Timer',
       'launch',
       'name',
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

    def join(self, timeout=None) -> type:
        super().join(timeout)
        return self._result

    def run(self) -> None:
        func, args = self.queue.get()
        try:
            self._result = func(*args)
        except Exception as exc:
            Error.add(exc)
            if args and "ready" in dir(args[0]):
                args[0].ready()


class Timer(Object):

    def __init__(self, sleep, func, *args, thrname=None):
        Object.__init__(self)
        self.args  = args
        self.func  = func
        self.sleep = sleep
        self.name  = thrname or str(self.func).split()[2]
        self.state = {}
        self.timer = None

    def run(self) -> None:
        self.state["latest"] = time.time()
        launch(self.func, *self.args)

    def start(self) -> None:
        timer = threading.Timer(self.sleep, self.run)
        timer.name   = self.name
        timer.daemon = True
        timer.sleep  = self.sleep
        timer.state  = self.state
        timer.func   = self.func
        timer.state["starttime"] = time.time()
        timer.state["latest"]    = time.time()
        timer.start()
        self.timer   = timer

    def stop(self) -> None:
        if self.timer:
            self.timer.cancel()


class Repeater(Timer):

    def run(self) -> Thread:
        thr = launch(self.start)
        super().run()
        return thr


def launch(func, *args, **kwargs):
    nme = kwargs.get("name", name(func))
    thread = Thread(func, nme, *args, **kwargs)
    thread.start()
    return thread


def name(obj) -> str:
    typ = type(obj)
    if isinstance(typ, types.ModuleType):
        return obj.__name__
    if '__self__' in dir(obj):
        return f'{obj.__self__.__class__.__name__}.{obj.__name__}'
    if '__class__' in dir(obj) and '__name__' in dir(obj):
        return f'{obj.__class__.__name__}.{obj.__name__}'
    if '__class__' in dir(obj):
        return f"{obj.__class__.__module__}.{obj.__class__.__name__}"
    if '__name__' in dir(obj):
        return f'{obj.__class__.__name__}.{obj.__name__}'
    return None
