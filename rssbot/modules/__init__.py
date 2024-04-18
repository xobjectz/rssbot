# This file is placed in the Public Domain.
#
# pylint: disable=C,R
# ruff: noqa: F401


"modules"


from . import cmd, err, irc, mod, rss


def __dir__():
    return (
        'cmd',
        'err',
        'irc',
        'mod',
        'rss'
    )


__all__ = __dir__()
