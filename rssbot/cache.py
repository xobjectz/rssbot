# This file is placed in the Public Domain.


"caching"


from .object import Object


class Cache:

    "Broker"

    def __init__(self):
        self.objs = Object()

    def get(self, orig):
        "return object by origin (repr)"
        return getattr(self.objs, orig, None)

    def register(self, obj):
        "add an object to the broker."
        ids = object.__repr__(obj)
        setattr(self.objs, ids, obj)


def __dir__():
    return (
        'Cache',
    )
