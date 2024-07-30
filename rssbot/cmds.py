# This file is placed in the Public Domain.
# pylint: disable=R0903


"commands"


import inspect


from .object import Object


class Commands:

    "Commands"

    cmds     = Object()
    modnames = Object()


    @staticmethod
    def add(func):
        "add command."
        setattr(Commands.cmds, func.__name__, func)
        if func.__module__ != "__main__":
            setattr(Commands.modnames, func.__name__, func.__module__)

    @staticmethod
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
    )
