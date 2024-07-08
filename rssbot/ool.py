# This file is placed in the Public Domain.
#
# pylint: disable=R0903


"object of lists"


from .object import Object


class OoL(Object):

    "Object of Lists."


def ladd(obj, name, val):
    "add value to list."
    if name not in obj:
        setattr(obj, name, [])
    lll = getattr(obj, name)
    lll.append(val)


def lextend(obj, name, lis=None):
    "extend list."
    if lis is None:
        lis = []
    if name not in obj:
        setattr(obj, name, lis)
    lll = getattr(obj, name)
    lll.extend(lis)


def __dir__():
    return (
        "ladd",
        "lextend"
    )
