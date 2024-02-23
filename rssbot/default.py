# This file is placed in the Public Domain.
#
# pylint: disable=C,R


"defaults"


from .objects import Object


def __dir__():
    return (
        'Default',
    )


__all__ = __dir__()


class Default(Object):

    __slots__ = ("__default__",)

    def __init__(self):
        Object.__init__(self)
        self.__default__ = ""

    def __getattr__(self, key):
        return self.__dict__.get(key, self.__default__)
