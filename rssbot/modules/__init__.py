# This file is placed in the Public Domain.
# ruff: noqa: F401


"modules"


from . import cmd, err, fnd, irc, mod, req, rss, thr, tmr, upt


def __dir__():
    return (
        'cmd',
        'err',
        'fnd',
        'irc',
        'mod',
        'req',
        'rss',
        'thr',
        'tmr',
        'upt'
    )
