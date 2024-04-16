# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0105


"persist"


import datetime
import os
import time


from .default import Default
from .object  import Object, fqn, read, search, update, write
from .workdir import liststore, store, strip


class Persist(Object):

    "Persist"

    classes = Object()


def whitelist(clz):
    "add class to whitelist."
    name = str(clz).split()[1][1:-2]
    setattr(Persist.classes, name, clz)


def fns(mtc=""):
    "show list of files."
    dname = ''
    pth = store(mtc)
    for rootdir, dirs, _files in os.walk(pth, topdown=False):
        if dirs:
            for dname in sorted(dirs):
                if dname.count('-') == 2:
                    ddd = os.path.join(rootdir, dname)
                    fls = sorted(os.listdir(ddd))
                    for fll in fls:
                        yield strip(os.path.join(ddd, fll))

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


def fntime(daystr):
    "convert file name to it's saved time."
    daystr = daystr.replace('_', ':')
    datestr = ' '.join(daystr.split(os.sep)[-2:])
    if '.' in datestr:
        datestr, rest = datestr.rsplit('.', 1)
    else:
        rest = ''
    timed = time.mktime(time.strptime(datestr, '%Y-%m-%d %H:%M:%S'))
    if rest:
        timed += float('.' + rest)
    return timed


def find(mtc, selector=None, index=None, deleted=False):
    "find object matching the selector dict."
    clz = long(mtc)
    nrs = -1
    for fnm in sorted(fns(clz), key=fntime):
        obj = Default()
        fetch(obj, fnm)
        if not deleted and '__deleted__' in obj:
            continue
        if selector and not search(obj, selector):
            continue
        nrs += 1
        if index is not None and nrs != int(index):
            continue
        yield (fnm, obj)


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

def sync(obj, pth=None):
    "sync object to disk."
    if pth is None:
        pth = ident(obj)
    pth2 = store(pth)
    write(obj, pth2)
    return pth


"interface"


def __dir__():
    return (
        'Persist',
        'fetch',
        'fntime',
        'find',
        'last',
        'long',
        'ident',
        'sync',
        'whitelist'
    )


__all__ = __dir__()
