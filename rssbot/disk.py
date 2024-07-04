# This file is placed in the Public Domain.
# pylint: disable=R0903


"persistence"


import os
import pathlib


from .decode import read
from .dft    import Default
from .encode import write
from .object import Object, fqn, ident, search, update
from .lock   import disklock
from .utils  import fntime, strip


class Persist(Object):

    "Workdir"

    fqns = []
    workdir = ""


def fetch(obj, pth):
    "read object from disk."
    with disklock:
        pth2 = store(pth)
        read(obj, pth2)
        return os.sep.join(pth.split(os.sep)[-3:])


def fns(mtc=""):
    "show list of files."
    dname = ''
    pth = store(mtc)
    for rootdir, dirs, _files in os.walk(pth, topdown=False):
        if dirs:
            for dname in sorted(dirs):
                if dname.count('-') == 2:
                    ddd = os.path.join(rootdir, dname)
                    for fll in os.scandir(ddd):
                        yield strip(os.path.join(ddd, fll))


def find(mtc, selector=None, index=None, deleted=False):
    "find object matching the selector dict."
    clz = long(mtc)
    nrs = -1
    for fnm in sorted(fns(clz), key=fntime):
        obj = Default()
        fetch(obj, fnm)
        if not deleted and '__deleted__' in obj and obj.__deleted__:
            continue
        if selector and not search(obj, selector):
            continue
        nrs += 1
        if index is not None and nrs != int(index):
            continue
        yield (fnm, obj)


def last(obj, selector=None):
    "return last object saved."
    if selector is None:
        selector = {}
    result = sorted(
                    find(fqn(obj), selector),
                    key=lambda x: fntime(x[0])
                   )
    res = None
    if result:
        inp = result[-1]
        update(obj, inp[-1])
        res = inp[0]
    return res


def long(name):
    "match from single name to long name."
    split = name.split(".")[-1].lower()
    res = name
    for named in types():
        if split in named.split(".")[-1].lower():
            res = named
            break
    return res


def skel():
    "create directory,"
    stor = os.path.join(Persist.workdir, "store", "")
    path = pathlib.Path(stor)
    path.mkdir(parents=True, exist_ok=True)


def store(pth=""):
    "return objects directory."
    stor = os.path.join(Persist.workdir, "store", "")
    if not os.path.exists(stor):
        skel()
    return os.path.join(Persist.workdir, "store", pth)


def sync(obj, pth=None):
    "sync object to disk."
    with disklock:
        if pth is None:
            pth = ident(obj)
        pth2 = store(pth)
        write(obj, pth2)
        return pth


def types():
    "return types stored."
    return [x.name for x in os.scandir(store())]


def whitelist(clz):
    "whitelist classes."
    Persist.fqns.append(fqn(clz))


def __dir__():
    return (
        'Persist',
        'fetch',
        'fns',
        'find',
        'last',
        'long',
        'skel',
        'store',
        'sync',
        'types'
    )
