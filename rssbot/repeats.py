# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0718,E0402


"threads"


import threading
import time


from .objects import Object
from .threads import launch


def __dir__():
    return (
       'Repeater',
    )


__all__ = __dir__()


class Timer(Object):

    def __init__(self, sleep, func, *args, thrname=None):
        Object.__init__(self)
        self.args  = args
        self.func  = func
        self.sleep = sleep
        self.name  = thrname or str(self.func).split()[2]
        self.state = {}
        self.timer = None

    def run(self):
        self.state["latest"] = time.time()
        launch(self.func, *self.args)

    def start(self):
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

    def stop(self):
        if self.timer:
            self.timer.cancel()


class Repeater(Timer):

    def run(self):
        thr = launch(self.start)
        super().run()
        return thr
