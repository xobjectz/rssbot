# This file is placed in the Public Domain.
# pylint: disable=W0718


"main"


from .client import Client, command
from .cmds   import Commands
from .errors import Errors
from .disk   import Persist
from .event  import Event
from .log    import Logging
from .thread import launch
from .utils  import skip, spl


def cmnd(txt, outer):
    "do a command using the provided output function."
    if not txt:
        return None
    cli = Client(outer)
    evn = Event()
    evn.txt = txt
    command(cli, evn)
    evn.wait()
    return evn


def enable(outer):
    "enable printing."
    Client.out = Errors.out = Logging.out = outer


def init(modstr, *pkgs, disable=None):
    "scan modules for commands and classes"
    thrs = []
    for mod in spl(modstr):
        if disable and mod in spl(disable):
            continue
        for pkg in pkgs:
            modi = getattr(pkg, mod, None)
            if not modi:
                continue
            if "init" not in dir(modi):
                continue
            thrs.append(launch(modi.init))
            break
    return thrs


def scan(modstr, *pkgs, disable=""):
    "scan modules for commands and classes"
    mds = []
    for modname in spl(modstr):
        if skip(modname, disable):
            continue
        for pkg in pkgs:
            module = getattr(pkg, modname, None)
            if not module:
                continue
            Commands.scan(module)
            Persist.scan(module)
    return mds


def __dir__():
    return (
        'cmnd',
        'enable',
        'init',
        'scan'
    )
