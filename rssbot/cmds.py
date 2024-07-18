# This file is placed in the Public Domain.
# pylint: disable=R0903


"commands"


import inspect
import time


from .object import Object, fqn
from .parse  import parse
from .utils  import skip


class Commands:

    "Commands"

    cmds     = Object()
    modnames = Object()


def add(func):
    "add command."
    setattr(Commands.cmds, func.__name__, func)
    if func.__module__ != "__main__":
        setattr(Commands.modnames, func.__name__, func.__module__)


def command(bot, evt):
    "check for and run a command."
    parse(evt)
    func = getattr(Commands.cmds, evt.cmd, None)
    if func and evt.txt:
        if "target" not in dir(func) or skip(fqn(bot).split(".")[-1].lower(), func.target):
            func(evt)
            bot.show(evt)
    evt.ready()
    time.sleep(0.001)

def scan(mod) -> None:
    "scan module for commands."
    for key, cmd in inspect.getmembers(mod, inspect.isfunction):
        if key.startswith("cb"):
            continue
        if 'event' in cmd.__code__.co_varnames:
            add(cmd)


def __dir__():
    return (
        'Commands',
        'add',
        'command',
        'scan'
    )
