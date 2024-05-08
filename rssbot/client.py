# This file is placed in the Public Domain.


"client"


import inspect


from .handler import Event, Handler
from .object  import Default, Object
from .thread  import later


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


class Command(Object): # pylint: disable=R0903

    "Command"

    cmds = Object()


def add(func):
    "add command."
    setattr(Command.cmds, func.__name__, func)


def command(bot, evt):
    "check for and run a command."
    parse(evt)
    func = getattr(Command.cmds, evt.cmd, None)
    if func:
        try:
            func(evt)
        except Exception as exc: # pylint: disable=W0718
            later(exc)
    bot.show(evt)
    evt.ready()


def cmnd(txt, outer):
    "do a command using the provided output function."
    clt = Client()
    clt.raw = outer
    evn = Event()
    evn.orig = object.__repr__(clt)
    evn.txt = txt
    command(clt, evn)
    evn.wait()
    return evn


def laps(seconds, short=True):
    "show elapsed time."
    txt = ""
    nsec = float(seconds)
    if nsec < 1:
        return f"{nsec:.2f}s"
    yea = 365*24*60*60
    week = 7*24*60*60
    nday = 24*60*60
    hour = 60*60
    minute = 60
    yeas = int(nsec/yea)
    nsec -= yeas*yea
    weeks = int(nsec/week)
    nsec -= weeks*week
    nrdays = int(nsec/nday)
    nsec -= nrdays*nday
    hours = int(nsec/hour)
    nsec -= hours*hour
    minutes = int(nsec/minute)
    nsec -= int(minute*minutes)
    sec = int(nsec)
    if yeas:
        txt += f"{yeas}y"
    if weeks:
        nrdays += weeks * 7
    if nrdays:
        txt += f"{nrdays}d"
    if short and txt:
        return txt.strip()
    if hours:
        txt += f"{hours}h"
    if minutes:
        txt += f"{minutes}m"
    if sec:
        txt += f"{sec}s"
    txt = txt.strip()
    return txt


def parse(obj, txt=None):
    "parse a string for a command."
    args = []
    obj.args    = obj.args or []
    obj.cmd     = obj.cmd or ""
    obj.gets    = obj.gets or Default()
    obj.hasmods = obj.hasmod or False
    obj.index   = None
    obj.mod     = obj.mod or ""
    obj.opts    = obj.opts or ""
    obj.result  = obj.reult or []
    obj.sets    = obj.sets or Default()
    obj.txt     = txt or obj.txt or ""
    obj.otxt    = obj.txt
    _nr = -1
    for spli in obj.otxt.split():
        if spli.startswith("-"):
            try:
                obj.index = int(spli[1:])
            except ValueError:
                obj.opts += spli[1:]
            continue
        if "==" in spli:
            key, value = spli.split("==", maxsplit=1)
            if key in obj.gets:
                val = getattr(obj.gets, key)
                value = val + "," + value
            setattr(obj.gets, key, value)
            continue
        if "=" in spli:
            key, value = spli.split("=", maxsplit=1)
            if key == "mod":
                obj.hasmods = True
                if obj.mod:
                    obj.mod += f",{value}"
                else:
                    obj.mod = value
                continue
            setattr(obj.sets, key, value)
            continue
        _nr += 1
        if _nr == 0:
            obj.cmd = spli
            continue
        args.append(spli)
    if args:
        obj.args = args
        obj.txt  = obj.cmd or ""
        obj.rest = " ".join(obj.args)
        obj.txt  = obj.cmd + " " + obj.rest
    else:
        obj.txt = obj.cmd or ""


def scancmd(mod) -> None:
    "scan module for commands."
    for key, cmd in inspect.getmembers(mod, inspect.isfunction):
        if key.startswith("cb"):
            continue
        if 'event' in cmd.__code__.co_varnames:
            add(cmd)


def __dir__():
    return (
        'Client',
        'Commands',
        'add',
        'command',
        'laps',
        'parse',
        'scancmd'
    )
