# This file is placed in the Public Domain.
#
# pylint: disable=C,R,E0402,W0105


"available modules"


from ..command import Command


from . import __dir__


def mod(event):
    event.reply(",".join(sorted(__dir__())))


Command.add(mod)
