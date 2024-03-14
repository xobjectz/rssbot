# This file is placed in the Public Domain.
#
# pylint: disable=C,R,E0402,W0105


"available modules"


import os


from objx.handler import Client


from . import __dir__


"commands"


def mod(event):
    res = []
    if os.path.exists("mods"):
        import mods
        res.extend(mods.__dir__())
    res.extend(__dir__())
    event.reply(",".join(sorted(res)))


Client.add(mod)
