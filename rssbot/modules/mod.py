# This file is placed in the Public Domain.


"available modules"


from . import __dir__


def mod(event):
    "show available modules."
    event.reply(",".join(sorted(__dir__())))
