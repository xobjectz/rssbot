# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0105,W0613,E0101,E0402


"decoding"


import json


from .objects import Object, construct


"classes"


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


"utilities"


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


"interface"


def __dir__():
    return (
        'ObjectDecoder',
        'hook',
        'load',
        'loads'
    )


__all__ = __dir__()
