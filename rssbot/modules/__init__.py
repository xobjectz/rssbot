# This file is placed in the Public Domain.
# ruff: noqa: F401


"modules"


from . import cmd, err, irc, mod, rss, skl, thr, upt


def __dir__():
    return (
        'cmd',
        'err',
        'irc',
        'mod',
        'rss',
        'skl',
        'thr',
        'upt'
    )
