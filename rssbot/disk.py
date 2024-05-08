# This file is placed in the Public Domain.


"disk"


import datetime
import inspect
import os
import pathlib


from .object import Object, fqn, read, write


class Workdir(Object): # pylint: disable=R0903

    "Workdir"

    workdir = ""


def fetch(obj, pth):
    "read object from disk."
    pth2 = store(pth)
    read(obj, pth2)
    return strip(pth)


def ident(obj):
    "return an id for an object."
    return os.path.join(
                        fqn(obj),
                        os.path.join(*str(datetime.datetime.now()).split())
                       )


def lsstore():
    "return types stored."
    return os.listdir(store())


def skel():
    "create directory,"
    pth  = os.path.join(Workdir.workdir, "store", "")
    path = pathlib.Path(pth)
    path.mkdir(parents=True, exist_ok=True)


def store(pth=""):
    "return objects directory."
    return os.path.join(Workdir.workdir, "store", pth)


def strip(pth, nmr=3):
    "reduce to path with directory."
    return os.sep.join(pth.split(os.sep)[-nmr:])


def sync(obj, pth=None):
    "sync object to disk."
    if pth is None:
        pth = ident(obj)
    pth2 = store(pth)
    write(obj, pth2)
    return pth


class Whitelist(Object): # pylint: disable=R0903

    "Whitelist"

    classes = Object()


def scancls(mod) -> None:
    "scan module for classes."
    for key, clz in inspect.getmembers(mod, inspect.isclass):
        if key.startswith("cb"):
            continue
        if not issubclass(clz, Object):
            continue
        whitelist(clz)


def whitelist(clz):
    "add class to whitelist."
    name = str(clz).split()[1][1:-2]
    setattr(Whitelist.classes, name, clz)


def long(name):
    "match from single name to long name."
    split = name.split(".")[-1].lower()
    res = name
    for named in Whitelist.classes:
        if split in named.split(".")[-1].lower():
            res = named
            break
    if "." not in res:
        for fnm in lsstore():
            claz = fnm.split(".")[-1]
            if fnm == claz.lower():
                res = fnm
    return res


def __dir__():
    return (
        'Whitelist',
        'Workdir',
        'fetch',
        'ident',
        'lsstore',
        'long',
        'scancls',
        'skel',
        'store',
        'strip',
        'sync',
        'whitelist'
    )
