# This file is placed in the Public Domain.


"persist"


import inspect


from .object  import Object
from .workdir import liststore


class Whitelist(Object): # pylint: disable=R0903

    "Whitelist"

    classes = Object()


def scan(mod) -> None:
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
        for fnm in liststore():
            claz = fnm.split(".")[-1]
            if fnm == claz.lower():
                res = fnm
    return res


def __dir__():
    return (
        'Whitelist',
        'long',
        'whitelist'
    )
