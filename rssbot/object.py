# This file is placed in the Public Domain.
# pylint: disable=R0902,W0105


"a clean namespace"


import datetime


class Object:

    "Object"

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
        kin = f"{obj.__module__}.{obj.__name__}"
    return kin


def ident(obj):
    "return an id for an object."
    return pjoin(fqn(obj), *str(datetime.datetime.now()).split())


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


def match(obj, txt):
    "check if object has matching keys."
    for key in keys(obj):
        if txt in key:
            return True
    return False


def search(obj, selector):
    "check if object matches provided values."
    res = False
    if not selector:
        return res
    for key, value in items(selector):
        val = getattr(obj, key, None)
        if not val:
            continue
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


"interface"


def pjoin(*args):
    "path join."
    return "/".join(args)


def __dir__():
    return (
        'Object',
        'construct',
        'edit',
        'fmt',
        'fqn',
        'ident',
        'items',
        'keys',
        'match',
        'search',
        'update',
        'values',
    )
