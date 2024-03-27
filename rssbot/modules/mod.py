# This file is placed in the Public Domain.
#
# pylint: disable=C,R,E0402,W0105


"available modules"


from ..handler import Client


from . import __dir__


def mod(event):
    event.reply(",".join(sorted(__dir__())))


Client.add(mod)
