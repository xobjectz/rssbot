# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0105


"default"


from .object import Object


class Default(Object):

    "Default"

    def __getattr__(self, key):
        return self.__dict__.get(key, "")
