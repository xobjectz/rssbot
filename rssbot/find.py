# This file is placed in the Public Domain.


"find"


import os


from .classes import Classes
from .default import Default
from .object  import fqn, search, update
from .disk    import Workdir, fetch
from .utils   import fntime, strip


def fns(mtc=""):
    "show list of files."
    dname = ''
    pth = Workdir.store(mtc)
    for rootdir, dirs, _files in os.walk(pth, topdown=False):
        if dirs:
            for dname in sorted(dirs):
                if dname.count('-') == 2:
                    ddd = os.path.join(rootdir, dname)
                    fls = sorted(os.listdir(ddd))
                    for fll in fls:
                        yield strip(os.path.join(ddd, fll))


def find(mtc, selector=None, index=None, deleted=False):
    "find object matching the selector dict."
    clz = Classes.long(mtc)
    nrs = -1
    result = []
    for fnm in sorted(fns(clz), key=fntime):
        obj = Default()
        fetch(obj, fnm)
        if not deleted and '__deleted__' in dir(obj):
            continue
        if selector and not search(obj, selector):
            continue
        nrs += 1
        if index is not None and nrs != int(index):
            continue
        result.append((fnm, obj))
    return result


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


def __dir__():
    return (
        'fns',
        'find',
        'last'
    )
