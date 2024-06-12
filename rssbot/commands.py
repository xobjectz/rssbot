# This file is placed in the Public Domain.


"client"


import inspect


from .object import Object
from .parser import parse
from .errors import later


class Commands: # pylint: disable=R0903

    "Commands"

    cmds = Object()


    @staticmethod
    def add(func):
        "add command."
        setattr(Commands.cmds, func.__name__, func)


def command(bot, evt):
    "check for and run a command."
    parse(evt)
    func = getattr(Commands.cmds, evt.cmd, None)
    if func:
        try:
            func(evt)
        except Exception as exc: # pylint: disable=W0718
            later(exc)
    bot.show(evt)
    evt.ready()


def scan(mod) -> None:
    "scan module for commands."
    for key, cmd in inspect.getmembers(mod, inspect.isfunction):
        if key.startswith("cb"):
            continue
        if 'event' in cmd.__code__.co_varnames:
            Commands.add(cmd)


def __dir__():
    return (
        'Commands',
        'command',
        'scan'
    )
