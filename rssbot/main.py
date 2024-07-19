# This file is placed in the Public Domain.
# pylint: disable=W0718


"main"


from .client import Client
from .cmds   import command
from .cmds   import scan as scancmd
from .defer  import Errors, later
from .disk   import scan as scancls
from .event  import Event
from .log    import Logging
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
            scancmd(module)
            scancls(module)
    return mds


def __dir__():
    return (
        'cmnd',
        'enable',
        'init',
        'scan'
    )
