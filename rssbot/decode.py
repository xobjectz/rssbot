# This file is placed in the Public Domain.
# pylint: disable=R0902,W0105


"object decoder"


import json


from .lock   import lock
from .object import Object, construct, update


class ObjectDecoder(json.JSONDecoder):

    "ObjectDecoder"

    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, *args, **kwargs)

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


def read(obj, pth):
    "read an object from file path."
    with lock:
        with open(pth, 'r', encoding='utf-8') as ofile:
            update(obj, load(ofile))


"interface"


def __dir__():
    return (
        'hook',
        'load',
        'loads',
        'read'
    )
