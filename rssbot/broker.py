# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0105,W0212,W0613,W0718,E0402,E1102


"""broker

This Broker class stores objects on their repr name and can thus be
retrieved by a client presenting a repr of an object.

Client can carry a string (the repr) around instead of a memory
reference to the object.

Adding an object takes the repr and stores it in a dict, the rest are
methods to retrieve an object from the broker.

Broker is operating at an class level where the class level attributes
are manipulated instead of an object inherited from that class.

::

    >>> from objx import Object
    >>> from objr import Broker
    >>> b = Broker()
    >>> o = Object()
    >>> b.add(o)
    >>> oo = b.get(repr(o))
    >>> o is oo
    True

"""


from .object import Object, keys


rpr = object.__repr__


class Broker:

    "Broker"

    def __init__(self):
        self.objs = Object()

    def add(self, obj):
        "add an object to the broker."
        setattr(self.objs, rpr(obj), obj)

    def first(self):
        "return first object."
        for key in keys(self.objs):
            return getattr(self.objs, key)

    def get(self, orig):
        "return object by origin (repr)"
        return getattr(self.objs, orig, None)

    def remove(self, obj):
        "remove object from broker"
        delattr(self.objs, rpr(obj))
