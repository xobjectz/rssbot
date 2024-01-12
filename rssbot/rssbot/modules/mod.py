# This file is placed in the Public Domain.
#
# pylint: disable=C,R,E0402


"available modules"


from . import __dir__


def mod(event):
    try:
        import objmod
        event.reply(",".join(sorted(__dir__() + objmod.__dir__())))
    except ModuleNotFoundError:
        event.reply(",".join(__dir__()))
