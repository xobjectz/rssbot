# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0105,W0212,W0613,W0718,E0402,E1102


"runtime"


import io
import time
import traceback
import _thread


from .default import Default
from .objects import Object, keys, values


"defines"


rpr = object.__repr__


"classes"


class Broker:

    objs = Object()

    @staticmethod
    def add(obj):
        setattr(Broker.objs, rpr(obj), obj)

    @staticmethod
    def all():
        return values(Broker.objs)

    @staticmethod
    def first():
        for key in keys(Broker.objs):
            return getattr(Broker.objs, key)

    @staticmethod
    def get(orig):
        return getattr(Broker.objs, orig, None)

    @staticmethod
    def remove(obj):
        delattr(Broker.objs, rpr(obj))


class Errors:

    errors = []
    filter = []
    output = None
    shown  = []

    @staticmethod
    def add(exc):
        excp = exc.with_traceback(exc.__traceback__)
        Errors.errors.append(excp)

    @staticmethod
    def enable(out):
        Errors.output = out

    @staticmethod
    def format(exc):
        res = ""
        stream = io.StringIO(
                             traceback.print_exception(
                                                       type(exc),
                                                       exc,
                                                       exc.__traceback__
                                                      )
                            )
        for line in stream.readlines():
            res += line + "\n"
        return res

    @staticmethod
    def out(exc):
        if Errors.output:
            txt = str(Errors.format(exc))
            Errors.output(txt)

    @staticmethod
    def show():
        for exc in Errors.errors:
            Errors.out(exc)

    @staticmethod
    def skip(txt):
        for skp in Errors.filter:
            if skp in str(txt):
                return True
        return False


"utilitites"


def debug(txt):
    if Errors.output and not Errors.skip(txt):
        Errors.output(txt)


def forever():
    while 1:
        try:
            time.sleep(1.0)
        except (KeyboardInterrupt, EOFError):
            _thread.interrupt_main()


def init(pkg, modstr, disable="", wait=False):
    mds = []
    for modname in spl(modstr):
        if modname in spl(disable):
            continue
        module = getattr(pkg, modname, None)
        if not module:
            continue
        if "init" in dir(module):
            module.init()
            mds.append(module)
    return mds


def parse_cmd(obj, txt=None):
    args = []
    obj.args    = obj.args or []
    obj.cmd     = obj.cmd or ""
    obj.gets    = obj.gets or Default()
    obj.hasmods = obj.hasmod or False
    obj.index   = None
    obj.mod     = obj.mod or ""
    obj.opts    = obj.opts or ""
    obj.result  = obj.reult or []
    obj.sets    = obj.sets or Default()
    obj.txt     = txt or obj.txt or ""
    obj.otxt    = obj.txt
    _nr = -1
    for spli in obj.otxt.split():
        if spli.startswith("-"):
            try:
                obj.index = int(spli[1:])
            except ValueError:
                obj.opts += spli[1:]
            continue
        if "==" in spli:
            key, value = spli.split("==", maxsplit=1)
            if key in obj.gets:
                val = getattr(obj.gets, key)
                value = val + "," + value
            setattr(obj.gets, key, value)
            continue
        if "=" in spli:
            key, value = spli.split("=", maxsplit=1)
            if key == "mod":
                obj.hasmods = True
                if obj.mod:
                    obj.mod += f",{value}"
                else:
                    obj.mod = value
                continue
            setattr(obj.sets, key, value)
            continue
        _nr += 1
        if _nr == 0:
            obj.cmd = spli
            continue
        args.append(spli)
    if args:
        obj.args = args
        obj.txt  = obj.cmd or ""
        obj.rest = " ".join(obj.args)
        obj.txt  = obj.cmd + " " + obj.rest
    else:
        obj.txt = obj.cmd or ""


def spl(txt):
    try:
        res = txt.split(',')
    except (TypeError, ValueError):
        res = txt
    return [x for x in res if x]


"interfacce"


def __dir__():
    return (
        'Broker',
        'Errors',
        'debug',
        'forever',
        'init',
        'parse_cmd',
        'spl'
    )


__all__ = __dir__()
