# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0718,W0611,E0402


"commands"


from .excepts import Error
from .objects import Object
from .parsers import parse_cmd


def __dir__():
    return (
        'Command',
        'command'
    )


__all__ = __dir__()


class Command(Object):

    cmds = Object()

    @staticmethod
    def add(func):
        setattr(Command.cmds, func.__name__, func)


def command(evt):
    parse_cmd(evt)
    func = getattr(Command.cmds, evt.cmd, None)
    if func:
        try:
            func(evt)
            evt.show()
        except Exception as exc:
            Error.add(exc)
    evt.ready()
