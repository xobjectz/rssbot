# This file is placed in the Public Domain.
#
# pylint: disable=C,R
# ruff: noqa: F401


"modules"


from . import cmd, irc, rss


def __dir__():
    return (
        'cmd',
        'irc',
        'rss'
    )


__all__ = __dir__()
