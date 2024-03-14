# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0105,W0613,E0101


"a clean namespace"


class Object:

    def __contains__(self, key):
        return key in dir(self)

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __str__(self):
        return str(self.__dict__)


"methods"


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
        val = getattr(obj, key, None)
        if str(value).lower() in str(val).lower():
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


"interface"


def __dir__():
    return (
        'Object',
        'construct',
        'edit',
        'fmt',
        'fqn',
        'items',
        'keys',
        'search',
        'update',
        'values'
    )


__all__ = __dir__()
