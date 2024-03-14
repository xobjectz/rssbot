# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0105,W0212,W0613,W0718,E0402,E1102


"hander"


import queue
import threading
import _thread


from .default import Default
from .objects import Object
from .runtime import Broker, Errors, parse_cmd
from .threads import launch


"classes"


class Event(Default):

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
        self._ready.set()

    def reply(self, txt):
        self.result.append(txt)

    def wait(self):
        if self._thr:
            self._thr.join()
        self._ready.wait()
        return self.result


class Handler:

    def __init__(self):
        self.cbs = Object()
        self.queue    = queue.Queue()
        self.stopped  = threading.Event()
        self.threaded = True

    def callback(self, evt):
        func = getattr(self.cbs, evt.type, None)
        if not func:
            evt.ready()
            return
        evt._thr = launch(func, evt)

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


class Client(Handler):

    cmds = Object()

    def __init__(self):
        Handler.__init__(self)
        self.register("command", self.command)
        Broker.add(self)

    @staticmethod
    def add(func):
        setattr(Client.cmds, func.__name__, func)

    def announce(self, txt):
        self.raw(txt)

    def command(self, evt):
        parse_cmd(evt)
        func = getattr(Client.cmds, evt.cmd, None)
        if func:
            try:
                func(evt)
            except Exception as exc:
                Errors.add(exc)
        self.show(evt)
        evt.ready()

    def raw(self, txt):
        pass

    def say(self, channel, txt):
        self.raw(txt)

    def show(self, evt):
        for txt in evt.result:
            self.say(evt.channel, txt)


"utilities"


def cmnd(txt, out):
    clt = Client()
    clt.raw = out
    evn = Event()
    evn.orig = object.__repr__(clt)
    evn.txt = txt
    clt.command(evn)
    evn.wait()
    return evn


"interface"


def __dir__():
    return (
        'Event',
        'Handler',
        'Client',
        'cmnd'
    )


__all__ = __dir__()
