# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0105,W0613,E0101,E0402


"encoding"


import json


from .objects import Object


"classes"


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


"utilities"


def dump(*args, **kw):
    ""
    kw["cls"] = ObjectEncoder
    return json.dump(*args, **kw)


def dumps(*args, **kw):
    ""
    kw["cls"] = ObjectEncoder
    return json.dumps(*args, **kw)


"interface"


def __dir__():
    return (
        'ObjectEncoder',
        'dump',
        'dumps'
    )


__all__ = __dir__()
