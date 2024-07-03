# This file is placed in the Public Domain.
#
# pylint: disable=R0903


"commands"


from .object import Object
from .parse  import parse


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
    if func:
        func(evt)
        bot.show(evt)
    evt.ready()


def __dir__():
    return (
        'Commands',
        'add',
        'command',
        'modnames'
    )
