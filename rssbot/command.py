# This file is placed in the Public Domain.


"command"


import inspect


from .object import Object


class Command(Object): # pylint: disable=R0903

    "Command"

    cmds = Object()


def add(func):
    "add command."
    setattr(Command.cmds, func.__name__, func)


def scan(mod) -> None:
    "scan module for commands."
    for key, cmd in inspect.getmembers(mod, inspect.isfunction):
        if key.startswith("cb"):
            continue
        if 'event' in cmd.__code__.co_varnames:
            add(cmd)


def __dir__():
    return (
        'add',
        'scan'
    )
