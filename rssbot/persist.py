# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0105


"persist"


from .object  import Object
from .workdir import liststore


class Persist(Object):

    "Persist"

    classes = Object()


def whitelist(clz):
    "add class to whitelist."
    name = str(clz).split()[1][1:-2]
    setattr(Persist.classes, name, clz)


def long(name):
    "match from single name to long name."
    split = name.split(".")[-1].lower()
    res = name
    for named in Persist.classes:
        if split in named.split(".")[-1].lower():
            res = named
            break
    if "." not in res:
        for fnm in liststore():
            claz = fnm.split(".")[-1]
            if fnm == claz.lower():
                res = fnm
    return res
