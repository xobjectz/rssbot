# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0105,W0212,W0613,W0718,E0402,E1102


"""object broker

This Broker class stores objects on their repr name and can thus be
retrieved by a client presenting a repr of an object.

Client can carry a string (the repr) around instead of a memory
reference to the object.

Adding an object takes the repr and stores it in a dict, the rest are
methods to retrieve an object from the broker.

Broker is operating at an class level where the class level attributes
are manipulated instead of an object inherited from that class.

"""


from .object import Object, keys, values


rpr = object.__repr__


class Broker:

    objs = Object()

    @staticmethod
    def add(obj):
        "add an object to the broker."
        setattr(Broker.objs, rpr(obj), obj)

    @staticmethod
    def all():
        "return all objects."
        return values(Broker.objs)

    @staticmethod
    def first():
        "return first object."
        for key in keys(Broker.objs):
            return getattr(Broker.objs, key)

    @staticmethod
    def get(orig):
        "return object by origin (repr)"
        return getattr(Broker.objs, orig, None)

    @staticmethod
    def remove(obj):
        "remove object from broker"
        delattr(Broker.objs, rpr(obj))


"interfacce"


def __dir__():
    return (
        'Broker',
    )


__all__ = __dir__()
