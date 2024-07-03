# This file is placed in the Public Domain.


"deferred exception handling"


from ..cmds  import add
from ..defer import Errors


def err(event):
    "show errors."
    nmr = 0
    for exc in Errors.errors:
        txt = Errors.format(exc)
        for line in txt.split():
            event.reply(line)
        nmr += 1
    if not nmr:
        event.reply("no errors")
        return
    event.reply(f"found {nmr} errors.")


add(err)
