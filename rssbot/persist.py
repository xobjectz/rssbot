# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0105,E0402


"persistence"


import datetime
import inspect
import os
import pathlib
import time
import _thread


from .objects import Default, Object, dump, fqn, load, search, update


def __dir__():
    return (
        'Persist',
        'Workdir',
        'fetch',
        'fntime',
        'find',
        'last',
        'ident',
        'read',
        'sync',
        'write'
    )


__all__ = __dir__()


class Workdir(Object):

    wd = ""

    @staticmethod
    def cdir(pth) -> None:
        if os.path.exists(pth):
            return
        pth = pathlib.Path(pth)
        os.makedirs(pth, exist_ok=True)

    @staticmethod
    def skel():
        Workdir.cdir(os.path.join(Workdir.wd, "store", ""))

    @staticmethod
    def store(pth=""):
        return os.path.join(Workdir.wd, "store", pth)

    @staticmethod
    def strip(pth, nmr=3):
        return os.sep.join(pth.split(os.sep)[-nmr:])

    @staticmethod
    def types():
        return os.listdir(Workdir.store())



lock = _thread.allocate_lock()


class Persist(Object):

    classes = Object()

    @staticmethod
    def add(clz):
        name = str(clz).split()[1][1:-2]
        setattr(Persist.classes, name, clz)

    @staticmethod
    def fns(mtc=""):
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

    @staticmethod
    def scan(mod):
        for _key, clz in inspect.getmembers(mod, inspect.isclass):
            if not issubclass(clz, Object):
                continue
            Persist.add(clz)


def fetch(obj, pth):
    pth2 = Workdir.store(pth)
    read(obj, pth2)
    return Workdir.strip(pth)


def ident(obj):
    return os.path.join(
                        fqn(obj),
                        os.path.join(*str(datetime.datetime.now()).split())
                       )

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


def read(obj, pth):
    with lock:
        with open(pth, 'r', encoding='utf-8') as ofile:
            update(obj, load(ofile))


def sync(obj, pth=None):
    if pth is None:
        pth = ident(obj)
    pth2 = Workdir.store(pth)
    write(obj, pth2)
    return pth


def write(obj, pth):
    with lock:
        Workdir.cdir(os.path.dirname(pth))
        with open(pth, 'w', encoding='utf-8') as ofile:
            dump(obj, ofile, indent=4)


"utilities"


def laps(seconds, short=True):
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
