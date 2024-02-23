# This file is placed in the Public Domain
#
# pylint: disable=C,R


"find objects"


import os


from .default import Default
from .objects import fqn, search, update
from .persist import fetch, long
from .workdir import store
from .utility import fntime, strip


def __dir__():
    return (
        'find',
        'fns',
        'last'
    )


__all__ = __dir__()


def find(mtc, selector=None, index=None, deleted=False):
    clz = long(mtc)
    nr = -1
    for fnm in sorted(fns(clz), key=fntime):
        obj = Default()
        fetch(obj, fnm)
        if not deleted and '__deleted__' in obj:
            continue
        if selector and not search(obj, selector):
            continue
        nr += 1 
        if index is not None and nr != int(index):
            continue
        yield (fnm, obj)


def fns(mtc=""):
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


def last(obj, selector=None):
    if selector is None:
        selector = {}
    result = sorted(
                    find(fqn(obj), selector),
                    key=lambda x: fntime(x[0])
                   )
    if result:
        inp = result[-1]
        update(obj, inp[-1])
        return inp[0]
