# This file is placed in the Public Domain.
# pylint: disable=W0718


"main"


from .cli   import CLI
from .cmds  import command
from .defer import later
from .event import Event
from .utils import spl


def cmnd(txt, outer):
    "do a command using the provided output function."
    if not txt:
        return None
    cli = CLI(outer)
    evn = Event()
    evn.txt = txt
    command(cli, evn)
    evn.wait()
    return evn


def init(pkg, modstr, disable=None):
    "scan modules for commands and classes"
    mds = []
    for mod in spl(modstr):
        if disable and mod in spl(disable):
            continue
        module = getattr(pkg, mod, None)
        if not module:
            continue
        if "init" not in dir(module):
            continue
        try:
            module.init()
        except Exception as ex:
            later(ex)
    return mds


def __dir__():
    return (
        'cmnd',
        'init',
        'scan'
    )
