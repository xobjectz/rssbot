# This file is placed in the Public Domain.


"deferred exception handling"


from ..thread import Errors, formatexc


def err(event):
    "show errors."
    nmr = 0
    event.reply(f"status: {nmr} errors: {len(Errors.errors)}")
    for exc in Errors.errors:
        txt = formatexc(exc)
        for line in txt.split():
            event.reply(line)
