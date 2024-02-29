# This file is placed in the Public Domain.
#
# pylint: disable=C,R,E0402


"available modules"


from . import __dir__


def mod(event):
    event.reply(",".join(__dir__()))
