# This file is placed in the Public Domain,
#
# pylint: disable=C,R,W0105,W0613,E0101


"objects"


import json


def __dir__():
    return (
        "Object",
        "construct",
        "dump",
        "dumps",
        "edit",
        "fmt",
        "fqn",
        "items",
        "keys",
        "load",
        "loads",
        "search",
        "update",
        "values",
    )


__all__ = __dir__()


class Object:

    def __contains__(self, key):
        return key in dir(self)

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __repr__(self):
        return dumps(self)

    def __str__(self):
        return str(self.__dict__)


def construct(obj, *args, **kwargs):
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
    kin = str(type(obj)).split()[-1][1:-2]
    if kin == "type":
        kin = obj.__name__
    return kin


def items(obj):
    if isinstance(obj, type({})):
        return obj.items()
    return obj.__dict__.items()


def keys(obj):
    if isinstance(obj, type({})):
        return obj.keys()
    return list(obj.__dict__.keys())


def search(obj, selector):
    res = False
    if not selector:
        return True
    for key, value in items(selector):
        if key not in obj:
            res = False
            break
        for vval in spl(str(value)):
            val = getattr(obj, key, None)
            if str(vval).lower() in str(val).lower():
                res = True
            else:
                res = False
                break
    return res


def update(obj, data, empty=True):
    for key, value in items(data):
        if empty and not value:
            continue
        setattr(obj, key, value)


def values(obj):
    return obj.__dict__.values()


class ObjectDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        ""
        return json.JSONDecoder.__init__(self, *args)

    def decode(self, s, _w=None):
        ""
        val = json.JSONDecoder.decode(self, s)
        if not val:
            val = {}
        return hook(val)

    def raw_decode(self, s, idx=0):
        ""
        return json.JSONDecoder.raw_decode(self, s, idx)


def hook(objdict, typ=None):
    if typ:
        obj = typ()
    else:
        obj = Object()
    construct(obj, objdict)
    return obj


def load(fpt, *args, **kw):
    kw["cls"] = ObjectDecoder
    kw["object_hook"] = hook
    return json.load(fpt, *args, **kw)


def loads(string, *args, **kw):
    kw["cls"] = ObjectDecoder
    kw["object_hook"] = hook
    return json.loads(string, *args, **kw)


class ObjectEncoder(json.JSONEncoder):
    def __init__(self, *args, **kwargs):
        ""
        return json.JSONEncoder.__init__(self, *args, **kwargs)

    def default(self, o):
        ""
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
            return object.__repr__(o)

    def encode(self, o) -> str:
        ""
        return json.JSONEncoder.encode(self, o)

    def iterencode(self, o, _one_shot=False):
        ""
        return json.JSONEncoder.iterencode(self, o, _one_shot)


def dump(*args, **kw) -> None:
    ""
    kw["cls"] = ObjectEncoder
    return json.dump(*args, **kw)


def dumps(*args, **kw) -> str:
    ""
    kw["cls"] = ObjectEncoder
    return json.dumps(*args, **kw)


"utility"


def spl(txt):
    try:
        res = txt.split(',')
    except (TypeError, ValueError):
        res = txt
    return [x for x in res if x]
