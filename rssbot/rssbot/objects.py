# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0105


"""an object with a clean namespace

This module provides an Object class and it's json encoder/decoder.
A locked read and write method is provides as well as basic dict methods
put in as function with the object as the first argument. This provides an 
object with a, no methods, clean namespace to inherit from.

basic usage is:

   >>> from objx import Object, read, write
   >>> o = Object()
   >>> o.a = "b"
   >>> write(o, "test")
   >>> oo = Object()
   >>> read(oo, "test")
   >>> oo
   {"a": "b"}


"""


import pathlib
import json
import os
import _thread


def __dir__():
    return (
        'Default',
        'Object',
        'cdir',
        'construct',
        'edit',
        'fmt',
        'fqn',
        'items',
        'keys',
        'read',
        'update',
        'values',
        'write'
    )


__all__ = __dir__()


lock = _thread.allocate_lock()


def cdir(pth) -> None:
    " create directory "
    if os.path.exists(pth):
        return
    pth = pathlib.Path(pth)
    os.makedirs(pth, exist_ok=True)


class Object:

    "a no methods base class to provide a clean namespace."

    def __contains__(self, key):
        "see if attribute is available."
        return key in dir(self)

    def __iter__(self):
        "iterate over attributes."
        return iter(self.__dict__)

    def __len__(self):
        "return number of attributes."
        return len(self.__dict__)

    def __repr__(self):
        "return json string."
        return dumps(self)

    def __str__(self):
        "return python string."
        return str(self.__dict__)


class Default(Object):

    "default values"

    __slots__ = ("__default__",)

    def __init__(self):
        Object.__init__(self)
        self.__default__ = ""

    def __getattr__(self, key):
        return self.__dict__.get(key, self.__default__)


class ObjectDecoder(json.JSONDecoder):

    "decode from json string."

    def decode(self, s, _w=None):
        "decode a json string."
        val = json.JSONDecoder.decode(self, s)
        if not val:
            val = {}
        return hook(val)

    def raw_decode(self, s, idx=0):
        "decode raw text at index."
        return json.JSONDecoder.raw_decode(self, s, idx)


def hook(objdict, typ=None) -> Object:
    "construct with json data."
    if typ:
        obj = typ()
    else:
        obj = Object()
    construct(obj, objdict)
    return obj


def load(fpt, *args, **kw) -> Object:
    "load from disk."
    kw["cls"] = ObjectDecoder
    kw["object_hook"] = hook
    return json.load(fpt, *args, **kw)


def loads(string, *args, **kw) -> Object:
    "load from string."
    kw["cls"] = ObjectDecoder
    kw["object_hook"] = hook
    return json.loads(string, *args, **kw)


class ObjectEncoder(json.JSONEncoder):

    "encode into a json string."

    def default(self, o) -> str:
        "return json printable data."
        if isinstance(o, dict):
            return o.items()
        if isinstance(o, Object):
            return vars(o)
        if isinstance(o, list):
            return iter(o)
        if isinstance(
                      o,
                      (
                       type(str),
                       type(True),
                       type(False),
                       type(int),
                       type(float)
                      )
                     ):
            return o
        try:
            return json.JSONEncoder.default(self, o)
        except TypeError:
            return object.__repr__(o)

    def encode(self, o) -> str:
        "return json string."
        return json.JSONEncoder.encode(self, o)

    def iterencode(
                   self,
                   o,
                   _one_shot=False
                  ) -> str:
        "piecemale encoding to string."
        return json.JSONEncoder.iterencode(self, o, _one_shot)


def dump(*args, **kw) -> None:
    "write to file."
    kw["cls"] = ObjectEncoder
    return json.dump(*args, **kw)


def dumps(*args, **kw) -> str:
    "write to string."
    kw["cls"] = ObjectEncoder
    return json.dumps(*args, **kw)


"methods"


def construct(obj, *args, **kwargs) -> None:
    "construct from another type."
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


def edit(obj, setter, skip=False) -> None:
    "edit with a dict and it's values."
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


def fmt(obj, args=None, skip=None, plain=False) -> str:
    "key=value formatted string."
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
            txt += f'{key}={value} '
    return txt.strip()


def fqn(obj) -> str:
    "full qualified name."
    kin = str(type(obj)).split()[-1][1:-2]
    if kin == "type":
        kin = obj.__name__
    return kin


def items(obj) -> []:
    "return (key,value) list of object items."
    if isinstance(obj, type({})):
        return obj.items()
    return obj.__dict__.items()


def keys(obj) -> []:
    "list of attributes names."
    if isinstance(obj, type({})):
        return obj.keys()
    return list(obj.__dict__.keys())


def read(obj, pth) -> None:
    "locked read from path."
    with lock:
        with open(pth, 'r', encoding='utf-8') as ofile:
            update(obj, load(ofile))


def update(obj, data, empty=True) -> None:
    "update attributes with a key/value dict."
    for key, value in items(data):
        if empty and not value:
            continue
        setattr(obj, key, value)


def values(obj) -> []:
    "list of values."
    return obj.__dict__.values()


def write(obj, pth) -> None:
    "locked write to path."
    with lock:
        cdir(os.path.dirname(pth))
        with open(pth, 'w', encoding='utf-8') as ofile:
            dump(obj, ofile)
