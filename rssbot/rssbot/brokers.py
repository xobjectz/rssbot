# This file is placed in the Public Domain.
#
# pylint: disable=C,R,E0402


"list of bots"


from .objects import Object


def __dir__():
    return (
        "Fleet",
        "byorig"
    )


__all__ = __dir__()


class Fleet(Object):

    objs = []

    @staticmethod
    def add(obj) -> None:
        Fleet.objs.append(obj)

    @staticmethod
    def first():
        if Fleet.objs:
            return Fleet.objs[0]

    @staticmethod
    def remove(obj):
        if obj in Fleet.objs:
            Fleet.objs.remove(obj)

    @staticmethod
    def byorig(orig) -> Object:
        for obj in Fleet.objs:
            if object.__repr__(obj) == orig:
                return obj
        return None


def byorig(orig):
    return Fleet.byorig(orig)
