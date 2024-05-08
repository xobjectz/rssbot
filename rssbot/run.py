# This file is placed in the Public Domain.


"runtime"


from .broker  import Broker
from .client  import scancmd
from .disk    import scancls
from .thread  import later


broker = Broker()


def init(pkg, modstr, disable=""):
    "start modules"
    mds = []
    for modname in spl(modstr):
        if skip(modname, disable):
            continue
        mod = getattr(pkg, modname, None)
        if not mod:
            continue
        if "init" in dir(mod):
            try:
                mod.init()
                mds.append(mod)
            except Exception as ex: # pylint: disable=W0718
                later(ex)
    return mds


def scan(pkg, modstr, disable=""):
    "scan modules for commands and classes"
    mds = []
    for modname in spl(modstr):
        if skip(modname, disable):
            continue
        module = getattr(pkg, modname, None)
        if not module:
            continue
        scancmd(module)
        scancls(module)
    return mds


def skip(name, skipp):
    "check for skipping"
    for skp in spl(skipp):
        if skp in name:
            return True
    return False


def spl(txt):
    "split comma separated string into a list."
    try:
        res = txt.split(',')
    except (TypeError, ValueError):
        res = txt
    return [x for x in res if x]


def __dir__():
    return (
        'broker',
        'init',
        'scan',
        'skip',
        'spl'
    )
