# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0622,E0402,W0105


"status of bots"


from ..command import Command
from ..errors  import Errors, tostr


def err(event):
    nmr = 0
    event.reply(f"status: {nmr} errors: {len(Errors.errors)}")
    for exc in Errors.errors:
        txt = tostr(exc)
        for line in txt.split():
            event.reply(line)


Command.add(err)
