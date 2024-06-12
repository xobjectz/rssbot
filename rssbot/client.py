# This file is placed in the Public Domain.


"client"


from .commands import command
from .commands import scan as scancmd
from .errors   import later
from .event    import Event
from .handler  import Handler
from .run      import broker
from .utils    import skip, spl


class Client(Handler):

    "Client"

    def __init__(self):
        Handler.__init__(self)
        self.register("command", command)

    def announce(self, txt):
        "announce text."
        self.raw(txt)

    def raw(self, txt):
        "raw output."

    def say(self, _channel, txt):
        "say text in a channel."
        self.raw(txt)

    def show(self, evt):
        "show results into a channel."
        for txt in evt.result:
            self.say(evt.channel, txt)


def cmnd(txt, outer=None):
    "do a command using the provided output function."
    clt = Client()
    ids = broker.add(clt)
    if outer:
        clt.raw = outer
    evn = Event()
    evn.orig = ids
    evn.txt = txt
    command(clt, evn)
    evn.wait()
    return evn


def init(pkg, modstr, disable=""):
    "start modules"
    mds = []
    for modname in spl(modstr):
        if skip(modname, disable):
            continue
        mod = getattr(pkg, modname, None)
        if not mod:
            continue
        if "init" in dir(mod):
            try:
                mod.init()
                mds.append(mod)
            except Exception as ex: # pylint: disable=W0718
                later(ex)
    return mds


def scan(pkg, modstr, disable=""):
    "scan modules for commands and classes"
    mds = []
    for modname in spl(modstr):
        if skip(modname, disable):
            continue
        module = getattr(pkg, modname, None)
        if not module:
            continue
        scancmd(module)
    return mds


def __dir__():
    return (
        'Client',
        'cmnd',
        'init',
        'scan'
    )
