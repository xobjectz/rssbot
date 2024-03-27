# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0105,E0402


"""persistence

Object persistence.

"""


import datetime
import os
import time


from .object import Default, Object, cdir, fqn, read, search, update, write


class Workdir(Object):

    "directory to store objects."

    wd = ""

    @staticmethod
    def skel():
        "create directory,"
        cdir(os.path.join(Workdir.wd, "store", ""))

    @staticmethod
    def store(pth=""):
        "return objects directory."
        return os.path.join(Workdir.wd, "store", pth)

    @staticmethod
    def strip(pth, nmr=3):
        "reduce to path with directory."
        return os.sep.join(pth.split(os.sep)[-nmr:])

    @staticmethod
    def types():
        "return types stored."
        return os.listdir(Workdir.store())


class Persist(Object):

    "whitelist of types saveable to disk."

    classes = Object()

    @staticmethod
    def add(clz):
        "add class to whitelist."
        name = str(clz).split()[1][1:-2]
        setattr(Persist.classes, name, clz)

    @staticmethod
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
                            yield Workdir.strip(os.path.join(ddd, fll))

    @staticmethod
    def long(name):
        "match from single name to long name."
        split = name.split(".")[-1].lower()
        res = name
        for named in Persist.classes:
            if split in named.split(".")[-1].lower():
                res = named
                break
        if "." not in res:
            for fnm in Workdir.types():
                claz = fnm.split(".")[-1]
                if fnm == claz.lower():
                    res = fnm
        return res


def laps(seconds, short=True):
    "show elapsed time."
    txt = ""
    nsec = float(seconds)
    if nsec < 1:
        return f"{nsec:.2f}s"
    yea = 365*24*60*60
    week = 7*24*60*60
    nday = 24*60*60
    hour = 60*60
    minute = 60
    yeas = int(nsec/yea)
    nsec -= yeas*yea
    weeks = int(nsec/week)
    nsec -= weeks*week
    nrdays = int(nsec/nday)
    nsec -= nrdays*nday
    hours = int(nsec/hour)
    nsec -= hours*hour
    minutes = int(nsec/minute)
    nsec -= int(minute*minutes)
    sec = int(nsec)
    if yeas:
        txt += f"{yeas}y"
    if weeks:
        nrdays += weeks * 7
    if nrdays:
        txt += f"{nrdays}d"
    if short and txt:
        return txt.strip()
    if hours:
        txt += f"{hours}h"
    if minutes:
        txt += f"{minutes}m"
    if sec:
        txt += f"{sec}s"
    txt = txt.strip()
    return txt


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
    clz = Persist.long(mtc)
    nr = -1
    for fnm in sorted(Persist.fns(clz), key=fntime):
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


def fetch(obj, pth):
    "read object from disk."
    pth2 = Workdir.store(pth)
    read(obj, pth2)
    return Workdir.strip(pth)


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
    if result:
        inp = result[-1]
        update(obj, inp[-1])
        return inp[0]


def sync(obj, pth=None):
    "sync object to disk."
    if pth is None:
        pth = ident(obj)
    pth2 = Workdir.store(pth)
    write(obj, pth2)
    return pth


"interface"


def __dir__():
    return (
        'Persist',
        'Workdir',
        'fetch',
        'fntime',
        'find',
        'laps',
        'last',
        'ident',
        'read',
        'sync',
        'write'
    )


__all__ = __dir__()
