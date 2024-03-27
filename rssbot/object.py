# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0105,W0613,E0101


"""a clean namespace

This module allows for easy json save//load to/from disk of objects. It
provides an "clean namespace" Object class that only has dunder
methods, so the namespace is not cluttered with method names. This makes
storing and reading to/from json possible.

"""


import json
import os
import pathlib
import _thread


disklock = _thread.allocate_lock()


class Object:

    "Base class."

    def __contains__(self, key):
        return key in dir(self)

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __str__(self):
        return str(self.__dict__)


def construct(obj, *args, **kwargs):
    "construct an object from provided arguments."
    if args:
        val = args[0]
        if isinstance(val, zip):
            update(obj, dict(val))
        elif isinstance(val, dict):
            update(obj, val)
        elif isinstance(val, Object):
            update(obj, vars(val))
    if kwargs:
        update(obj, kwargs)


def edit(obj, setter, skip=False):
    "edit an object from provided dict/dict-like."
    for key, val in items(setter):
        if skip and val == "":
            continue
        try:
            setattr(obj, key, int(val))
            continue
        except ValueError:
            pass
        try:
            setattr(obj, key, float(val))
            continue
        except ValueError:
            pass
        if val in ["True", "true"]:
            setattr(obj, key, True)
        elif val in ["False", "false"]:
            setattr(obj, key, False)
        else:
            setattr(obj, key, val)


def fmt(obj, args=None, skip=None, plain=False):
    "format an object to a printable string."
    if args is None:
        args = keys(obj)
    if skip is None:
        skip = []
    txt = ""
    for key in args:
        if key.startswith("__"):
            continue
        if key in skip:
            continue
        value = getattr(obj, key, None)
        if value is None:
            continue
        if plain:
            txt += f"{value} "
        elif isinstance(value, str) and len(value.split()) >= 2:
            txt += f'{key}="{value}" '
        else:
            txt += f"{key}={value} "
    return txt.strip()


def fqn(obj):
    "return full qualified name of an object."
    kin = str(type(obj)).split()[-1][1:-2]
    if kin == "type":
        kin = obj.__name__
    return kin


def items(obj):
    "return the items of an object."
    if isinstance(obj, type({})):
        return obj.items()
    return obj.__dict__.items()


def keys(obj):
    "return keys of an object."
    if isinstance(obj, type({})):
        return obj.keys()
    return list(obj.__dict__.keys())


def read(obj, pth):
    "read an object from file path."
    with disklock:
        with open(pth, 'r', encoding='utf-8') as ofile:
            update(obj, load(ofile))


def search(obj, selector):
    "check if object matches provided values."
    res = False
    if not selector:
        return True
    for key, value in items(selector):
        val = getattr(obj, key, None)
        if str(value).lower() in str(val).lower():
            res = True
        else:
            res = False
            break
    return res


def update(obj, data, empty=True):
    "update an object."
    for key, value in items(data):
        if empty and not value:
            continue
        setattr(obj, key, value)


def values(obj):
    "return values of an object."
    return obj.__dict__.values()


def write(obj, pth):
    "write an object to disk."
    with disklock:
        cdir(os.path.dirname(pth))
        with open(pth, 'w', encoding='utf-8') as ofile:
            dump(obj, ofile, indent=4)


class ObjectDecoder(json.JSONDecoder):

    "Object decoded"

    def __init__(self, *args, **kwargs):
        return json.JSONDecoder.__init__(self, *args)

    def decode(self, s, _w=None):
        "decoding string to object."
        val = json.JSONDecoder.decode(self, s)
        if not val:
            val = {}
        return hook(val)

    def raw_decode(self, s, idx=0):
        "decode partial string to object."
        return json.JSONDecoder.raw_decode(self, s, idx)


def hook(objdict, typ=None):
    "construct object from dict."
    if typ:
        obj = typ()
    else:
        obj = Object()
    construct(obj, objdict)
    return obj


def load(fpt, *args, **kw):
    "load object from file."
    kw["cls"] = ObjectDecoder
    kw["object_hook"] = hook
    return json.load(fpt, *args, **kw)


def loads(string, *args, **kw):
    "load object from string."
    kw["cls"] = ObjectDecoder
    kw["object_hook"] = hook
    return json.loads(string, *args, **kw)


class ObjectEncoder(json.JSONEncoder):

    "Object encoder."

    def __init__(self, *args, **kwargs):
        return json.JSONEncoder.__init__(self, *args, **kwargs)

    def default(self, o):
        "return stringable value."
        if isinstance(o, dict):
            return o.items()
        if isinstance(o, Object):
            return vars(o)
        if isinstance(o, list):
            return iter(o)
        if isinstance(o, (type(str), type(True), type(False), type(int), type(float))):
            return o
        try:
            return json.JSONEncoder.default(self, o)
        except TypeError:
            return o.__dict__

    def encode(self, o) -> str:
        "encode object to string."
        return json.JSONEncoder.encode(self, o)

    def iterencode(self, o, _one_shot=False):
        "loop over object to encode to string."
        return json.JSONEncoder.iterencode(self, o, _one_shot)


def dump(*args, **kw):
    "dump object to file."
    kw["cls"] = ObjectEncoder
    return json.dump(*args, **kw)


def dumps(*args, **kw):
    "dump object to string."
    kw["cls"] = ObjectEncoder
    return json.dumps(*args, **kw)


class Default(Object):

    "Object that return a default value if key does not exist."

    __slots__ = ("__default__",)

    def __init__(self):
        Object.__init__(self)
        self.__default__ = ""

    def __getattr__(self, key):
        return self.__dict__.get(key, self.__default__)


def cdir(pth):
    "create directory."
    if os.path.exists(pth):
        return
    pth = pathlib.Path(pth)
    os.makedirs(pth, exist_ok=True)


def spl(txt):
    "split comma separated string into a list."
    try:
        res = txt.split(',')
    except (TypeError, ValueError):
        res = txt
    return [x for x in res if x]


"interface"


def __dir__():
    return (
        'Default',
        'Object',
        'construct',
        'dump',
        'dumps',
        'edit',
        'fmt',
        'fqn',
        'hook',
        'items',
        'keys',
        'load',
        'loads',
        'read',
        'search',
        'update',
        'values',
        'write'
    )


__all__ = __dir__()
